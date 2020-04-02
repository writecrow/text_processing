#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 21:09:58 2020

@author: CCloveHH
"""

import argparse
import sys
import re
import os
import pandas as pd 

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--df_file', action="store", dest='df_file', default='')
args = parser.parse_args()

# filename = "/Users/CCloveHH/Desktop/Intern_script/Demo_data/PAD1 - Eddie Green_and_Xu Zhang.txt"

# df = pd.read_excel('/Users/CCloveHH/Desktop/Intern_script/Merge.xlsx')

def add_header_to_file(filename, df, overwrite = False):
    found_text_files = False
    student_first_name = []
    student_last_name = []
    
    if '.txt' in filename:
        found_text_files = True
        filename_parts = filename.split('- ')
        student_name = re.sub(r'\.txt', r'', filename_parts[1])
        student_name = re.sub(r'\s+', r' ', student_name)
        
        if '_and_' in student_name: #find group homework
            print ('It is a group homework: ' + filename)
            student_parts_group = student_name.split('_and_')
            for i in range(len(student_parts_group)):
                student_first_name.append(student_parts_group[i].split()[0])
                student_last_name.append(student_parts_group[i].split()[1])
        else: # find individual homework
            student_first_name.append(student_name.split()[0])
            student_last_name.append(student_name.split()[1])
            print ('It is an individual homework')
            
        for i in range(len(student_first_name)):
            df1 = df[df['Last Name']==student_last_name[i]]
            df2 = df1[df1['First Name']==student_first_name[i]]
            if df2.empty:
                print('***********************************************')
                print('Unable to find metadata for this file: ')
                print(filename)
                print(student_first_name + student_last_name)
        
            if df2.shape[0] > 1:
                print('***********************************************')
                print('More than one row in metadata for this file: ')
                print(filename)
                print(student_first_name + student_last_name)
            else:
                print('Adding headers to file ' + filename)
                textfile = open(filename, 'r')
                not_windows_filename = re.sub(r'\\', r'/', filename)
                clean_filename = re.sub(r'\.\.\/', r'', not_windows_filename)
                filename_parts2 = clean_filename.split('/')
        
                course = df2['Catalog Nbr'].to_string(index=False)
                course = course.strip()
                course = re.sub(r'NaN', r'NA', course)
        
                assignment = filename_parts2[4][:2]
                draft = filename_parts2[4][2:]
                draft = re.sub('D', '', draft)
                
                country_code = df2['Birth Country Code'].to_string(index=False)
                country_code = country_code.strip()
                country_code = re.sub(r'NaN', r'NAN', country_code)
        
        
                year_in_school = df2['Acad Level'].to_string(index=False)
                year_in_school = year_in_school.strip()
                year_in_school_numeric = 'NA'
        
                if year_in_school not in ['1','2','3','4']:
                    if year_in_school.lower() == 'freshman':
                        year_in_school_numeric = '1'
                    elif year_in_school.lower() == 'sophomore':
                        year_in_school_numeric = '2'
                    elif year_in_school.lower() == 'junior':
                        year_in_school_numeric = '3'
                    elif year_in_school.lower() == 'senior':
                        year_in_school_numeric = '4'
                    else:
                        year_in_school_numeric = 'NA'
                else:
                    year_in_school_numeric = year_in_school
                
                gender = df2['Gender'].to_string(index=False)
                gender = gender.strip()
                gender = re.sub(r'NaN', r'NA', gender)
        
                crow_id = df2['Crow ID'].to_string(index=False)
                crow_id = crow_id.strip()
                crow_id = re.sub(r'NaN', r'NA', crow_id)
        
                institution_code = re.sub(r'[a-z\s]', r'', df2['institution'].to_string(index=False))
                
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
                output_filename += year_in_school_numeric
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
                    term = df2['term'].to_string(index=False)
                    term = term.strip()
                    path = "files_with_headers/" + term + "/ENGL " + course+ "/" + assignment + "/" + draft + "/"
        
                    if not os.path.exists(path):
                        os.makedirs(path)
        
                    output_file = open(path + output_filename, 'w')
            
                    country = df2['Birth Country Code'].to_string(index=False)
                    country = country.strip()
            
                    institution = df2['institution'].to_string(index=False)
                    institution = institution.strip()
                
                    semester = term.split()[0]
                    year = term.split()[1]
                    college = df2['College'].to_string(index=False)
                    program = df2['Major'].to_string(index=False)
                    TOEFL_COMPI = df2['TOEFL COMPI'].to_string(index=False)
                    TOEFL_Listening = df2['TOEFL Listening'].to_string(index=False)
                    TOEFL_Reading = df2['TOEFL Reading'].to_string(index=False)
                    TOEFL_Writing = df2['TOEFL Writing'].to_string(index=False)
                    TOEFL_Speaking = df2['TOEFL Speaking'].to_string(index=False)
                    # IELTS_Overall = df2['IELTS Overall'].to_string(index=False)
                    # IELTS_Listening = df2['IELTS Listening'].to_string(index=False)
                    # IELTS_Reading = df2['IELTS Reading'].to_string(index=False)
                    # IELTS_Writing = df2['IELTS Writing'].to_string(index=False)
                    # IELTS_Speaking = df2['IELTS Speaking'].to_string(index=False)
                    instructor = df2['Instructor Code'].to_string(index=False)
                    section = df2['Class Section'].to_string(index=False)
                    # mode = df2['mode_of_course'].to_string(index=False)
                    # length = df2['length_of_course'].to_string(index=False)
                    
                    program = program.strip()
                    TOEFL_COMPI = TOEFL_COMPI.strip()
                    TOEFL_Listening = TOEFL_Listening.strip()
                    TOEFL_Reading = TOEFL_Reading.strip()
                    TOEFL_Writing = TOEFL_Writing.strip()
                    TOEFL_Speaking = TOEFL_Speaking.strip()
                    # IELTS_Overall = IELTS_Overall.strip()
                    # IELTS_Listening = IELTS_Listening.strip()
                    # IELTS_Reading = IELTS_Reading.strip()
                    # IELTS_Writing = IELTS_Writing.strip()
                    # IELTS_Speaking = IELTS_Speaking.strip()
                    instructor = instructor.strip()
                    section = section.strip()
                    # mode = mode.strip()
                    # length = length.strip()
                    
                    country = re.sub(r'NaN', r'NA', country)
                    TOEFL_COMPI = re.sub(r'NaN', r'NA', TOEFL_COMPI)
                    TOEFL_Listening = re.sub(r'NaN', r'NA', TOEFL_Listening)
                    TOEFL_Reading = re.sub(r'NaN', r'NA', TOEFL_Reading)
                    TOEFL_Writing = re.sub(r'NaN', r'NA', TOEFL_Writing)
                    TOEFL_Speaking = re.sub(r'NaN', r'NA', TOEFL_Speaking)
                    # IELTS_Overall = re.sub(r'NaN', r'NA', IELTS_Overall)
                    # IELTS_Listening = re.sub(r'NaN', r'NA', IELTS_Listening)
                    # IELTS_Reading = re.sub(r'NaN', r'NA', IELTS_Reading)
                    # IELTS_Writing = re.sub(r'NaN', r'NA', IELTS_Writing)
                    # IELTS_Speaking = re.sub(r'NaN', r'NA', IELTS_Speaking)
                    
                    proficiency_exam = ''
                    exam_total = ''
                    exam_reading = ''
                    exam_listening = ''
                    exam_speaking = ''
                    exam_writing = ''
        
                    if TOEFL_COMPI != 'NA':
                        proficiency_exam = 'TOEFL'
                        exam_total = TOEFL_COMPI
                        exam_reading = TOEFL_Reading
                        exam_listening = TOEFL_Listening
                        exam_speaking = TOEFL_Speaking
                        exam_writing = TOEFL_Writing
                    # elif IELTS_Overall != 'NA':
                    #     proficiency_exam = 'IELTS'
                    #     exam_total = IELTS_Overall
                    #     exam_reading = IELTS_Reading
                    #     exam_listening = IELTS_Listening
                    #     exam_speaking = IELTS_Speaking
                    #     exam_writing = IELTS_Writing
                    elif TOEFL_COMPI != 'NA' and IELTS_Overall != 'NA':
                        proficiency_exam = 'TOEFL;IELTS'
                        exam_total = TOEFL_COMPI + ';' + IELTS_Overall
                        exam_reading = TOEFL_Reading + ';' + IELTS_Reading
                        exam_listening = TOEFL_Listening + ';' + IELTS_Listening
                        exam_speaking = TOEFL_Speaking + ';' + IELTS_Speaking
                        exam_writing = TOEFL_Writing + ';' + IELTS_Writing
                    else:
                        proficiency_exam = 'NA'
                        exam_total = 'NA'
                        exam_reading = 'NA'
                        exam_listening = 'NA'
                        exam_speaking = 'NA'
                        exam_writing = 'NA'
                    
                    # write headers in
                    print("<Student ID: " + crow_id + ">", file = output_file)
                    print("<Country: " + country + ">", file = output_file)
                    print("<Institution: " + institution + ">", file = output_file)
                    print("<Course: ENGL " + course + ">", file = output_file)
                    # print("<Mode: " + mode + ">", file = output_file)
                    # print("<Length: " + length + ">", file = output_file)
                    # print("<Assignment: " + assignment + ">", file = output_file)
                    # print("<Draft: " + draft + ">", file = output_file)
                    print("<Year in School: " + year_in_school_numeric + ">", file = output_file)
                    print("<Gender: " + gender + ">", file = output_file)
                    print("<Course Year: " + year + ">", file = output_file)
                    print("<Course Semester: " + semester + ">" , file = output_file)
                    print("<College: " + college + ">", file = output_file)
                    print("<Program: " + program + ">", file = output_file)
                    print("<Proficiency Exam: " + proficiency_exam +">", file = output_file)
                    print("<Exam total: " + exam_total + ">", file = output_file)
                    print("<Exam reading: " + exam_reading + ">", file = output_file)
                    print("<Exam listening: " + exam_listening + ">", file = output_file)
                    print("<Exam speaking: " + exam_speaking + ">", file = output_file)
                    print("<Exam writing: " + exam_writing + ">", file = output_file)
                    print("<Instructor: " + instructor + ">", file = output_file)
                    print("<Section: " + section + ">", file = output_file)
                    print("<End Header>", file = output_file)
                    print("", file = output_file)
                    
                    for line in textfile:
                        this_line = re.sub(r'\r?\n', r'\r\n', line)
                        if this_line != '\r\n':
                            new_line = re.sub(r'\s+', r' ', this_line)
                            new_line = new_line.strip()
                            print(new_line, file = output_file)
                    output_file.close()
                textfile.close()
    return(found_text_files)

def add_headers_recursive(directory, df, overwrite=False):
    found_text_files = False
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            is_this_a_text_file = add_header_to_file(os.path.join(dirpath, name), df) # the last overwrite is deleted
            if is_this_a_text_file:
                found_text_files = True
    if not found_text_files:
        print('No text files found in the directory.')
        
if args.df_file and args.dir:
    if '.xls' in args.df_file:
        df_file = pd.ExcelFile(args.df_file)
        df_data = pd.read_excel(df_file)
    elif '.csv' in args.df_file:
        df_data = pd.read_csv(args.df_file)

    add_headers_recursive(args.dir, df_data)
else:
    print('You need to supply a valid df file and directory with textfiles')





