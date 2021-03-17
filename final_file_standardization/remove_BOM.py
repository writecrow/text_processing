#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: this is a generic text processing script that can be used as a
# template for text processing
#
# Usage example:
#   python text_processing_skeleton.py --directory=files_with_headers

import argparse
import os
import re
import sys


# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Process Textfiles in a Directory')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()

# individual text processing function that is called by the recursive function
def process_file(filename, overwrite=False):
    # only process text files
    found_text_files = False
    if '.txt' in filename:
        found_text_files = True

        # create output filename with directory path
        # first eliminate any relative path dots from filename
        # so that files are saved relative to current directory only
        cleaned_filename = re.sub(r'\.\.[\\\/]', r'', filename)
        # create a new folder
        output_directory = 'no_BOM'
        # join the new folder with the folders already in the filename
        output_filename = os.path.join(output_directory, cleaned_filename)
        # get the directory path (without the actual filename, just folders)
        directory = os.path.dirname(output_filename)
        # check if the folder structure already exists
        if not os.path.exists(directory):
            # create folder structure if it does not exist
            os.makedirs(directory)

        # open original textfile and new output file
        original_textfile = open(filename, 'r')
        output_file = open(output_filename, 'w')

        file_contents = original_textfile.read()

        if file_contents[0] != "<" and file_contents[1] == "<":
            output_file.write(file_contents[1:])
        elif file_contents[0] == "<":
            output_file.write(file_contents[0:])
        else:
            print("Couldn't process file" + filename)

        # close original textfile and new output file
        original_textfile.close()
        output_file.close()

    return(found_text_files)

# recursive function that calls in the individual process file function for
# every file in the directory passed as a argument
def process_recursive(directory, overwrite=False):
    # create control for text files, to check if there are any text files
    # in the give directory
    found_text_files = False
    # walk the subfolders in the given directory
    for dirpath, dirnames, files in os.walk(directory):
        # for every file in all the subfolders
        for name in files:
            # call individual text processing function that returns a boolean
            is_this_a_text_file = process_file(os.path.join(dirpath, name), overwrite)
            # if is_this_a_text_file is True that means a text file was found
            # and processed
            if is_this_a_text_file:
                found_text_files = True
    # notify the user that no text files were found in the given directory
    if not found_text_files:
        print('No text files found in the directory.')

# check if a directory as entered as an argument when calling the script
if args.dir:
    # if there's a directory provided, call recursive processing function
    process_recursive(args.dir, args.overwrite)
else:
    # if there's no argument for a directory, let the user know
    print('You need to supply a directory with text files. Use --directory= after the script name')
