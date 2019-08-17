#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given a metadata excel file with names to remove
# and a directory with text files passed as arguments to the script,
# names of students and instructors are replaced with <name>
#
# Usage example:
#   python deidentify_macaws.py --directory=../headers/files_with_headers/ --master_file=../../../MACAWS/Portuguese/metadata/master_metadata_spring2017_spring2019.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Portuguese.xlsx
#   python deidentify_macaws.py --directory=../headers/files_with_headers/ --master_file=../../../MACAWS/Russian/newest_master_meta.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Russian.csv --language_to_process="RSSS_"
#   python deidentify_macaws.py --directory=../../../MACAWS/Portuguese/files_with_headers/ --master_file=../../../MACAWS/Portuguese/metadata/master_metadata_spring2017_spring2019.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Portuguese.xlsx
#   python deidentify_macaws.py --directory=../../../MACAWS/Russian/files_with_headers/ --master_file=../../../MACAWS/Russian/newest_master_meta.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Russian.csv --language_to_process="RSSS_"

import argparse
import nltk
import os
import pandas
import re
import sys

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='De-identify Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--master_file', action="store", dest='master_file', default='')
parser.add_argument('--language_to_process', action="store", dest='target_language', default='PORT_')
parser.add_argument('--master_instructor_file', action="store", dest='master_instructor_file', default='')
args = parser.parse_args()


def deidentify_file(filename, master, master_instructor, language, stops, overwrite=False):
    # only process text files
    found_text_files = False
    if '.txt' in filename and language in filename:
        found_text_files = True
        # get only file name, by removing directory path
        cleaned_filename = re.sub(r'.+\/', r'', filename)
        # split filename to get to student crow id
        filename_parts = cleaned_filename.split('_')
        macaws_id = int(filename_parts[7])

        # find student in the metadata master
        student_metadata = master[master['MACAWS ID'] == macaws_id]
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

            # fill NaN with a space, for later checking of altername name
            student_metadata = student_metadata.fillna(' ')

            # create an empty list of names
            names2remove = []
            # for every row in this class section
            for index, row in student_metadata.iterrows():
                if language == 'PORT_':
                    student_consent_name = row['Consent Name']
                    student_consent_name = student_consent_name.strip()
                    student_consent_name = re.sub(r'\s+', ' ', student_consent_name)

                student_file_name = row['filename']
                student_file_name = student_file_name.strip()
                student_file_name = re.sub(r'\s+', ' ', student_file_name)
                student_file_name = re.sub(r'\[?NA(\\s\])?',r'',student_file_name)
                student_file_name = re.sub(r'\s+', ' ', student_file_name)

                student_survey_name = row['survey_student_name']
                student_survey_name = student_survey_name.strip()
                student_survey_name = re.sub(r'\s+', ' ', student_survey_name)

                # constants that come before and after the regex
                before_regex = '(?<=\s|\.|\,|"|\()'
                after_regex = '(\b|(\r+)?\n|\s|\.|,|\)|:|!|\?|;|\-)'

                # add different name combinations to list of names
                # re.I flag is to ignore case
                # re.DOTALL is to find all instances of regex
                if language == 'PORT_':
                    if student_consent_name != '':
                        names2remove.append(re.compile('^' + student_consent_name + after_regex, re.I | re.DOTALL))
                        names2remove.append(re.compile(before_regex + student_consent_name + after_regex, re.I | re.DOTALL))

                        consent_name_parts = student_consent_name.split(' ')
                        for name_part in consent_name_parts:
                            # initials are problematic
                            if len(name_part) > 1:
                                name_part = name_part.strip()
                                if name_part != '' and name_part != ' ' and name_part.lower() not in stops:
                                    names2remove.append(re.compile('^' + name_part + after_regex , re.I| re.DOTALL))
                                    names2remove.append(re.compile(before_regex + name_part + after_regex , re.I| re.DOTALL))

                if student_file_name != '' and student_file_name != 'NO TEXT FILES':
                    student_file_name = re.sub(r'_', r' ', student_file_name)

                    names2remove.append(re.compile('^' + student_file_name + after_regex, re.I | re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_file_name + after_regex, re.I | re.DOTALL))

                    student_file_name = re.sub(r'\(|\)|\|\\s|\?', r'', student_file_name)
                    student_file_name_parts = student_file_name.split(' ')
                    for name_part in student_file_name_parts:
                        # initials are problematic
                        if len(name_part) > 1:
                            name_part = name_part.strip()
                            if name_part != '' and name_part != ' ' and name_part.lower() not in stops:
                                names2remove.append(re.compile('^' + name_part + after_regex , re.I| re.DOTALL))
                                names2remove.append(re.compile(before_regex + name_part + after_regex , re.I| re.DOTALL))

                if student_survey_name != '':
                    names2remove.append(re.compile('^' + student_survey_name + after_regex, re.I | re.DOTALL))
                    names2remove.append(re.compile(before_regex + student_survey_name + after_regex, re.I | re.DOTALL))

                    student_survey_name_parts = student_survey_name.split(' ')
                    for name_part in student_survey_name_parts:
                        # initials are problematic
                        if len(name_part) > 1:
                            name_part = name_part.strip()
                            if name_part != '' and name_part != ' ' and name_part.lower() not in stops:
                                names2remove.append(re.compile('^' + name_part + after_regex , re.I| re.DOTALL))
                                names2remove.append(re.compile(before_regex + name_part + after_regex , re.I| re.DOTALL))

            found_text_body = False

            for line in textfile:
                new_line = line
                new_line = re.sub(r'\sNan>', r' NA>', new_line)

                # get instructor code from header
                if '<Instructor: ' in line:
                    instructor_code = re.sub(r'<Instructor:\s|>', r'', line)
                    instructor_code = float(instructor_code)
                    instructor_info = master_instructor[master_instructor['instructor_code'] == instructor_code]
                    if instructor_info.empty:
                        print('***********************************************')
                        print('Unable to find metadata for this instructor: ')
                        print(filename)
                        print(instructor_code)
                    else:
                        for index, row in instructor_info.iterrows():
                            instructor_first_name = row['instructor']
                            instructor_first_name = instructor_first_name.strip()
                            instructor_first_name = re.sub(r'\s+', ' ', instructor_first_name)

                            names2remove.append(re.compile('^' + instructor_first_name + after_regex, re.I | re.DOTALL))
                            names2remove.append(re.compile(before_regex + instructor_first_name + after_regex, re.I | re.DOTALL))

                            instructor_full_name = row['instructor_full_name']
                            instructor_full_name = instructor_full_name.strip()
                            instructor_full_name = re.sub(r'\s+', ' ', instructor_full_name)

                            names2remove.append(re.compile('^' + instructor_full_name + after_regex, re.I | re.DOTALL))
                            names2remove.append(re.compile(before_regex + instructor_full_name + after_regex, re.I | re.DOTALL))

                            instructor_full_name_parts = instructor_full_name.split(' ')
                            for name_part in instructor_full_name_parts:
                                if len(name_part) > 1:
                                    name_part = name_part.strip()
                                    if name_part != '' and name_part != ' ' and name_part.lower() not in stops:
                                        names2remove.append(re.compile('^' + name_part + after_regex , re.I| re.DOTALL))
                                        names2remove.append(re.compile(before_regex + name_part + after_regex , re.I| re.DOTALL))


                # for every name in the list of names
                for name in names2remove:
                    # replace the name with <name>
                    new_line = re.sub(name, r'<name>\g<1>', new_line)

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
                    # remove name tags
                    cleaned_line = re.sub(r'<name>', r'', cleaned_line)
                    # remove names
                    cleaned_line = re.sub(r'(([A-Z][a-z]+\s){1,3})?[A-Z][a-z]+', r'', cleaned_line)
                    cleaned_line = re.sub(r'(([А-Я][а-я]+\s){1,3})?[А-Я][а-я]+', r'', cleaned_line)
                    cleaned_line = re.sub(r'\-', r'', cleaned_line)
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
                                # replace phone numbers with <phone_number>
                                # (520) 999-9999
                                new_line2 = re.sub(r'\(?[0-9]{3}\)?\s?[0-9]{3}\-?[0-9]{4}', r'<phone_number>', new_line2)
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

def deidentify_recursive(directory, master, master_instructor, language, stops, overwrite=False):
    found_text_files = False
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            is_this_a_text_file = deidentify_file(os.path.join(dirpath, name), master, master_instructor, language, stops, overwrite)
            if is_this_a_text_file:
                found_text_files = True
    if not found_text_files:
        print('No text files found in the directory.')


if args.master_file and args.dir and args.master_instructor_file:
    if '.xls' in args.master_file:
        master_file = pandas.ExcelFile(args.master_file)
        master_data = pandas.read_excel(master_file)
    elif '.csv' in args.master_file:
        master_data = pandas.read_csv(args.master_file)

    if '.xls' in args.master_instructor_file:
        master_instructor_file = pandas.ExcelFile(args.master_instructor_file)
        master_instructor_data = pandas.read_excel(master_instructor_file)
    elif '.csv' in args.master_instructor_file:
        master_instructor_data = pandas.read_csv(args.master_instructor_file)

    language = args.target_language

    if language == 'PORT_':
        stopwords = nltk.corpus.stopwords.words('portuguese')
        stopwords.append('mata')
    elif language == 'RSSS_':
        stopwords = nltk.corpus.stopwords.words('russian')
    #print(stopwords)

    #print(master_instructor_data)
    #print(master_instructor_data.dtypes)

    deidentify_recursive(args.dir, master_data, master_instructor_data, language, stopwords, args.overwrite)
else:
    print('You need to supply a valid master file and directory with textfiles')
