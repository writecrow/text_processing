#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys #imports the library for command line
import re #imports the library for regular expressions
import glob #imports the library for seeing all files
import os #imports the library for opening and writing files

# to run this:
# python python_headers.py files/**/*.txt

# function that gets a list with all names in the csv file
# and returns a list with unique names (it eliminated repeated names)
def get_unique_names(list):
    new_list = [] # create new empty list
    for element in list: 
        if element not in new_list:
            new_list.append(element) # add elements that are not in the new list yet
    return new_list

if __name__ == '__main__': #iniitalizes the main block of code
    if len(sys.argv) > 1: #1st element is script name and other elements follow
        # open csv file first, to creat hash table/dictionary
        csv_filename = "test.csv" 
        csv_file = open(csv_filename,'r') #opens the file as read only (w is write)
        csvhash = {}
        for line in csv_file: #for every line in the file; can be used for lists as well; can also use counter if you want
            #print(line)#print the lines in the file
            #x = raw_input('press enter to continue')
            cleanline = re.sub('\r?\n', '', line)         
            elements_of_line = cleanline.split(',')#splits on comma (columns in csv file)
            #print(elements_of_line)
            #x = input('press enter to continue')

            # create a new list for all names in the csv files
            all_names = [] # create empty list
            all_names.append(elements_of_line[16]) # add first name
            all_names.append(elements_of_line[17]) # add last name
            
            csvhash[elements_of_line[16]+' '+elements_of_line[17]] = {'course':elements_of_line[0], 'section':elements_of_line[1], 
            'year in school':elements_of_line[4], 'school':elements_of_line[5], 'major':elements_of_line[6], 'country':elements_of_line[7], 
            'gender':elements_of_line[8], 'TOEFL total':elements_of_line[9], 'TOEFL listening':elements_of_line[10], 'TOEFL reading':elements_of_line[11], 
            'TOEFL writing':elements_of_line[12], 'TOEFL speaking':elements_of_line[13], 'student ID':elements_of_line[14], 
            'instructor ID':elements_of_line[15], 'semester':elements_of_line[18], 'year':elements_of_line[19]}
        #for element in csvhash: 
         #   print(element, csvhash[element])
        #x = input('press enter to continue')

            
        for arg in sys.argv[1:]: #for every argument in the list of arguments
           
            # for every file entered as argument in the command line
            for file in glob.iglob(arg): #extra line for windows--> whenever *.txt for example is used, this tells the script to read as a list of files
                # open the file as read-only ('r')
                with open(file, 'r') as f: #opens file and names it 'f'
                    try:
                        # get the file name
                        print("original filename: ", f.name)#print filename
                        x = raw_input('press enter to continue')
                        txt_filename = f.name
                        txt_filename = re.sub('\.txt', '', txt_filename)
                        #print(txt_filename)#print filename
                        #x = input('press enter to continue')
                        txt_filename_parts = txt_filename.split('/')#splits filename by directory
                        #print("original filename: ", txt_filename_parts)
                        
                        #x = raw_input('press enter to continue')
                        txt_filename_parts = txt_filename_parts[2].split(' ')
                        print("original filename: ", txt_filename_parts)
                        x = raw_input('press enter to continue')
                        assignment_draft = txt_filename_parts[0]
                        print("assignment and draft", assignment_draft)
                        x = raw_input('press enter to continue')
                        assignment = assignment_draft[0:2]
                        print("assignment: ", assignment)
                        x = raw_input('press enter to continue')
                        draft = assignment_draft[3:4]
                        print("draft: ", draft)
                        x = raw_input('press enter to continue')
                        name_one = txt_filename_parts[2]
                        name_two = txt_filename_parts[3]
                        print("key: ", name_one + " " + name_two)
                        x = raw_input('press enter to continue')
                        key_one = name_one + " " + name_two
                        key_two = name_two + " " + name_one
                        for element in csvhash:
                            if key_one == element:
                                new_filename = (csvhash[key_one]['course'] + '_' + assignment + '_' + draft + 
                                '_' + csvhash[key_one]['country'] + '_' + csvhash[key_one]['year in school'] + '_' + csvhash[key_one]['gender'] + '_' + csvhash[key_one]['student ID'] + '_' + 'UA' + '.txt') #creates file name
                                print("new filename: ", new_filename)
                                x = raw_input('press enter to continue')
                                path = "headers/ENGL " + csvhash[key_one]['course'] + "/" + assignment + "/D" + draft + "/"
                                print("new path: ", path)
                                x = raw_input('press enter to continue')
                                if not os.path.exists(path):
                                    os.makedirs(path)
                                new_file = open(path + new_filename, "w")
                                #x = raw_input('press enter to continue')
                                new_file.write("<ID: " + csvhash[key_one]['student ID'] + ">" + "\r\n")
                                #print("<ID: " + csvhash[key_one]['student ID'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Country: " + csvhash[key_one]['country'] + ">" + "\r\n")
                                #print("<Country: " + csvhash[key_one]['country'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Institution: University of Arizona>" + "\r\n")
                                #print("<Institution: University of Arizona>")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Course: " + csvhash[key_one]['course'] + ">" + "\r\n")
                                #print("<Course: " + csvhash[key_one]['course'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Assignment: " + assignment + ">" + "\r\n")
                                #print("<Assignment: " + assignment + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Draft: " + draft + ">" + "\r\n")
                                #print("<Draft: " + draft + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Year in School: " + csvhash[key_one]['year in school'] + ">" + "\r\n")
                                #print("<Year in School: " + csvhash[key_one]['year in school'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Gender: " + csvhash[key_one]['gender'] + ">" + "\r\n")
                                #print("<Gender: " + csvhash[key_one]['gender'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Year writing: " + csvhash[key_one]['year'] + ">" + "\r\n")
                                #print("<Year writing: " + csvhash[key_one]['year'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Semester writing: " + csvhash[key_one]['semester'] + ">" + "\r\n")
                                #print("<Semester writing: " + csvhash[key_one]['semester'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<College: " + csvhash[key_one]['school'] + ">" + "\r\n")
                                #print("<College: " + csvhash[key_one]['school'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Program: " + csvhash[key_one]['major'] + ">" + "\r\n")
                                #print("<Program: " + csvhash[key_one]['major'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<TOEFL total: " + csvhash[key_one]['TOEFL total'] + ">" + "\r\n")
                                #print("<TOEFL total: " + csvhash[key_one]['TOEFL total'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<TOEFL reading: " + csvhash[key_one]['TOEFL reading'] + ">" + "\r\n")
                                #print("<TOEFL reading: " + csvhash[key_one]['TOEFL reading'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<TOEFL listening: " + csvhash[key_one]['TOEFL listening'] + ">" + "\r\n")
                                #print("<TOEFL listening: " + csvhash[key_one]['TOEFL listening'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<TOEFL speaking: " + csvhash[key_one]['TOEFL speaking'] + ">" + "\r\n")
                                #print("<TOEFL speaking: " + csvhash[key_one]['TOEFL speaking'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<TOEFL writing: " + csvhash[key_one]['TOEFL writing'] + ">" + "\r\n")
                                #print("<TOEFL writing: " + csvhash[key_one]['TOEFL writing'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<Instructor: " + csvhash[key_one]['instructor ID'] + ">" + "\r\n")
                                #print("<Instructor: " + csvhash[key_one]['instructor ID'] + ">")
                                #x = raw_input('press enter to continue')
                                new_file.write("<End Header>\r\n\r\n")
                                #print("<End Header>\r\n")
                                for line in f:
                                    if line != '\r\n':
                                        new_file.write(line)
                                new_file.close()
                    except:
                        print(f.name + "\t" + str(sys.exc_info()[0]) + "\t" + str(sys.exc_info()[1]))#prints file name and errors in case the file doesn't open.
                        #x = raw_input('press enter to continue')
                        
