#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import glob
import os
import codecs

institution_long = {'PRD':'Purdue University', 'UA':'University of Arizona'}
output_dir = 'output'

csv_filename = "instructors_Arizona.csv"

def get_unique_names(list):
    new_list = []  # create new empty list
    for element in list:
        if element not in new_list:
            new_list.append(element)  # add elements that are not in the new list yet
    return new_list

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

if __name__ == '__main__':
    if len(sys.argv) > 1:  # 1st element is script name and other elements follow
        if not os.path.isfile(csv_filename):
            sys.exit('No CSV file found. Exiting...')
        # open csv file first, to create hash table/dictionary
        csv_file = open(csv_filename, 'r')  # opens the file as read only (w is write)
        csvhash = {}
        for line in csv_file:  # for every line in the file; can be used for lists as well; can also use counter if you want
            #print(line)  # print the lines in the file
            #x = input('press enter to continue')
            cleanline = re.sub('\r?\n', '', line)
            elements_of_line = cleanline.split(',')  # splits on comma (columns in csv file)
            print(elements_of_line)
            #x = input('press enter to continue')
            # create a new list for all names in the csv files
            all_names = []  # create empty list
            all_names.append(elements_of_line[1])  # add first name
            all_names.append(elements_of_line[2])  # add last name
            csvhash[elements_of_line[2]] = {"ID": elements_of_line[0]}
            print(csvhash[elements_of_line[2]])
            x = input('press enter to continue')

        for argument in sys.argv[1:]:
            for file in glob.iglob(argument):
                if not os.path.isfile(file):
                    sys.exit('No file found at', file, '. Please try again.')
                with open(file, 'r') as f:
                    original_directory = os.path.dirname(file)
                    original_filename = os.path.basename(file)
                    filename_base, file_extension = os.path.splitext(
                        original_filename)
                    print('Full path:', file)
                    print("Original path: ", original_directory)
                    print("Original filename: ", filename_base)
                    print('File extension:', file_extension)
                    filename_parts = filename_base.split('_')
                    print("Filename parts: ", filename_parts)
                    institution = filename_parts[4]
                    print("Institution:", institution)
                    text_ID = filename_parts[3]
                    print("text ID:", text_ID)
                    ped_type = filename_parts[2]
                    print("material type:", ped_type)
                    assignment = filename_parts[1]
                    print("assignment:", assignment)
                    course = filename_parts[0]
                    print("course:", course)
                    #x = input('press enter to continue')
                    directory_parts = splitall(original_directory)
                    print(directory_parts)
                    # The term must be the second-level directory
                    term = directory_parts[1]
                    print("term:", term)
                    #x = input('press enter to continue')
                    split_term = term.split(" ")
                    semester = split_term[0]
                    print("semester:", semester)
                    #x = input('press enter to continue')
                    year = split_term[1]
                    print("year:", year)
                    #x = input('press enter to continue')
                    instr_name = directory_parts[2]
                    print("Instructor:", instr_name)
                    #x = input('press enter to continue')
                    topic = directory_parts[3]
                    print("Topic:", topic)
                    #x = input('press enter to continue')
                    #fullname_parts = directory_parts[2].split(' ')
                    #print("Name Components: ", fullname_parts)
                    #x = input('press enter to continue')
                   # name_one = fullname_parts[0]
                    name_two = directory_parts[2]
                    print("Instructor Key: ", name_two)
                    #x = input('press enter to continue')
                    key_one = name_two
                    for element in csvhash:
                        if instr_name == element:
                            output_file_name = filename_base + '.txt'
                            print("new file name:", output_file_name)
                            path = "headers/ENGL" + course + "/" + assignment + "/"
                            print("new path: ", path)
                            print ("Instructor name" + instr_name)
                            print ("Element:" + element)
                            if not os.path.exists(path):
                                os.makedirs(path)
                            output_file_location = os.path.join(path, output_file_name)
                            output_file = open(output_file_location, "w")
                            output_file.close()
                            # for each line in this file
                            text = '<Institution: ' + institution_long[institution] + '>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<Course Year: ' + year + '>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<Course Semester: ' + semester + '>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<Course: ENGL ' + course + '>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<Assignment: ' + assignment + '>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<Mode: Face to Face>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<Length: 16 weeks>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<Document Type: ' + ped_type + '>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<Topic: ' + topic + '>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<File ID: ' + text_ID + '>'
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<Instructor: ' + csvhash[instr_name]['ID'] + '>'
                            #this doesn't make sense to me since it will just be the last item in the hash.
                            print(text, file=open(output_file_location, mode="a"))
                            text = '<End Header>\r\n'
                            print(text, file=open(output_file_location, mode="a"))
                            for line in f:
                                do_print = True
                                # write our text in the file
                                if line == '\n':
                                    #print("Skipped line")
                                    do_print = False
                                if do_print:
                                    line = line[:-1]
                                    print(line, file=open(output_file_location, mode="a"))  