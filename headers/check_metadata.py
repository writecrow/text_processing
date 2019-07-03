#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file and text files passed as arguments to the script,
# metadata headers are added to each individual text files
#
# Usage example:
#    python check_metadata.py --directory=../../../Spring\ 2018/Normalized/ --master_file=../../../Metadata/Spring\ 2018/Metadata_Spring\ 2018.xlsx

import argparse
import sys
import re
import os
import pandas

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--master_file', action="store", dest='master_file', default='')
args = parser.parse_args()


def add_header_to_file(filename, master, overwrite=False):
    if '.txt' in filename:
        output_filename = filename
        if (not overwrite):
            output_dir = 'files_with_headers'
            output_filename = os.path.join(output_dir, filename)
            output_directory = os.path.dirname(output_filename)
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

        # Open the file so we can guess its encoding.
        textfile = open(filename, 'r')
        filename_parts = filename.split('- ')
        student_name = re.sub(r'\.txt', r'', filename_parts[1])
        student_name = re.sub(r'\s+', r' ', student_name)
        if student_name[-1] == '-':
            student_name = student_name[:-1]
        student_name_parts = student_name.split()
        if len(student_name_parts) != 2:
            print('***********************************************')
            print('File has student name with more than two names: ' + filename)
            print(student_name_parts)

        filtered_master1 = master[master['Last Name'] == student_name_parts[-1]]
        filtered_master2 = filtered_master1[filtered_master1['First Name'] == student_name_parts[0]]
        if filtered_master2.empty:
            print('***********************************************')
            print('Unable to find metadata for this file: ')
            print(filename)
            print(student_name_parts)

        if filtered_master2.shape[0] > 1:
            print('***********************************************')
            print('More than one row in metadata for this file: ')
            print(filename)
            print(student_name_parts)

        textfile.close()

def add_headers_recursive(directory, master, overwrite=False):
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            add_header_to_file(os.path.join(dirpath, name), master, overwrite)


if args.master_file and args.dir:
    if '.xls' in args.master_file:
        master_file = pandas.ExcelFile(args.master_file)
        master_data = pandas.read_excel(master_file)
    elif '.csv' in args.master_file:
        master_data = pandas.read_csv(args.master_file)

    add_headers_recursive(args.dir, master_data, args.overwrite)
else:
    print('You need to supply a valid master file and directory with textfiles')
