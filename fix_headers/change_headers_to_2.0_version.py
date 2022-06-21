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
        output_dir = 'new_header'
        output_filename = os.path.join(output_dir, clean_filename)
        output_directory = os.path.dirname(output_filename)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        original_file = open(filename, 'r')
        original_contents = original_file.read()

        print("Changing headers of file: " + output_filename)

        where_body = original_contents.find("<End Header>")
        text_body = original_contents[where_body+13:]
        headers = original_contents[:where_body+13]

        list_of_headers = headers.split("\n")

        output_file = open(output_filename, 'w')
        student_ID_line = list_of_headers[0]

        print("<Text>", file=output_file)
        print("<Student IDs: " + student_ID_line[13:], file=output_file)
        print("<Group ID: NA>", file=output_file)
        print(list_of_headers[2], file=output_file)
        print(list_of_headers[3], file=output_file)
        print(list_of_headers[4], file=output_file)
        print(list_of_headers[5], file=output_file)
        print(list_of_headers[6], file=output_file)
        print(list_of_headers[7], file=output_file)
        print(list_of_headers[10], file=output_file)
        print(list_of_headers[11], file=output_file)
        print(list_of_headers[20], file=output_file)
        if "Section" in list_of_headers[21]:
           print(list_of_headers[21], file=output_file)
        else:
            print("<Section: NA>", file=output_file)
        print("</Text>", file=output_file)
        print("", file=output_file)
        print("<Student 1>", file=output_file)
        print(list_of_headers[0], file=output_file)
        print(list_of_headers[1], file=output_file)
        print("<L1: NA>", file=output_file)
        print("<Heritage Spanish Speaker: NA>", file=output_file)
        print(list_of_headers[8], file=output_file)
        print(list_of_headers[9], file=output_file)
        print(list_of_headers[12], file=output_file)
        print(list_of_headers[13], file=output_file)
        print(list_of_headers[14], file=output_file)
        print(list_of_headers[15], file=output_file)
        print(list_of_headers[16], file=output_file)
        print(list_of_headers[17], file=output_file)
        print(list_of_headers[18], file=output_file)
        print(list_of_headers[19], file=output_file)
        print("</Student 1>", file=output_file)
        if "End Header" in list_of_headers[22]:
            print(list_of_headers[22], file=output_file)
        else:
            print("<End Header>", file=output_file)
        print("", file=output_file)
        print(text_body, file=output_file)

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
