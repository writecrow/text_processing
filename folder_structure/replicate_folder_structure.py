#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given a directory with text files passed as argument
# to the script, the folder directory is copied without copying
# the actual text files.
#
# Usage example:
#   python replicate_folder_structure.py --directory=../../../Fall\ 2017/deidentified/
#   python replicate_folder_structure.py --directory=deidentified_files/Spring\ 2018/
#   python replicate_folder_structure.py --directory=../../../MACAWS/deidentified_files/


import argparse
import os
import re
import sys

from shutil import copyfile

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Copy folder structure')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()


def copy_folder_structure(directory):
    list_of_directories = []
    for dirpath, dirnames, files in os.walk(directory):
        copied_dir = re.sub(r'\.\.[\\\/]', r'', dirpath)
        extra_directory = 'copied_folder_structure'
        output_directory = os.path.join(extra_directory, copied_dir)
        print("Creating directory: " + output_directory)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)


if args.dir:
    copy_folder_structure(args.dir)
else:
    print('You need to supply a valid directory with textfiles')