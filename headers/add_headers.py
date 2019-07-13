#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file and text files passed as arguments to the script,
# metadata headers are added to each individual text files
#
# Usage example:
#    python add_headers.py --directory=../../../Spring\ 2018/normalized/ --master_file=../../../Metadata/Spring\ 2018/Metadata_Spring\ 2018.xlsx
#    python add_headers.py --directory=../../../Fall\ 2017/normalized/ --master_file=../../../Metadata/Fall\ 2017/Metadata_Fall_2017.xlsx
#    python add_headers.py --directory=../../../Fall\ 2018/normalized/ --master_file=../../../Metadata/Fall\ 2018/Metadata_Fall\ 2018.xlsx


import argparse
import sys
import re
import os
import pandas

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--master_file', action="store", dest='master_file', default='')
args = parser.parse_args()


def add_header_to_file(filename, master, overwrite=False):
    found_text_files = False
    if '.txt' in filename:
        found_text_files = True
        filename_parts = filename.split('- ')
        student_name = re.sub(r'\.txt', r'', filename_parts[1])
        student_name = re.sub(r'\s+', r' ', student_name)
        if student_name[-1] == '-':
            student_name = student_name[:-1]
        student_name_parts = student_name.split()
        if len(student_name_parts) != 2:
            print('***********************************************')
            print('File has student name with more than two names: ' + filename)
            print(student_name_parts)

        filtered_master1 = master[master['Last Name'] == student_name_parts[-1]]
        filtered_master2 = filtered_master1[filtered_master1['First Name'] == student_name_parts[0]]
        if filtered_master2.empty:
            print('***********************************************')
            print('Unable to find metadata for this file: ')
            print(filename)
            print(student_name_parts)

        if filtered_master2.shape[0] > 1:
            print('***********************************************')
            print('More than one row in metadata for this file: ')
            print(filename)
            print(student_name_parts)
        else:
            print('Adding headers to file ' + textfile)
            textfile = open(filename, 'r')
            filename_parts2 = filename.split('/')

            course = filtered_master2['Catalog Nbr'].to_string(index=False)
            assignment = filename_parts2[7][:2]
            draft = filename_parts2[7][2:]
            country_code = filtered_master2['Birth Country Code'].to_string(index=False)
            year_in_school = 'NA'
            gender = filtered_master2['Gender'].to_string(index=False)
            crow_id = filtered_master2['Crow ID'].to_string(index=False)
            institution_code = re.sub(r'[a-z\s]', r'', filtered_master2['institution'].to_string(index=False))

            #course assignment draft country yearinschool gender studentID institution '.txt'
            output_filename = ''
            output_filename += course
            output_filename += '_'
            output_filename += assignment
            output_filename += '_'
            output_filename += draft
            output_filename += '_'
            output_filename += country_code
            output_filename += '_'
            output_filename += year_in_school
            output_filename += '_'
            output_filename += gender
            output_filename += '_'
            output_filename += crow_id
            output_filename += '_'
            output_filename += institution_code
            output_filename += '.txt'
            output_filename = re.sub(r'\s', r'', output_filename)
            output_filename = re.sub(r'__', r'_NA_', output_filename)

            if 'Series' not in output_filename:
                term = filtered_master2['term'].to_string(index=False)
                folder_term = term.strip()
                path = "files_with_headers/" + term + "/ENGL" + course+ "/" + assignment + "/" + draft + "/"

                if not os.path.exists(path):
                    os.makedirs(path)

                output_file = open(path + output_filename, 'w')

                country = filtered_master2['Descr'].to_string(index=False)
                institution = filtered_master2['institution'].to_string(index=False)

                semester = term.split()[0]
                year = term.split()[1]
                college = filtered_master2['College'].to_string(index=False)
                program = filtered_master2['Major'].to_string(index=False)
                TOEFL_COMPI = filtered_master2['TOEFL COMPI'].to_string(index=False)
                TOEFL_Listening = filtered_master2['TOEFL Listening'].to_string(index=False)
                TOEFL_Reading = filtered_master2['TOEFL Reading'].to_string(index=False)
                TOEFL_Writing = filtered_master2['TOEFL Writing'].to_string(index=False)
                TOEFL_Speaking = filtered_master2['TOEFL Speaking'].to_string(index=False)
                instructor = filtered_master2['Instructor Code'].to_string(index=False)
                section = filtered_master2['Class Section'].to_string(index=False)
                mode = filtered_master2['mode_of_course'].to_string(index=False)
                length = filtered_master2['length_of_course'].to_string(index=False)

                country = re.sub(r'NaN', r'NA', country)
                TOEFL_COMPI = re.sub(r'NaN', r'NA', TOEFL_COMPI)
                TOEFL_Listening = re.sub(r'NaN', r'NA', TOEFL_Listening)
                TOEFL_Reading = re.sub(r'NaN', r'NA', TOEFL_Reading)
                TOEFL_Writing = re.sub(r'NaN', r'NA', TOEFL_Writing)
                TOEFL_Speaking = re.sub(r'NaN', r'NA', TOEFL_Speaking)

                # write headers in
                output_file.write("<ID: " + crow_id + ">" + "\r\n")
                output_file.write("<Country: " + country + ">" + "\r\n")
                output_file.write("<Institution: " + institution + ">" + "\r\n")
                output_file.write("<Course: " + course + ">" + "\r\n")
                output_file.write("<Mode: " + mode + ">" + "\r\n")
                output_file.write("<Length: " + length + ">" + "\r\n")
                output_file.write("<Assignment: " + assignment + ">" + "\r\n")
                output_file.write("<Draft: " + draft + ">" + "\r\n")
                output_file.write("<Year in School: " + year_in_school + ">" + "\r\n")
                output_file.write("<Gender: " + gender + ">" + "\r\n")
                output_file.write("<Year writing: " + year + ">" + "\r\n")
                output_file.write("<Semester writing: " + semester + ">" + "\r\n")
                output_file.write("<College: " + college + ">" + "\r\n")
                output_file.write("<Program: " + program + ">" + "\r\n")
                output_file.write("<TOEFL total: " + TOEFL_COMPI + ">" + "\r\n")
                output_file.write("<TOEFL reading: " + TOEFL_Reading + ">" + "\r\n")
                output_file.write("<TOEFL listening: " + TOEFL_Listening + ">" + "\r\n")
                output_file.write("<TOEFL speaking: " + TOEFL_Speaking + ">" + "\r\n")
                output_file.write("<TOEFL writing: " + TOEFL_Writing + ">" + "\r\n")
                output_file.write("<Instructor: " + instructor + ">" + "\r\n")
                output_file.write("<Section: " + section + ">" + "\r\n")
                output_file.write("<End Header>\r\n\r\n")

                for line in textfile:
                    this_line = re.sub(r'\r?\n', r'\r\n', line)
                    if this_line != '\r\n':
                        new_line = re.sub(r'\s+', r' ', this_line)
                        new_line = new_line.strip()
                        print(new_line, file = output_file, end = '\r\n')

                output_file.close()
            textfile.close()
    return(found_text_files)


def add_headers_recursive(directory, master, overwrite=False):
    found_text_files = False
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            is_this_a_text_file = add_header_to_file(os.path.join(dirpath, name), master, overwrite)
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

    add_headers_recursive(args.dir, master_data, args.overwrite)
else:
    print('You need to supply a valid master file and directory with textfiles')
