#Description: Given a metadata spreadsheet for one semester and a folder with files 
#from that semester, the script looks to see if the names in the filenames match the 
#names in the spreadsheet

#use case: python match_names.py --directory=../../Spring\ 2019/UTF8_encoded/ --master_file=Spring_2019_test_processed.csv 

import argparse
import sys
import pandas
import os
import re

parser = argparse.ArgumentParser(description='Matching names')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--master_file', action="store", dest='master', default='')
args = parser.parse_args()


if '.xls' in args.master:
    master_file = pandas.ExcelFile(args.master)
    master_data = pandas.read_excel(master_file)
elif '.csv' in args.master:
    master_data = pandas.read_csv(args.master)


# new data frame with split value columns
new = master_data["Name"].str.split(",", n = 1, expand = True)
  
# making separate first name column from new data frame
master_data["First Name"]= new[1]
  
# making separate last name column from new data frame
master_data["Last Name"]= new[0]
 
# combine First Name and Last Name
master_data['Name'] = master_data['First Name'].str.cat(master_data['Last Name'],sep=" ")

list_of_names = master_data['Name'].values
#print(list_of_names)

student_filenames = []
student_not_found = []
for dirpath, dirnames, files in os.walk(args.dir):
    for filename in files:
        found_text_files = False       
        if '.txt' in filename:
            found_text_files = True
            filename_parts = filename.split('- ')
            #print(filename_parts)
            student_filename = re.sub(r'\.txt', r'', filename_parts[1])
            student_filename = re.sub(r'\s+', r' ', student_filename)
            if student_filename not in student_filenames:
                student_filenames.append(student_filename)
#print(student_filenames)

for name in list_of_names:
    if name not in student_filenames:
        if name not in student_not_found:
            student_not_found.append(name)
            print("These student names are in the spreadsheet but not in the filenames:")                
            print('\n'.join(map(str, student_not_found)))
            print("***************")     

for student_filename in student_filenames:
    if student_filename not in list_of_names:
        print("These student names are NOT in the spreadsheet but are in the filenames:")
        print(student_filename)





            




