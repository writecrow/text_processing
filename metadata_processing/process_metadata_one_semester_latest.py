#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file or files passed as arguments to the script,
# create one csv file with all tabs for instructors in the original spreadsheet
# The original spreadsheet needs a master tab, which is the first tab in
# the original excel file.
#
# Usage example:
#    python process_metadata_one_semester.py --directory=../../../Metadata/Fall\ 2018/ --master_student_file=../../../Metadata/Master_Student_metadata_legacy.xlsx --instructor_codes_file=../../../Metadata/Instructor_Codes.xlsx
# The directory is where the multiple excel files are stored. 
# The master student file is the master spreadsheet with all metadata from previous semesters. 
# The instructor codes file is the spreadsheet where the instructor codes (and names) are stored.
# A new csv file with a similar name to the original spreadsheet
# will be created.


import argparse
import sys
import re
import os
import codecs
import pandas
import numpy

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Excel to CSV')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--file', action="store", dest='file', default='')
parser.add_argument('--master_student_file', action="store", dest='master_student', default='')
parser.add_argument('--instructor_codes_file', action="store", dest='instructor_codes', default='')
args = parser.parse_args()


def combine_tabs(filename):
    if '.xlsx' in filename or '.xls' in filename:
        print("Opening file " + filename)
        data = pandas.ExcelFile(filename)
        tabs = data.sheet_names
        mastertab = pandas.read_excel(data, 0)
        #print(mastertab.head())
        frames = []

        # comment: get each tab in the excel file
        for i in range(1,len(tabs)):
            studentid = []
            tab = tabs[i]
            print("Getting data from " + tab + " tab.")
            this_tab = pandas.read_excel(data, tab)
            print(this_tab.columns)
            # comment: add the tab name as a new column in the data
            this_tab["Instructor Last Name"] = tab
            #print(this_tab)
            #print(this_tab.columns)
            # comment: add student ids to list of studdent ids

            for element in this_tab["Registrar ID"].tolist():
                studentid.append(element)
            print("instructor tab: ", len(studentid))

            # comment: get the same students from the master tab

            filterid = mastertab.loc[mastertab["Registrar ID"].isin(studentid)]
            #print(filterid["ID"])
            #print (len(studentid[,]))
            #print ("mastertab: ", len (filterid["ID"].tolist()))

            # comment: make sure tab and master are the same
            if len(studentid) == len(filterid["Registrar ID"].tolist()):

                #print("they are the same")
                # comment: add this tab to frames list to combine data
                frames.append(this_tab)
            else:
                print("There's a mismatch between instructor tab and master tab")

        # comment: combine all data
        if len(frames) != 0:
            combined_data = pandas.concat(frames, sort=False)
            #print(combined_data)

            # comment: get list of student IDs
            allstudents = combined_data["Registrar ID"].unique()
            print("There are " + str(len(allstudents)) + " students to process.")
            new_frames = []
            # comment: for every student id
            for student in allstudents:
                print("Checking student rows.")

                this_student_data = combined_data.loc[combined_data["Registrar ID"] == student]

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
                new_frames.append(new_row)

            return(new_frames)

def combine_recursive(directory):
    all_frames = []
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            this_new_frame = combine_tabs(os.path.join(dirpath, name))
            if this_new_frame:
                all_frames += combine_tabs(os.path.join(dirpath, name))
    return(all_frames)

def process_new_data(output_frames, master_student_data, all_master, instructor_codes, output_filename):
    new_combined_data = pandas.concat(output_frames, sort=False)

    if len(output_frames) > 0:
        #print(master_student_data)
        # get last (highest) student code from master student file
        last_student_code = master_student_data['Crow ID'].max()
        last_section_code = master_student_data['Class Section'].max()

        # very important step, so student ID works
        new_combined_data = new_combined_data.reset_index(drop = True)
        # get first student ID we should use
        start = last_student_code+1
        # add Crow IDs to new dataframe
        new_combined_data['New Crow ID'] = new_combined_data.index + start
        
        new_combined_data2 = pandas.merge(new_combined_data, instructor_codes,
        on= 'Instructor Last Name', how='left')
        new_combined_data3 = pandas.merge(new_combined_data2, master_student_data,
        on='Registrar ID', how='left')
        new_combined_data3[['Crow ID']] = new_combined_data3[['Crow ID']].fillna(0)
        new_combined_data3[['Crow ID']] = new_combined_data3[['Crow ID']].astype(int)

        df = new_combined_data3
        print(df)
        df['Crow_ID'] = numpy.where(df['Crow ID']==0,  df['New Crow ID'], df['Crow ID'])

        # Delete the extra crow ID columns from the dataframe
        df = df.drop("New Crow ID", axis=1)
        df = df.drop("Crow ID", axis=1)
        df = df.rename(index=str, columns={'Crow_ID': 'Crow ID'})

        df = df.drop_duplicates()

        df['course_section'] = df['Catalog Nbr'].astype(str) + df['Class Section_x'].astype(str)

        print(df['course_section'])
        
        section_dictionary = {}
        
        for item in df['course_section']:
            if item not in section_dictionary:
                section_dictionary[item] = last_section_code +1
                last_section_code +=1

        print(section_dictionary)
        df = df.replace({"course_section": section_dictionary})

        df.rename(columns={'course_section':'Class Section'}, inplace=True)

        df = df.drop("Class Section_x", axis=1)
        df = df.drop("Class Section_y", axis=1)

        print(df)

        df.to_csv(output_filename, index = False)
        


        df = df.rename(columns = {"Acad Level": "year_in_school"})
        #df = df.rename(columns = {"IELTS Overall Band Score": "IELTS Overall"})
    
        master_slice = df[['Catalog Nbr', 'Class Section', 'Registrar ID','First Name', 'Last Name','Name','IELTS Speaking', 'IELTS Listening','IELTS Reading','IELTS Writing', 'IELTS Overall Band Score','year_in_school', 'College', 'Major', 'Birth Country Code', 'Gender', 'TOEFL COMPI', 'TOEFL Listening', 'TOEFL Reading', 'TOEFL Writing', 'TOEFL Speaking', 'Crow ID', 'Instructor Code', 'Alternate Name', 'term', 'mode_of_course', 'length_of_course', 'institution']]
   
        new_master = pandas.concat([all_master, master_slice], sort = False)
        output_filename = re.sub(r'\s+', r'_', output_filename)
        new_master.to_csv('master_' + output_filename, index = False)


if args.master_student and args.instructor_codes:
    if '.xls' in args.master_student:
        master_student_file = pandas.ExcelFile(args.master_student)
        master_student_data = pandas.read_excel(master_student_file)
    elif '.csv' in args.master_student:
        master_student_data = pandas.read_csv(args.master_student)

    # get last (highest) section code from master student file
    last_section_code = master_student_data['Class Section'].max()


    instructor_codes_file = pandas.ExcelFile(args.instructor_codes)
    instructor_codes = pandas.read_excel(instructor_codes_file)

    if args.dir and os.path.isdir(args.dir):
        output_filename = re.sub(r'\.+\/|\.+\\', r'', args.dir)
        output_filename = re.sub(r'\/|\\', r'_', output_filename)
        output_filename += '_processed.csv'
        output_filename = re.sub(r'_+', r'_', output_filename)
        output_frames = combine_recursive(args.dir)
        process_new_data(output_frames, master_student_data[['Registrar ID', 'Crow ID', 'Class Section']], master_student_data, instructor_codes, output_filename)

    elif args.file and os.path.isfile(args.file):
        output_filename = re.sub(r'.+\/|.+\\|\.xlsx?', r'', args.file)
        output_filename += '_processed.csv'
        output_filename = re.sub(r'_+', r'_', output_filename)
        output_frames = combine_tabs(args.file)
        process_new_data(output_frames, last_student_code, master_student_data[['Registrar ID', 'Crow ID', 'Class Section']], instructor_codes)
    else:
        print('You need to supply a valid directory or filename')
else:
    print('You need to supply a valid master student and instructor codes files')
