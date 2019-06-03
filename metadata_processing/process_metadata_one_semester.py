#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file or files passed as arguments to the script,
# create one csv file with all tabs for instructors in the original spreadsheet
# The original spreadsheet needs a master tab, which is the first tab in
# the original excel file.
#
# Usage example:
#    python process_metadata_one_semester.py --file=myfile.xlsx
#    python process_metadata_one_semester.py --directory=Spring2018
#
# A new csv file with a similar name to the original spreadsheet
# will be created.


import argparse
import sys
import re
import os
import codecs
import pandas

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Excel to CSV')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--file', action="store", dest='file', default='')
args = parser.parse_args()

def combine_tabs(filename):
    data = pandas.ExcelFile(filename)
    tabs = data.sheet_names
    mastertab = pandas.read_excel(data, 0)
    #print(mastertab.head())
    frames = []
    output_filename = re.sub(r'.+\/|.+\\|\.xlsx?', r'', filename)
    output_filename += '_processed.csv'

    # comment: get each tab in the excel file
    for i in range(1,len(tabs)):
        studentid = []
        tab = tabs[i]
        print("Getting data from " + tab + " tab.")
        this_tab = pandas.read_excel(data, tab)
        #print(this_tab)
        # comment: add the tab name as a new column in the data
        this_tab["source"] = tab
        #print(this_tab)
        #print(this_tab.columns)
        # comment: add student ids to list of studdent ids
        for element in this_tab["ID"].tolist():
            studentid.append(element)
        #print("instructor tab: ", len(studentid))

        # comment: get the same students from the master tab
        filterid = mastertab.loc[mastertab["ID"].isin(studentid)]
        #print(filterid["ID"])
        #print (len(studentid[,]))
        #print ("mastertab: ", len (filterid["ID"].tolist()))

        # comment: make sure tab and master are the same
        if len(studentid) == len(filterid["ID"].tolist()):
            #print("they are the same")
            # comment: add this tab to frames list to combine data
            frames.append(this_tab)
        else:
            print("There's a mismatch between instructor tab and master tab")

    # comment: combine all data
    combined_data = pandas.concat(frames)
    #print(combined_data)

    # comment: get list of student IDs
    allstudents = combined_data["ID"].unique()
    print("There are " + str(len(allstudents)) + " students to process.")
    new_frames = []
    # comment: for every student id
    for student in allstudents:
        print("Checking student rows.")
        this_student_data = combined_data.loc[combined_data["ID"] == student]
        #print(this_student_data)
        #print("*****")
        #print(len(this_student_data))
        if len(this_student_data) > 1:
            major = ""
            college = ""
            for index,row in this_student_data.iterrows():
                major += row["Major"] + "; "
                college += row["College"] + "; "
                #print(row)
                #print(row["Major"])
            new_row = this_student_data.iloc[[0]]
            new_row["Major"] = major[:-2].replace(",", " ")
            new_row["College"] = college[:-2].replace(",", " ")

        else:
            new_row = this_student_data.iloc[[0]]
            new_row["Major"] = new_row["Major"].replace(",", " ")
            new_row["College"] = new_row["College"].replace(",", " ")
        #print (new_row)
        new_frames.append(new_row)

    new_combined_data = pandas.concat(new_frames)
    new_combined_data.to_csv(output_filename)

def combine_recursive(directory):
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            combine_tabs(os.path.join(dirpath, name))

if args.dir and os.path.isdir(args.dir):
    combine_recursive(args.dir)
elif args.file and os.path.isfile(args.file):
    combine_tabs(args.file)
else:
    print('You need to supply a valid directory or filename')
