#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# DESCRIPTION: Given a directory with text files passed as argument
# to the script, a stratified (by directory) sample of file texts
# is created.
#
# Usage example:
#   python get_random_sample.py --directory=../../../Fall\ 2017/deidentified/ --n_files=2
#   python get_random_sample.py --directory=deidentified_files/Spring\ 2018/ --n_files=2
#   python get_random_sample.py --directory=../../../MACAWS/deidentified_files/ --n_files=2


import argparse
import numpy as np
import os
import re
import sys

from shutil import copyfile

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Get Random Sample of Textfiles')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--n_files', action="store", dest='n_files', default=1)
args = parser.parse_args()

def get_sample(filename):
    # create output filename with directory path
    cleaned_filename = re.sub(r'\.\.[\\\/]', r'', filename)
    output_directory = 'random_sample'
    output_filename = os.path.join(output_directory, cleaned_filename)
    directory = os.path.dirname(output_filename)
    if not os.path.exists(directory):
        os.makedirs(directory)

    copyfile(filename, output_filename)



def get_sample_recursive(directory, n):
    list_of_files = {}
    for dirpath, dirnames, files in os.walk(directory):
        for dir in dirpath:
            list_of_files[dirpath] = []
        for name in files:
            if '.txt' in name and '_DF_' in name:
                found_text_files = True
                list_of_files[dirpath].append(name)

    random_file_list = []
    for dir in list_of_files:
        if len(list_of_files[dir]) > 0:
            this_random_list = np.random.choice(list_of_files[dir], n)
            for file_chosen in this_random_list:
                random_file_list.append(os.path.join(dir, file_chosen))


    print('A total of ' + str(len(random_file_list)) + ' files have been chosen randomly, stratified by directory.')
    for file_chosen in random_file_list:
        get_sample(file_chosen)

    if len(list_of_files) == 0:
        print('No text files found in the directory.')


if args.dir:
    get_sample_recursive(args.dir, int(args.n_files))
else:
    print('You need to supply a valid directory with textfiles')
