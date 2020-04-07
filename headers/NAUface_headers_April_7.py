#!/usr/bin/env python
import argparse
import sys
import re
import os
import pandas


# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()

student_ids_dictionary = {}

def add_id_to_dictionary(my_dictionary, my_key):
    # function to add default value if key not in dictionary
    # create a default value, which depends on how many keys are already in the dictionary
    default_value = 10000 + len(my_dictionary)
    # "create" the entry for that key, if the key exists, it assigns the current value of that key to the key
    # if the key doesn't exist, it assigns the default_value to the key (which was not in the dictionary)
    my_dictionary[my_key] = my_dictionary.get(my_key, default_value)

    # return the changed dictionary
    return(my_dictionary)

def process_file(filename):
    print(filename)

    if ".txt" in filename:
                # filename: Users/adriana/Desktop/FACE/my_files/textfile1.txt
         # ['Users/adriana/Desktop/FACE/my_files/', 'textfile1.txt']
        filename_clean = os.path.split(filename)
        filename_part2 = filename_clean[1].strip(".txt")
        print(filename_part2)

        filename_parts = filename_part2.split('_')
        course_name = '105'

        print(filename_parts)

    # if it is an english file (With length of 3)
        if len(filename_parts) > 2:
            assignment_code = filename_part2.split("_")[0]
            print(assignment_code)
            student_ID = filename_part2.split("_")[2]

            assignment = re.sub(r"LA", r"Long Argument", assignment_code)
            print("Assignment: ", assignment)

            instructor = "NA"
            print("Instructor's name: ", instructor)

            semester = "NA"
            print("Semester: ", semester)

            year = "NA"
            print("Year: ", year)

            add_id_to_dictionary(student_ids_dictionary, student_ID)
            # print(student_ids_dictionary)

            crow_id = student_ids_dictionary[student_ID]
            print("crow ID: ", crow_id)

            language = "English"
            print("Language: ", language)


        else:
            assignment_code = filename_part2.split("_")[1]
            shortened_filename = filename_part2.split("_")[0]
            print(shortened_filename)

            assignment = re.sub(r"LA", r"Long Argument", assignment_code)
            print("Assignment: ", assignment)

            instructor = filename_part2[:2]
            print("Instructor's name: ", instructor)

            semester0 = filename_part2[2]
            semester = re.sub(r"F", r"Fall", semester0)
            semester = re.sub(r"S", r"Spring", semester0)
            print("Semester: ", semester)

            year = filename_part2[3:5]
            year = re.sub(r"11", r"2011", year)
            year = re.sub(r"12", r"2012", year)
            print("Year: ", year)

            language = filename_part2[5]
            language = re.sub(r"A", r"Arabic", language)
            print("Language: ", language)

            student_ID = shortened_filename[-1]+instructor+semester0
            if shortened_filename[-2].isdigit():
                student_ID = shortened_filename[-2] + shortened_filename[-1]+instructor+semester0
            else:
                pass
            print("Student_id:",student_ID)

            # add student_ID to dictionary of ids if not there already
            add_id_to_dictionary(student_ids_dictionary, student_ID)
            print(student_ids_dictionary)

            crow_id = student_ids_dictionary[student_ID]

            print("Student ID: ",crow_id)


        textfile = open(filename, 'r')

        output_filename = ''
        output_filename += course_name
        output_filename += '_'
        output_filename += assignment_code
        output_filename += '_'
        output_filename += "DF"
        output_filename += '_'
        output_filename += "NA"
        output_filename += '_'
        output_filename += "NA"
        output_filename += '_'
        output_filename += "NA"
        output_filename += '_'
        output_filename += str(crow_id)
        output_filename += '_'
        output_filename += "NAU"
        output_filename += '.txt'
        #output_filename = re.sub(r'\s', r'', output_filename)
        #output_filename = re.sub(r'__', r'_NA_', output_filename)

        old_folder = filename_clean[1]
        new_folder = "files_with_headers"
        cwd = os.getcwd()
        path = os.path.join(cwd, new_folder, course_name, language)
        print('New path: ', path)

        if not os.path.exists(path):
            os.makedirs(path)

        output_file = open(os.path.join(path, output_filename), 'w')

        print("<Student ID: " + str(crow_id) + ">", file = output_file)
        print("<Country: " + "NA" + ">", file = output_file)
        print("<Institution: " + "NAU" + ">", file = output_file)
        print("<Course: ENGL " + "NA" + ">", file = output_file)
        print("<Mode: " + "Face to Face" + ">", file = output_file)
        print("<Length: " + "16 weeks" + ">", file = output_file)
        print("<Assignment: " + assignment + ">", file = output_file)
        print("<Draft: " + "DF" + ">", file = output_file)
        print("<Year in School: " + "NA" + ">", file = output_file)
        print("<Gender: " + "NA" + ">", file = output_file)
        print("<Course Year: " + year + ">", file = output_file)
        print("<Course Semester: " + semester + ">" , file = output_file)
        print("<College: " + "NA" + ">", file = output_file)
        print("<Program: " + "NA" + ">", file = output_file)
        print("<Proficiency Exam: " + "NA" +">", file = output_file)
        print("<Exam total: " + "NA" + ">", file = output_file)
        print("<Exam reading: " + "NA" + ">", file = output_file)
        print("<Exam listening: " + "NA" + ">", file = output_file)
        print("<Exam speaking: " + "NA" + ">", file = output_file)
        print("<Exam writing: " + "NA" + ">", file = output_file)
        print("<Instructor: " + instructor + ">", file = output_file)
        print("<Section: " + "NA" + ">", file = output_file)
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


def process_directory(directory_name):
    cwd = os.getcwd()
    for dirpath, dirnames, files in os.walk(directory_name):
        print(dirpath, dirnames, files)
        for filename in files:
            process_file(os.path.join(cwd, dirpath, filename))
        # get relative path from home


process_directory(args.dir)
