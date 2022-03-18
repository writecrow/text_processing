#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION:
# Given a folder with .txt files (inlcuding subfolders) and an excel file with metadata,
# the script extracts information from the excel file and adds metadata headers to each individual text file.

# Usage examples
# Run the line below from the terminal on a Mac or command prompr on windows:
# Mac OS example:
# D2L
#    python ciabatta_headers.py --directory=standardized/101 --master_file=metadata_folder/master_student_data.xlsx
# BLACKBOARD
#    python ciabatta_headers.py --directory=standardized/10600 --master_file=metadata_folder/purdue_registrar_data.xlsx --cms=blackboard --config_file=metadata_folder/config_purdue.yaml

# Windows example:
# D2L
#    python ciabatta_headers.py --directory=standardized\101 --master_file=metadata_folder\master_student_data.xlsx
# BLACKBOARD
#   python ciabatta_headers.py --directory=standardized\10600 --master_file=metadata_folder\purdue_registrar_data.xlsx --cms=blackboard --config_file=metadata_folder\config_purdue.yaml

# imports packages
import argparse
import sys
import re
import os
import pandas
import yaml

# lists the required arguments (e.g. --directory=) sent to the script
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--master_file', action="store", dest='master_file', default='')
parser.add_argument('--cms', action="store", dest='cms', default='d2l')
parser.add_argument('--config_file', action="store", dest='config_file', default='metadata_folder/config.yaml')
args = parser.parse_args()

# function that removes leading spaces and replaces "NaN" with "NA"
def clean_string(my_string):
    my_string = my_string.strip()
    my_string = re.sub(r'NaN', r'NA', my_string)
    return(my_string)

# function to add the metadata headers to each individual text file
def add_header_common(filename, master_row, config_file, overwrite=False):
    # open individual text file
    textfile = open(filename, 'r')

    # open config file with column names
    config_file = open(config_file, 'r')
    headers_list = yaml.load(config_file, Loader=yaml.FullLoader)
    column_specs = headers_list['column_specs']
    fixed_expressions = headers_list['fixed_expressions']

    # normalizes path to work across platforms (PC, Mac)
    normed_path = os.path.normpath(filename)
    # splits the parts of the path across platforms
    filename_parts = normed_path.split(os.sep)

    print("Processing file: ", filename_parts)

    # retrieves and cleans course number from "course" column in the metadata spreasheet
    course = clean_string(master_row[column_specs['course']].to_string(index=False))

    # gets assignment and draft from the filename path (included in the folder structure)
    assignment = filename_parts[3][:2]
    draft = filename_parts[3][2:]
    # replaces "D" for draft to an empty space
    draft = re.sub('D', '', draft)

    # retrieves country code from "country_code" column in the metadata spreasheet
    country_code = master_row[column_specs['country_code']].to_string(index=False)
    # strips white spaces around the country_code values in the column
    country_code = country_code.strip()
    # replaces "NaN" to "NAN" for the country_code variable
    country_code = re.sub(r'NaN', r'NAN', country_code)

    # retrieves and cleans year in school from "year_in_school" column in the metadata spreasheet
    year_in_school = clean_string(master_row[column_specs['year_in_school']].to_string(index=False))

    # if school year is not one of the four numbers (1,2,3 or 4)
    if year_in_school not in ['1','2','3','4']:
        # if school year is freshman than year in school is 1
        if year_in_school.lower() == 'freshman':
            year_in_school_numeric = '1'
        # if school year is sophomore than year in school is 2
        elif year_in_school.lower() == 'sophomore':
            year_in_school_numeric = '2'
        # if school year is junior than year in school is 3
        elif year_in_school.lower() == 'junior':
            year_in_school_numeric = '3'
        # if school year is senior than year in school is 4
        elif year_in_school.lower() == 'senior':
            year_in_school_numeric = '4'
        # if school year is a different number we don't know what to do with it
        else:
            year_in_school_numeric = 'NA'
    # if school year is already a number than just save that
    else:
        year_in_school_numeric = year_in_school

    # retrieves and cleans gender from "gender" column in the metadata spreasheet
    gender = clean_string(master_row[column_specs['gender']].to_string(index=False))
    

    # retrieves crow id from "crow_id" column in the metadata spreasheet
    crow_id = clean_string(master_row[column_specs['crow_id']].to_string(index=False))
    if crow_id == "NA":
         print("This student does not have a Crow ID")
   

    # retrieves institution values from "institution_code" column in the metadata spreadsheet (for example University of Arizona)
    # and removes all lowercase characters from the string resulting in UA as an institution code
    institution_code = clean_string(master_row[column_specs['institution_code']].to_string(index=False))
    print("institution code: " + institution_code)

    # concatenate all parts to create filename in the following format: 106_LN_1_CH_2_F_20034_UA.txt
    output_filename = ''
    output_filename += course
    output_filename += '_'
    output_filename += assignment
    output_filename += '_'
    output_filename += draft
    output_filename += '_'
    output_filename += country_code
    output_filename += '_'
    output_filename += year_in_school_numeric
    output_filename += '_'
    output_filename += gender
    output_filename += '_'
    output_filename += crow_id
    output_filename += '_'
    output_filename += institution_code
    output_filename += '.txt'
    output_filename = re.sub(r'\s', r'', output_filename)
    output_filename = re.sub(r'__', r'_NA_', output_filename)

    # check if master_row has just one row
    if 'Series' not in output_filename:
        # retrieve term info from metadata row
        term = master_row[column_specs['term']].to_string(index=False)
        term = term.strip()

        # creates an output folder named "files_with_headers" with the term, course, assignment and draft subfolders
        new_folder = "files_with_headers"
        cwd = os.getcwd()
        path = os.path.join(cwd, new_folder, term, "ENGL " + course, assignment, draft)

        # checks if such a folder exists, if not, it creates the folder
        if not os.path.exists(path):
            os.makedirs(path)

        # specifies the path for the file to be written
        whole_path = os.path.join(path, output_filename)
        # open output file
        output_file = open(whole_path, 'w')
        print("Writing on file: ", path + output_filename)

        # retrieves and cleans country from "country" column in the metadata spreasheet
        country = clean_string(master_row[column_specs['country']].to_string(index=False))

        # retrieves and cleans institution from "institution" column in the metadata spreasheet
        institution = clean_string(master_row['institution'].to_string(index=False))
        

        section = clean_string(master_row['section'].to_string(index=False))
        L1 = clean_string(master_row['NATIVE_LANGUAGE_DESC'].to_string(index=False))

        # creates a semester variable from the first element of the term variable
        # assuming term is "Spring 2019" for example
        semester = term.split()[0]
        # creates a year variable from the second element of the term variable
        year = term.split()[1]

        # retrieves college from "college" column in the metadata spreasheet
        college = clean_string(master_row[column_specs['college']].to_string(index=False))
        # retrieves program from "program" column in the metadata spreasheet
        program = clean_string(master_row[column_specs['program']].to_string(index=False))
        # retrieves overall TOEFL scores from "TOEFL_COMPI" column in the metadata spreasheet
        TOEFL_COMPI = clean_string(master_row[column_specs['TOEFL_COMPI']].to_string(index=False))
        # retrieves TOEFL listening scores from "TOEFL_Listening" column in the metadata spreasheet
        TOEFL_Listening = clean_string(master_row[column_specs['TOEFL_Listening']].to_string(index=False))
        # retrieves TOEFL reading scores from "TOEFL_Reading" column in the metadata spreasheet
        TOEFL_Reading = clean_string(master_row[column_specs['TOEFL_Reading']].to_string(index=False))
        # retrieves TOEFL writing scores from "TOEFL_Writing" column in the metadata spreasheet
        TOEFL_Writing = clean_string(master_row[column_specs['TOEFL_Writing']].to_string(index=False))
        # retrieves TOEFL speaking scores from "TOEFL_Speaking" column in the metadata spreasheet
        TOEFL_Speaking = clean_string(master_row[column_specs['TOEFL_Speaking']].to_string(index=False))
        # retrieves overall IELTS scores from "IELTS_Overall" column in the metadata spreasheet
        IELTS_Overall = clean_string(master_row[column_specs['IELTS_Overall']].to_string(index=False))
        # retrieves IELTS listening scores from "IELTS_Listening" column in the metadata spreasheet
        IELTS_Listening = clean_string(master_row[column_specs['IELTS_Listening']].to_string(index=False))
        # retrieves IELTS reading scores from "IELTS_Reading" column in the metadata spreasheet
        IELTS_Reading = clean_string(master_row[column_specs['IELTS_Reading']].to_string(index=False))
        # retrieves IELTS writing scores from "IELTS_Writing" column in the metadata spreasheet
        IELTS_Writing = clean_string(master_row[column_specs['IELTS_Writing']].to_string(index=False))
        # retrieves IELTS speaking scores from "IELTS_Speaking" column in the metadata spreasheet
        IELTS_Speaking = clean_string(master_row[column_specs['IELTS_Speaking']].to_string(index=False))
        # retrieves instructor information from "instructor" column in the metadata spreasheet
        instructor = clean_string(master_row[column_specs['instructor']].to_string(index=False))
        #section = master_row[column_specs['country']].to_string(index=False)

        # retrieves mode (e.g. face to face) from "mode" column in the metadata spreasheet
        mode = clean_string(master_row[column_specs['mode']].to_string(index=False))
        # retrieves course length (e.g. 16 weeks) from "length" column in the metadata spreasheet
        length = clean_string(master_row[column_specs['length']].to_string(index=False))

        # creates new variables to combine proficiency exam scores
        proficiency_exam = ''
        exam_total = ''
        exam_reading = ''
        exam_listening = ''
        exam_speaking = ''
        exam_writing = ''

        # checks if the "TOEFL_COMPI" values are not "NA"s
        if TOEFL_COMPI != 'NA':
            # if they are not "NA"s, then the proficiency exam is TOEFL
            proficiency_exam = 'TOEFL'
            exam_total = TOEFL_COMPI
            exam_reading = TOEFL_Reading
            exam_listening = TOEFL_Listening
            exam_speaking = TOEFL_Speaking
            exam_writing = TOEFL_Writing
        # checks if the "IELTS_Overall" values are not "NA"s
        elif IELTS_Overall != 'NA':
            # if they are not "NA"s, then the proficiency exam is IELTS
            proficiency_exam = 'IELTS'
            exam_total = IELTS_Overall
            exam_reading = IELTS_Reading
            exam_listening = IELTS_Listening
            exam_speaking = IELTS_Speaking
            exam_writing = IELTS_Writing
        # checks if both the "IELTS_Overall" values and "TOEFL_COMPI" are not "NA"s
        elif TOEFL_COMPI != 'NA' and IELTS_Overall != 'NA':
            # if they are not "NA"s, then the proficiency exams are both TOEFL and IELTS
            proficiency_exam = 'TOEFL;IELTS'
            exam_total = TOEFL_COMPI + ';' + IELTS_Overall
            exam_reading = TOEFL_Reading + ';' + IELTS_Reading
            exam_listening = TOEFL_Listening + ';' + IELTS_Listening
            exam_speaking = TOEFL_Speaking + ';' + IELTS_Speaking
            exam_writing = TOEFL_Writing + ';' + IELTS_Writing
        # if the conditions above are not met, the proficiency exam scores are not available
        else:
            proficiency_exam = 'NA'
            exam_total = 'NA'
            exam_reading = 'NA'
            exam_listening = 'NA'
            exam_speaking = 'NA'
            exam_writing = 'NA'

        # get fixed expression for course from config file
        course_prefix = fixed_expressions['course_prefix']

        # write headers out in the output file
        print("<Text>", file=output_file)
        print("<Student IDs: " + crow_id + ">", file = output_file)
        print("<Group ID: NA>", file = output_file)
        print("<Institution: " + institution + ">", file = output_file)
        print("<Course: " + course_prefix + " " + course + ">", file = output_file)
        print("<Mode: " + mode + ">", file = output_file)
        print("<Length: " + length + ">", file = output_file)
        print("<Assignment: " + assignment + ">", file = output_file)
        print("<Draft: " + draft + ">", file = output_file)
        print("<Course Year: " + year + ">", file = output_file)
        print("<Course Semester: " + semester + ">" , file = output_file)
        print("<Instructor: " + instructor + ">", file = output_file)
        print("<Section: " + section + ">", file = output_file)
        print("</Text>", file=output_file)
        print("", file=output_file)
        print("<Student 1>", file=output_file)
        print("<Student ID: " + crow_id + ">", file = output_file)
        print("<Country: " + country + ">", file = output_file)
        print("<L1: " + L1 + ">", file = output_file)
        print("<Heritage Spanish Speaker: NA>", file = output_file)
        print("<Year in School: " + year_in_school_numeric + ">", file = output_file)
        print("<Gender: " + gender + ">", file = output_file)
        print("<College: " + college + ">", file = output_file)
        print("<Program: " + program + ">", file = output_file)
        print("<Proficiency Exam: " + proficiency_exam +">", file = output_file)
        print("<Exam total: " + exam_total + ">", file = output_file)
        print("<Exam reading: " + exam_reading + ">", file = output_file)
        print("<Exam listening: " + exam_listening + ">", file = output_file)
        print("<Exam speaking: " + exam_speaking + ">", file = output_file)
        print("<Exam writing: " + exam_writing + ">", file = output_file)
        print("</Student 1>", file=output_file)
        print("<End Header>", file = output_file)
        print("", file = output_file)

        # attempt to standardize line breaks
        for line in textfile:
            this_line = re.sub(r'\r?\n', r'\r\n', line)
            if this_line != '\r\n':
                new_line = re.sub(r'\s+', r' ', this_line)
                new_line = new_line.strip()
                print(new_line, file = output_file)

        output_file.close()
    textfile.close()
    config_file.close()

# creates a function specific to blackboard metadata, which uses career accounts to match
# the spreadsheet data and filenames
def add_header_to_file_blackboard(filename, master, config_file, overwrite=False):
    found_text_files = False
    if '.txt' in filename: #check the indent
        found_text_files = True

        # create a list fo all career accounts
        career_account_list = master_data['User_ID'].tolist()
             

        # for each career account in list
        for career_account in career_account_list:
            # check if that career account is in filename (that's our student!)
            if re.search('_'+str(career_account)+'_', filename):
                # let user know that there was a match
                print('Matched: ', '_'+career_account+'_', "is in", filename,'and adding headers...')

                # retrieve row for that student from metadata
                filtered_master = master[master['User_ID'] == career_account]

                # call add header with that student metadata row
                add_header_common(filename, filtered_master, config_file, overwrite=False)

    # let main function know text files were processed (or not)
    return(found_text_files)

# creates a function specific to d2l course management system metadata, which uses student names to match
# the spreadsheet data and filenames
def add_header_to_file_d2l(filename, master, config_file, overwrite=False):
    # only works with .txt files
    found_text_files = False
    if '.txt' in filename:
        # indicates that this is a .txt file
        found_text_files = True
        # splits the filename by a dash with a space "- "
        filename_parts = filename.split('- ')
        
        # removes ".txt" extension from the filename
        student_name = re.sub(r'\.txt', r'', filename_parts[1])
        # removes any extra spaces from the filename
        student_name = re.sub(r'\s+', r' ', student_name)
      
        # checks to see if the last element of the student name is "-"
        if student_name[-1] == '-':
            # if it is, it removes it
            student_name = student_name[:-1]
        # splits the student name by white space
        student_name_parts = student_name.split()
        # checks if the student name has more than two names
        if len(student_name_parts) != 2:
            print('***********************************************')
            # if there are more than two names, it prints 'File has student name with more than two names: '
            print('File has student name with more than two names: ' + filename)
            print(student_name_parts)

        # retrieves last name from "Last Name" column in the metadata spreasheet
        filtered_master1 = master[master['Last Name'] == student_name_parts[-1]]
        # retrieves first name from "First Name" column in the metadata spreasheet
        filtered_master2 = filtered_master1[filtered_master1['First Name'] == student_name_parts[0]]
        # checks to see if the given student names exist in the metadata spreadsheet
        if filtered_master2.empty:
            print('***********************************************')
            print('Unable to find metadata for this file: ')
            print(filename)
            print(student_name_parts)

        # checks to see if there is more than one row for the same student in the metadata spreadsheet
        if filtered_master2.shape[0] > 1:
            print('***********************************************')
            print('More than one row in metadata for this file: ')
            print(filename)
            print(student_name_parts)
        else:
            print('Adding headers to file ' + filename)
            add_header_common(filename, filtered_master2, config_file, overwrite=False)
        #institution_code = re.sub(r'[a-z\s]', r'', master_row[column_specs['institution_code']].to_string(index=False))

    # returns whether text file was found
    return(found_text_files)

# creates a function that adds headers and changes filenames recursively on all the files in the specified directory
def add_headers_recursive(directory, master, cms, config_file, overwrite=False):
    # creates control variable to check if there were any text files in the provided folder
    found_text_files = False
    # walks folder structure to get all files in all folders
    for dirpath, dirnames, files in os.walk(directory):
        # for every file found in a folder
        for name in files:
            if cms == "d2l":
                # calls function that add headers to an individual file specific to d2l
                is_this_a_text_file = add_header_to_file_d2l(os.path.join(dirpath, name), master, config_file, overwrite)
            elif cms == "blackboard":
                # calls function that add headers to an individual file specific to blackboard
                is_this_a_text_file = add_header_to_file_blackboard(os.path.join(dirpath, name), master, config_file, overwrite)
            # changes the variable if a text file was processed
            if is_this_a_text_file:
                found_text_files = True
    # if no .txt texts were found in the directory, it prints "No text files found in the directory"
    if not found_text_files:
        print('No text files found in the directory.')

# checks if the user has specified the master student file (excel or csv file)
if args.master_file and args.dir:
    if '.xls' in args.master_file:
        master_file = pandas.ExcelFile(args.master_file)
        master_data = pandas.read_excel(master_file)

    elif '.csv' in args.master_file:
        master_data = pandas.read_csv(args.master_file)

    # calls function that adds headers to each file in a folder and all subfolders recursively
    add_headers_recursive(args.dir, master_data, args.cms, args.config_file, args.overwrite)
else:
    print('You need to supply a valid master file and directory with textfiles')
