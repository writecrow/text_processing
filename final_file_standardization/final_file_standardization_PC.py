#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given a directory with text files passed as argument
# to the script, the folder directory is copied copying over
# all text files. File names are cleaned (_checked and _deidentified) are
# removed from file and folder names. And all lines breaks are replaced with
# notepad readable line breaks (\r\n)
#
# Usage example:
#   python final_file_standardization.py --directory=../../../Fall\ 2017/deidentified/
#   python final_file_standardization.py --directory=deidentified_files/Spring\ 2018/
#   python final_file_standardization.py --directory=../../../MACAWS/deidentified_files/


import argparse
import os
import re
import sys

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Copy folder structure')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()


def clean_file(filename, overwrite=False):
    if '.txt' in filename:
        clean_filename = re.sub(r'\.\.[\\\/]', r'', filename)
        clean_filename = re.sub(r'(\s)?_checked|_deidentified', '', clean_filename, flags=re.IGNORECASE)
        # remove extra folders
        clean_filename = re.sub(r'(.+[\\\/])+(Fall|Spring|Summer|Winter)', '\\g<2>', clean_filename)
        output_dir = 'final_version'
        output_filename = os.path.join(output_dir, clean_filename)
        output_directory = os.path.dirname(output_filename)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        original_file = open(filename, 'r', encoding = 'utf-8')
        original_contents = original_file.read()

        print("Preparing final version of file: " + output_filename)
        #clean_contents = re.sub(r'(\r+)?\n', '\r\n', original_contents)

        output_file = open(output_filename, 'w', encoding='utf-8')
        output_file.write(original_contents)

        original_file.close()
        output_file.close()

def clean_all_files(directory, overwrite=False):
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            clean_file(os.path.join(dirpath, name), overwrite)

if args.dir:
    clean_all_files(args.dir)
else:
    print('You need to supply a valid directory with textfiles')
