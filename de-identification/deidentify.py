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
parser.add_argument('--master_file', action="store", dest='master_file', default='')
args = parser.parse_args()


def deidentify_file(filename, master, stops, overwrite=False):
    # only process text files
    found_text_files = False
    if '.txt' in filename:
        found_text_files = True
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
            cleaned_filename2 = re.sub(r'\.\.[\\\/]', r'', filename)
            output_directory = 'deidentified'
            output_filename = os.path.join(output_directory, cleaned_filename2)
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
                student_first_name = row['First Name']
                student_first_name = student_first_name.strip()
                student_last_name = row['Last Name']
                student_last_name = student_last_name.strip()
                student_alternate_name = row['Alternate Name']
                student_alternate_name = student_alternate_name.strip()
                instructor_first_name = row['Instructor First Name']
                instructor_first_name = instructor_first_name.strip()
                instructor_last_name = row['Instructor Last Name']
                instructor_last_name = instructor_last_name.strip()

                # constants that come before and after the regex
                before_regex = '(?<=\s|\.|\,|"|\()'
                after_regex = '(\b|(\r+)?\n|\s|\.|,|\)|:|!|\?)'

                # add different name combinations to list of names
                # re.I flag is to ignore case
                # re.DOTALL is to find all instances of regex
                names2remove.append(re.compile('^' + student_first_name + '\s?' + student_last_name + after_regex, re.I | re.DOTALL))
                names2remove.append(re.compile('^' + student_last_name + '\s?' + student_first_name + after_regex, re.I | re.DOTALL))
                names2remove.append(re.compile(before_regex + student_first_name + '\s?' + student_last_name + after_regex, re.I | re.DOTALL))
                names2remove.append(re.compile(before_regex + student_last_name + '\s?' + student_first_name + after_regex, re.I | re.DOTALL))

                # ignore case only if student's name not an English word
                if student_last_name.lower() not in stops:
                    names2remove.append(re.compile('^' + student_last_name + after_regex, re.I | re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_last_name + after_regex, re.I | re.DOTALL))
                else:
                    names2remove.append(re.compile('^' + student_last_name + after_regex, re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_last_name + after_regex, re.DOTALL))

                if student_first_name.lower() not in stops:
                    names2remove.append(re.compile('^' + student_first_name + after_regex, re.I | re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_first_name + after_regex, re.I | re.DOTALL))
                else:
                    names2remove.append(re.compile('^' + student_first_name + after_regex, re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_first_name + after_regex, re.DOTALL))

                if student_alternate_name != '':
                    if student_alternate_name.lower() not in stops:
                        names2remove.append(re.compile('^' + student_alternate_name + after_regex, re.I| re.DOTALL))
                        names2remove.append(re.compile(before_regex + student_alternate_name + after_regex, re.I| re.DOTALL))
                    else:
                        names2remove.append(re.compile('^' + student_alternate_name + after_regex, re.DOTALL))
                        names2remove.append(re.compile(before_regex + student_alternate_name + after_regex, re.DOTALL))

                    names2remove.append(re.compile('^' + student_alternate_name + '\s?' + student_last_name + after_regex, re.I | re.DOTALL))
                    names2remove.append(re.compile('^' + student_alternate_name + '\s?' + student_first_name + after_regex, re.I | re.DOTALL))
                    names2remove.append(re.compile('^' + student_last_name + '\s?' + student_alternate_name + '\s?' + student_first_name + after_regex, re.I | re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_alternate_name + after_regex, re.I| re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_alternate_name + '\s?' + student_last_name + after_regex, re.I | re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_alternate_name + '\s?' + student_first_name + after_regex, re.I | re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_last_name + '\s?' + student_alternate_name+ '\s?' + student_first_name+ after_regex, re.I | re.DOTALL))
                    alternate_name_parts = student_alternate_name.split(' ')
                    for name_part in alternate_name_parts:
                        # initials are problematic
                        if len(name_part) > 1:
                            if name_part.lower() not in stops:
                                names2remove.append(re.compile('^' + name_part + after_regex , re.I| re.DOTALL))
                                names2remove.append(re.compile(before_regex + name_part + after_regex , re.I| re.DOTALL))
                            else:
                                names2remove.append(re.compile('^' + name_part + after_regex , re.DOTALL))
                                names2remove.append(re.compile(before_regex + name_part + after_regex , re.DOTALL))
                names2remove.append(re.compile('^' + instructor_first_name + '\s?' + instructor_last_name + after_regex, re.I| re.DOTALL))
                names2remove.append(re.compile('^' + instructor_last_name + after_regex, re.I| re.DOTALL))
                names2remove.append(re.compile(before_regex + instructor_first_name + '\s?' + instructor_last_name + after_regex, re.I| re.DOTALL))
                names2remove.append(re.compile(before_regex + instructor_last_name + after_regex, re.I| re.DOTALL))
                #names2remove.append(re.compile('\s' + row['Instructor First Name'] + '(\b|(\r+)?\n|\s)', re.I| re.DOTALL))

            found_text_body = False
            if '_RF_' in filename:
                this_is_reflection = True
            else:
                this_is_reflection = False

            for line in textfile:
                new_line = line
                # for every name in the list of names
                for name in names2remove:
                    # replace the name with <name>
                    new_line = re.sub(name, r'<name>\g<1>', new_line)

                # Reflection assignment has instructor all over
                if this_is_reflection:
                    this_pattern = re.compile(instructor_first_name, re.I| re.DOTALL)
                    new_line = re.sub(this_pattern, r'<name>', new_line)

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
                    # remove any initials like H. and j.
                    cleaned_line = re.sub(r'\s[A-Za-z]\.', r'', cleaned_line)
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
                                matches = re.findall(r'^(professor|prof\.|teacher|instructor|m\.|mrs?\.|ms\.|dr\.|student|net\s?id|id)', new_line2, flags = re.IGNORECASE)
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
                    cleaned_line1 = 'not empty'
                    # check if line starts with identifying words
                    matches = re.findall(r'^(professor|prof\.|teacher|instructor|m\.|mrs?\.|ms\.|dr\.|student|net\s?id|id)', new_line, flags = re.IGNORECASE)
                    if len(matches) != 0:
                        # remove from line patterns for proper names
                        cleaned_line1 = re.sub(r'(\r+)?\n', r'', new_line)
                        cleaned_line1 = re.sub(r'Mr\.|Dr\.|Mr?s\.|[A-Z]\.|\s[A-Za-z]\s', r'', cleaned_line1)
                        cleaned_line1 = re.sub(r'(,|\.|\:)', r'', cleaned_line1)
                        cleaned_line1 = re.sub(r'<name>', r'', cleaned_line1)
                        cleaned_line1 = re.sub(r'(([A-Z][a-z]+\s){1,3})?[A-Z][a-z]+', r'', cleaned_line1)
                        # remove any extra spaces
                        cleaned_line1 = re.sub(r'\s', r'', cleaned_line1)
                        cleaned_line1 = cleaned_line1.strip()
                    if (cleaned_line != '' and cleaned_line1 != ''):
                        if not ('.' not in new_line and '<name>' in new_line):
                            # check if like is a Word comment
                            if new_line[0] != '[':
                                new_line2 = re.sub(r'\s+', r' ', new_line)
                                # remove other Word comments, e.g., [AP 1]
                                new_line2 = re.sub(r'\[([A-Z][A-Z]\s?[0-9]{1,2})\]', r'', new_line2)
                                # replace emails with <email>
                                new_line2 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'<email>', new_line2)
                                output_file.write(new_line2.strip() + '\r\n')


            output_file.close()
            textfile.close()
    return(found_text_files)

def deidentify_recursive(directory, master, stops, overwrite=False):
    found_text_files = False
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            is_this_a_text_file = deidentify_file(os.path.join(dirpath, name), master, stops, overwrite)
            if is_this_a_text_file:
                found_text_files = True
    if not found_text_files:
        print('No text files found in the directory.')


if args.master_file and args.dir:
    if '.xls' in args.master_file:
        master_file = pandas.ExcelFile(args.master_file)
        master_data = pandas.read_excel(master_file)
    elif '.csv' in args.master_file:
        master_data = pandas.read_csv(args.master_file)

    stops = stopwords.words('english')

    deidentify_recursive(args.dir, master_data, stops, args.overwrite)
else:
    print('You need to supply a valid master file and directory with textfiles')
