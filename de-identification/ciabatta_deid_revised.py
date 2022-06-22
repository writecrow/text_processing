#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


# DESCRIPTION:
# Given a folder with .txt files (inlcuding subfolders),
# the script removes lines before the body of the student texts that have names, initials, emails, etc.
# Disclaimer: this script deletes consecutive capitalized words and might delete assignment titles


# Usage example:
# Run this line below from the terminal on a Mac or command prompt on Windows
# Mac example: python ciabatta_deid.py --directory=../../../spring_2018/files_with_headers/
# PC example: python ciabatta_deid.py --directory=..\..\..\spring_2018\files_with_headers\
# what follows --directory= is the folder with the files on your computer which you need to specify


# imports packages
import argparse
import os
import re

# Lists the required arguments (e.g. --directory=) sent to the script
parser = argparse.ArgumentParser(description='De-identify Individual Textfile')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action='store', dest='dir', default='')
args = parser.parse_args()

# creates a function to remove any name patterns from lines
def clean_names_from_line(original_line):
    # cleans white space and line break in lines before text body
    cleaned_line = re.sub(r'(\r+)?\n', r'', original_line)

    # removes any initials like H. and j.
    cleaned_line = re.sub(r'\s[A-Za-z]\.', r'', cleaned_line)

    # removes titles and other identifiers
    cleaned_line = re.sub(r'name|net\s?id|id|student|professor|prof\.|teacher|instructor|Mr\.|Dr\.|Mr?s\.|[A-Z]\.|\s[A-Za-z]\s', r'', cleaned_line, flags=re.IGNORECASE)

    # removes comma, period, colon, and parentheses after removing titles and other identifiers
    cleaned_line = re.sub(r'(,|\.|\:|\(|\))', r'', cleaned_line)

    # removes up to three capitalized words (first, middle, last)
    cleaned_line = re.sub(r'(([A-Z][a-z]+){1,3})', r'', cleaned_line)

    # removes numerals
    cleaned_line = re.sub(r'[0-9]+', r'', cleaned_line)

    # removes any extra spaces
    cleaned_line = re.sub(r'\s', r'', cleaned_line)
    #cleaned_line = cleaned_line.strip()
    cleaned_line = re.sub(r'(\r+)?\n', '\n', cleaned_line)

    # returns the line with the above patterns removed
    return(cleaned_line)

# creates a function to remove any email addresses
def clean_email_from_line(original_line):
    # removes email patterns from line
    cleaned_line = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'', original_line)

    # removes any extra spaces
    cleaned_line = re.sub(r'\s', r'', cleaned_line)
    #cleaned_line = cleaned_line.strip()
    cleaned_line = re.sub(r'(\r+)?\n', '\n', cleaned_line)

    # returns the line with email addresses removed
    return(cleaned_line)


# creates a function that deidentifies an individual file
def deidentify_file(filename, overwrite=False):
    # only works with .txt files
    found_text_files = False
    if '.txt' in filename:
        # tells the user file is being processed
        print("Processing file " + filename)

        # switches flag to true
        found_text_files = True

        # deletes slashes and periods from the filename path ../../../spring_2018/files_with_headers/
        cleaned_filename2 = re.sub(r'\.\.[\\\/]', r'', filename)

        # creates an output directory called "deidentified"
        output_directory = 'deidentified'

        # creates new files with the same name as original files in the "deidentified" output directory
        output_filename = os.path.join(output_directory, cleaned_filename2)

        # creates a directory with subdirectories inside the "deidentified" directory with the same names as the original directory and subdirectories
        directory = os.path.dirname(output_filename)

        # if output directory does not exist already, it creates one
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        try:
            # opens and reads in the file
            textfile = open(filename, 'r')

            # opens the output file and writes in it
            output_file = open(output_filename, "w")

            found_text_body=False
            # loops through every line in the file

            for line in textfile:
                # strips spaces at the end of the line
                line_nobreaks = line.strip()

                # if there's text in the line (if the line is not empty)
                if line_nobreaks != '':
                    # if the last character in the line is a period, semicolon, exclamation or question mark
                    if line_nobreaks[-1] in ['.', ';', '!', '?']:
                        # creates a found_text_body variable to identify the body of the text
                        found_text_body = True


                # calls function to clean names from the lines before the body of the text
                # (if removing names makes line empty, the line
                # had only names and nothing else)
                line_no_names = clean_names_from_line(line)

                # calls function to clean email addresses from the lines before the body of the text
                # (if removing email addresses makes line empty, the line
                # had only email addresses and nothing else)
                line_no_emails = clean_email_from_line(line)

                if (line_no_names != '' and
                        line_no_emails != ''):

                    # check if line is a Word comment
                    if not line[0] == '[':
                        # removes other Word comments, e.g., [AP 1]
                        new_line2 = re.sub(r'\[([A-Z][A-Z]\s?[0-9]{1,2})\]', r'', line)

                        # if the body of the texts has not started yet
                        if not found_text_body:
                            # removes any remaining emails
                            new_line2 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'', new_line2)
                        # if we are in the body of the text already
                        else:
                            # replaces emails with <email>
                            new_line2 = re.sub(r'([A-Z]|[a-z]|[0-9]|\.)+@.+', r'<email>', new_line2)

                        # removes any exra spaces
                        new_line2 = re.sub(r'\s+', r' ', new_line2)

                        # writes out line and linebreak for cross-platform use
                        new_line3 = re.sub('(\r+)?\n', os.linesep, new_line2)
                        output_file.write(new_line3.strip() + '\n')
        except:
            print("File " + filename + " could not be opened. Check if the file is UTF-8 encoded. If not, use the Corpus Text Processor Tool.")
                
            # closes the file after writing
            output_file.close()
            textfile.close()
        

    # returns whether text file was found
    return(found_text_files)

# creates a function that deidentifies each file in a folder and all subfolders recursively
def deidentify_recursive(directory, overwrite=False):
    # creates control variable to check if there were any text files in the provided folder
    found_text_files = False

    # walks folder structure to get all files in all folders
    for dirpath, dirnames, files in os.walk(directory):
        # for every file found in a folder
        for name in files:
            # calls function that deidentifies an individual file
            is_this_a_text_file = deidentify_file(os.path.join(dirpath, name), overwrite)

            # changes the variable if a text file was processed
            if is_this_a_text_file:
                found_text_files = True

    # if no .txt texts were found in the directory, it prints "No text files found in the directory"
    if not found_text_files:
        print('No text files found in the directory.')

# checks if the user has specified directory with the .txt files to be deidentified
if args.dir:
    # calls function that deidentifies each file in a folder and all subfolders recursively
    deidentify_recursive(args.dir)
else:
    print('You need to supply a directory with textfiles')
