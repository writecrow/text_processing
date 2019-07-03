#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given a metadata excel file with names to remove
# and a directory with text files passed as arguments to the script,
# names of students and instructors are replaced with <name>
#
# Usage example:
#    python deidentify.py --directory=files_with_headers_Spring_2018/ENGL\ 106/CS/D1 --master_file=../../../Metadata/Spring\ 2018/Metadata_Spring\ 2018.xlsx

import argparse
import sys
import re
import os
import pandas

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='De-identify Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--master_file', action="store", dest='master_file', default='')
args = parser.parse_args()


def deidentify_file(filename, master, overwrite=False):
    # only process text files
    if '.txt' in filename:
        # get only file name, by removing directory path
        cleaned_filename = re.sub(r'.+\/', r'', filename)
        # split filename to get to student crow id
        filename_parts = cleaned_filename.split('_')
        crow_id = int(filename_parts[6])

        # find student in the metadata master
        student_metadata = master[master['Crow ID'] == crow_id]
        if student_metadata.empty:
            print('***********************************************')
            print('Unable to find metadata for this file: ')
            print(filename)
        else:
            # create output filename with directory path
            output_directory = 'deidentified'
            output_filename = os.path.join(output_directory, filename)
            directory = os.path.dirname(output_filename)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # open original textfile and new output file
            textfile = open(filename, 'r')
            output_file = open(output_filename, "w")
            # update user on progress
            print('De-identifying file ' + filename)

            # get class section for this student
            class_section = student_metadata['Class Section'].to_string(index=False)
            class_section = int(class_section)

            # get dataframe slice for that class section
            filtered_metadata = master[master['Class Section'] == class_section]
            # fill NaN with a space, for later checking of altername name
            filtered_metadata = filtered_metadata.fillna(' ')


            for line in textfile:
                this_line = re.sub(r'\r?\n', r'', line)
                if this_line != '':
                    # the next few lines may remove titles
                    # remove from line patterns for proper names
                    cleaned_line = re.sub(r'(([A-Z][a-z]+\s)+)?[A-Z][a-z]+', r'', this_line)
                    # remove any extra spaces
                    cleaned_line = re.sub(r'\s', r'', cleaned_line)
                    cleaned_line = cleaned_line.strip()
                    # if removing proper names makes line empty, the line
                    # had only proper names and nothing else
                    #if cleaned_line != '':
                    if True:
                        # create an empty list of names
                        names2remove = []
                        # for every row in this class section
                        for index, row in filtered_metadata.iterrows():
                            # add different name combinations to list of names
                            # re.I flag is to ignore case
                            # re.DOTALL is to find all instances of regex 
                            names2remove.append(re.compile(row['First Name'] + ' ' + row['Last Name'], re.I | re.DOTALL))
                            names2remove.append(re.compile(row['Last Name'] + ' ' + row['First Name'], re.I | re.DOTALL))
                            if row['Alternate Name'] != ' ':
                                names2remove.append(re.compile(row['Alternate Name'], re.I| re.DOTALL))
                                names2remove.append(re.compile(row['Alternate Name'] + ' ' + row['Last Name'], re.I | re.DOTALL))
                                names2remove.append(re.compile(row['Alternate Name'] + ' ' + row['First Name'], re.I | re.DOTALL))
                                names2remove.append(re.compile(row['Last Name'] + ' ' + row['Alternate Name'] + ' ' + row['First Name'], re.I | re.DOTALL))
                            names2remove.append(re.compile(row['Instructor First Name'] + ' ' + row['Instructor Last Name'], re.I| re.DOTALL))
                            names2remove.append(re.compile(row['Instructor Last Name'], re.I| re.DOTALL))

                        new_line = this_line
                        # for every name in the list of names
                        for name in names2remove:
                            new_line = re.sub(name, '<name>', new_line)

                        output_file.write(new_line + '\r\n')

            output_file.close()
            textfile.close()


def deidentify_recursive(directory, master, overwrite=False):
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            deidentify_file(os.path.join(dirpath, name), master, overwrite)


if args.master_file and args.dir:
    if '.xls' in args.master_file:
        master_file = pandas.ExcelFile(args.master_file)
        master_data = pandas.read_excel(master_file)
    elif '.csv' in args.master_file:
        master_data = pandas.read_csv(args.master_file)

    deidentify_recursive(args.dir, master_data, args.overwrite)
else:
    print('You need to supply a valid master file and directory with textfiles')
