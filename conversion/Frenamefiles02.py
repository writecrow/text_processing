import os
import sys
import subprocess as SP
from dabfunctions import checkArgs


################################################################################
##234567890123456789012345678901234567890123456789012345678901234567890123456789
##
## Main program.

#checkArgs(5, 'usage: a.out classnumber sectionnumber papernumber draft/final')

#classnumber = sys.argv[1]
#sectionnumber = sys.argv[2]
#papernumber = sys.argv[3]
#draftfinal = sys.argv[4]

#outstring = 'ARGUMENTS: classnumber, sectionnumber, papernumber, draft/final = '
#outstring += '%s %s %s %s\n' % \
#             (classnumber, sectionnumber, papernumber, draftfinal)
#print(outstring)

sequencenumber = -1
oldstudentname = 'aaaaaaaaa'
filenames = os.listdir('.')
for filename in filenames:
    if filename.startswith('.'): continue
    if filename.startswith('_'): continue
    if filename.endswith('.py'): continue
    print('FILE OLD  %s' % (filename))

    filenametokenlist = filename.split('_') 
    print('FILE LIST %s' % (filenametokenlist))
    newstudentname = filenametokenlist[4]
    if newstudentname != oldstudentname:
        sequencenumber += 1
        sequencestring = '%03d' % (sequencenumber)
        print('FILE SEQ  %s %s %s\n' % (oldstudentname, newstudentname, sequencestring))
        oldstudentname = newstudentname

    newfilename = filename.replace(filenametokenlist[4], sequencestring)
    newfilename = newfilename.replace('_draft', 'draft')
    newfilename = newfilename.replace('_final', 'final')
    print('FILE NEW  %s %s\n' % (filename, newfilename))

    os.rename(filename, newfilename)






