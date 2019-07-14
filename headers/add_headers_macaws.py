#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file and text files passed as arguments to the script,
# metadata headers are added to each individual text files
#
# Usage example:
#    python add_headers_macaws.py --directory=../../../MACAWS/Portuguese/Spring_2017/Processed/ --master_file=../../../MACAWS/Portuguese/metadata/master_metadata_spring2017_spring2019.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Portuguese.xlsx



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
parser.add_argument('--master_instructor_file', action="store", dest='master_instructor_file', default='')
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
        clean_filename = re.sub(r'\\', r'/', filename)
        clean_filename = re.sub(r'\.\.\/', r'', filename)
        file_folders = clean_filename.split('/')

        target_language = file_folders[1]
        target_language_code = target_language[:4].upper()
        semester = re.sub(r'_', r' ',file_folders[2])
        course = file_folders[4]
        intructor_first_name = file_folders[5]
        section = file_folders[6]
        mode_of_assignment = file_folders[7]
        assignment = file_folders[8]
        draft = file_folders[9]

        filtered_master1 = master[master['semester'] == semester]

        student_id = 0
        for index, row in filtered_master1.iterrows():
            this_row_filename = row['filename']
            this_row_filename = this_row_filename.strip()
            this_row_filename = re.sub(r'\s', r'\\s', this_row_filename)
            this_regex = re.compile(this_row_filename, re.I)
            this_match = re.match(this_regex, student_name)
            if this_match:
                student_id = row['MACAWS ID']

        filtered_master2 = filtered_master1[filtered_master1['MACAWS ID'] == student_id]

        if filtered_master2.empty:
            print('***********************************************')
            print('Unable to find metadata for this file: ')
            print(filename)
            print(student_name)
            print('***********************************************')

        if filtered_master2.shape[0] > 1:
            print('***********************************************')
            print('More than one row in metadata for this file: ')
            print(filename)
            print(student_name)
            print('***********************************************')
        else:
            print('Adding headers to file ' + filename)
            textfile = open(filename, 'r')

            year_in_school = filtered_master2['year'].to_string(index=False)
            year_in_school = year_in_school.strip()
            year_in_school_numeric = '1'
            if year_in_school.lower() == 'sophomore':
                year_in_school_numeric = '2'
            elif year_in_school.lower() == 'junior':
                year_in_school_numeric = '3'
            elif year_in_school.lower() == 'senior':
                year_in_school_numeric = '4'

            institution =  filtered_master2['institution'].to_string(index=False)
            institution = institution.strip()
            institution_code = re.sub(r'[a-z\s]', r'',institution)

            language_code = ''
            first_languages = filtered_master2['native_languages'].to_string(index=False)
            first_languages = first_languages.strip()
            
            if ';' in first_languages:
                language_code = 'MLT'
            elif 'Arabic' in first_languages:
                language_code = 'ARA'
            elif 'Spanish' in first_languages:
                language_code = 'SPA'
            elif 'English' in first_languages:
                language_code = 'ENG'
            elif 'Korean' in first_languages:
                language_code = 'KOR'
            elif 'Portuguese' in first_languages:
                language_code = 'POR'

            heritage_target_language = filtered_master2['heritage'].to_string(index=False)
            heritage_code = '0'
            heritage_header = 'No'

            if heritage_target_language == '1.0':
                heritage_code = '1'
                heritage_header = 'Yes'

            assignment_code = 'AA'

            str_student_id = str(student_id)
            str_student_id = str_student_id[:-2]

            new_course = re.sub(r'\s+', r'_', course)

            #course assignment draft country yearinschool gender studentID institution '.txt'
            output_filename = ''
            output_filename += new_course
            output_filename += '_'
            output_filename += language_code
            output_filename += '_'
            output_filename += heritage_code
            output_filename += '_'
            output_filename += assignment
            output_filename += '_'
            output_filename += draft
            output_filename += '_'
            output_filename += str_student_id
            output_filename += '_'
            output_filename += institution_code
            output_filename += '.txt'
            output_filename = re.sub(r'\s', r'', output_filename)

            if 'Series' not in output_filename and 'S([],)' not in output_filename:
                folder_term = semester
                path = "files_with_headers/" + folder_term + "/" + course+ "/" + assignment + "/" + draft + "/"

                if not os.path.exists(path):
                    os.makedirs(path)

                output_file = open(path + output_filename, 'w')

                semester_season = semester.split()[0]
                semester_year = semester.split()[1]

                major = filtered_master2['major'].to_string(index=False)
                major = major.strip()
                major = re.sub(r'NaN', r'NA', major)

                minor = filtered_master2['minor'].to_string(index=False)
                minor = minor.strip()
                minor = re.sub(r'NaN', r'NA', minor)

                mode_of_course = filtered_master2['mode_of_course'].to_string(index=False)
                mode_of_course = mode_of_course.strip()

                length_of_course = filtered_master2['length_of_course'].to_string(index=False)
                length_of_course = length_of_course.strip()

                additional_languages = filtered_master2['aditional_languages'].to_string(index=False)
                additional_languages = additional_languages.strip()
                additional_languages = re.sub(r'NaN', r'NA', additional_languages)

                instructor_code = '000'

                current_courses = filtered_master2['courses_taking'].to_string(index=False)
                current_courses = current_courses.strip()
                current_courses = re.sub(r'NaN', r'NA', current_courses)

                previous_courses = filtered_master2['previous_courses'].to_string(index=False)
                previous_courses = previous_courses.strip()
                previous_courses = re.sub(r'NaN', r'NA', previous_courses)

                age = filtered_master2['age'].to_string(index=False)
                age = age.strip()
                age = re.sub(r'NaN', r'NA', age)

                began_target_language = filtered_master2['began_target_language'].to_string(index=False)
                began_target_language = began_target_language.strip()
                began_target_language = re.sub(r'NaN', r'NA', began_target_language)

                profiency_exam = filtered_master2['profiency_exam'].to_string(index=False)
                profiency_exam = profiency_exam.strip()
                profiency_exam = re.sub(r'NaN', r'NA', profiency_exam)

                exam_scores = filtered_master2['exam_scores'].to_string(index=False)
                exam_scores = exam_scores.strip()
                exam_scores = re.sub(r'NaN', r'NA', exam_scores)

                experience_abroad = filtered_master2['experience_abroad'].to_string(index=False)
                experience_abroad = experience_abroad.strip()
                experience_abroad = re.sub(r'NaN', r'NA', experience_abroad)

                other_experience = filtered_master2['other_experience'].to_string(index=False)
                other_experience = other_experience.strip()
                other_experience = re.sub(r'NaN', r'NA', other_experience)

                # write headers
                output_file.write('<Target Language: ' + target_language + '>\r\n')
                output_file.write('<Course: ' + course + '>\r\n')
                output_file.write('<L1: ' + first_languages + '>\r\n')
                output_file.write('<Other Languages: ' + additional_languages + '>\r\n')
                output_file.write('<Assignment: ' + assignment + '>\r\n')
                output_file.write('<Draft: ' + draft + '>\r\n')
                output_file.write('<Student ID: ' + str_student_id + '>\r\n')
                output_file.write('<Institution: ' + institution + '>\r\n')
                output_file.write('<Mode of Course: ' + mode_of_course + '>\r\n')
                output_file.write('<Length of Course: ' + length_of_course + '>\r\n')
                output_file.write('<Mode of Assignment: ' + mode_of_assignment +
                                        '>\r\n')
                output_file.write('<Course Year: ' + semester_year + '>\r\n')
                output_file.write('<Course Semester: ' + semester_season+ '>\r\n')
                output_file.write('<Instructor: ' + instructor_code + '>\r\n')
                output_file.write('<Heritage of Target Language: ' +
                                   heritage_header + '>\r\n')
                output_file.write('<Proficiency Exam: ' + profiency_exam + '>\r\n')
                output_file.write('<Proficiency Exam Score: ' + exam_scores + '>\r\n')
                output_file.write('<Experience Abroad: ' + experience_abroad + '>\r\n')
                output_file.write('<Other Experience with Target Language: ' +
                                   other_experience + '>\r\n')
                output_file.write('<Began Learning Target Language: ' + began_target_language + '>\r\n')
                output_file.write('<Courses Currently Enrolled: ' +
                                    current_courses + '>\r\n')
                output_file.write('<Courses Previously Enrolled: '+
                                    previous_courses +'>\r\n')
                output_file.write('<Age: ' + age + '>\r\n')
                output_file.write('<Year in School: ' + year_in_school + '>\r\n')
                output_file.write('<Major: ' + major + '>\r\n')
                output_file.write('<Minor: ' + minor + '>\r\n')
                output_file.write("<End Header>\r\n\r\n")

                for line in textfile:
                    this_line = line.strip()
                    if this_line != '':
                        new_line = re.sub(r'\s+', r' ', this_line)
                        new_line = new_line.strip()
                        output_file.write(new_line+'\r\n')

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

    add_headers_recursive(args.dir, master_data, args.overwrite)
else:
    print('You need to supply a valid master file, a directory with textfiles, and a master instructor file')
