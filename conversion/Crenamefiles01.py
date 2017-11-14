import os
import sys
import subprocess as SP
from dabfunctions import checkArgs


################################################################################
##234567890123456789012345678901234567890123456789012345678901234567890123456789
## Program to get 'txt' files.
## 'zipfile_dir' is a directory of zip files; we assume the name ends in 'zips'.
## Each zip file should have a set of 'docx' files (and other stuff).
## This program unzips and converts the 'docx' files into 'txt files and puts
## the 'txt' into a new directory with the 'zips' stripped off the dir name.
##
def get_docx_text(zipsdirname, logfile):
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'

    ## Create the dir without the 'zips' in the name.
    txtdirname = zipsdirname.replace('zips', '')
    callargument = '%s %s' % ('rm -r', txtdirname)
    SP.call(callargument, shell=True)
    callargument = '%s %s' % ('mkdir', txtdirname)
    SP.call(callargument, shell=True)

    ## the outer loop is on the zip file names in the dir of zips
    zipfilenames = os.listdir(zipsdirname)
    for zipfilename in zipfilenames:
        if not zipfilename.endswith('zip'):
            outstring = 'NOT A ZIP  %s\n' % (zipfilename)
            print(outstring)
            logfile.write(outstring)
            logfile.flush()
            continue
        outstring = 'ZIPNAME  %s\n' % (zipfilename)
        print(outstring)
        logfile.write(outstring)
        logfile.flush()
        thezipfile = zipfile.ZipFile(zipsdirname + '/' + zipfilename)


        ## the outer loop is on the zip file names in the dir of zips
        ## the inner loop is on the zip files themselves
        first_time_this_paper = True
        names_in_zipfile = thezipfile.namelist()
        for filename in names_in_zipfile:
#            logfile.write('FILENAME %s\n' % (filename))
#            logfile.flush()

            paperdirname = zipfilename.replace('.zip', '')
            if first_time_this_paper:
                callargument = '%s %s' % ('rm -r', txtdirname + '/' + paperdirname)
                SP.call(callargument, shell=True)
                callargument = '%s %s' % ('mkdir', txtdirname + '/' + paperdirname)
                SP.call(callargument, shell=True)
                first_time_this_paper = False

            ## skip anything that isn't a 'docx' file
            if (not filename.endswith('docx')):
#                outstring = 'SKIP %s\n' % (filename)
#                logfile.write(outstring)
                continue

            ## at this point we have work to do
            outstring = 'PROCESS %s\n' % (filename)
            print(outstring)
            logfile.write(outstring)
            logfile.flush()

            thedocxfile = thezipfile.read(filename)
            txtfilename = filename.replace('docx', 'txt')
            with open(txtdirname + '/' + paperdirname + '/' + filename, "wb") as f:
                f.write(thedocxfile)
                f.close()

            ## Now we finally get around to reading the docx file.
            outstring = 'THEDOC %s\n' % ((txtdirname + '/' + paperdirname + '/' + filename))
            print(outstring)
            logfile.write(outstring)
            logfile.flush()
            try:
                thedoc = zipfile.ZipFile(txtdirname + '/' + paperdirname + '/' + filename)
            except:
                outstring = 'EXCEPTION %s\n' % ((txtdirname + '/' + paperdirname + '/' + filename))
                print(outstring)
                logfile.write(outstring)
                logfile.flush()
                continue
#
#            outstring = 'THIS DOC NAMELIST %s\n' % (thedocxfile.namelist())
#            logfile.write(outstring)
#            logfile.flush()

            xmlcontent = thedoc.read('word/document.xml')
            tree = XML(xmlcontent)

            paragraphs = []
            for paragraph in tree.getiterator(PARA):
                texts = [] 
                texts = [node.text 
                        for node in paragraph.getiterator(TEXT)
                        if node.text]
                if texts:
                    paragraphs.append(''.join(texts))

            thetext = '\n\n'.join(paragraphs)
            thetxtfilename = filename.replace('docx', 'txt')
            with open(txtdirname + '/' + paperdirname + '/' + thetxtfilename, "wb") as f:
                f.write(thetext.encode("utf-8"))
                f.close()


    logfile.flush()
    sys.exit()

## zork : after this is old code
#            ## Create the new file that is just the docx from the zip.
#            outstring = 'DIR NEWNAME %s\n' % (newfilename)
#            logfile.write(outstring)
#            logfile.flush()
#            with open(newfilename, "wb") as f:
#                f.write(thezipcontent)
#                f.close()
#
#            xml_content = thedoc.read('word/document.xml')
#            tree = XML(xml_content)


    thezipfile.close()
    return 'NO DOCX FILES FOUND\n'

################################################################################
##234567890123456789012345678901234567890123456789012345678901234567890123456789
##
## Main program.

checkArgs(5, 'usage: a.out classnumber sectionnumber papernumber draft/final')

classnumber = sys.argv[1]
sectionnumber = sys.argv[2]
papernumber = sys.argv[3]
draftfinal = sys.argv[4]

outstring = 'ARGUMENTS: classnumber, sectionnumber, papernumber, draft/final = '
outstring += '%s %s %s %s\n' % \
             (classnumber, sectionnumber, papernumber, draftfinal)
print(outstring)

filenames = os.listdir('.')
for filename in filenames:
    print('FILE OLD  %s' % (filename))
    filenamewithoutblanks = filename.replace(' ', '_')
    print('FILE SUB  %s' % (filenamewithoutblanks))

    filenametokenlist = filenamewithoutblanks.split('_') 
    attemptindex = filenametokenlist.index('attempt') 
    print('FILE LIST ZZ%dZZ %s\n' % (attemptindex, filenametokenlist))

    newfilename = '2016_4_' + classnumber + '_' + sectionnumber + '_'
    newfilename += filenametokenlist[attemptindex-1] + '_'
    newfilename += draftfinal + papernumber + '.txt'
    print('FILE NEW  %s\n' % (newfilename))

    os.rename(filename, newfilename)






