#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given a directory with text files passed as argument
# to the script, student, course and draft headers are changed to
# match PSLW headers
#
# Usage example:
#   python fix_aslw_headers.py --directory=../../../final_version/ASLW/Fall\ 2017/

import argparse
import os
import re
import sys

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Fix ASLW headers')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()


def fix_headers(filename, overwrite=False):
    if '.txt' in filename:
        clean_filename = re.sub(r'\.\.[\\\/]', r'', filename)
        output_dir = 'fixed_headers'
        output_filename = os.path.join(output_dir, clean_filename)
        output_directory = os.path.dirname(output_filename)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        original_file = open(filename, 'r')
        original_contents = original_file.read()

        print("Fixing headers of file: " + output_filename)
        # add "Student" before "ID" in ID header
        fixed_contents = re.sub(r'(<)(ID:\s\d+>)', '\g<1>Student \g<2>', original_contents)

        # add "ENGL" before course number in course header
        fixed_contents = re.sub(r'(<Course:\s)(\d+>)', '\g<1>ENGL \g<2>', fixed_contents)

        # remove "D" from draft number in draft header
        fixed_contents = re.sub(r'(<Draft:\s)D(\d|F>)', '\g<1>\g<2>', fixed_contents)

        # add space after <End Header>
        fixed_contents = re.sub(r'(<End Header>)', '\g<1>\r\n', fixed_contents)

        output_file = open(output_filename, 'w')
        output_file.write(fixed_contents)

        original_file.close()
        output_file.close()

def fix_headers_all_files(directory, overwrite=False):
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            fix_headers(os.path.join(dirpath, name), overwrite)

if args.dir:
    fix_headers_all_files(args.dir)
else:
    print('You need to supply a valid directory with textfiles')
