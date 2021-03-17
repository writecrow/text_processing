#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION:
# Given a folder with .txt files (including subfolders) the script extracts
# metadata headers in each individual text file and outputs the info
# in a tab separated format
#
# Example on how to run the script
#   python get_headers_from_files.py --directory=files_with_headers > output_file.tsv

import argparse
import sys
import re
import os

# lists the required arguments (e.g. --directory=) sent to the script
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()

def print_headers(filename, other_files):
    # open text file
    input_file = open(filename, "r")

    # read contents
    contents = input_file.read()

    # find end of headers
    p = contents.find("<End Header>")

    # extract headers from content
    headers = contents[0:p-1]

    # print header labels just for first file
    if not other_files:
        labels = re.findall(r"<[A-Za-z\s\-0-9]+", headers)
        label_line = '\t'.join(labels)
        label_line = re.sub(r"<", "", label_line)
        print("filename\t" + label_line)

    # remove label of header to keep only value after :
    headers = re.sub(r"<[A-Za-z\s\-0-9]+:\s", "", headers)

    # replace the closing > with a tab for tab separated value
    headers = re.sub(">", "\t", headers)

    # remove line breaks
    headers = re.sub(r"\r?\n", "", headers)

    # don't include folder names in filename to print out
    just_filename = os.path.split(filename)[1]

    # print line with headers separated by tab
    print(just_filename + "\t" + headers)

    # close file
    input_file.close()

def main(my_folder):
    # creates control variable to check if there were any text files in the provided folder
    found_text_files = False
    # walks folder structure to get all files in all folders
    for dirpath, dirnames, files in os.walk(my_folder):
        # for every file found in a folder
        for name in files:
            if '.txt' in name:
                print_headers(os.path.join(dirpath, name), found_text_files)
                found_text_files = True
    # if no .txt texts were found in the directory, it prints "No text files found in the directory"
    if not found_text_files:
        print('No text files found in the directory.')

if __name__ == "__main__":
    if args.dir:
        main(args.dir)
    else:
        print("Please enter a directory name by using the --directory parameter")
