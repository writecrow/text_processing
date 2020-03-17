#!/usr/bin/env python
import argparse
import sys
import re
import os
import pandas

"""<Student ID: #####>
<Country: CHN>
<Language: >
<Institution: Northern Arizona University>
<Course: ENGL 105>
<Mode: Face to Face>
<Length: 16 weeks>
<Assignment: AA>
<Draft: F>
<Course Year: 2016>
<Course Semester: Fall>
<Instructor: 3###>
<End Header>"""



# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()

def process_file(filename):

    if ".txt" in filename:
        # current directory: Users/adriana
        # directory=FACE/my_files/
        # filename: Users/adriana/Desktop/FACE/my_files/textfile1.txt
         # ['Users/adriana/Desktop/FACE/my_files/', 'textfile1.txt']
        filename_clean = os.path.split(filename)
        filename_part2 = filename_clean[1].strip(".txt")
        print(filename_part2)
        
        filename_parts = filename_part2.split('_')
        english_file = False
        
        if len(filename_parts) > 2:
            english_file = True
            
        else:
            
        
        assignment = filename_part2.split("_")[1]
        shortened_filename = filename_part2.split("_")[0]

        #assignment = re.sub(r"LA", r"Long Argument", assignment)
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

        student_ID = shortened_filename[-1]
        
        if shortened_filename[-2].isdigit():
            student_ID = shortened_filename[-2] + shortened_filename[-1]
        else:
            pass
            #student_ID = shortened_filename[-1]
        print("Student ID: ", student_ID)
        
        course_name = '105'

        textfile = open(filename, 'r')

        output_filename = ''
        output_filename += course_name
        output_filename += '_'
        output_filename += assignment
        output_filename += '_'
        output_filename += "DF"
        output_filename += '_'
        output_filename += "NA"
        output_filename += '_'
        output_filename += "NA"
        output_filename += '_'
        output_filename += "NA"
        output_filename += '_'
        output_filename += instructor
        output_filename += student_ID
        output_filename += semester0
        output_filename += '_'
        output_filename += "NAU"
        output_filename += '.txt'
        #output_filename = re.sub(r'\s', r'', output_filename)
        #output_filename = re.sub(r'__', r'_NA_', output_filename)

        old_folder = filename_clean[1]
        new_folder = "files_with_headers"
        path = os.path.join(cwd, new_folder, course_name, 'English', )

        if not os.path.exists(path):
            os.makedirs(path)

        output_file = open(path + output_filename, 'w')

        print("<Student ID: " + student_ID + ">", file = output_file)
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
    for filename in os.listdir(directory_name):
        # get relative path from home
        cwd = os.getcwd()
        process_file(os.path.join(cwd, directory_name, filename))

process_directory(args.dir)
