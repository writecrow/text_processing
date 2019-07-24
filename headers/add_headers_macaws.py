#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file and text files passed as arguments to the script,
# metadata headers are added to each individual text files
#
# Usage example:
#    python add_headers_macaws.py --directory=../../../MACAWS/Portuguese/normalized_all_semesters/Spring_2017/Processed/ --master_file=../../../MACAWS/Portuguese/metadata/master_metadata_spring2017_spring2019.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Portuguese.xlsx --master_assignment_file=../../../MACAWS/Assignment_and_Instructor_codes/assignment_codes_across_languages.xlsx --master_course_file=../../../MACAWS/Portuguese/metadata/port_course_credit_hours.xlsx
#    python add_headers_macaws.py --directory=../../../MACAWS/Portuguese/normalized_all_semesters/ --master_file=../../../MACAWS/Portuguese/metadata/master_metadata_spring2017_spring2019.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Portuguese.xlsx --master_assignment_file=../../../MACAWS/Assignment_and_Instructor_codes/assignment_codes_across_languages.xlsx --master_course_file=../../../MACAWS/Portuguese/metadata/port_course_credit_hours.xlsx
#    python add_headers_macaws.py --directory=../../../MACAWS/Russian/Spring_2018/Normalized/ --master_file=../../../MACAWS/Russian/new_master_meta.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Russian.csv --master_assignment_file=../../../MACAWS/Assignment_and_Instructor_codes/assignment_codes_across_languages.xlsx
#    python add_headers_macaws.py --directory=../../../MACAWS/Russian/Spring_2018/Normalized/RSSS_202/Novikov/Section_001-2/Writing/Climate_change --master_file=../../../MACAWS/Russian/new_master_meta.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Russian.csv --master_assignment_file=../../../MACAWS/Assignment_and_Instructor_codes/assignment_codes_across_languages.xlsx
#    python add_headers_macaws.py --directory=../../../MACAWS/Russian/Fall_2018/Normalized/ --master_file=../../../MACAWS/Russian/newest_master_meta.xlsx --master_instructor_file=../../../MACAWS/Assignment_and_Instructor_codes/Instructor_codes_Russian.csv --master_assignment_file=../../../MACAWS/Assignment_and_Instructor_codes/assignment_codes_across_languages.xlsx


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
parser.add_argument('--master_assignment_file', action="store", dest='master_assignment_file', default='')
parser.add_argument('--master_course_file', action="store", dest='master_course_file', default='')
args = parser.parse_args()


def add_header_to_file(filename, master, master_instructor, master_assignment, overwrite=False):
    found_text_files = False
    found_all_metadata = True
    if '.txt' in filename:
        found_text_files = True
        print('Checking metadata for file ' + filename)

        # get info from file folder structure
        clean_filename = re.sub(r'\\', r'/', filename)
        clean_filename = re.sub(r'\.\.\/', r'', filename)
        file_folders = clean_filename.split('/')

        filename_parts = clean_filename.split('- ')

        if len(filename_parts) == 1:
            filename_parts = clean_filename.split('/')
            student_name = re.sub(r'\.txt', r'', filename_parts[-1])
            student_name = re.sub(r'\s+', r' ', student_name)
        else:
            student_name = re.sub(r'\.txt', r'', filename_parts[1])
            student_name = re.sub(r'\s+', r' ', student_name)
            if student_name[-1] == '-':
                student_name = student_name[:-1]

        student_name = re.sub(r'_',r' ', student_name)
        student_name = re.sub(r'Essay.+',r'', student_name, re.I | re.DOTALL)
        student_name = student_name.strip()

        # where is the semester folder?
        where_semester = -1
        for i in range(0,len(file_folders)):
            folder = file_folders[i]
            if 'Spring' in folder:
                where_semester = i
            elif 'Fall' in folder:
                where_semester = i

        if where_semester == -1:
            print('***********************************************')
            print('Unable to find semester folder for this file: ')
            print(filename)
            print('***********************************************')
            found_all_metadata = False

        target_language = file_folders[1]
        target_language_code = target_language[:4].upper()
        semester = re.sub(r'_', r' ',file_folders[where_semester])
        course = re.sub(r'_', r' ',file_folders[where_semester+2])
        intructor_first_name = file_folders[where_semester+3]
        intructor_first_name = intructor_first_name.strip()
        section_original = re.sub(r'_', r' ',file_folders[where_semester+4])
        section = section_original.split(' ')[1]
        mode_of_assignment = file_folders[where_semester+5]
        assignment = file_folders[where_semester+6]
        assignment = assignment.strip()
        draft = file_folders[where_semester+7]

        if len(draft) > 2 and draft[0] != 'D':
            print('***********************************************')
            print('Unable to find draft folder for this file: ')
            print(filename)
            print('***********************************************')
            found_all_metadata = False


        filtered_master1 = master[master['semester'] == semester]


        student_id = 0
        for index, row in filtered_master1.iterrows():
            this_row_filename = str(row['filename'])
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
            #print(file_folders)
            print('***********************************************')
            found_all_metadata = False

        if filtered_master2.shape[0] > 1:
            print('***********************************************')
            print('More than one row in metadata for this file: ')
            print(filename)
            print(student_name)
            #print(file_folders)
            print('***********************************************')
            found_all_metadata = False


        instructor_info = master_instructor[master_instructor['instructor'] == intructor_first_name]
        if instructor_info.empty:
            print('***********************************************')
            print('Unable to find instructor: ')
            print(filename)
            print(intructor_first_name)
            print('***********************************************')
            found_all_metadata = False

        master_assignment['Folder name'] = master_assignment['Folder name'].str.lower()
        assignment_info = master_assignment[master_assignment['Folder name'] == assignment.lower()]
        if assignment_info.empty:
            print('***********************************************')
            print('Unable to find assignment: ')
            print(filename)
            print(assignment)
            print('***********************************************')
            found_all_metadata = False

        if found_all_metadata:
            print('Adding headers to file ' + filename)
            textfile = open(filename, 'r')

            year_in_school = filtered_master2['year'].to_string(index=False)
            year_in_school = year_in_school.strip()
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

            institution = filtered_master2['institution'].to_string(index=False)
            institution = institution.strip()
            institution_code = re.sub(r'[a-z\s]', r'',institution)

            language_code = ''
            first_languages = filtered_master2['native_languages'].to_string(index=False)
            first_languages = first_languages.strip()
            first_languages = re.sub(r'^NaN$', r'NA', first_languages)

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
            elif 'Russian' in first_languages:
                language_code = 'RUS'
            elif 'Bulgarian' in first_languages:
                language_code = 'BUL'
            elif 'Uzbek' in first_languages:
                language_code = 'UZB'
            else:
                language_code = 'NAN'

            heritage_target_language = filtered_master2['heritage'].to_string(index=False)
            heritage_code = '0'
            heritage_header = 'No'

            if heritage_target_language == '1.0' or heritage_target_language == 'TRUE':
                heritage_code = '1'
                heritage_header = 'Yes'

            assignment_code = assignment_info['Assignment Code'].to_string(index=False)
            assignment_code = assignment_code.strip()
            assignment_code = re.sub(r'^NaN$', r'NA', assignment_code)

            str_student_id = str(student_id)
            str_student_id = re.sub(r'\.0',r'',str_student_id)

            new_course = re.sub(r'\s+', r'_', course)

            #course assignment draft country yearinschool gender studentID institution '.txt'
            output_filename = ''
            output_filename += new_course
            output_filename += '_'
            output_filename += language_code
            output_filename += '_'
            output_filename += heritage_code
            output_filename += '_'
            output_filename += assignment_code
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
                #print(path + output_filename)

                # look for course units info
                if args.master_course_file:
                    if '.xls' in args.master_course_file:
                        master_course_file = pandas.ExcelFile(args.master_course_file)
                        master_course_data = pandas.read_excel(master_course_file)
                    elif '.csv' in args.master_instructor_file:
                        master_course_data = pandas.read_csv(args.master_course_file)
                    course_info = master_course_data[master_course_data['course'] == course]
                    course_units = course_info['credit hours'].to_string(index=False)
                else:
                    course_units = filtered_master2['credit hours'].to_string(index=False)

                course_units = course_units.strip()
                course_units = re.sub(r'^NaN$', r'NA', course_units)

                semester_season = semester.split()[0]
                semester_year = semester.split()[1]

                major = filtered_master2['major'].to_string(index=False)
                major = major.strip()
                major = re.sub(r'^NaN$', r'NA', major)

                minor = filtered_master2['minor'].to_string(index=False)
                minor = minor.strip()
                minor = re.sub(r'^NaN$', r'NA', minor)
                minor = re.sub(r'^-$', r'NA', minor)

                mode_of_course = filtered_master2['mode_of_course'].to_string(index=False)
                mode_of_course = mode_of_course.strip()

                length_of_course = filtered_master2['length_of_course'].to_string(index=False)
                length_of_course = length_of_course.strip()

                additional_languages = filtered_master2['aditional_languages'].to_string(index=False)
                additional_languages = additional_languages.strip()
                additional_languages = re.sub(r'^NaN$', r'NA', additional_languages)

                instructor_code = instructor_info['instructor_code'].to_string(index=False)
                instructor_code = instructor_code.strip()
                instructor_code = re.sub(r'^NaN$', r'NA', instructor_code)

                current_courses = filtered_master2['courses_taking'].to_string(index=False)
                current_courses = current_courses.strip()
                current_courses = re.sub(r'^NaN$', r'NA', current_courses)

                previous_courses = filtered_master2['previous_courses'].to_string(index=False)
                previous_courses = previous_courses.strip()
                previous_courses = re.sub(r'^NaN$', r'NA', previous_courses)

                age = filtered_master2['age'].to_string(index=False)
                age = age.strip()
                age = re.sub(r'^NaN$', r'NA', age)

                began_target_language = filtered_master2['began_target_language'].to_string(index=False)
                began_target_language = began_target_language.strip()
                began_target_language = re.sub(r'^NaN$', r'NA', began_target_language)

                profiency_exam = filtered_master2['profiency_exam'].to_string(index=False)
                profiency_exam = profiency_exam.strip()
                profiency_exam = re.sub(r'^NaN$', r'NA', profiency_exam)

                exam_scores = filtered_master2['exam_scores'].to_string(index=False)
                exam_scores = exam_scores.strip()
                exam_scores = re.sub(r'^NaN$', r'NA', exam_scores)

                experience_abroad = filtered_master2['experience_abroad'].to_string(index=False)
                experience_abroad = experience_abroad.strip()
                experience_abroad = re.sub(r'^NaN$', r'NA', experience_abroad)

                other_experience = filtered_master2['other_experience'].to_string(index=False)
                other_experience = other_experience.strip()
                other_experience = re.sub(r'^NaN$', r'NA', other_experience)

                # write headers
                print('<Target Language: ' + target_language + '>', file = output_file)
                print('<Course: ' + course + '>', file = output_file)
                print('<L1: ' + first_languages + '>', file = output_file)
                print('<Other Languages: ' + additional_languages + '>', file = output_file)
                #print('<Macro Genre: ' + macro_genre + '>', file = output_file)
                #print('<Assignment Topic: ' + assignment_topic + '>', file = output_file)
                print('<Assignment Name: ' + assignment + '>', file = output_file)
                print('<Assignment Code: ' + assignment_code + '>', file = output_file)
                print('<Draft: ' + draft + '>', file = output_file)
                print('<Student ID: ' + str_student_id + '>', file = output_file)
                print('<Institution: ' + institution + '>', file = output_file)
                print('<Mode of Course: ' + mode_of_course + '>', file = output_file)
                print('<Length of Course: ' + length_of_course + '>', file = output_file)
                print('<Credit Hours: ' + course_units + '>', file = output_file)
                print('<Course Year: ' + semester_year + '>', file = output_file)
                print('<Course Semester: ' + semester_season+ '>', file = output_file)
                print('<Instructor: ' + instructor_code + '>', file = output_file)
                print('<Section: ' + section + '>', file = output_file)
                print('<Heritage of Target Language: ' +
                                   heritage_header + '>', file = output_file)
                print('<Proficiency Exam: ' + profiency_exam + '>', file = output_file)
                print('<Proficiency Exam Score: ' + exam_scores + '>', file = output_file)
                print('<Experience Abroad: ' + experience_abroad + '>', file = output_file)
                print('<Out-of-class Target Language Practice: ' +
                                   other_experience + '>', file = output_file)
                print('<Began Formal Education in the Target Language: ' + began_target_language + '>', file = output_file)
                print('<Courses Currently Enrolled: ' +
                                    current_courses + '>', file = output_file)
                print('<Courses Previously Enrolled: '+
                                    previous_courses +'>', file = output_file)
                print('<Age: ' + age + '>', file = output_file)
                print('<Year in School: ' + year_in_school_numeric + '>', file = output_file)
                print('<Major: ' + major + '>', file = output_file)
                print('<Minor: ' + minor + '>', file = output_file)
                print("<End Header>", file = output_file)
                print("", file = output_file)

                contents = textfile.read()
                print(contents, file = output_file)


                output_file.close()
            textfile.close()
    return(found_text_files)


def add_headers_recursive(directory, master, master_instructor, master_assignment, overwrite=False):
    found_text_files = False
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            is_this_a_text_file = add_header_to_file(os.path.join(dirpath, name), master, master_instructor, master_assignment, overwrite)
            if is_this_a_text_file:
                found_text_files = True
    if not found_text_files:
        print('No text files found in the directory.')


if args.master_file and args.dir and args.master_instructor_file and args.master_assignment_file:
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

    if '.xls' in args.master_assignment_file:
        master_assignment_file = pandas.ExcelFile(args.master_assignment_file)
        master_assignment_data = pandas.read_excel(master_assignment_file)
    elif '.csv' in args.master_assignment_file:
        master_assignment_data = pandas.read_csv(args.master_assignment_file)

    add_headers_recursive(args.dir, master_data, master_instructor_data, master_assignment_data, args.overwrite)
else:
    print('You need to supply a valid master file, a directory with textfiles, a master instructor file, and a master assignment file')
