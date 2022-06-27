#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import sys
import os
import pandas
from shutil import copyfile

# PURPOSE: Given a structured directory of plaintext files with prepared filenames,
# prepend headers to each file and save to directory "files_with_headers".
#
# COMMAND SYNTAX:
#   python macaws_repository_filenames.py path
# Example (with actual test folder)
#   python macaws_repository_headers.py test_data/pre_headers test_data/metadata.csv

### BEGIN PRE-RUN CHECKS ###

if len(sys.argv) < 2:
    print('** You must parameters to the script as follows: **')
    print('python macaws_repository_filenames.py test_data/pre_headers test_data/metadata.csv')
    exit()
directory = sys.argv[1]

if not os.path.isdir(directory):
    print('The supplied folder is not a valid directory')
    exit()
metadata_file = sys.argv[2]
if '.xlsx' in metadata_file:
    metadata_file = pandas.ExcelFile(metadata_file)
    metadata = pandas.read_excel(metadata_file)
elif '.csv' in metadata_file:
    metadata = pandas.read_csv(metadata_file)
else:
    print('The supplied metadata file must be a CSV or XLSX file')
    exit()

# Convert the metadata spreadsheet to an easily traversable dictionary.
data = metadata.to_dict(orient="records")
institution = 'UA'

### END PRE-RUN CHECKS ###

# Removes leading spaces and replaces "NaN" with "NA"
def clean(my_string):
    if (type(my_string)) is not str:
        my_string = str(my_string)
    my_string = my_string.strip()
    my_string = re.sub(r'nan', r'NA', my_string)
    my_string = re.sub(r'NaN', r'NA', my_string)
    return my_string

### Try to find the text's metadata by 'Assignment Code' match.
def get_metadata_by_assignment(assignment):
    for row in data:
        if str(row['Assignment Code']) == str(assignment):
            return row
    # Otherwise, no metadata was found.
    return False

def add_heading(key, value, filename):
    print("<" + key + ": " + value + ">", file=filename)


def add_header_to_file(filepath, info):
    # print('Adding headers to file ' + filepath)
    textfile = open(filepath, 'r')

    path = os.path.normpath(filepath)
    path_parts = path.split(os.sep)

    # @todo: manipulate output filename as needed.
    output_filename = path_parts[-1]
    output_path = os.path.join(
        'files_with_headers', path_parts[-6], path_parts[-5], path_parts[-4], path_parts[-3], path_parts[-2])
    ## Get data from metadata
    macrogenre = clean(info['Macrogenre'])

    if not os.path.exists(output_path):
        os.makedirs(output_path)
    output_file = open(os.path.join(output_path, output_filename), 'w')

    # Write headers, line by line.
    add_heading('Institution', institution, output_file)
    add_heading('Macrogenre', macrogenre, output_file)
    print("<End Header>", file=output_file)
    print("", file=output_file)
    for line in textfile:
        this_line = re.sub(r'\r?\n', r'\r\n', line)
        if this_line != '\r\n':
            new_line = re.sub(r'\s+', r' ', this_line)
            new_line = new_line.strip()
            print(new_line, file=output_file)
    output_file.close()
    textfile.close()

def add_headers_recursive(directory):
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
            parts = name.split('_')
            assignment = parts[1]
            total_files = total_files + 1
            filepath = os.path.join(dirpath, name)
            # Retrieve metadata for this file from the spreadsheet.
            info = get_metadata_by_assignment(assignment)
            if info:
                # We found metadata. Proceed to add headers to the file.
                results = add_header_to_file(filepath, info)
                files_with_metadata = files_with_metadata + 1
            else:
                files_without_metadata = files_without_metadata + 1
    print("")
    print('***************************************')
    print('Files found: ' + str(total_files))
    print('Files processed: ' + str(files_with_metadata))
    print('Files failed to process (no metadata match): ' + str(files_without_metadata))
    print('***************************************')

add_headers_recursive(directory)
