#!/usr/local/bin/python3

# DESCRIPTION: Given a file or files passed as arguments to the script,
# attempt to guess the character encoding and open each file as such.
# If that fails, try to open the file as.
# Finally, encode the file in utf8 and place it in an "output" directory
#
# Usage example:
#    python3 convert_to_utf8.py --file=myfile.txt
#    python text_processing/normalization/convert_to_utf8_normalize.py --directory=Converted/
#
# A new file, at output/myfile.txt will be created, with a best attempt at
# utf8 encoding.

import argparse
import chardet
import codecs
import os
import shutil
import sys
import re

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Convert to UTF-8')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--file', action="store", dest='file', default='')
args = parser.parse_args()

def normalize_file(original_file):
    #print ("encoding type:", encoding_type)
    rawdata = open(original_file, 'rb').read()
    detected = chardet.detect(rawdata)
    encoding_method = get_encoding(detected['encoding'])
    if not encoding_method:
        encoding_method = 'utf8'
    with codecs.open(original_file, 'r', encoding=encoding_method) as f:
        try:
            output_directory = 'normalized'
            output_filename = os.path.join(output_directory, original_file)
            directory = os.path.dirname(output_filename)
            if not os.path.exists(directory):
                os.makedirs(directory)
            # create a new file with that name, "w" is for writable
            output_file = open(output_filename, "w")
            # for each line in this file
            for line in f:
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
                # replace i with diacritics with quotes
                line = line.replace('ì', u'"')
                line = line.replace('í', u'"')
                # replace ellipsis with single period
                line = line.replace(u'\u2024', u'.')
                line = line.replace(u'\u2025', u'.')
                line = line.replace(u'\u2026', u'.')
                # replace Armenian apostophre with regular apostophre
                line = line.replace(u'\u055a', u"'")
                # replace inverted question mark with nothing
                line = line.replace(u'\u00bf', u' ')
                # replace all dashes with regular hifen
                line = line.replace(u'\u2010', u'-')
                line = line.replace(u'\u2011', u'-')
                line = line.replace(u'\u2012', u'-')
                line = line.replace(u'\u2013', u'-')
                line = line.replace(u'\u2014', u'-')
                line = line.replace(u'\u2015', u'-')
                # sentence normalization
                line = re.sub(r'([\.\?;:])([A-Z][a-z]+)','\g<1> \g<2>', line)
                line = re.sub(r'([,;:])([a-z][a-z]+)','\g<1> \g<2>', line)
                line = re.sub(r'([a-z])([A-Z])','\g<1> \g<2>', line)
                line = re.sub(r'([\.\?;:])([0-9]+\s+)','\g<1> \g<2>', line)
                #line = re.sub(r'\r',' ', line)
                line = re.sub(r'([a-z])(\n[A-Z])','\g<1>. \g<2>', line)
                # flatten diacritics
                line = re.sub(r'[áàãäâåāăąǎȃȧ]','a', line)
                line = re.sub(r'[ÁÀÃÄÂÅĀĂĄǍȂȦ]','A', line)
                line = re.sub(r'[éèêëēĕėęěȇ]','e', line)
                line = re.sub(r'[ÉÈÊËĒĔĖĘĚȆ]','E', line)
                line = re.sub(r'[íìîïīĭįǐȋ]','i', line)
                line = re.sub(r'[ÍÌÎÏĪĬĮİǏȊ]','I', line)
                line = re.sub(r'[øóòöõôȏȯ]','o', line)
                line = re.sub(r'[ØÓÒÖÕÔȎȮ]','O', line)
                line = re.sub(r'[úùüûǔȗ]','u', line)
                line = re.sub(r'[ÚÙÜÛǓȖ]','U', line)
                line = re.sub(r'[ÝȲ]','Y', line)
                line = re.sub(r'[ýÿȳ]','y', line)
                line = re.sub(r'œ','oe', line)
                line = re.sub(r'æ','ae', line)
                line = re.sub(r'Æ','AE', line)
                line = re.sub(r'[çćĉċč]','c', line)
                line = re.sub(r'[ÇĆĈĊČ]','C', line)
                line = re.sub(r'ñ','n', line)
                line = re.sub(r'Ñ','N', line)
                # use a regular expression to find non-english characters and
                # replace them with space
                # capture any name that is written in different scripts
                line = re.sub(r'[^\x00-\x7F]+', ' ', line)
                # get rid of weird line breaks (this does not seem to be working)
                line = re.sub(r'([a-z]+)\s*\n\s*([a-z]+)','\g<1> \g<2>', line)
                # get rid of all double spaces
                line = re.sub(r'\s+', ' ', line)
                #print(line)
                # get rid space in the beginning of a line
                line = line.strip()
                # re-add tab
                line = re.sub(r'<tab>', '\t', line)
                # write our text in the file
                output_file.write(line + "\r\n")
                #print(line, file=output_file)
            # be polite and close the file
            output_file.close()
        except:
           print(output_filename + "\t" + str(sys.exc_info()[0]) + "\t" + str(sys.exc_info()[1]))

def get_encoding(argument):
    # In the below dictionary, the key is encoding provided by the chardet
    # module. The value is the encoding to use from the codecs
    # module. See
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    switcher = {
        'ascii': 'ascii',
        'ISO-8859-1': 'utf-8-sig',
        'ISO-8859-2': 'utf-8-sig',
        'MacCyrillic': 'cp1256',
        'windows-1251': 'windows-1251',
        'Windows-1252': 'cp1252',
        'Windows-1254': 'cp1254',
        'UTF-8-SIG': 'utf-8-sig',
        'UTF-16': 'utf-16',
        'UTF-16LE': 'utf-16',
        'UTF-32': 'utf_32'
    }
    return switcher.get(argument, False)


def decode(filename, encoding_method):
    try:
        f = codecs.open(filename, 'r', encoding_method)
        return {'file': f.read(), 'encoding': encoding_method}
    except UnicodeDecodeError:
        pass
    f = codecs.open(filename, 'r', 'latin_1')
    return {'file': f.read(), 'encoding': 'latin_1'}


def convert_file(filename, overwrite=False):
    if '.txt' in filename:
        output_filename = filename
        if (not overwrite):
            output_dir = 'converted'
            output_filename = os.path.join(output_dir, filename)
            output_directory = os.path.dirname(output_filename)
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

        # Open the file so we can guess its encoding.
        rawdata = open(filename, 'rb').read()
        detected = chardet.detect(rawdata)
        encoding_method = get_encoding(detected['encoding'])
        if (encoding_method):
            u = decode(filename, encoding_method)
            out = codecs.open(output_filename, 'w', 'utf-8')
            out.write(u['file'])
            out.close()
            print(filename, "converted from", u['encoding'])
        else:
            shutil.copy(filename, output_filename)
            if (detected['encoding'] == 'utf-8'):
                print(filename, "already encoded in utf-8")
            else:
                print(filename, "detected as", detected['encoding'], "(No change)")
        normalize_file(output_filename)
    else:
        print(filename, "is not a text file")


def convert_recursive(directory, overwrite=False):
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            convert_file(os.path.join(dirpath, name), overwrite)


if args.dir and os.path.isdir(args.dir):
    convert_recursive(args.dir, args.overwrite)
elif args.file and os.path.isfile(args.file):
    convert_file(args.file, args.overwrite)
else:
    print('You need to supply a valid directory or filename')
