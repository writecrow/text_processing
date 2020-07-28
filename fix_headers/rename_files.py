import argparse
import os
import re
import sys

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Fix filename & headers')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()


def fix_headers(filename, overwrite=False):
    if '.txt' in filename:
        #clean_filename = re.sub(r'\.\.[\\\/]', r'', filename)
        output_dir = 'fixed_files'
        output_filename = os.path.join(output_dir, filename)
        output_directory = os.path.dirname(output_filename)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        original_file = open(filename, 'r')
        original_contents = original_file.read()

        print("Fixing headers and filesnames: " + output_filename)
        # add "Student" before "ID" in ID header
        
        if "_DF_" in filename:
            filename = re.sub("_DF" , "_F_", filename)
        if "_D1_" in filename:
            filename = re.sub("_D1" , "_1_", filename)
        if "_D2_" in filename:
            filename = re.sub("_D2" , "_2_", filename)
        if "_D3_" in filename:
            filename = re.sub("_D3" , "_3_", filename)
        if "_D4_" in filename:
            filename = re.sub("_D4" , "_4_", filename)
        if "_D5_" in filename:
            filename = re.sub("_D5" , "_5_", filename)

        #fixed_contents = re.sub(r'(<)(ID:\s\d+>)', '\g<1>Student \g<2>', original_contents)

        # add "ENGL" before course number in course header
        #fixed_contents = re.sub(r'(<Course:\s)(\d+>)', '\g<1>ENGL \g<2>', fixed_contents)

        # remove "D" from draft number in draft header
        #fixed_contents = re.sub(r'(<Draft:\s)D(\d|F>)', '\g<1>\g<2>', fixed_contents)

        # add space after <End Header>
        #fixed_contents = re.sub(r'(<End Header>)', '\g<1>\r\n', fixed_contents)

        output_file = open(output_filename, 'w')
        output_file.write(output_filename)

        original_file.close()
        output_file.close()

def fix_headers_all_files(directory, overwrite=False):
    for dirpath, dirnames, files in os.walk(directory):
        for name in files:
            fix_headers(os.path.join(dirpath, name), overwrite)

if args.dir:
    fix_headers_all_files(args.dir)
else:
    print('You need to supply a valid directory with textfiles')