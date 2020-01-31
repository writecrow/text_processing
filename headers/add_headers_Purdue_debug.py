#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file and text files passed as arguments to the script,
# metadata headers are added to each individual text files

# Windows run with Anaconda Prompt example:
#    python add_headers.py --directory="Fall 2018/normalized/" --master_file="Metadata_Fall_2018_updated.csv"

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

def add_header_to_file(filename, master, overwrite=False): # filename = folder1.../Lan/Lan_p1d3/WA_Second Draft_lan12_attempt_2017-06-29_Lan Ge_WA Second.txt
    found_text_files = False
    if '.txt' in filename:
        found_text_files = True
        #filename_parts = filename.split('_')

        if match_pattern = re.match(r’_([a-z]+[0-9]+)_’):
            # only assign "[a-z]+[0-9]+" to career account (lan12)
            career_acount = match.group(1)
		else:
            # there are exceptions, for example, a small set of career account has only lowercase letters w/o numebers
			print(filename,">>> this is the file for mannual check") 
        
        # Use "==" for comparison: to compare a value with all values in a list and returns a boolean value (T or F): 
        # If a career account matches an item in the master['User ID'] column (true), then store all metainfo of this row in the filtered_master data frame
		filtered_master = master[master['User_ID'] == career_account] #master is the metainfo file that is passed to the function by command line arg.
        
        # QUESTION-1 ".empty"? 
        if filtered_master.empty:
            print('***********************************************')
            print('Unable to find metadata for this file: ')
            print(filename)
            print(career_account)

		else:
            print('Adding headers to file ' + filename)
            textfile = open(filename, 'r')
            filename_parts2 = filename.split('\\') #split based on the unix filename pattern

            # QUESTION-2: Subj + Course number = ENGL 10600
            # To-do: merge two columns with a space or join course numbe with a string "ENGL". 
            course = filtered_master['COURSE_NUMBER'].to_string(index=False)
            course = course.strip()
            course = re.sub(r'NaN', r'NA', course)
			
			# Identify assignment and draft based on folder structure
			# Example:filename_parts2 = ['Summer2017','Lan','Lan_p1d3','WA_Second_la12_attempt_2017-06-16','assignment1']
            assignment_draft_string = filename_parts2[2] #Lan_p1d3
			if re.research(r'([a-zA-Z]+\_)p1d1',filename_parts2[2]):
				assignment = 'LN'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p1d2',filename_parts2[2]):
				assignment = 'LN'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p1d3',filename_parts2[2]):
				assignment = 'LN'
				draft = 'F'
			if re.research(r'([a-zA-Z]+\_)p2d1',filename_parts2[2]):
				assignment = 'RP'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p2d2',filename_parts2[2]):
				assignment = 'RP'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p2d3',filename_parts2[2]):
				assignment = 'RP'
				draft = 'F'
			if re.research(r'([a-zA-Z]+\_)p3d1',filename_parts2[2]):
				assignment = 'IR'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p3d2',filename_parts2[2]):
				assignment = 'IR'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p3d3',filename_parts2[2]):
				assignment = 'IR'
				draft = 'F'
			if re.research(r'([a-zA-Z]+\_)p4d1',filename_parts2[2]):
				assignment = 'SY'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p4d2',filename_parts2[2]):
				assignment = 'SY'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p4d3',filename_parts2[2]):
				assignment = 'SY'
				draft = 'F'
			if re.research(r'([a-zA-Z]+\_)p5d1',filename_parts2[2]):
				assignment = 'AR'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p5d2',filename_parts2[2]):
				assignment = 'AR'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p5d3',filename_parts2[2]):
				assignment = 'AR'
				draft = 'F'
			
            # To-do (Wendy): create a new column for country code (three letters): https://www.iban.com/country-codes
            country_code = filtered_master['NATION_OF_CITIZENSHIP'].to_string(index=False)
            country_code = country_code.strip()
            country_code = re.sub(r'NaN', r'NAN', country_code)
			
            # STUDENT_CLASS_BOAP is a number to show the semester in school for students
            # STUDENT_CLASS_BOAP_DESC is a string to descibe students' status (junior 45-60 hours)
			semester_in_school = filtered_master['STUDENT_CLASS_BOAP']
            year_in_school = filtered_master['STUDENT_CLASS_BOAP_DESC'].to_string(index=False)
            year_in_school = year_in_school.strip()
			year_in_school_numeric = 'NA'
			
			if re.search(r'Freshmen(\:.*)',year_in_school):
				year_in_school_numeric = '1'
			if re.search(r'Sophomore(\:.*)',year_in_school):
				year_in_school_numeric = '2'
			if re.search(r'Junior(\:.*)',year_in_school):
				year_in_school_numeric = '3'
			if re.search(r'Senior(\:.*)',year_in_school):
				year_in_school_numeric = '4'
            else:
                year_in_school_numeric = year_in_school

            gender = filtered_master['GENDER'].to_string(index=False)
            gender = gender.strip()
            gender = re.sub(r'NaN', r'NA', gender)

            crow_id = filtered_master['Crow ID'].to_string(index=False)
            crow_id = crow_id.strip()
            crow_id = re.sub(r'NaN', r'NA', crow_id)
			
            institution_code = 'PRD' # hard coding: PRD = Purdue University 
			
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
            
            # To-do: separate semster: summer 2017 -> ['summer', '2017']
            term = filtered_master['semester'].to_string(index=False)
            term = term.strip()

			# QUESTION-3: To-do: change this path format for windows pattern
            # path = "files_with_headers/" + term + "/ENGL " + course+ "/" + assignment + "/" + draft + "/"
            path = "files_with_headers\\" + term + "\\ENGL " + course+ "\\" + assignment + "\\" + draft + "\\"

            if not os.path.exists(path):
                os.makedirs(path)
            output_file = open(path + output_filename, 'w')

			country = filtered_master['NATION_OF_CITIZENSHIP_DESC'].to_string(index=False)
            country = country.strip()
			institution = 'Purdue University'
            institution = institution.strip()
             
            # To-do: check QUESTION-3 
			semester = term.split()[0]
            year = term.split()[1]
				
            college = filtered_master['COLLEGE'].to_string(index=False)
            program = filtered_master['PROGRAM_DESC'].to_string(index=False)
            TOEFL_COMPI = filtered_master['TIBT - TOEFL IBT Total Score'].to_string(index=False)
            TOEFL_Listening = filtered_master['TIBL - TOEFL IBT Listening Score'].to_string(index=False)
            TOEFL_Reading = filtered_master['TIBR - TOEFL IBT Reading Score'].to_string(index=False)
            TOEFL_Writing = filtered_master['TIBW - TOEFL IBT Writing Score'].to_string(index=False)
            TOEFL_Speaking = filtered_master['TIBS - TOEFL IBT Speaking Score'].to_string(index=False)
            IELTS_Overall = filtered_master['ILT2 - IELTS Overall'].to_string(index=False)
            IELTS_Listening = filtered_master['ILT1 - IELTS Listening'].to_string(index=False)
            IELTS_Reading = filtered_master['ILT3 - IELTS Reading'].to_string(index=False)
            IELTS_Writing = filtered_master['ILT5 - IELTS Writing'].to_string(index=False)
            IELTS_Speaking = filtered_master['ILT4 - IELTS Speaking'].to_string(index=False)
            instructor = filtered_master['Instructor Code'].to_string(index=False)
            section = filtered_master['COURSE_REFERENCE_NUMBER'].to_string(index=False)
                
			#To-do (Wendy): add mode and length manually to the meta-info file
			mode = filtered_master['mode_of_course'].to_string(index=False)
            length = filtered_master['length_of_course'].to_string(index=False)
           
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
            
			mode = mode.strip()
            length = length.strip()

            country = re.sub(r'NaN', r'NA', country)
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


			# Identify the exams
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

            # write headers
            print("<Student ID: " + crow_id + ">", file = output_file)
            print("<Country: " + country + ">", file = output_file)
            print("<Institution: " + institution + ">", file = output_file)
            print("<Course: ENGL " + course + ">", file = output_file)
            print("<Mode: " + mode + ">", file = output_file)
            print("<Length: " + length + ">", file = output_file)
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
    return(found_text_files)
    

def add_headers_recursive(directory, master, overwrite=False):
    found_text_files = False
    for dirpath, dirnames, files in os.walk(directory): #dirpath = whole path, dirnames = folder names, file = filename.txt (with txt)
        for name in files: #with each filename.txt in the files list (WA_second Draft_lan12_attempt_2017-06-29_Lan Ge_WA Second.txt)
            is_this_a_text_file = add_header_to_file(os.path.join(dirpath, name), master, overwrite) #dirpath join name together = folder/folder2/file'sname.txt
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



