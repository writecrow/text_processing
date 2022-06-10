#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file and text files passed as arguments to the script,
# metadata headers are added to each individual text files, 
# written to the directory "files_with_headers"
#
# Mac OS example:
#    python add_headers.py --directory=Spring\ 2018/normalized/ --master_file=Metadata_Spring_2018_updated.csv
#    python add_headers.py --directory=Fall\ 2018/normalized/ --master_file=Metadata_Fall_2018_updated.csv
#    python add_headers.py --directory=../../../Fall\ 2017/normalized/ --master_file=../../../Metadata/Fall\ 2017/Metadata_Fall_2017.xlsx
#
# Windows run with Anaconda Prompt example:
#    python add_headers.py --directory="Fall 2018/normalized/" --master_file="Metadata_Fall_2018_updated.csv"

import argparse
import re
import os
import pandas

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--master_file', action="store", dest='master_file', default='')
args = parser.parse_args()


def get_metadata_for_file(filepath, master):
    # Convert the master spreadsheet to an easily traversable dictionary.
    data = master.to_dict(orient="records")
    normed_path = os.path.normpath(filepath)
    # splits the parts of the path across platforms
    filepath_parts = normed_path.split(os.sep)
    # The filename is the final segment of a split path.
    filename = filepath_parts[-1]
    # Check two different methods to discover the metadata: explicit filename, or student name concatenated.
    matches = 0
    possible_matches = []
    target_row = {}
    # Loop through rows in the master spreadsheet.
    for row in data:
        fullname = row['First Name'] + ' ' + row['Last Name']
        short_first_name = row['First Name'].split(' ')
        short_last_name = row['Last Name'].split(' ')
        if short_last_name[-1]:
            short_last_name = short_last_name[-1]
        if short_first_name[0]:
            short_first_name = short_first_name[0]
        short_fullname = short_first_name + ' ' + short_last_name
        # If there is an explicit filename segment in this row, see if it is contained in the file's name.
        if str(row['Filename']) in filename:
            matches = matches + 1
            target_row = row
        elif fullname in filename:
            matches = matches + 1
            target_row = row
        elif short_fullname in filename:
            matches = matches + 1
            target_row = row
        elif row['Last Name'] in filename:
            possible_matches.append(
                row['First Name'] + ' ' + row['Last Name'])
    # Report the results of our search.
    if matches == 0:
        print('Unable to find any metadata for this file: ' + filename)
        if possible_matches:
            print('Possible match in spreadsheet:')
            print(possible_matches)
        return False
    elif matches > 1:
        print('More than one row of metadata matches this file: ' + filename)
        return False
    else:
        # Success! We found a single metadata row corresponding to this file.
        return target_row

# function that removes leading spaces and replaces "NaN" with "NA"
def clean(my_string):
    if (type(my_string)) is not str:
        my_string = str(my_string)
    my_string = my_string.strip()
    my_string = re.sub(r'NaN', r'NA', my_string)
    return my_string

def add_header_to_file(filepath, metadata):
    # print('Adding headers to file ' + filepath)
    textfile = open(filepath, 'r')
    not_windows_filename = re.sub(r'\\', r'/', filepath)
    clean_filename = re.sub(r'\.\.\/', r'', not_windows_filename)
    filename_parts = clean_filename.split('/')
    course = clean(metadata['Catalog Nbr'])
    assignment = filename_parts[-2][:2]
    draft = filename_parts[-2][2:]
    draft = re.sub('D', '', draft)
    country_code = clean(metadata['Birth Country Code'])
    year_in_school = clean(metadata['Acad Level'])
    if year_in_school not in ['1','2','3','4']:
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
    gender = clean(metadata['Gender'])
    crow_id = clean(metadata['Crow ID'])
    institution_code = re.sub(r'[a-z\s\-\–]', r'', clean(metadata['institution']))
    # Format: course_assignment_draft_country_yearinschool_gender_studentID_institution.txt
    output_filename = '_'.join([course, assignment, draft, country_code, year_in_school_numeric, gender, crow_id, institution_code])
    if "cues" in str(metadata['institution']):
        output_filename += "_c"
    output_filename += '.txt'
    output_filename = re.sub(r'\s', r'', output_filename)
    output_filename = re.sub(r'__', r'_NA_', output_filename)
    if 'Series' in output_filename:
        print('Series found in output filename: ' + output_filename + '. Skipping...')
        return False

    term = clean(metadata['term'])
    path = os.path.join('files_with_headers', term, 'ENGL ' + course, assignment, draft)

    if not os.path.exists(path):
        os.makedirs(path)
    output_file = open(os.path.join(path, output_filename), 'w')

    country = clean(metadata['Descr'])
    institution = clean(metadata['institution'])
    semester = term.split()[0]
    year = term.split()[1]
    college = clean(metadata['College'])
    program = clean(metadata['Major'])
    TOEFL_COMPI = clean(metadata['TOEFL COMPI'])
    TOEFL_Listening = clean(metadata['TOEFL Listening'])
    TOEFL_Reading = clean(metadata['TOEFL Reading'])
    TOEFL_Writing = clean(metadata['TOEFL Writing'])
    TOEFL_Speaking = clean(metadata['TOEFL Speaking'])
    IELTS_Overall = clean(metadata['IELTS Overall Band Score'])
    IELTS_Listening = clean(metadata['IELTS Listening'])
    IELTS_Reading = clean(metadata['IELTS Reading'])
    IELTS_Writing = clean(metadata['IELTS Writing'])
    IELTS_Speaking = clean(metadata['IELTS Speaking'])
    instructor = clean(metadata['Instructor Code'])
    section = clean(metadata['Class Section'])
    mode = clean(metadata['mode_of_course'])
    length = clean(metadata['length_of_course'])
    L1 = clean(metadata['L1'])
    heritage_spanish = clean(metadata['Heritage Spanish'])
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

    # write headers in
    print("<Student ID: " + crow_id + ">", file = output_file)
    print("<Country: " + country + ">", file = output_file)
    print("<L1: " + L1 + ">", file = output_file)
    print("<Heritage Spanish Speaker: " + heritage_spanish.capitalize() + ">", file = output_file)
    print("<Institution: " + institution + ">", file = output_file)
    print("<Course: ENGL " + course + ">", file = output_file)
    print("<Mode: " + mode + ">", file = output_file)
    print("<Length: " + length + ">", file = output_file)
    print("<Assignment: " + assignment + ">", file = output_file)
    print("<Draft: " + draft + ">", file = output_file)
    print("<Year in School: " + year_in_school_numeric + ">", file = output_file)
    print("<Gender: " + gender + ">", file = output_file)
    print("<Course Year: " + year + ">", file = output_file)
    print("<Course Semester: " + semester + ">" , file = output_file)
    print("<College: " + college + ">", file = output_file)
    print("<Program: " + program + ">", file = output_file)
    print("<Proficiency Exam: " + proficiency_exam +">", file = output_file)
    print("<Exam total: " + exam_total + ">", file = output_file)
    print("<Exam reading: " + exam_reading + ">", file = output_file)
    print("<Exam listening: " + exam_listening + ">", file = output_file)
    print("<Exam speaking: " + exam_speaking + ">", file = output_file)
    print("<Exam writing: " + exam_writing + ">", file = output_file)
    print("<Instructor: " + instructor + ">", file = output_file)
    print("<Section: " + section + ">", file = output_file)
    print("<End Header>", file = output_file)
    print("", file = output_file)
    for line in textfile:
        this_line = re.sub(r'\r?\n', r'\r\n', line)
        if this_line != '\r\n':
            new_line = re.sub(r'\s+', r' ', this_line)
            new_line = new_line.strip()
            print(new_line, file = output_file)
    output_file.close()
    textfile.close()


def add_headers_recursive(directory, master):
    total_files = 0
    files_with_metadata = 0
    files_without_metadata = 0
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
                add_header_to_file(filepath, metadata)
                files_with_metadata = files_with_metadata + 1
            else:
                files_without_metadata = files_without_metadata + 1
    print('***************************************')
    print('Total files found: ' + str(total_files))
    print('Files successfully processed: ' + str(files_with_metadata))
    print('Files failed to process: ' + str(files_without_metadata))
    print('***************************************')


if args.master_file and args.dir:
    if '.xls' in args.master_file:
        master_file = pandas.ExcelFile(args.master_file)
        master_data = pandas.read_excel(master_file)
    elif '.csv' in args.master_file:
        master_data = pandas.read_csv(args.master_file)
    add_headers_recursive(args.dir, master_data)
else:
    print('You need to supply a valid master file and directory with textfiles')
