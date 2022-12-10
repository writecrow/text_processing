#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION:
# Given a folder with .txt files (inlcuding subfolders) and an excel file with metadata,
# the script extracts information from the excel file and adds metadata headers to each individual text file.

# Usage examples
# Run the line below from the terminal on a Mac or command prompr on windows:
# Mac OS example:
# D2L
#    python purdue_add_headers.py --directory=purdue_data --master_file=modified_registrar_fall2018.xlsx --cms=d2l
# BLACKBOARD
#    python purdue_add_headers.py --directory=purdue_data --master_file=modified_registrar_fall2018.xlsx --cms=blackboard

# Windows example:
# D2L
#    python python purdue_add_headers.py --directory=standardized\101 --master_file=metadata_folder\master_student_data.xlsx
# BLACKBOARD
#   python python purdue_add_headers.py --directory=standardized\10600 --master_file=metadata_folder\purdue_registrar_data.xlsx --cms=blackboard

# imports packages
import argparse
import hashlib
import sys
import re
import os
import pandas

# lists the required arguments (e.g. --directory=) sent to the script
parser = argparse.ArgumentParser(description="Add Headers to Individual Textfile")
parser.add_argument("--directory", action="store", dest="dir", default="")
parser.add_argument("--master_file", action="store", dest="master_file", default="")
parser.add_argument("--cms", action="store", dest="cms", default="d2l")
args = parser.parse_args()

column_specs = {
    "IELTS_Listening": "ILT1 - IELTS Listening",
    "IELTS_Overall": "ILT2 - IELTS Overall",
    "IELTS_Reading": "ILT3 - IELTS Reading",
    "IELTS_Speaking": "ILT4 - IELTS Speaking",
    "IELTS_Writing": "ILT5 - IELTS Writing",
    "L1": "NATIVE_LANGUAGE_DESC",
    "TOEFL_COMPI": "TIBT - TOEFL IBT Total Score",
    "TOEFL_Listening": "TIBL - TOEFL IBT Listening Score",
    "TOEFL_Reading": "TIBR - TOEFL IBT Reading Score",
    "TOEFL_Speaking": "TIBS - TOEFL IBT Speaking Score",
    "TOEFL_Writing": "TIBW - TOEFL IBT Writing Score",
    "college": "COLLEGE_DESC",
    "country": "NATION_OF_CITIZENSHIP_DESC",
    "country_code": "COUNTRY_CODE",
    "course": "COURSE_NUMBER",
    "crow_id": "Crow ID",
    "gender": "GENDER",
    "institution": "institution",
    "institution_code": "institution_code",
    "instructor": "Instructor_Code",
    "length": "length_of_course",
    "mode": "mode_of_course",
    "program": "PROGRAM_DESC",
    "section": "Class Section",
    "subject": "SUBJECT",
    "term": "ACADEMIC_PERIOD_DESC",
    "year_in_school": "year_in_school",
}
fixed_expressions = {"course_prefix": "ENGL"}

# Remove leading spaces, replace "NaN" with "NA", enforce string
def clean(my_string):
    if (type(my_string)) is not str:
        my_string = str(my_string)
    my_string = my_string.strip()
    my_string = re.sub(r'nan', r'NA', my_string)
    my_string = re.sub(r'NaN', r'NA', my_string)
    return my_string

# Create a formatted header.
def add_heading(key, value):
    if value == "":
        value = "NA"
    return "<" + key + ": " + value + ">"


def get_year_in_school_numeric(raw):
    year_in_school = clean(raw)
    if year_in_school not in ["1", "2", "3", "4"]:
        if year_in_school.lower() == "freshman":
            year_in_school_numeric = "1"
        elif year_in_school.lower() == "sophomore":
            year_in_school_numeric = "2"
        elif year_in_school.lower() == "junior":
            year_in_school_numeric = "3"
        elif year_in_school.lower() == "senior":
            year_in_school_numeric = "4"
        else:
            year_in_school_numeric = "NA"
    else:
        year_in_school_numeric = year_in_school
    return year_in_school_numeric


def create_file_hash(filename, blocksize=65536):
    file_handle = open(filename, "rb")
    buf = file_handle.read(blocksize)
    hasher = hashlib.md5()
    while len(buf) > 0:
        hasher.update(buf)
        buf = file_handle.read(blocksize)
    return hasher.hexdigest()


def analyze_results(results):
    seen_content = set()
    seen_filenames = set()
    duplicate_hashes = []
    duplicate_filenames = []
    for r in results:
        if r[1] in seen_content:
            duplicate_hashes.append(r[1])
        else:
            seen_content.add(r[1])
        if r[2] in seen_filenames:
            duplicate_filenames.append(r[2])
        else:
            seen_filenames.add(r[2])
    inc = 0
    duplicate_content = []
    if duplicate_hashes:
        inc = inc + 1
        duplicate_content = []
        for i in duplicate_hashes:
            group = []
            for j in results:
                if i == j[1]:
                    group.append(j[0])
            duplicate_content.append(group)
        print()
        print("** SOME ORIGINAL FILES HAD IDENTICAL CONTENTS: **")
        for i in duplicate_content:
            print(i)
    if duplicate_filenames:
        print()
        print(
            "** SOME FILES GENERATED IDENTICAL FILENAMES, EFFECTIVELY OVERWRITING EACH OTHER: **"
        )
        for i in duplicate_filenames:
            print("* " + i)


# Given a single row of student metadata, add it to the list of headers
def get_student_data(row, headers):
    crow_id = clean(row[column_specs["crow_id"]])
    if crow_id == "NA":
        print("This student does not have a Crow ID")
        exit()
    # retrieves country code from "country_code" column in the metadata spreasheet
    country_code = row[column_specs["country_code"]]
    # strips white spaces around the country_code values in the column
    country_code = clean(country_code)
    # replaces "NaN" to "NAN" for the country_code variable
    country_code = re.sub(r"NaN", r"NAN", country_code)
    country = clean(row[column_specs["country"]])
    course = clean(row[column_specs["course"]])
    year_in_school = row[column_specs["year_in_school"]]
    year_in_school_numeric = get_year_in_school_numeric(year_in_school)
    # retrieves and cleans gender from "gender" column in the metadata spreasheet
    gender = clean(row[column_specs["gender"]])
    L1 = clean(row["NATIVE_LANGUAGE_DESC"])

    # retrieves college from "college" column in the metadata spreasheet
    college = clean(row[column_specs["college"]])
    # retrieves program from "program" column in the metadata spreasheet
    program = clean(row[column_specs["program"]])
    # retrieves overall TOEFL scores from "TOEFL_COMPI" column in the metadata spreasheet
    TOEFL_COMPI = clean(row[column_specs["TOEFL_COMPI"]])
    # retrieves TOEFL listening scores from "TOEFL_Listening" column in the metadata spreasheet
    TOEFL_Listening = clean(row[column_specs["TOEFL_Listening"]])
    # retrieves TOEFL reading scores from "TOEFL_Reading" column in the metadata spreasheet
    TOEFL_Reading = clean(row[column_specs["TOEFL_Reading"]])
    # retrieves TOEFL writing scores from "TOEFL_Writing" column in the metadata spreasheet
    TOEFL_Writing = clean(row[column_specs["TOEFL_Writing"]])
    # retrieves TOEFL speaking scores from "TOEFL_Speaking" column in the metadata spreasheet
    TOEFL_Speaking = clean(row[column_specs["TOEFL_Speaking"]])
    # retrieves overall IELTS scores from "IELTS_Overall" column in the metadata spreasheet
    IELTS_Overall = clean(row[column_specs["IELTS_Overall"]])
    # retrieves IELTS listening scores from "IELTS_Listening" column in the metadata spreasheet
    IELTS_Listening = clean(row[column_specs["IELTS_Listening"]])
    # retrieves IELTS reading scores from "IELTS_Reading" column in the metadata spreasheet
    IELTS_Reading = clean(row[column_specs["IELTS_Reading"]])
    # retrieves IELTS writing scores from "IELTS_Writing" column in the metadata spreasheet
    IELTS_Writing = clean(row[column_specs["IELTS_Writing"]])
    # retrieves IELTS speaking scores from "IELTS_Speaking" column in the metadata spreasheet
    IELTS_Speaking = clean(row[column_specs["IELTS_Speaking"]])
    # retrieves instructor information from "instructor" column in the metadata spreasheet

    # creates new variables to combine proficiency exam scores
    proficiency_exam = ""
    exam_total = ""
    exam_reading = ""
    exam_listening = ""
    exam_speaking = ""
    exam_writing = ""

    # checks if the "TOEFL_COMPI" values are not "NA"s
    if TOEFL_COMPI != "NA":
        # if they are not "NA"s, then the proficiency exam is TOEFL
        proficiency_exam = "TOEFL"
        exam_total = TOEFL_COMPI
        exam_reading = TOEFL_Reading
        exam_listening = TOEFL_Listening
        exam_speaking = TOEFL_Speaking
        exam_writing = TOEFL_Writing
    # checks if the "IELTS_Overall" values are not "NA"s
    elif IELTS_Overall != "NA":
        # if they are not "NA"s, then the proficiency exam is IELTS
        proficiency_exam = "IELTS"
        exam_total = IELTS_Overall
        exam_reading = IELTS_Reading
        exam_listening = IELTS_Listening
        exam_speaking = IELTS_Speaking
        exam_writing = IELTS_Writing
    # checks if both the "IELTS_Overall" values and "TOEFL_COMPI" are not "NA"s
    elif TOEFL_COMPI != "NA" and IELTS_Overall != "NA":
        # if they are not "NA"s, then the proficiency exams are both TOEFL and IELTS
        proficiency_exam = "TOEFL;IELTS"
        exam_total = TOEFL_COMPI + ";" + IELTS_Overall
        exam_reading = TOEFL_Reading + ";" + IELTS_Reading
        exam_listening = TOEFL_Listening + ";" + IELTS_Listening
        exam_speaking = TOEFL_Speaking + ";" + IELTS_Speaking
        exam_writing = TOEFL_Writing + ";" + IELTS_Writing
    # if the conditions above are not met, the proficiency exam scores are not available
    else:
        proficiency_exam = "NA"
        exam_total = "NA"
        exam_reading = "NA"
        exam_listening = "NA"
        exam_speaking = "NA"
        exam_writing = "NA"

    headers.append(add_heading("Student ID", crow_id))
    headers.append(add_heading("Country", country))
    headers.append(add_heading("L1", L1))
    headers.append(add_heading("Heritage Spanish Speaker", "NA"))
    headers.append(add_heading("Year in School", year_in_school_numeric))
    headers.append(add_heading("Gender", gender))
    headers.append(add_heading("College", college))
    headers.append(add_heading("Program", program))
    headers.append(add_heading("Proficiency Exam", proficiency_exam))
    headers.append(add_heading("Exam total", exam_total))
    headers.append(add_heading("Exam reading", exam_reading))
    headers.append(add_heading("Exam listening", exam_listening))
    headers.append(add_heading("Exam speaking", exam_speaking))
    headers.append(add_heading("Exam writing", exam_writing))
    return headers

# Look for a string like 001_01.
def get_group_id(filename):
    regex = r"_(\d\d\d)_(\d\d)"
    match = re.search(regex, filename)
    if match is not None:
        group = str(match.group())
        # Remove leading underscore
        group = group[1:]
        return group
    regex = r"G(\d\d\d)_(\d\d)"
    match = re.search(regex, filename)
    if match is not None:
        group = str(match.group())
        # Remove leading 'G'
        group = group[1:]
        return str(group)
    return False

def get_output_filename(course, group_id):
    # concatenate all parts to create filename in the following format: 106_LN_1_CH_2_F_20034_UA.txt
    underscore = "_"
    parts = []
    parts.append(course["name"])
    parts.append(course["assignment"])
    parts.append(course["draft"])
    if (group_id == "NA"):
        parts.append(course["country_code"])
        parts.append(course["year_in_school_numeric"])
        parts.append(course["gender"])
        parts.append(course["crow_id"])
    else:
        parts.append('G' + group_id)
    parts.append(course["institution_code"])
    output_filename = underscore.join(parts) + ".txt"
    output_filename = re.sub(r"\s", r"", output_filename)
    output_filename = re.sub(r"__", r"_NA_", output_filename)
    return output_filename


def get_course_data(row, filename_parts):
    course = {}
    # retrieves crow id from "crow_id" column in the metadata spreasheet
    course["crow_id"] = clean(row[column_specs["crow_id"]])
    if course["crow_id"] == "NA":
        print(row)
        print("This student does not have a Crow ID")
        exit()
    course["instructor"] = clean(int(row[column_specs["instructor"]]))
    course["mode"] = clean(row[column_specs["mode"]])
    course["length"] = clean(row[column_specs["length"]])
    course["institution_code"] = clean(row[column_specs["institution_code"]])
    course["section"] = clean(int(row["section"]))
    course["institution"] = clean(row["institution"])
    course["country"] = clean(row[column_specs["country"]])
    course["year_in_school"] = row[column_specs["year_in_school"]]
    course["year_in_school_numeric"] = get_year_in_school_numeric(
        course["year_in_school"]
    )
    course["gender"] = clean(row[column_specs["gender"]])
    country_code = row[column_specs["country_code"]]
    # strips white spaces around the country_code values in the column
    country_code = clean(country_code)
    # replaces "NaN" to "NAN" for the country_code variable
    course["country_code"] = re.sub(r"NaN", r"NAN", country_code)
    course["subject"] = clean(row[column_specs["subject"]])
    course["name"] = clean(int(row[column_specs["course"]]))
    if (len(filename_parts[-2]) >= 4):
        ## The assignment code is everything in the second-to-last
        ## part of the path minus the final 2 characters.
        course["assignment"] = filename_parts[-2][:-2]
        # The draft is the final character in the second-to-last
        ## part of the path.
        course['draft'] = filename_parts[-2][-1]
    else:
        ## Assume the draft is Final.
        course["assignment"] = filename_parts[-2]
        course['draft'] = "F"
    course["term"] = clean(row[column_specs["term"]])
    # creates a semester variable from the first element of the term variable
    term_parts = re.split(' |_', course["term"])
    # assuming term is "Spring 2019" for example
    course["semester"] = term_parts[0]
    # creates a year variable from the second element of the term variable
    course["year"] = term_parts[1]
    return course


# function to add the metadata headers to each individual text file
def add_header_common(filepath, metadata, results):
    comma = ","
    textfile = open(filepath, "r")
    # Normalize path to work across platforms (PC, Mac)
    normed_path = os.path.normpath(filepath)
    # Split the parts of the path across platforms
    filename_parts = normed_path.split(os.sep)
    # print("Processing file: ", filename_parts)

    # Isolate the first row from the metadata for general text information
    # (Texts written by a group will have multiple rows)
    first_row = metadata[0]
    if len(metadata) != 1:
        group_id = str(first_row['CROW_GROUP_ID'])
    else:
        group_id = 'NA'
    course = get_course_data(first_row, filename_parts)
    output_filename = get_output_filename(course, group_id)
    # check if master_row has just one row
    if "Series" in output_filename:
        return results

    # creates an output folder named "files_with_headers" with the term, course, assignment and draft subfolders
    new_folder = "files_with_headers"
    cwd = os.getcwd()
    path = os.path.join(
        cwd,
        new_folder,
        course["term"],
        course["subject"] + " " + course["name"],
        course["assignment"],
        course["draft"],
    )
    # checks if such a folder exists, if not, it creates the folder
    if not os.path.exists(path):
        os.makedirs(path)
    # specifies the path for the file to be written
    whole_path = os.path.join(path, output_filename)
    output_file = open(whole_path, "w", encoding="utf-8")


    # Build general metadata
    headers = []
    headers.append("<Text>")
    ids = []
    for student in metadata:
        ids.append(clean(student[column_specs["crow_id"]]))

    headers.append(add_heading("Student IDs", comma.join(ids)))
    headers.append(add_heading("Group ID", group_id))
    headers.append(add_heading("Institution", course["institution"]))
    headers.append(add_heading("Course", fixed_expressions["course_prefix"] + " " + course["name"]))
    headers.append(add_heading("Mode", course["mode"]))
    headers.append(add_heading("Length", course["length"]))
    headers.append(add_heading("Assignment", course["assignment"]))
    headers.append(add_heading("Draft", course["draft"]))
    headers.append(add_heading("Course Year", course["year"]))
    headers.append(add_heading("Course Semester", course["semester"]))
    headers.append(add_heading("Instructor", course["instructor"]))
    headers.append(add_heading("Section", course["section"]))
    headers.append("</Text>")
    headers.append("")

    # Build student(s) metadata
    # (if the text is written by a group, there will be more than one)
    inc = 1
    for student in metadata:
        headers.append("<Student " + str(inc) + ">")
        headers = get_student_data(student, headers)
        headers.append("</Student " + str(inc) + ">")
        headers.append("")
        inc += 1

    headers.append("<End Header>")
    headers.append("")
    # Write headers, line by line.
    # print("Writing on file: ", path + output_filename)
    for header in headers:
        print(header, file=output_file)
    for line in textfile:
        this_line = re.sub(r"\r?\n", r"\r\n", line)
        if this_line != "\r\n":
            new_line = re.sub(r"\s+", r" ", this_line)
            new_line = new_line.strip()
            print(new_line, file=output_file)
    output_file.close()
    textfile.close()
    hash = create_file_hash(filepath)
    results.append([filepath, hash, output_filename])
    return results


# creates a function specific to blackboard metadata, which uses career accounts to match
# the spreadsheet data and filenames
def add_header_to_file_blackboard(filename, metadata, results):
    target_rows = []
    for row in metadata:
        # check if that career account is in filename (that's our student!)
        if re.search("_" + str(row['User_ID']), filename):
            # let user know that there was a match
            #print("Matched: ", "_" + career_account + "_", "is in", filename, "and adding headers...")
            target_rows.append(row)
    if len(target_rows) == 0:
        print('* No matching metadata found for file ' + filename)
    else:
        results = add_header_common(filename, target_rows, results)
    return results


# creates a function specific to d2l course management system metadata, which uses student names to match
# the spreadsheet data and filenames
def add_header_to_file_d2l(filename, master, results):
    # splits the filename by a dash with a space "- "
    filename_parts = filename.split("- ")
    if len(filename_parts) > 1:
        student_part = filename_parts[1]
    else:
        student_part = filename
    # removes ".txt" extension from the filename
    student_name = re.sub(r"\.txt", r"", student_part)
    # removes any extra spaces from the filename
    student_name = re.sub(r"\s+", r" ", student_name)
    # checks to see if the last element of the student name is "-"
    if student_name[-1] == "-":
        # if it is, it removes it
        student_name = student_name[:-1]
    # splits the student name by white space
    student_name_parts = student_name.split()
    # checks if the student name has more than two names
    if len(student_name_parts) != 2:
        print("***********************************************")
        # if there are more than two names, it prints 'File has student name with more than two names: '
        print("File has student name with more than two names: " + filename)
        print(student_name_parts)
    # retrieves last name from "Last Name" column in the metadata spreasheet
    filtered_master1 = master[master["Last Name"] == student_name_parts[-1]]
    # retrieves first name from "First Name" column in the metadata spreasheet
    filtered_master2 = filtered_master1[
        filtered_master1["First Name"] == student_name_parts[0]
    ]
    # checks to see if the given student names exist in the metadata spreadsheet
    if filtered_master2.empty:
        print("***********************************************")
        print("Unable to find metadata for this file: ")
        print(filename)
        print(student_name_parts)
    # checks to see if there is more than one row for the same student in the metadata spreadsheet
    if filtered_master2.shape[0] > 1:
        print("***********************************************")
        print("More than one row in metadata for this file: ")
        print(filename)
        print(student_name_parts)
    else:
        print("Adding headers to file " + filename)
        # This will be returned as a list, to normalize it with groups.
        rows = [filtered_master2]
        results = add_header_common(filename, rows, results)
    # institution_code = re.sub(r'[a-z\s]', r'', master_row[column_specs['institution_code']])

    return results


# Add headers and change filenames recursively on all the files in the specified directory
def add_headers_recursive(directory, metadata, cms):
    data = metadata.to_dict(orient="records")
    total_files = 0
    results = []
    # walks folder structure to get all files in all folders
    for dirpath, dirnames, files in os.walk(directory):
        # for every file found in a folder
        for name in files:
            # Skip non text files.
            if ".txt" not in name:
                continue
            total_files = total_files + 1
            group_id = get_group_id(name)
            if group_id is not False:
                target_rows = []
                for row in data:
                    search = str(row['GROUP_ID'])
                    group_id = (str(group_id))
                    if re.search(group_id, row['GROUP_ID']):
                        target_rows.append(row)
                if len(target_rows) == 0:
                    print("No group ID for the following: ")
                    print(name)
                    print(group_id)
                    # exit()
                else:
                    results = add_header_common(os.path.join(dirpath, name), target_rows, results)
            elif cms == "d2l":
                # calls function that add headers to an individual file specific to d2l
                results = add_header_to_file_d2l(os.path.join(dirpath, name), metadata, results)
            elif cms == "blackboard":
                # calls function that add headers to an individual file specific to blackboard
                results = add_header_to_file_blackboard(os.path.join(dirpath, name), data, results)
    # if no .txt texts were found in the directory, it prints "No text files found in the directory"
    if total_files == 0:
        print("No text files found in the directory.")
    else:
        print("***************************************")
        print("Files found:     " + str(total_files))
        print("Files processed: " + str(len(results)))
        print("***************************************")
    analyze_results(results)


# checks if the user has specified the master student file (excel or csv file)
if args.master_file and args.dir:
    if ".xls" in args.master_file:
        master_file = pandas.ExcelFile(args.master_file)
        master_data = pandas.read_excel(master_file)

    elif ".csv" in args.master_file:
        master_data = pandas.read_csv(args.master_file)

    # calls function that adds headers to each file in a folder and all subfolders recursively
    add_headers_recursive(args.dir, master_data, args.cms)
else:
    print("You need to supply a valid master file and directory with textfiles")
