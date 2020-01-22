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
        filename_parts = filename.split('_')
        
		#based on the observation, the career account is in the -3, -4, or -5 position
		#there are exceptions, for example, a small set of career account has only lowercase letters w/o numebers
		if re.search(r'[a-z]+[0-9]+',filename_parts[-3]):
			career_account = filename_parts[-3]
		elif re.search(r'[a-z]+[0-9]+',filename_parts[-4]):
			career_account = filename_parts[-4]
		elif re.search(r'[a-z]+[0-9]+',filename_parts[-5]):
			career_account = filename_parts[-5]
		else:
			print(filename,">>> this is the file for mannual check")
				
		#filter by Purdue Career Account: lan12
		#Question-1: how does this work? career_account is a string whereas master['User_ID'] is a column with all cases of career account
		filtered_master = master[master['User_ID'] == career_account] #master is the metainfo file that is passed to the function by command line arg.

        if filtered_master.empty: #if the career_account (lan12) extracted from the filename does not match any career_account in the User_ID column
            print('***********************************************')
            print('Unable to find metadata for this file: ')
            print(filename)
            print(career_account)
#------------------------------------------------------------------------------------------------------------------------------------
		else:
            print('Adding headers to file ' + filename)
            textfile = open(filename, 'r')
            filename_parts2 = filename.split('\\') #split based on the unix filename pattern
			
			#Question-2: related to Question-1, what is 'filtered_master' and how does it work?
            course = filtered_master['COURSE_NUMBER'].to_string(index=False)#may need to loc row here?????
            course = course.strip()
            course = re.sub(r'NaN', r'NA', course)
			
			#identify assignment and draft based on folder structure
			#Example:filename_parts2 = ['Summer2017','Lan','Lan_p1d3','WA_Second_la12_attempt_2017-06-16','assignment1']
            assignment_draft_string = filename_parts2[2] #Lan_p1d3
			if re.research(r'([a-zA-Z]+\_)p1d1',filename_parts2[2]):
				assignment = 'narratives'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p1d2',filename_parts2[2]):
				assignment = 'narratives'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p1d3',filename_parts2[2]):
				assignment = 'narratives'
				draft = '3'
			if re.research(r'([a-zA-Z]+\_)p2d1',filename_parts2[2]):
				assignment = 'proposal'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p2d2',filename_parts2[2]):
				assignment = 'proposal'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p2d3',filename_parts2[2]):
				assignment = 'proposal'
				draft = '3'
			if re.research(r'([a-zA-Z]+\_)p3d1',filename_parts2[2]):
				assignment = 'interview report'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p3d2',filename_parts2[2]):
				assignment = 'interview report'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p3d3',filename_parts2[2]):
				assignment = 'interview report'
				draft = '3'
			if re.research(r'([a-zA-Z]+\_)p4d1',filename_parts2[2]):
				assignment = 'synthesis paper'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p4d2',filename_parts2[2]):
				assignment = 'synthesis paper'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p4d3',filename_parts2[2]):
				assignment = 'synthesis paper'
				draft = '3'
			if re.research(r'([a-zA-Z]+\_)p5d1',filename_parts2[2]):
				assignment = 'argumentative paper'
				draft = '1'
			if re.research(r'([a-zA-Z]+\_)p5d2',filename_parts2[2]):
				assignment = 'argumentative paper'
				draft = '2'
			if re.research(r'([a-zA-Z]+\_)p5d3',filename_parts2[2]):
				assignment = 'argumentative paper'
				draft = '3'
			
			# Question-3: what's the difference between country and country_code? for example CN for China is the code?
            country_code = filtered_master['NATION_OF_CITIZENSHIP'].to_string(index=False)
            country_code = country_code.strip()
            country_code = re.sub(r'NaN', r'NAN', country_code)

            year_in_school = filtered_master['STUDENT_CLASS_BOAP_DESC'].to_string(index=False)
            year_in_school = year_in_school.strip()
			year_in_school_numeric = 'NA'
			
			if re.research(r'Freshmen(\:.*)',year_in_school):
				year_in_school_numeric = '1'
			if re.research(r'Sophomore(\:.*)',year_in_school):
				year_in_school_numeric = '2'
			if re.research(r'Junior(\:.*)',year_in_school):
				year_in_school_numeric = '3'
			if re.research(r'Senior(\:.*)',year_in_school):
				year_in_school_numeric = '4'
            else:
                year_in_school_numeric = year_in_school

            gender = filtered_master['GENDER_DESC'].to_string(index=False)
            gender = gender.strip()
            gender = re.sub(r'NaN', r'NA', gender)

            crow_id = filtered_master['Crow ID'].to_string(index=False)#to-do: modified the register_data_modified_2.0 to add Crow ID in the metainfo file
            crow_id = crow_id.strip()
            crow_id = re.sub(r'NaN', r'NA', crow_id)
			
			#Question-5: what it institution code? Can we just do hard coding here, for example institution_code = 2 (for Purdue)
            institution_code = re.sub(r'[a-z\s]', r'', filtered_master2['institution'].to_string(index=False))
			
#-----------------------------------------------------------------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------------------------------------------------------------
            #Question-6: why Series in the output filename?
			if 'Series' not in output_filename:
                term = filtered_master2['term'].to_string(index=False)
                term = term.strip()
				#create a path for files with headers 
				#change this path format for windows pattern
                path = "files_with_headers/" + term + "/ENGL " + course+ "/" + assignment + "/" + draft + "/"

                if not os.path.exists(path):
                    os.makedirs(path)
                output_file = open(path + output_filename, 'w')

                
				country = filtered_master['NATION_OF_CITIZENSHIP_DESC'].to_string(index=False)
                country = country.strip()
				
				#Question-7: We have no institution in the metainfo file, can we do hard coding here, institution = Purdue?
                institution = filtered_master2['institution'].to_string(index=False)
                institution = institution.strip()
                
				semester = term.split()[0]
                year = term.split()[1]
				
				
                college = filtered_master['COLLEGE_DESC'].to_string(index=False)
                program = filtered_master['MAJOR_DESC'].to_string(index=False)
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
                
				# Question-8: we have no mode and length info in the metainfo file, we can do hard coding right, for the exisiting data? mode = face-to-face, length = 16 weeks 
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


				# Question-9: the variables below are only for AZ data right? we don't have exam_toal kind of columns in Purdue data
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
#------------------------------------------------------------------------------------------------------------------------------------------------------
                # write headers in
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



