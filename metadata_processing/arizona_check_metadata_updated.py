#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file and text files passed as arguments to the script,
# metadata headers are added to each individual text files
#
# Usage example:
#    python arizona_check_metadata.py --directory=Standardized --master_file=combined_spreadsheets_processed.csv
#    python check_metadata.py --directory=../../../Fall\ 2017/normalized --master_file=../../../Metadata/Fall\ 2017/Metadata_Fall_2017.xlsx
#    python check_metadata.py --directory=../../../Fall\ 2018/normalized --master_file=../../../Metadata/Fall\ 2018/Metadata_Fall\ 2018.xlsx

import argparse
import sys
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
        print('Unable to find any metadata for file:')
        print('    ' + filepath)
        if possible_matches:
            print('    Possible matches: ' + ', '.join(possible_matches))
        print('****************************************************************')
        return False
    #elif matches > 1:
        #print('More than one row of metadata matches this file: ' + filename)
        #return False
    else:
        # Success! We found a single metadata row corresponding to this file.
        return True

def get_student_name(name):
    parts = os.path.splitext(name)
    # Try to split name on hyphen
    student_filename = parts[0].split('- ')
    if len(student_filename) > 1:
        student_filename = student_filename[1]
    else:
        student_filename = student_filename[0]
    student_filename = re.sub(r'\s+', r' ', student_filename)
    return student_filename.strip()

def get_metadata_names(master):
    names = []
    data = master.to_dict(orient="records")
    for row in data:
        names.append(row['First Name'] + ' ' + row['Last Name'])
    return names


def check_metadata_recursive(directory, master):
    total_files = 0
    files_with_metadata = 0
    files_without_metadata = 0
    student_metadata_not_found = []
    student_filename_not_found = []
    students_names_from_files = []
    student_names_from_metadata = get_metadata_names(master)
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            # Skip non text files.
            if '.txt' not in name:
                continue
            total_files = total_files + 1
            filepath = os.path.join(dirpath, name)
            # Retrieve metadata for this file from the spreadsheet.
            metadata = get_metadata_for_file(filepath, master)
            if not metadata:
                files_without_metadata = files_without_metadata + 1
            else: 
                files_with_metadata = files_with_metadata + 1
            student_name_from_file = get_student_name(name)
            students_names_from_files.append(student_name_from_file)

    for name in student_names_from_metadata:
        if name not in students_names_from_files:
            if name not in student_metadata_not_found:
                student_metadata_not_found.append(name)
    print("***************")
    print("These student names are in the spreadsheet but NOT in the filenames: ")
    print("***************")
    print('\n'.join(map(str, student_metadata_not_found)))
    for student_filename in students_names_from_files:
        if student_filename not in student_names_from_metadata:
            if student_filename not in student_filename_not_found:
                student_filename_not_found.append(student_filename)
    print("***************")
    print("These student names are NOT in the spreadsheet but are in the filenames:")
    print("***************")
    print('\n'.join(map(str, student_filename_not_found)))

    print('***************************************')
    print('Total files found: ' + str(total_files))
    print('Files with matching metadata: ' + str(files_with_metadata))
    print('Files without matching metadata: ' + str(files_without_metadata))
    print('***************************************')


if args.master_file and args.dir:
    if '.xls' in args.master_file:
        master_file = pandas.ExcelFile(args.master_file)
        master_data = pandas.read_excel(master_file)
    elif '.csv' in args.master_file:
        master_data = pandas.read_csv(args.master_file)

    check_metadata_recursive(args.dir, master_data)
else:
    print('You need to supply a valid master file and directory with textfiles')
