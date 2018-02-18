#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

'''process_script.py: This file should be modified, as needed, to
apply any arbitrary text manipulation/processing tasks to a file
or files. It is a helper function for the gpio.py script, which
is a user interface for determining which files should be processed.

In the example here, a single "remove_tags() function is uses in
the process() function.

The process() function takes text input from an opened file and should
return the text according to any modifications you want to make.
'''
import re

''' The following function is just a demonstration of a function that
could be used within the process() function. It removes HTML tags.'''
TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

def process(infile):
    # Below, a series of text processing functions can be added serially,
    # with the ultimate output to be return to the calling function (@see
    # gpio.py's `process_file() function)
    output = remove_tags(infile)
    # The below line will not need to change.
    return output
