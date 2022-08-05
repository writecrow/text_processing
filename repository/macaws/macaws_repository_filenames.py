#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys  # imports the library for command line
import os  # imports the library for opening and writing files
from os.path import exists
from shutil import copyfile  # library for system operations

# Given a file located in a specific folder path,
# rename the file using the path elements
# The command syntax is as follows:
#   python macaws_repository_filenames.py path
# Example (with actual test folder)
#   python macaws_repository_filenames.py test_data/pre_finalized_filenames

## This number should be set to the *next*
counter = 1000
lang = "RSSS"
allowed_extensions = ['.pdf', '.docx']
cwd = os.getcwd()

institution = "UA"
separator = "_"

# Define the folder structure of this data set, working backward from the file.
# Original > semester_year > course > instructor number  > assignment code > material type
semester_year_level = -5
course_level = -4
instructor_level = -3
assignment_level = -2
material_level = -1

def splitall(path):
    """ Given a relative directory path, split out each directory into a list """
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

if __name__ == '__main__':  # iniitalizes the main block of code
    if len(sys.argv) <= 1:  # 1st element is script name and other elements follow
        print('You must supply a directory target')
        exit()
    for arg in sys.argv[1:]:  ## for every argument in the list of arguments
        for dirpath, dirnames, files in os.walk(arg):
            for name in files:        
                fullpath = os.path.join(dirpath, name)
                # print('Full path:', fullpath)
                # x = input('press enter to continue')
                if not os.path.isfile(fullpath):
                    sys.exit('No file found at', fullpath, '. Please try again.')
                ## Get the original filename
                filename = os.path.basename(name)
                filename_base, file_extension = os.path.splitext(filename)
                # print("Original file: ", file_extension)
                if file_extension not in allowed_extensions:
                    continue
                directory_parts = splitall(dirpath)
                # print(directory_parts)
                course = directory_parts[course_level]
                sem_year = directory_parts[semester_year_level]
                term = sem_year.split('_')
                semester = term[0]
                year = term[1]
                instructor = directory_parts[instructor_level]
                assignment = directory_parts[assignment_level]
                if assignment != "NA":
                    assignment = assignment.zfill(4)
                # Establish multi-assignment syntax.
                assignment.replace('_and_', ',')
                material = directory_parts[material_level]
                # print("Counter:", counter)
                # LANG_COURSE_ASSIGNMENT CODE_MATERIAL TYPE_UNIQUE FILE ID_INSTITUTION
                new_filename = separator.join([lang, course, assignment , material, str(counter), institution]) + str(file_extension)
                # print("new filename: ", new_filename)
                # x = input('press enter to continue')
                newpath = os.path.join(cwd, 'pdfs_with_filenames', sem_year, 'RSSS ' + course, material)
                os.makedirs(newpath, exist_ok=True)
                # print("new path: ", newpath)
                #x = input('press enter to continue')
                ## Defines new file, with same folder location
                output_file = os.path.join(newpath, new_filename)
                ## Copies the original file to the newly named file
                if (exists(output_file)):
                    print('File with filename ' + output_file + ' already exists.')
                    exit()
                copyfile(fullpath, output_file)
                print('Created ' + output_file)
                counter = counter + 1
