#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

''' The following function is just a demonstration of a function that
could be used within the process() function. It removes cleans characters.'''

import re


def normalize(text):
    # for each line in this file
    lines = text.splitlines()
    output = ''
    for line in lines:
        # replace tabs with <tab>
        line = re.sub(r'\t', '<tab>', line)
        # replace smart quotes with regular quotes
        line = line.replace(u'\u2018', u"'")
        line = line.replace(u'\u2019', u"'")
        line = line.replace(u'\u201a', u"'")
        line = line.replace(u'\u201b', u"'")
        line = line.replace(u'\u201c', u'"')
        line = line.replace(u'\u201d', u'"')
        line = line.replace(u'\u201e', u'"')
        line = line.replace(u'\u201f', u'"')
        line = line.replace(u'\u2032', u"'")
        line = line.replace(u'\u2035', u"'")
        line = line.replace(u'\u2033', u'"')
        line = line.replace(u'\u2034', u'"')
        line = line.replace(u'\u2036', u'"')
        line = line.replace(u'\u2037', u'"')
        # replace ellipsis with single period
        line = line.replace(u'\u2024', u'.')
        line = line.replace(u'\u2025', u'.')
        line = line.replace(u'\u2026', u'.')
        # replace Armenian apostophre with regular apostophre
        line = line.replace(u'\u055a', u"'")
        # replace inverted question mark with nothing
        line = line.replace(u'\u00bf', u' ')
        # replace all dashes with regular hyphen
        line = line.replace(u'\u2010', u'-')
        line = line.replace(u'\u2011', u'-')
        line = line.replace(u'\u2012', u'-')
        line = line.replace(u'\u2013', u'-')
        line = line.replace(u'\u2014', u'-')
        line = line.replace(u'\u2015', u'-')
        # sentence normalization
        line = re.sub(r'([\.\?;:])([A-Z][a-z]+)', '\g<1> \g<2>', line)
        line = re.sub(r'([,;:])([a-z][a-z]+)', '\g<1> \g<2>', line)
        line = re.sub(r'([a-z])([A-Z])', '\g<1> \g<2>', line)
        line = re.sub(r'([\.\?;:])([0-9]+\s+)', '\g<1> \g<2>', line)
        line = re.sub(r'\r', ' ', line)
        line = re.sub(r'([a-z])(\n[A-Z])', '\g<1>. \g<2>', line)
        # replace some weird characters from cp1251 conversion
        line = re.sub(r'вЂњ', '"', line)
        line = re.sub(r'вЂќ', '"', line)
        line = re.sub(r'вЂ™', "'", line)
        # use a regular expression to find non-english characters
        # and replace them with space
        line = re.sub(r'[^\x00-\x7F]+', ' ', line)
        # get rid of weird line breaks (this does not seem to be working)
        line = re.sub(r'([a-z]+)\s*\n\s*([a-z]+)', '\g<1> \g<2>', line)
        # get rid of all double spaces
        line = re.sub(r'\s+', ' ', line)
        # get rid space in the beginning of a line
        if line and line[0] == ' ':
            line = line[1:]
        # readd tab
        line = re.sub(r'<tab>', '\t', line)
        # write our text in the file
        output = output + (line + "\r\n")
    return output
