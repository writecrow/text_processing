#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given a metadata excel file with names to remove
# and a directory with text files passed as arguments to the script,
# names of students and instructors are replaced with <name>
#
# Usage example:
#   python deidentify.py --directory=files_with_headers_Spring_2018/ENGL\ 106/CS/D4 --master_file=../../../Metadata/Spring\ 2018/Metadata_Spring\ 2018.xlsx
#   python deidentify.py --directory=files_with_headers_Spring_2018 --master_file=../../../Metadata/Spring\ 2018/Metadata_Spring\ 2018.xlsx

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

            # create an empty list of names
            names2remove = []
            # for every row in this class section
            for index, row in filtered_metadata.iterrows():
                # add different name combinations to list of names
                # re.I flag is to ignore case
                # re.DOTALL is to find all instances of regex
                names2remove.append(re.compile('^\s?' + row['First Name'] + '\s?' + row['Last Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                names2remove.append(re.compile('^\s?' + row['Last Name'] + '\s?' + row['First Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                names2remove.append(re.compile('^\s?' + row['Last Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                names2remove.append(re.compile('^\s?' + row['First Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                names2remove.append(re.compile('\s' + row['First Name'] + '\s?' + row['Last Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                names2remove.append(re.compile('\s' + row['Last Name'] + '\s?' + row['First Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                names2remove.append(re.compile('\s' + row['Last Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                names2remove.append(re.compile('\s' + row['First Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                if row['Alternate Name'] != ' ':
                    names2remove.append(re.compile('^\s?' + row['Alternate Name'] + '(\b|(\r+)?\n|\s)', re.I| re.DOTALL))
                    names2remove.append(re.compile('^\s?' + row['Alternate Name'] + '\s?' + row['Last Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                    names2remove.append(re.compile('^\s?' + row['Alternate Name'] + '\s?' + row['First Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                    names2remove.append(re.compile('^\s?' + row['Last Name'] + '\s?' + row['Alternate Name'] + '\s?' + row['First Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                    names2remove.append(re.compile('\s' + row['Alternate Name'] + '(\b|(\r+)?\n|\s)', re.I| re.DOTALL))
                    names2remove.append(re.compile('\s' + row['Alternate Name'] + '\s?' + row['Last Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                    names2remove.append(re.compile('\s' + row['Alternate Name'] + '\s?' + row['First Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                    names2remove.append(re.compile('\s' + row['Last Name'] + '\s?' + row['Alternate Name'] + '\s?' + row['First Name'] + '(\b|(\r+)?\n|\s)', re.I | re.DOTALL))
                names2remove.append(re.compile('(^\s?)' + row['Instructor First Name'] + '\s?' + row['Instructor Last Name'], re.I| re.DOTALL))
                names2remove.append(re.compile('(^\s?)' + row['Instructor Last Name'] + '(\b|(\r+)?\n|\s)', re.I| re.DOTALL))
                names2remove.append(re.compile('(^\s?)' + row['Instructor First Name'] + '(\b|(\r+)?\n|\s)', re.I| re.DOTALL))
                names2remove.append(re.compile('\s' + row['Instructor First Name'] + '\s?' + row['Instructor Last Name'], re.I| re.DOTALL))
                names2remove.append(re.compile('\s' + row['Instructor Last Name'] + '(\b|(\r+)?\n|\s)', re.I| re.DOTALL))
                names2remove.append(re.compile('\s' + row['Instructor First Name'] + '(\b|(\r+)?\n|\s)', re.I| re.DOTALL))

            found_text_body = False
            for line in textfile:
                new_line = line
                # for every name in the list of names
                for name in names2remove:
                    # replace the name with <name>
                    new_line = re.sub(name, ' <name> ', new_line)

                # check if there's punctuation at the end of the line
                # eliminate line breaks and trailing spaces
                line_nobreaks = new_line.strip()
                # if there's text in the line
                if line_nobreaks != '':
                    # if the last character in the line is a punctiation
                    if line_nobreaks[-1] in ['.', ';', '!', '?']:
                        found_text_body = True

                # if the body of text hasn't started yet
                if not found_text_body:
                    # the next few lines may remove titles
                    # remove from line patterns for proper names
                    cleaned_line = re.sub(r'(\r+)?\n', r'', new_line)
                    cleaned_line = re.sub(r'<name>', r'', cleaned_line)
                    cleaned_line = re.sub(r'(([A-Z][a-z]+\s){1,3})?[A-Z][a-z]+', r'', cleaned_line)
                    # remove any extra spaces
                    cleaned_line = re.sub(r'\s', r'', cleaned_line)
                    cleaned_line = cleaned_line.strip()
                    # if removing numbers makes line empty, the line
                    # had only numbers and nothing else
                    cleaned_line2 = re.sub(r'(\r+)?\n', r'', new_line)
                    cleaned_line2 = re.sub(r'[0-9]+', r'', cleaned_line2)
                    # remove any extra spaces
                    cleaned_line2 = re.sub(r'\s', r'', cleaned_line2)
                    cleaned_line2 = cleaned_line2.strip()
                    # if removing email addresses makes line empty, the line
                    # had only email addresses and nothing else
                    cleaned_line3 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'', new_line)
                    # remove any extra spaces
                    cleaned_line3 = re.sub(r'\s', r'', cleaned_line3)
                    cleaned_line3 = cleaned_line3.strip()
                    if (cleaned_line != '' and
                        cleaned_line2 != '' and
                        cleaned_line3 != ''):
                        if not ('.' not in new_line and '<name>' in new_line):
                            # check if like is a Word comment
                            if not new_line[0] == '[':
                                # remove other Word comments, e.g., [AP 1]
                                new_line2 = re.sub(r'\[([A-Z][A-Z]\s?[0-9]{1,2})\]', r'', new_line)
                                # replace emails with <email>
                                new_line2 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'<email>', new_line2)
                                # check if line starts with identifying words
                                matches = re.findall(r'^(professor|prof\.|teacher|instructor|m\.|mrs?\.|ms\.|student|net\s?id|id)', new_line2, flags = re.IGNORECASE)
                                # if the line does not start with any of the above
                                if len(matches) == 0:
                                    new_line2 = re.sub(r'\s+', r' ', new_line2)
                                    output_file.write(new_line2.strip() + '\r\n')
                # if the text body has started
                else:
                    # if removing email addresses makes line empty, the line
                    # had only email addresses and nothing else
                    cleaned_line = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@([A-Z]|[a-z]|[0-9]|\.)+', r'', new_line)
                    # remove any extra spaces
                    cleaned_line = re.sub(r'\s', r'', cleaned_line)
                    cleaned_line = cleaned_line.strip()
                    if cleaned_line != '':
                        if not ('.' not in new_line and '<name>' in new_line):
                            # check if like is a Word comment
                            if not new_line[0] == '[':
                                new_line2 = re.sub(r'\s+', r' ', new_line2)
                                # remove other Word comments, e.g., [AP 1]
                                new_line2 = re.sub(r'\[([A-Z][A-Z]\s?[0-9]{1,2})\]', r'', new_line)
                                # replace emails with <email>
                                new_line2 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'<email>', new_line2)
                                output_file.write(new_line2.strip() + '\r\n')


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
