#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys  # imports the library for command line
import re  # imports the library for regular expressions
import glob  # imports the library for seeing all files
import os  # imports the library for opening and writing files
from shutil import copyfile  # library for system operations

# Given a file located in a specific folder path,
# rename the file using the instructor ID and other elements
# The command syntax is as follows:
# python convert_filename.py <course-number>/<firstname lastname>/<assignment>/<file-name>.<extension>
# Example (with actual test file)
# python convert_filename.py 101/Mark\ Fullmer/Narrative/test\ file.pdf
# will rename the file to: headers/ENGL 2001/Narrative/2001_Narrative_901_UA.pdf

# The CSV file for getting instructor ID is defined, relative to:
csv_filename = "instructors.csv"

# Auto-increment starting point
counter = 900

# function that gets a list with all names in the csv file
# and returns a list with unique names (it eliminated repeated names)


def get_unique_names(list):
    new_list = []  # create new empty list
    for element in list:
        if element not in new_list:
            new_list.append(element)  # add elements that are not in the new list yet
    return new_list

if __name__ == '__main__':  # iniitalizes the main block of code
    if len(sys.argv) > 1:  # 1st element is script name and other elements follow
        if not os.path.isfile(csv_filename):
            sys.exit('No CSV file found. Exiting...')
        # open csv file first, to create hash table/dictionary
        csv_file = open(csv_filename, 'r')  # opens the file as read only (w is write)
        csvhash = {}
        for line in csv_file:  # for every line in the file; can be used for lists as well; can also use counter if you want
            print(line)  # print the lines in the file
            x = input('press enter to continue')
            cleanline = re.sub('\r?\n', '', line)
            elements_of_line = cleanline.split(',')  # splits on comma (columns in csv file)
            print(elements_of_line)
            x = input('press enter to continue')
            # create a new list for all names in the csv files
            all_names = []  # create empty list
            all_names.append(elements_of_line[1])  # add first name
            all_names.append(elements_of_line[2])  # add last name
            csvhash[elements_of_line[1] + ' ' + elements_of_line[2]] = {"ID": elements_of_line[0]}

        for arg in sys.argv[1:]:  # for every argument in the list of arguments
            if not os.path.isfile(arg):
                sys.exit('No file found at', arg, '. Please try again.')

            # Get the original filename
            filename = os.path.basename(arg)
            print("Original file: ", filename)
            directory = os.path.dirname(arg)
            print("Original path: ", directory)
            filename_base, file_extension = os.path.splitext(filename)
            print('File extension:', file_extension)
            x = input('press enter to continue')
            directory_parts = arg.split('/')
            print(directory_parts)
            x = input('press enter to continue')
            name = directory_parts[1].split(' ')
            print("Name Components: ", name)
            x = input('press enter to continue')
            # The course number must be the first-level directory
            course_number = directory_parts[0]
            print("Course Number", course_number)
            x = input('press enter to continue')
            # Instructor must be the second-level directory
            instr_name = directory_parts[1]
            print("Instructor's name: ", instr_name)
            x = input('press enter to continue')
            # Assignment must be the third-level directory
            assignment = directory_parts[2]
            print("Assignment:", assignment)
            x = input('press enter to continue')
            name_one = name[0]
            name_two = name[1]
            print("Instructor Key: ", name_one + " " + name_two)
            x = input('press enter to continue')
            key_one = name_one + " " + name_two
            counter = counter + 1
            print("Counter:", counter)
            x = input('press enter to continue')
            for element in csvhash:
                if instr_name == element:
                    new_filename = (csvhash[key_one]["ID"] + '_' + assignment + '_' + str(counter) + '_UA' + str(file_extension))
                    print("new filename: ", new_filename)
                    x = input('press enter to continue')
                    path = "headers/ENGL " + csvhash[key_one]['ID'] + "/" + assignment + "/"
                    print("new path: ", path)
                    x = input('press enter to continue')
                    if not os.path.exists(path):
                        os.makedirs(path)
                    # Defines new file, with same folder location
                    output_file = os.path.join(path, new_filename)
                    # Moves the original file to the newly named file
                    copyfile(arg, output_file)
