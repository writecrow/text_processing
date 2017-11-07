#!/usr/bin/python

import sys
import re
import codecs

if __name__ == '__main__':
    if len(sys.argv) > 1:
        for filename in sys.argv[1:]:
            try:
                # open files with cp1251 encoding
                f = codecs.open(filename, 'r', 'cp1251')
                # output file name
                output_file_name = f.name
                # read file contentx
                u = f.read()
                # create new file (overwrite old file) with utf-8 encoding
                out = codecs.open(output_file_name, 'w', 'utf-8')
                # write contents to file
                out.write(u)
                out.close()
                print(output_file_name)
            except:
                pass
