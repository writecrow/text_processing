#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given an excel file or files passed as arguments to the script,
# create one csv file with all tabs for instructors in the original spreadsheet
# The original spreadsheet needs a master tab, which is the first tab in
# the original excel file.
#
# Usage example:
#    python process_metadata_ciabatta.py --file1=../../../Metadata/Fall\ 2018/ --file2../../../Metadata/Master_Student_metadata_legacy.xlsx --yaml_file=../../../Metadata/Instructor_Codes.xlsx
#
# A new csv file with a similar name to the original spreadsheet
# will be created.


import argparse
import codecs
import os
import pandas
import re
import sys
import yaml

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Merge Metadata')
parser.add_argument('--file1', action="store", dest='file1', default='')
parser.add_argument('--file2', action="store", dest='file2', default='')
parser.add_argument('--yaml_file', action="store", dest='yaml_file', default='')
args = parser.parse_args()


def flatten_tabs(file, new_name):
    tabs = file.sheet_names

    flatten_file = pandas.DataFrame()
    for t in tabs:
        print("Getting data from " + t + " tab")
        this_tab_data = pandas.read_excel(file, t)
        this_tab_data[new_name] = t
        flatten_file = pandas.concat([flatten_file, this_tab_data])


    return(flatten_file)

if args.file1 and args.file2 and args.yaml_file:
    if '.xls' in args.file1:
        file1 = pandas.ExcelFile(args.file1)
    elif '.csv' in args.file1:
        file1_data = pandas.read_csv(args.file1, index=False)

    if '.xls' in args.file2:
        file2 = pandas.ExcelFile(args.file2)
    elif '.csv' in args.file2:
        file2_data = pandas.read_csv(args.file2, index=False)

    # open and read yaml file
    yaml_file = open(args.yaml_file, "r")
    yaml_contents = yaml.load(yaml_file, Loader = yaml.FullLoader)

    # check if file 1 needs to be flatten
    new_column_name = yaml_contents["file_1"]["tab"]
    if new_column_name:
        file1_data = flatten_tabs(file1, new_column_name)
    else:
        file1_data = pandas.read_excel(file1)

    # check if file 2 needs to be flatten
    new_column_name = yaml_contents["file_2"]["tab"]
    if new_column_name:
        file2_data = flatten_tabs(file2, new_column_name)
    else:
        file2_data = pandas.read_excel(file2)

    combined_file = file1_data.join(file2_data.set_index('Name'), on='Name',
    lsuffix='_file1', rsuffix='_file2')

    combined_file.to_csv("metadata.csv", index=False)

else:
    print('You need to supply a file1, file2, and a yaml file')
