#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file and text files passed as arguments to the script,
# metadata headers are added to each individual text files, 
# written to the directory "files_with_headers"
#
# Mac/Linux example:
#    python arizona_add_headers.py --directory=Standardized --master_file=spring_2022_processed.csv
#    python arizona_add_headers.py --directory=Fall\ 2018/normalized/ --master_file=Metadata_Fall_2018_updated.csv
#    python arizona_add_headers.py --directory=../../../Fall\ 2017/normalized/ --master_file=../../../Metadata/Fall\ 2017/Metadata_Fall_2017.xlsx
#
# Windows run with Anaconda Prompt example:
#    python arizona_add_headers.py --directory="Fall 2018/normalized/" --master_file="Metadata_Fall_2018_updated.csv"

import argparse
import re
import os
import pandas
import hashlib

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--master_file', action="store", dest='master_file', default='')
args = parser.parse_args()

# Look for a string like G001_01.
def get_group_id(filename):
    regex = r"G(\d+)_(\d+)"
    match = re.search(regex, filename)
    if match is not None:
        return match.group()
    return False


def get_metadata_for_file(filepath, master):
    # Convert the master spreadsheet to an easily traversable dictionary.
    data = master.to_dict(orient="records")
    normed_path = os.path.normpath(filepath)
    # splits the parts of the path across platforms
    filepath_parts = normed_path.split(os.sep)
    # The filename is the final segment of a split path.
    filename = filepath_parts[-1]
    group_id = get_group_id(filename)
    if group_id is not False:
        target_rows = []
        for row in data:
            search = "G" + row['GROUP_ID']
            if search == group_id:
                target_rows.append(row)
        return target_rows
    # Check two different methods to discover the metadata: explicit filename, or student name concatenated.
    matches = 0
    possible_matches = []
    target_row = {}
    # Loop through rows in the master spreadsheet.
    for row in data:
        fullname = row['First Name'] + ' ' + row['Last Name']
        short_first_name = row['First Name'].split(' ')
        short_last_name = row['Last Name'].split(' ')
        if short_last_name[0]:
            for part in short_last_name:
                if len(part) > 2:
                    short_last_name = part
                    break
        if isinstance(short_last_name, list):
            short_last_name = row['Last Name']
        if short_first_name[0]:
            short_first_name = short_first_name[0]
        short_fullname = short_first_name + ' ' + short_last_name
        # If there is an explicit filename segment in this row, see if it is contained in the file's name.
        if str(row['Filename']) != '' and str(row['Filename']).lower() in filename.lower():
            matches = matches + 1
            target_row = row
        elif fullname.lower() in filename.lower():
            matches = matches + 1
            target_row = row
        elif short_fullname.lower() in filename.lower():
            matches = matches + 1
            target_row = row
        elif short_last_name in filename or short_first_name in filename:
            possible_matches.append(
                row['First Name'] + ' ' + row['Last Name'])
    # Report the results of our search.
    if matches == 0:
        print('Unable to find any metadata for this file: ' + filepath)
        if possible_matches:
            print('Possible match in spreadsheet:')
            print(possible_matches)
        exit()
        return False
    #elif matches > 1:
      #  print('More than one row of metadata matches this file: ' + filepath)
       # return False
    else:
        # Success! We found a single metadata row corresponding to this file.
        # This will be returned as a list, to normalize it with groups.
        return [target_row]

# function that removes leading spaces and replaces "NaN" with "NA"
def clean(my_string):
    if (type(my_string)) is not str:
        my_string = str(my_string)
    my_string = my_string.strip()
    my_string = re.sub(r'nan', r'NA', my_string)
    my_string = re.sub(r'NaN', r'NA', my_string)
    return my_string


def create_file_hash(filename, blocksize=65536):
    file_handle = open(filename, 'rb')
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
        print('** SOME ORIGINAL FILES HAD IDENTICAL CONTENTS: **')
        for i in duplicate_content:
            print(i)
    if duplicate_filenames:
        print()
        print('** SOME FILES GENERATED IDENTICAL FILENAMES, EFFECTIVELY OVERWRITING EACH OTHER: **')
        for i in duplicate_filenames:
            print('* ' + i)

def add_heading(key, value):
    if value == '':
        value = 'NA'
    return "<" + key + ": " + value + ">"

def get_year_in_school_numeric(raw):
    year_in_school = clean(raw)
    if year_in_school not in ['1', '2', '3', '4']:
        if year_in_school.lower() == 'freshman':
            year_in_school_numeric = '1'
        elif year_in_school.lower() == 'sophomore':
            year_in_school_numeric = '2'
        elif year_in_school.lower() == 'junior':
            year_in_school_numeric = '3'
        elif year_in_school.lower() == 'senior':
            year_in_school_numeric = '4'
        else:
            year_in_school_numeric = 'NA'
    else:
        year_in_school_numeric = year_in_school
    return year_in_school_numeric

# Given a single row of student metadata, add it to the list of headers
def add_student(row, headers):
    country_code = clean(row['Birth Country Code'])
    year_in_school_numeric = get_year_in_school_numeric(row['Acad Level'])
    gender = clean(row['Gender'])
    crow_id = clean(row['Crow ID'])
    country = clean(row['Descr'])
    college = clean(row['College'])
    program = clean(row['Major'])
    TOEFL_COMPI = clean(row['TOEFL COMPI'])
    TOEFL_Listening = clean(row['TOEFL Listening'])
    TOEFL_Reading = clean(row['TOEFL Reading'])
    TOEFL_Writing = clean(row['TOEFL Writing'])
    TOEFL_Speaking = clean(row['TOEFL Speaking'])
    IELTS_Overall = clean(row['IELTS Overall Band Score'])
    IELTS_Listening = clean(row['IELTS Listening'])
    IELTS_Reading = clean(row['IELTS Reading'])
    IELTS_Writing = clean(row['IELTS Writing'])
    IELTS_Speaking = clean(row['IELTS Speaking'])
    L1 = clean(row['L1'])
    heritage_spanish = clean(row['Heritage Spanish'])
    proficiency_exam = ''
    exam_total = ''
    exam_reading = ''
    exam_listening = ''
    exam_speaking = ''
    exam_writing = ''
    if TOEFL_COMPI != 'NA':
        proficiency_exam = 'TOEFL'
        exam_total = TOEFL_COMPI
        exam_reading = TOEFL_Reading
        exam_listening = TOEFL_Listening
        exam_speaking = TOEFL_Speaking
        exam_writing = TOEFL_Writing
    elif IELTS_Overall != 'NA':
        proficiency_exam = 'IELTS'
        exam_total = IELTS_Overall
        exam_reading = IELTS_Reading
        exam_listening = IELTS_Listening
        exam_speaking = IELTS_Speaking
        exam_writing = IELTS_Writing
    elif TOEFL_COMPI != 'NA' and IELTS_Overall != 'NA':
        proficiency_exam = 'TOEFL;IELTS'
        exam_total = TOEFL_COMPI + ';' + IELTS_Overall
        exam_reading = TOEFL_Reading + ';' + IELTS_Reading
        exam_listening = TOEFL_Listening + ';' + IELTS_Listening
        exam_speaking = TOEFL_Speaking + ';' + IELTS_Speaking
        exam_writing = TOEFL_Writing + ';' + IELTS_Writing
    else:
        proficiency_exam = 'NA'
        exam_total = 'NA'
        exam_reading = 'NA'
        exam_listening = 'NA'
        exam_speaking = 'NA'
        exam_writing = 'NA'
    headers.append(add_heading('Student ID', crow_id))
    headers.append(add_heading('Country', country))
    headers.append(add_heading('L1', L1))
    headers.append(add_heading('Heritage Spanish Speaker', heritage_spanish))
    headers.append(add_heading('Year in School', year_in_school_numeric))
    headers.append(add_heading('Gender', gender))
    headers.append(add_heading('College', college))
    headers.append(add_heading('Program', program))
    headers.append(add_heading('Proficiency Exam', proficiency_exam))
    headers.append(add_heading('Exam total', exam_total))
    headers.append(add_heading('Exam reading', exam_reading))
    headers.append(add_heading('Exam listening', exam_listening))
    headers.append(add_heading('Exam speaking', exam_speaking))
    headers.append(add_heading('Exam writing', exam_writing))
    return headers

def add_header_to_file(filepath, metadata, results):
    comma = ','
    # print('Adding headers to file ' + filepath)
    textfile = open(filepath, 'r')
    # Isolate the first row from the metadata for general text information
    # (Texts written by a group will have multiple rows)
    row = metadata[0]
    not_windows_filename = re.sub(r'\\', r'/', filepath)
    clean_filename = re.sub(r'\.\.\/', r'', not_windows_filename)
    filename_parts = clean_filename.split('/')
    assignment = filename_parts[-2][:2]
    draft = filename_parts[-2][2:]
    draft = re.sub('D', '', draft)
    course = clean(row['Catalog Nbr'])
    institution_code = re.sub(r'[a-z\s\-\–]', r'', clean(row['institution']))
    term = clean(row['term'])
    instructor = clean(row['Instructor Code'])
    section = clean(row['Class Section'])
    mode = clean(row['mode_of_course'])
    length = clean(row['length_of_course'])
    institution = clean(row['institution'])
    semester = term.split()[0]
    year = term.split()[1]
    if len(metadata) != 1:
        group_id = row['GROUP_ID']
    else:
        group_id = 'NA'


    # Build general headers.
    headers = []
    headers.append('<Text>')
    ids = []
    for student in metadata:
        ids.append(str(student['Crow ID'])) 
    headers.append(add_heading('Student IDs', comma.join(ids)))
    headers.append(add_heading('Group ID', group_id))
    headers.append(add_heading('Institution', institution))
    headers.append(add_heading('Course', 'ENGL ' + course))
    headers.append(add_heading('Mode', mode))
    headers.append(add_heading('Length', length))
    headers.append(add_heading('Assignment', assignment))
    headers.append(add_heading('Draft', draft))
    headers.append(add_heading('Course Year', year))
    headers.append(add_heading('Course Semester', semester))
    headers.append(add_heading('Instructor', instructor))
    headers.append(add_heading('Section', section))
    headers.append('</Text>')
    headers.append('')

    # Build student(s) metadata (if the text is written by a group, there will be more than one)
    inc = 1
    for student in metadata:
        headers.append('<Student ' + str(inc) + '>')
        headers = add_student(student, headers)
        headers.append('</Student ' + str(inc) + '>')
        headers.append('')
        inc += 1

    headers.append('<End Header>')
    headers.append('')

    # Build destintation directory
    path = os.path.join('files_with_headers', term, 'ENGL ' + course, assignment, draft)
    if not os.path.exists(path):
        os.makedirs(path)
    # Build output filename
    # Format: course_assignment_draft_country_yearinschool_gender_studentID_institution.txt
    filename_parts = [course, assignment, draft]
    if (len(metadata)) == 1:
        filename_parts.append(clean(row['Birth Country Code']))
        filename_parts.append(get_year_in_school_numeric(row['Acad Level']))
        filename_parts.append(clean(row['Gender']))
        filename_parts.append(clean(row['Crow ID']))
    else:
        filename_parts.append('G' + clean(row['GROUP_ID']))
    filename_parts.append(institution_code)
    output_filename = '_'.join(filename_parts)
    if "cues" in str(metadata[0]['institution']):
        output_filename += "_c"
    output_filename += '.txt'
    output_filename = re.sub(r'\s', r'', output_filename)
    output_filename = re.sub(r'__', r'_NA_', output_filename)
    if 'Series' in output_filename:
        print('Series found in output filename: ' + output_filename + '. Skipping...')
        return False

    output_file = open(os.path.join(path, output_filename), 'w', encoding="utf-8")
    filehash = create_file_hash(filepath)
    results.append([filepath, filehash, output_filename])

    # Write headers, line by line.
    for header in headers:
        print(header, file = output_file)
    for line in textfile:
        this_line = re.sub(r'\r?\n', r'\r\n', line)
        if this_line != '\r\n':
            new_line = re.sub(r'\s+', r' ', this_line)
            new_line = new_line.strip()
            print(new_line, file = output_file)
    output_file.close()
    textfile.close()
    return results


def add_headers_recursive(directory, master):
    total_files = 0
    files_with_metadata = 0
    files_without_metadata = 0
    results = []
    print('Running...')
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            # Skip non text files.
            if '.txt' not in name:
                continue
            total_files = total_files + 1
            filepath = os.path.join(dirpath, name)
            # Retrieve metadata for this file from the spreadsheet.
            metadata = get_metadata_for_file(filepath, master)
            if metadata:
                # We found metadata. Proceed to add headers to the file.
                results = add_header_to_file(filepath, metadata, results)
                files_with_metadata = files_with_metadata + 1
            else:
                files_without_metadata = files_without_metadata + 1
    print("")
    print('***************************************')
    print('Files found: ' + str(total_files))
    print('Files processed: ' + str(files_with_metadata))
    print('Files failed to process (no metadata match): ' + str(files_without_metadata))
    print('***************************************')
    analyze_results(results)

if args.master_file and args.dir:
    if '.xls' in args.master_file:
        master_file = pandas.ExcelFile(args.master_file)
        master_data = pandas.read_excel(master_file)
    elif '.csv' in args.master_file:
        master_data = pandas.read_csv(args.master_file)
    add_headers_recursive(args.dir, master_data)
else:
    print('You need to supply a valid master file and directory with textfiles')
