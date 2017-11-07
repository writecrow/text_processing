#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import re
import os
import codecs

# command line to run this (from command prompt)
# python textnormalization.py **/**/*.txt

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for file in sys.argv[1:]:
            with open(file, 'r') as f:
                try:
                    # get the file name
                    print(f.name)
                    file_name = re.sub(r'\.txt',r'',f.name)
                    file_name = re.sub(r'\.TXT',r'',file_name)

                    # get file path
                    matches = re.findall('[\w\s]+\/', file_name)
                    path = ''
                    for m in matches:
                        path = path + m

                    path = "cleaned/" + path
                    if not os.path.exists(path):
                        os.makedirs(path)


                    file_name = re.sub(r'[\w\s]+\/',r'',file_name)

                    # output file name
                    output_file_name = path + file_name + ".txt"
                    #print(output_file_name)
                    # create a new file with that name, "w" is for writable
                    output_file = open(output_file_name, "w")

                    # for each line in this file
                    for line in f:

                        # replace tabs with <tab>
                        line = re.sub(r'\t','<tab>', line)

                        # replace smart quotes with regular quotes
                        line = line.replace( u'\u2018', u"'")
                        line = line.replace( u'\u2019', u"'")
                        line = line.replace( u'\u201a', u"'")
                        line = line.replace( u'\u201b', u"'")
                        line = line.replace( u'\u201c', u'"')
                        line = line.replace( u'\u201d', u'"')
                        line = line.replace( u'\u201e', u'"')
                        line = line.replace( u'\u201f', u'"')
                        line = line.replace( u'\u2032', u"'")
                        line = line.replace( u'\u2035', u"'")
                        line = line.replace( u'\u2033', u'"')
                        line = line.replace( u'\u2034', u'"')
                        line = line.replace( u'\u2036', u'"')
                        line = line.replace( u'\u2037', u'"')

                        # replace ellipsis with single period
                        line = line.replace( u'\u2024', u'.')
                        line = line.replace( u'\u2025', u'.')
                        line = line.replace( u'\u2026', u'.')

                        # replace Armenian apostophre with regular apostophre
                        line = line.replace( u'\u055a', u"'")

                        # replace inverted question mark with nothing
                        line = line.replace( u'\u00bf', u' ')

                        # replace all dashes with regular hyphen
                        line = line.replace( u'\u2010', u'-')
                        line = line.replace( u'\u2011', u'-')
                        line = line.replace( u'\u2012', u'-')
                        line = line.replace( u'\u2013', u'-')
                        line = line.replace( u'\u2014', u'-')
                        line = line.replace( u'\u2015', u'-')

                        # sentence normalization
                        line = re.sub(r'([\.\?;:])([A-Z][a-z]+)','\g<1> \g<2>', line)
                        line = re.sub(r'([,;:])([a-z][a-z]+)','\g<1> \g<2>', line)
                        line = re.sub(r'([a-z])([A-Z])','\g<1> \g<2>', line)
                        line = re.sub(r'([\.\?;:])([0-9]+\s+)','\g<1> \g<2>', line)
                        line = re.sub(r'\r',' ', line)
                        line = re.sub(r'([a-z])(\n[A-Z])','\g<1>. \g<2>', line)

                        # replace some weird characters from cp1251 conversion
                        line = re.sub(r'вЂњ','"',line)
                        line = re.sub(r'вЂќ','"',line)
                        line = re.sub(r'вЂ™',"'",line)

                        # use a regular expression to find non-english characters and replace them with space
                        line = re.sub(r'[^\x00-\x7F]+',' ', line)

                        # get rid of weird line breaks (this does not seem to be working)
                        line = re.sub(r'([a-z]+)\s*\n\s*([a-z]+)','\g<1> \g<2>', line)

                        # get rid of all double spaces
                        line = re.sub(r'\s+',' ', line)
                        #print(line)

                        # get rid space in the beginning of a line
                        if line[0] == ' ':
                            line = line[1:]

                        # readd tab
                        line = re.sub(r'<tab>','\t', line)

                        # write our text in the file
                        output_file.write(line + "\r\n")


                    # be polite and close the file
                    output_file.close()
                except:
                    print(f.name + "\t" + str(sys.exc_info()[0]) + "\t" + str(sys.exc_info()[1]))
