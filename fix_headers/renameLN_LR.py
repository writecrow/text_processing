import argparse
import os
import sys
import re

parser = argparse.ArgumentParser(description='Renaming files')
parser.add_argument('--directory', action="store", dest='dir', default='')
args = parser.parse_args()

for root, dirs, files in os.walk(args.dir):
    for fileName in files:
        full_name= os.path.join(root,fileName)
        if "_LN_" in full_name:
            os.rename(full_name, full_name.replace("_LN_", "_LR_"))
        if ".txt" in full_name:
            with open(full_name, 'r') as f:
                s= f.read()
                if "<Assignment: LN>" in s:
                   s = s.replace('<Assignment: LN>', '<Assignment: LR>')
                   with open(full_name, "w") as f:
                            f.write(s)
                            f.close()
    
        