#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

'''gpio.py: Given a single file or directory by the user,
send each file, one at a time, to a generic "process" function.
This process function exists in process_script.py and may be modified
as needed for processing.

Example command for processing a single file called "text.txt"
        $ python gpio.py --file=test-data/text.txt
Example command for processing an entire directory called "input"
        $ python gpio.py --directory=input

An optional argument, "--overwrite", may be passed along with the
file or directory, and will save any changes to the same location
as the originating file. The default behavior, otherwise, is to
save identically named file(s) to an "output" directory.

The process() function receives the contents of each file as its
input, and should return the (modified) contents of the file as
its output.
'''

import argparse
import os
from process_script import process

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Convert to UTF-8')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--file', action="store", dest='file', default='')
args = parser.parse_args()


def process_file(filename, overwrite=False):
    ''' Open a file, send it to a process function, and write the output. '''
    output_filename = filename
    if (not overwrite):
        output_dir = 'output'
        output_filename = os.path.join(output_dir, filename)
        output_directory = os.path.dirname(output_filename)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

    infile = open(filename, 'r').read()
    # Here, the text is passed to the process() function.
    # @see process_script.py
    processed = process(infile)
    outfile = open(output_filename, 'w')
    outfile.write(processed)
    outfile.close()


def process_recursive(directory, overwrite=False):
    ''' Helper function for looping through files recursively '''
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            process_file(os.path.join(dirpath, name), overwrite)

''' Main logic here: take user arguments & process'''
if args.dir and os.path.isdir(args.dir):
    process_recursive(args.dir, args.overwrite)
elif args.file and os.path.isfile(args.file):
    process_file(args.file, args.overwrite)
else:
    print('You need to supply a valid directory or filename')
