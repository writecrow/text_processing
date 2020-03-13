#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file and text files passed as arguments to the script,
# metadata headers are added to each individual text files

# Windows run with Anaconda Prompt example:
# python add_headers.py --directory="Fall 2018/normalized/" --master_file="Metadata_Fall_2018_updated.csv"

import argparse
import csv
import pandas
import os
import re
from pandas import DataFrame

# define the way we retrive arguments sent to the script
parser = argparse.ArgumentParser(description='Add Headers to Individual Textfile')
parser.add_argument('--directory', action="store", dest='directory', default='')
parser.add_argument('--master_file', action="store", dest='master_file', default='')
parser.add_argument('--overwrite', action='store_true')
args = parser.parse_args()

#----------------------------------------------------------------------------------------------------------------------------------------
# function 1 is defined
def add_header_to_file(filename, master, overwrite=False): # filename = folder1.../Lan/Lan_p1d3/WA_Second Draft_lan12_attempt_2017-06-29_Lan Ge_WA Second.txt
    found_text_files = False
    if '.txt' in filename: #check the indent 
        found_text_files = True

        global career_account_list
        for career_account in career_account_list:
            #print("career_account is:", career_account)
            if re.search(career_account, filename):
                print('>>>>> matched: ', career_account, "is in", filename,'and adding headers...')
                #print('>>>>> add header to',filename)
                filtered_master = master[master['User_ID'] == career_account]
                #print(filtered_master)
                textfile = open(filename, 'r') 
                print(textfile.read())

    # check the ident of this line
    return(found_text_files)

#---------------------------------------------------------------------------------------------------------------------------------------
# function 2 is defined (master here is the master_data in the main program that has been excel_read())
def add_headers_recursive(directory, master, overwrite=False):
    found_text_files = False
    
    #dirpath = whole path without file's names (C:\folder1\folder2\folder3\)
    #files = file's name (p1d1.txt)
    #filename = os.path.join(dirpath,name) = whole path with file's name (C:\folder1\folder2\folder3\p1d1.txt)
    
    for dirpath, dirnames, files in os.walk(directory): 
        for name in files:
            #print(name) #this print file's name: WA_Second Draft_bai69_attempt_2017-06-19-01-07-23_Lu Bai_WA second.txt
            #print(os.path.join(dirpath, name)) #print file path and file's name: test\WA_Second Draft_bai69_attempt_2017-06-19-01-07-23_Lu Bai_WA second.txt
            # function 1 is called (with filename = os.path.join(dirpath,name), master, overwrite)
            is_this_a_text_file = add_header_to_file(os.path.join(dirpath, name), master, overwrite)
            if is_this_a_text_file:
                found_text_files = True
    if not found_text_files:
        print('No text files found in the directory.')

#---------------------------------------------------------------------------------------------------------------------------------------
# the main program starts here: 
if args.master_file and args.directory:
    if '.xlsx' in args.master_file:
        master_file = args.master_file
        master_data = pandas.read_excel(master_file)
        master_data_frame = pandas.DataFrame(master_data)
        
        #prepare a list with all career account name that will be used to map with the career account name in the files' names in the functions
        career_account_list = master_data_frame['User_ID'].tolist()
        #print(career_account_list)
    elif '.csv' in args.master_file:
        master_data = pandas.read_csv(args.master_file)
        master_data = pandas.read_excel(master_file)
        master_data_frame = pandas.DataFrame(master_file)
        
        #prepare a list with all career account name that will be used to map with the career account name in the files' names in the functions
        career_account_list = master_data_frame['User_ID'].tolist()
        #print(career_account_list) 
    # function 2 is called with three parameters: (1) directory (2) master_data (3)overwrite
    add_headers_recursive(args.directory, master_data, args.overwrite)
else:
    print('>>>>> Error report: provide a valid master_file and directory with student files.')


