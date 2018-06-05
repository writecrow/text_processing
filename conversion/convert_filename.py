#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys #imports the library for command line
import re #imports the library for regular expressions
import glob #imports the library for seeing all files
import os #imports the library for opening and writing files

# to run this:
# python rep.py 101/**/**/**.**

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
        csv_filename = "rep.csv" 
        csv_file = open(csv_filename,'r') #opens the file as read only (w is write)
        csvhash = {}
        for line in csv_file: #for every line in the file; can be used for lists as well; can also use counter if you want
            print(line)#print the lines in the file
            x = input('press enter to continue')
            cleanline = re.sub('\r?\n', '', line)         
            elements_of_line = cleanline.split(',')#splits on comma (columns in csv file)
            print(elements_of_line)
            x = input('press enter to continue')
            # create a new list for all names in the csv files
            all_names = [] # create empty list
            all_names.append(elements_of_line[1]) # add first name
            all_names.append(elements_of_line[2]) # add last name
            
            csvhash[elements_of_line[1]+' '+elements_of_line[2]] = {"ID": elements_of_line[0]}

        counter=900
        for arg in sys.argv[1:]: #for every argument in the list of arguments
            
           
            # for every file entered as argument in the command line
            
            for file in glob.iglob(arg):
            
    
               
                with open(file, 'r') as f: #opens file and names it 'f'
                    #i=1
                    #for i in range(len(sys.argv)):
                        #i+=1
                     
                        try:
                    
                        # get the file name
                    

                            print("original filename: ", f.name)#print filename
                           
                            x = input('press enter to continue')
    
                            txt_filename = f.name
                            #txt_filename = re.sub('/.**', '', txt_filename)
                            #print(txt_filename)#print filename
                            #x = input('press enter to continue')
                            txt_filename_parts = txt_filename.split('/')
                            print(txt_filename_parts)
                        
                            #splits filename by directory
                            #print("original filename: ", txt_filename_parts)
                            x = input('press enter to continue')
                        
                            name = txt_filename_parts[1].split(' ')
                            print("name: ", name)
                            x = input('press enter to continue')
                            extension = txt_filename_parts[3].split(".")
                            print(extension)
                            end = extension[1]
                            course_number = txt_filename_parts[0]
                            print("course number", course_number)
                            x = input('press enter to continue')
                            instr_name = txt_filename_parts[1]
                            print("instructor's name: ", instr_name)
                            x = input('press enter to continue')
                            assignment= txt_filename_parts[2]
                            print("assignment: ", assignment)
                            x = input('press enter to continue')
                            name_one = name[0]
                            name_two = name[1]
                            print("key: ", name_one + " " + name_two)
                            x = input('press enter to continue')
                            key_one = name_one + " " + name_two
                            #key_two = name_two + " " + name_one
                            counter=counter+1
                            print("counter:",counter)
                            x= input("Press to continue")

                            new_filename = 'my_new_filename.txt'
                            output_directory = os.path.dirname(arg) # Gets the directory of the file passed as an argument
                            output_file = os.path.join(output_directory, new_filename) # Defines new file, with same folder location
                            os.rename(arg, output_file) # Moves the original file to the newly named file

                            for element in csvhash:
                                if instr_name == element:
                                    #new_filename = (csvhash[key_one]["ID"] + '_' + assignment +'_'+str(counter)+"_" 'UA'+ "."+str(end)) #creates file nam
                                    print("new filename: ", new_filename)
                                    x = input('press enter to continue')
                                    path = "headers/ENGL " + csvhash[key_one]['ID'] + "/" + assignment + "/"
                                    print("new path: ", path)
                                    x = input('press enter to continue')
                                    if not os.path.exists(path):
                                        os.makedirs(path)
                                    new_file = open(path + new_filename, "w", encoding= "UTF-8")
                                  
                            for line in f:
                                if line != '\r\n':
                                    new_file.write(line)
                                    new_file.close()
                        except:
                            print(f.name + "\t" + str(sys.exc_info()[0]) + "\t" + str(sys.exc_info()[1]))#prints file name and errors in case the file doesn't open.
                        #x = raw_input('press enter to continue')
                        
