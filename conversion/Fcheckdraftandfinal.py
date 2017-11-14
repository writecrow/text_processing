import os
import sys
import subprocess as SP
from dabfunctions import checkArgs


################################################################################
##234567890123456789012345678901234567890123456789012345678901234567890123456789
##
## Main program.

#checkArgs(2, 'usage: a.out directory')

#dirname = sys.argv[1]
dirname = '.'

filenames = os.listdir(dirname)
for filename in filenames:
    if 'draft' in filename:
        draftfilename = filename
        finalfilename = draftfilename.replace('draft', 'final')
#        print('CHECK: %s %s' % (draftfilename, finalfilename))
        if finalfilename not in filenames:
            print('GLITCH: %s but no %s' % (draftfilename, finalfilename))
            draftfilename = 'odd_' + draftfilename
#            print('RENAME: %s  -->  %s' % (filename, draftfilename))
            os.rename(dirname + '/' + filename, dirname + '/' + draftfilename)

    if 'final' in filename:
        finalfilename = filename
        draftfilename = finalfilename.replace('final', 'draft')
#        print('CHECK: %s %s' % (finalfilename, draftfilename))
        if draftfilename not in filenames:
            print('GLITCH: %s but no %s' % (finalfilename, draftfilename))
            finalfilename = 'odd_' + finalfilename
#            print('RENAME: %s  -->  %s' % (filename, finalfilename))
            os.rename(dirname + '/' + filename, dirname + '/' + finalfilename)





