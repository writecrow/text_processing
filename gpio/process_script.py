#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

'''process_script.py: This file should be modified, as needed, to
apply any arbitrary text manipulation/processing tasks to a file
or files. It is a helper function for the gpio.py script, which
is a user interface for determining which files should be processed.

In the example here, a normalize() and remove_tags()
function are used in the process() function.

The process() function takes text input from an opened file and should
return the text, with any modifications you want to make, as its output.
'''
import normalization
import remove_tags


def process(infile):
    # Below, a series of text processing functions can be added serially,
    # with the ultimate output to be return to the calling function (@see
    # gpio.py's `process_file() function)
    output = normalization.normalize(infile)
    output = remove_tags.remove(output)
    # The below line will not need to change.
    return output
