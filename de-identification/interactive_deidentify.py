#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given a directory with text files passed as arguments
# to the script, the script looks for Name Patterns and prompts the user
# for name replacement with <name>
#
# Usage example:
#   python interactive_deidentify.py --directory=deidentified/files_with_headers_Spring_2018/ENGL\ 106/CS/D4
#   python interactive_deidentify.py --directory=deidentified/files_with_headers_Spring_2018

import argparse
import sys
import re
import os

from termcolor import colored


# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='De-identify Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()

def deidentify_file(filename, overwrite=False):
    # only process text files
    if '.txt' in filename:
        # create output filename with directory path
        output_directory = 'deidentified_round2'
        output_filename = os.path.join(output_directory, filename)
        directory = os.path.dirname(output_filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        # update user on progress
        print("De-identify file " + filename)
        input("*********** Press any key to continue *********** ")

        # open original textfile and new output file
        textfile = open(filename, 'r')
        output_file = open(output_filename, "w")
        for line in textfile:
            new_line = line
            clean_line = line.strip()
            if clean_line[0] != '<' and clean_line[-1] != '>':
                propername_pattern = re.compile('([a-z,]\s[A-Z][a-z]+|^[A-Z][a-z]+)((\s[A-Z][a-z]+)+)?')
                matches = propername_pattern.finditer(line)
                for m in matches:
                    position = m.start()
                    len_word = len(m.group())
                    os.system('clear')
                    print("De-identifing file " + filename)
                    print("**********************************")
                    if m.group()[1] != ' ':
                        print(line[:position] + colored(line[position:position+len_word], 'red') + line[position+len_word:])
                    else:
                        print(line[:position+2] + colored(line[position+2:position+len_word], 'red') + line[position+len_word:])
                    decision = input("Replace highlighted text with <name>? (y/N): ")
                    while decision not in ['yes', 'no', 'y', 'n', 'Y', 'N', '']:
                        print("Please enter Y or N for a response.")
                        decision = input("Replace highlighted text with <name>? (Y/N): ")

                    if decision in ['yes', 'y', 'Y']:
                        if m.group()[1] != ' ':
                            name2replace = re.compile(m.group())
                            new_line = re.sub(name2replace, ' <name> ', new_line, 1)
                        else:
                            name2replace = re.compile(m.group()[2:])
                            new_line = re.sub(name2replace, ' <name> ', new_line, 1)

            new_line = re.sub(r'\s+', ' ', new_line)
            new_line = new_line.strip()
            output_file.write(new_line + '\r\n')
        textfile.close()
        output_file.close()

def deidentify_recursive(directory, overwrite=False):
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            deidentify_file(os.path.join(dirpath, name), overwrite)


if args.dir:
    deidentify_recursive(args.dir, args.overwrite)
else:
    print('You need to supply a valid directory with textfiles')
