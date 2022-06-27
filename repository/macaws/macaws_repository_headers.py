#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import pandas
from shutil import copyfile

# PURPOSE: Given a structured directory of plaintext files with prepared filenames,
# prepend headers to each file and save to an output directory
#
# COMMAND SYNTAX:
#   python macaws_repository_filenames.py path
# Example (with actual test folder)
#   python macaws_repository_filenames.py test_data/pre_headers test_data/metadata.xlsx

output_dir = 'output'

### BEGIN PRE-RUN CHECKS ###

if len(sys.argv) < 2:
    print('** You must parameters to the script as follows: **')
    print('python macaws_repository_filenames.py test_data/pre_headers metadata_by_assignment_code.xlsx')
    exit()
directory = sys.argv[1:]

if not os.path.isdir(directory):
  print('The supplied folder is not a valid directory')
  exit()
metadata_file = sys.argv[2:]
if '.xls' in metadata_file:
        master_student_file = pandas.ExcelFile(metadata_file:)
        master_student_data = pandas.read_excel(metadata_file:)
    elif '.csv' in metadata_file:
        master_student_data = pandas.read_csv(metadata_file:)
    else:
        print('The supplied metadata file must be a CSV or XLSX file')
        exit()

### END PRE-RUN CHECKS ###

### Function to load the spreadsheet into a traversable list.
def get_metadata(file):
