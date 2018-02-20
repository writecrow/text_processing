#!/usr/local/bin/python3

# DESCRIPTION: Given a file or files passed as arguments to the script,
# attempt to guess the character encoding and open each file as such.
# If that fails, try to open the file as.
# Finally, encode the file in utf8 and place it in an "output" directory
#
# Usage example:
#    python3 convert_to_utf8.py --file=myfile.txt
#
# A new file, at output/myfile.txt will be created, with a best attempt at
# utf8 encoding.

import argparse
import chardet
import codecs
import os
import shutil

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Convert to UTF-8')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--directory', action="store", dest='dir', default='')
parser.add_argument('--file', action="store", dest='file', default='')
args = parser.parse_args()


def get_encoding(argument):
    # In the below dictionary, the key is encoding provided by the chardet
    # module. The value is the encoding to use from the codecs
    # module. See
    # https://docs.python.org/3/library/codecs.html#standard-encodings
    switcher = {
        'ascii': 'ascii',
        'ISO-8859-1': 'utf-8-sig',
        'MacCyrillic': 'cp1256',
        'windows-1251': 'windows-1251',
        'Windows-1252': 'cp1252',
        'Windows-1254': 'cp1254',
        'UTF-8-SIG': 'utf-8-sig',
        'UTF-16': 'utf-16',
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
    output_filename = filename
    if (not overwrite):
        output_dir = 'output'
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
