#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given a metadata excel file with names to remove
# and a directory with text files passed as arguments to the script,
# names of students and instructors are replaced with <name>
#
# Usage example:
#   python deidentify.py --directory=../../../Spring\ 2018/files_with_headers/ --master_file=../../../Metadata/Spring\ 2018/Metadata_Spring_2018.csv
#   python deidentify.py --directory=../../../Fall\ 2018/files_with_headers/ --master_file=../../../Metadata/Fall\ 2018/Metadata_Fall_2018.csv
#   python deidentify.py --directory=../../../Fall\ 2017/files_with_headers/Fall\ 2017/ --master_file=../../../Metadata/Fall\ 2017/Metadata_Fall_2017.xlsx

import argparse
import os
import pandas
import re
import sys

from nltk.corpus import stopwords

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='De-identify Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()

def deidentify_file(filename, overwrite=False):
    # only process text files
    found_text_files = False
    if '.txt' in filename:
        found_text_files = True
        cleaned_filename2 = re.sub(r'\.\.[\\\/]', r'', filename)
        output_directory = 'deidentified'
        output_filename = os.path.join(output_directory, cleaned_filename2)
        directory = os.path.dirname(output_filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        textfile = open(filename, 'r')
        output_file = open(output_filename, "w")
        found_text_body=False
        for line in textfile:
            # for every name in the list of names
            line_nobreaks = line.strip()
            # if there's text in the line
            if line_nobreaks != '':
                # if the last character in the line is a punctiation
                if line_nobreaks[-1] in ['.', ';', '!', '?']:
                    # print(line_nobreaks)
                    found_text_body = True


            if not found_text_body:
                #cleans white space and line break in lines before text body
                cleaned_line = re.sub(r'(\r+)?\n', r'', line)
                # remove any initials like H. and j.
                cleaned_line = re.sub(r'\s[A-Za-z]\.', r'', cleaned_line)
                #I dont think we need this line because we dont have <name>
                cleaned_line = re.sub(r'Name:|name:', r'', cleaned_line)
                cleaned_line = re.sub(r'(([A-Z][a-z]+\s+|-){1,3})?[A-Z][a-z]+', r'', cleaned_line)
                cleaned_line = re.sub(r'[0-9]+', r'', cleaned_line)
                # remove any extra spaces
                cleaned_line = re.sub(r'\s', r'', cleaned_line)
                cleaned_line = cleaned_line.strip()

                # if removing numbers makes line empty, the line
                # had only numbers and nothing else
                cleaned_line2 = re.sub(r'(\r+)?\n', r'', line)
                cleaned_line2 = re.sub(r'[0-9]+', r'', cleaned_line2)
                # remove any extra spaces
                cleaned_line2 = re.sub(r'\s', r'', cleaned_line2)
                cleaned_line2 = cleaned_line2.strip()

                # if removing email addresses makes line empty, the line
                # had only email addresses and nothing else
                cleaned_line3 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'', line)
                # remove any extra spaces
                cleaned_line3 = re.sub(r'\s', r'', cleaned_line3)
                cleaned_line3 = cleaned_line3.strip()
                if (cleaned_line != '' and
                        cleaned_line2 != '' and
                        cleaned_line3 != ''):
                    if not ('.' not in line and '<name>' in line):
                        # check if like is a Word comment
                        if not line[0] == '[':
                            # remove other Word comments, e.g., [AP 1]
                            new_line2 = re.sub(r'\[([A-Z][A-Z]\s?[0-9]{1,2})\]', r'', line)
                            # replace emails with <email>
                            new_line2 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'<email>', new_line2)
                            # check if line starts with identifying words
                            matches = re.findall(
                                r'^(professor|prof\.|teacher|instructor|m\.|mrs?\.|ms\.|dr\.|student|net\s?id|id)', new_line2, flags=re.IGNORECASE)
                            # if the line does not start with any of the above
                            if len(matches) == 0:
                                new_line2 = re.sub(r'\s+', r' ', new_line2)
                                output_file.write(new_line2.strip() + '\r\n')


            else:
                # if removing email addresses makes line empty, the line
                # had only email addresses and nothing else
                cleaned_line = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@([A-Z]|[a-z]|[0-9]|\.)+', r'', line)
                # remove any extra spaces
                cleaned_line = re.sub(r'\s', r'', cleaned_line)
                cleaned_line = cleaned_line.strip()
                cleaned_line1 = 'not empty'
                # check if line starts with identifying words
                matches = re.findall(
                    r'^(professor|prof\.|teacher|instructor|m\.|mrs?\.|ms\.|dr\.|student|net\s?id|id)', line, flags=re.IGNORECASE)
                if len(matches) != 0:
                    # remove from line patterns for proper names
                    cleaned_line1 = re.sub(r'(\r+)?\n', r'', line)
                    cleaned_line1 = re.sub(r'Mr\.|Dr\.|Mr?s\.|[A-Z]\.|\s[A-Za-z]\s', r'', cleaned_line1)
                    cleaned_line1 = re.sub(r'(,|\.|\:)', r'', cleaned_line1)
                    cleaned_line1 = re.sub(r'Name:|name:', r'', cleaned_line1)
                    cleaned_line1 = re.sub(r'(([A-Z][a-z]+\s){1,3})?[A-Z][a-z]+', r'', cleaned_line1)
                    # remove any extra spaces
                    cleaned_line1 = re.sub(r'\s', r'', cleaned_line1)
                    cleaned_line1 = cleaned_line1.strip()
                if (cleaned_line != '' and cleaned_line1 != ''):
                    if not ('.' not in line and '<name>' in line):
                        # check if like is a Word comment
                        if line[0] != '[':
                            new_line2 = re.sub(r'\s+', r' ', line)
                            # remove other Word comments, e.g., [AP 1]
                            new_line2 = re.sub(r'\[([A-Z][A-Z]\s?[0-9]{1,2})\]', r'', new_line2)
                            # replace emails with <email>
                            new_line2 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'<email>', new_line2)
                            output_file.write(new_line2.strip() + '\r\n')

        output_file.close()
        textfile.close()
    return(found_text_files)

def deidentify_recursive(directory, overwrite=False):
    found_text_files = False
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            is_this_a_text_file = deidentify_file(os.path.join(dirpath, name), overwrite)
            if is_this_a_text_file:
                found_text_files = True
    if not found_text_files:
        print('No text files found in the directory.')




deidentify_recursive(args.dir)
