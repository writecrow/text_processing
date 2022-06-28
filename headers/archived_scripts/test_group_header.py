#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 00:13:24 2020

@author: CCloveHH
"""

#It should be only in RTD*
# Mac users---run in terminal: python test_group_header.py --directory RTDF --master_file=Merge.xlsx --group_info=FYW_Purdue_metadata.xlsx

import argparse
import sys
import re
import os
import pandas as pd

# Define the way we retrieve arguments sent to the script.

parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--master_file', action="store", dest='master_file', default='')
parser.add_argument('--group_info', action="store", dest='group_info', default='')
args = parser.parse_args()



def get_group_number(filename): #to get the last element of each group file and to get the group number
    found_text_files = False
    group_number = ''
    if '.txt' in filename:
        filename_parts = filename.split('_')
        group_name = re.sub(r'\.txt', r'', filename_parts[-1])
        group_name = re.sub(r'\s+', r' ', group_name)
        group_number = group_name.split(' ')
        group_number = group_number[-1]
        found_text_files = True
    return group_number, found_text_files



def match_group_name(group_info, master, filename):  # to match names in a group and to split last and first names
    group_number,__ = get_group_number(filename)
    group_info1 = group_info[group_info['Group number'] == float(group_number)]
    first_name = []
    last_name = []
    name_parts = []
    
    for i in group_info1['Name']: # to split the first and last name in the group infomation file
        name_parts.append(i.split(' '))     
    for i in name_parts:
        first_name.append(i[0]) 
        last_name.append(i[-1])
    filtered_registrar3 = pd.DataFrame(columns = list(master.columns))
    for i in range(len(first_name)): #to match names in each group with the names in the registrar info
        filtered_registrar1 = master[master['Last Name'] == last_name[i]]
        filtered_registrar2 = filtered_registrar1[filtered_registrar1['First Name'] == first_name[i]]
        filtered_registrar3= filtered_registrar3.append(filtered_registrar2, ignore_index = True) # filtered_registrar 3 stored everyone's retistrar information in one group 
    return (filtered_registrar3)

def add_header_to_file(filename, master, group_info):
    
    filtered_registrar3 = match_group_name(group_info, master, filename)
    
    for i in filtered_registrar3.index:
        textfile = open(filename, 'r')
        
        course = str(filtered_registrar3['Catalog Nbr'][i])
        course = course.strip()
        course = re.sub(r'NaN', r'NA', course)
        
        assignment = 'RT'
        draft = 'F'
        
        country_code = str(filtered_registrar3['Birth Country Code'][i])
        country_code = country_code.strip()
        country_code = re.sub(r'NaN', r'NAN', country_code)
        
        year_in_school_numeric = str(filtered_registrar3['Acad Level'][i])
        year_in_school_numeric = year_in_school_numeric.strip()
    
        gender = str(filtered_registrar3['Gender'][i])
        gender = gender.strip()
        gender = re.sub(r'NaN', r'NA', gender)
        
        crow_id = str(filtered_registrar3['Crow ID'][i])
        crow_id = crow_id.strip()
        crow_id = re.sub(r'NaN', r'NA', crow_id)
    
        institution_code = str(re.sub(r'[a-z\s]', r'', filtered_registrar3['institution'][i]))
        
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
        
        term = str(filtered_registrar3['term'][i])
        term = term.strip()
        path = "files_with_headers/" + term + "/ENGL" + course + "/" + assignment + "/" + draft + "/"
        
        filename = path + output_filename
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        output_file = open(path + output_filename, "w")
        
        institution = str(filtered_registrar3['institution'][i])
        institution = institution.strip()
    
        semester = term.split()[0]
        year = term.split()[1]
        college = str(filtered_registrar3['College'][i])
        program = str(filtered_registrar3['Major'][i])
        TOEFL_COMPI = str(filtered_registrar3['TOEFL COMPI'][i])
        TOEFL_Listening = str(filtered_registrar3['TOEFL Listening'][i])
        TOEFL_Reading = str(filtered_registrar3['TOEFL Reading'][i])
        TOEFL_Writing = str(filtered_registrar3['TOEFL Writing'][i])
        TOEFL_Speaking = str(filtered_registrar3['TOEFL Speaking'][i])
        IELTS_Overall = str(filtered_registrar3['IELTS Overall'][i])
        IELTS_Listening = str(filtered_registrar3['IELTS Listening'][i])
        IELTS_Reading = str(filtered_registrar3['IELTS Reading'][i])
        IELTS_Writing = str(filtered_registrar3['IELTS Writing'][i])
        IELTS_Speaking = str(filtered_registrar3['IELTS Speaking'][i])
        instructor = str(filtered_registrar3['Instructor Code'][i])
        section = str(filtered_registrar3['Class Section'][i])
        # mode = str(filtered_registrar3['mode_of_course'][i])
        # length = str(filtered_registrar3['length_of_course'][i])
        
        college = college.strip()
        program = program.strip()
        TOEFL_COMPI = TOEFL_COMPI.strip()
        TOEFL_Listening = TOEFL_Listening.strip()
        TOEFL_Reading = TOEFL_Reading.strip()
        TOEFL_Writing = TOEFL_Writing.strip()
        TOEFL_Speaking = TOEFL_Speaking.strip()
        IELTS_Overall = IELTS_Overall.strip()
        IELTS_Listening = IELTS_Listening.strip()
        IELTS_Reading = IELTS_Reading.strip()
        IELTS_Writing = IELTS_Writing.strip()
        IELTS_Speaking = IELTS_Speaking.strip()
        instructor = instructor.strip()
        section = section.strip()
        # mode = mode.strip()
        # length = length.strip()
        
        country_code = re.sub(r'NaN', r'NA', country_code)
        TOEFL_COMPI = re.sub(r'NaN', r'NA', TOEFL_COMPI)
        TOEFL_Listening = re.sub(r'NaN', r'NA', TOEFL_Listening)
        TOEFL_Reading = re.sub(r'NaN', r'NA', TOEFL_Reading)
        TOEFL_Writing = re.sub(r'NaN', r'NA', TOEFL_Writing)
        TOEFL_Speaking = re.sub(r'NaN', r'NA', TOEFL_Speaking)
        IELTS_Overall = re.sub(r'NaN', r'NA', IELTS_Overall)
        IELTS_Listening = re.sub(r'NaN', r'NA', IELTS_Listening)
        IELTS_Reading = re.sub(r'NaN', r'NA', IELTS_Reading)
        IELTS_Writing = re.sub(r'NaN', r'NA', IELTS_Writing)
        IELTS_Speaking = re.sub(r'NaN', r'NA', IELTS_Speaking)   
        
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
        elif IELTS_Overall != 'NA':
            proficiency_exam = 'IELTS'
            exam_total = IELTS_Overall
            exam_reading = IELTS_Reading
            exam_listening = IELTS_Listening
            exam_speaking = IELTS_Speaking
            exam_writing = IELTS_Writing
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
        print("<Country: " + country_code + ">", file = output_file)
        print("<Institution: " + institution + ">", file = output_file)
        print("<Course: ENGL " + course + ">", file = output_file)
        # print("<Mode: " + mode + ">", file = output_file)
        # print("<Length: " + length + ">", file = output_file)
        print("<Assignment: " + assignment + ">", file = output_file)
        print("<Draft: " + draft + ">", file = output_file)
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
                              
def add_headers_recursive(directory, master,group_info):
    found_text_files = False
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            sys.stdout.write(os.path.join(dirpath, name))
            __,is_this_a_text_file = get_group_number(os.path.join(dirpath, name))
            if is_this_a_text_file:
                sys.stdout.write('heihei')
                found_text_files = True
                add_header_to_file(os.path.join(dirpath, name), master, group_info)
    if not found_text_files:
        print('No text files found in the directory.')    

                          
if args.master_file and args.dir and args.group_info:
    if '.xls' in args.master_file:
        master_file = pd.ExcelFile(args.master_file)
        master_data = pd.read_excel(master_file)
    elif '.csv' in args.master_file:
        master_data = pd.read_csv(args.master_file)
    if '.xls' in args.group_info:
#        group_data = pd.ExcelFile(args.group_info)
        group_info = pd.read_excel(args.group_info)
    elif '.csv' in args.group_info:
        group_info = pd.read_csv(args.group_info)
    
    add_headers_recursive(args.dir, master_data, group_info)
else:
    print('You need to supply a valid master file and directory with textfiles')                         
                
                             

            


    

    
    
    
    

   

