#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys  # imports the library for command line
import re  # imports the library for regular expressions
import glob  # imports the library for seeing all files
import os  # imports the library for opening and writing files
from shutil import copyfile  # library for system operations

# Given a file located in a specific folder path,
# rename the file using the path elements
# The command syntax is as follows:
# python repository_file_names.py path
# Example (with actual test folder)
# python repository_file_names.py 106i


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


## Auto-increment starting point
counter = 1249
if __name__ == '__main__':  # iniitalizes the main block of code
    if len(sys.argv) > 1:  # 1st element is script name and other elements follow
        for arg in sys.argv[1:]:  ## for every argument in the list of arguments
            for dirpath, dirnames, files in os.walk(arg):
                for name in files:        
                    fullpath = os.path.join(dirpath, name)
                    print('Full path:', fullpath)
                    x = input('press enter to continue')
                    if not os.path.isfile(fullpath):
                        sys.exit('No file found at', fullpath, '. Please try again.')
                        
                    ## Get the original filename
                    filename = os.path.basename(name)
                    print("Original file: ", filename)
                    if '.pdf' in filename:
                        directory = dirpath
                        print("Original path: ", dirpath)
                        filename_base, file_extension = os.path.splitext(filename)
                        print('File extension:', file_extension)
                        x = input('press enter to continue')
                        directory_parts = splitall(dirpath)
                        print(directory_parts)
                        x = input('press enter to continue')
                        print("Instructor number:", directory_parts[2])
                        x = input('press enter to continue')
                        ## The course number must be the first-level directory
                        course_number = directory_parts[0]
                        print("Course Number", course_number)
                        x = input('press enter to continue')
                        ## Term must be the second-level directory
                        term = directory_parts[1]
                        print("Term: ", term)
                        ## Instructor must be the third-level directory
                        instructor = directory_parts[2]
                        print("Instructor's number: ", instructor)
                        x = input('press enter to continue')
                        ## Assignment must be the fourth-level directory
                        assignment = directory_parts[3]
                        print("Assignment:", assignment)
                        x = input('press enter to continue')
                        pedmats = directory_parts[4]
                        print("Material Type:", pedmats)
                        x = input('press enter to continue')
                        topic = directory_parts[5]
                        print("Topic:", topic)
                        x = input('press enter to continue')

                        new_filename = (course_number + '_' + assignment + '_' + pedmats + '_' + str(counter) + '_UA' + str(file_extension))
                        print("new filename: ", new_filename)
                        x = input('press enter to continue')
                        
                        cwd = os.getcwd()
                        newpath = os.path.join(cwd, 'filenames', 'ENGL' + course_number, term, instructor, topic)
                        os.makedirs(newpath, exist_ok=True)
                        print("new path: ", newpath)
                        x = input('press enter to continue')
                        ## Defines new file, with same folder location
                        output_file = os.path.join(newpath, new_filename)
                        ## Moves the original file to the newly named file
                        copyfile(fullpath, output_file)
