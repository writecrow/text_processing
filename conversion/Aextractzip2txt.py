import os
import sys
import subprocess as SP
from dabfunctions import checkArgs
try:
    from xml.etree.cElementTree import XML
except ImportError:
    from xml.etree.ElementTree import XML
import zipfile 

################################################################################
##234567890123456789012345678901234567890123456789012345678901234567890123456789
## Program to get 'txt' files.
## 'zipfile_dir' is a directory of zip files; we assume the name ends in 'zips'.
## or 'zips/'.
## Each zip file should have a set of 'docx' files (and other stuff).
## This program unzips and converts the 'docx' files into 'txt files and puts
## the 'txt' into a new directory with the 'zips' stripped off the dir name.
##
def get_docx_text(zipsdirname, exceptionset, logfile):
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
            outstring = 'NOT A ZIP  %s' % (zipfilename)
            printoutput(outstring, logfile)
            continue
        outstring = 'ZIPNAME %s' % (zipfilename)
        printoutput(outstring, logfile)
        thezipfile = zipfile.ZipFile(zipsdirname + '/' + zipfilename)

        ## the outer loop is on the zip file names in the dir of zips
        ## the inner loop is on the zip files themselves
        first_time_this_paper = True
        names_in_zipfile = thezipfile.namelist()
        for filename in names_in_zipfile:
            outstring = 'FILENAME      %s' % (filename)
            printoutput(outstring, logfile)

            paperdirname = zipfilename.replace('.zip', '')
            if first_time_this_paper:
                callargument = '%s %s' % ('rm -r', txtdirname + '/' + paperdirname)
                SP.call(callargument, shell=True)
                callargument = '%s %s' % ('mkdir', txtdirname + '/' + paperdirname)
                SP.call(callargument, shell=True)
                first_time_this_paper = False

            ## skip anything that isn't a 'docx' file
            if (not filename.endswith('docx')):
                outstring = 'SKIP NOT DOCX %s' % (filename)
                printoutput(outstring, logfile)
                continue

            skipthisfile = False
            for excep in exceptionset:
#                outstring = 'EXCEPTION %s' % (excep)
#                printoutput(outstring, logfile)
                if excep in filename:
                    outstring = 'SKIP EXCEPTION %s' % (filename)
                    printoutput(outstring, logfile)
                    skipthisfile = True
                    break

            if skipthisfile:
                continue

            ## at this point we have work to do
            outstring = 'PROCESS       %s' % (filename)
            printoutput(outstring, logfile)

            thedocxfile = thezipfile.read(filename)
            txtfilename = filename.replace('docx', 'txt')
            with open(txtdirname + '/' + paperdirname + '/' + filename, "wb") as f:
                f.write(thedocxfile)
                f.close()

            ## Now we finally get around to reading the docx file.
            outstring = 'THEDOC        %s' % ((txtdirname + '/' + paperdirname + '/' + filename))
            printoutput(outstring, logfile)
            thedoc = 'zork'
            try:
                thedoc = zipfile.ZipFile(txtdirname + '/' + paperdirname + '/' + filename)
#                print(thedoc)
#                outstring = 'TRYGOOD\n'
#                print(outstring)
#                logfile.write(outstring)
#                logfile.flush()
            except:
                outstring = 'EXCEPTION %s' % ((txtdirname + '/' + paperdirname + '/' + filename))
                print(outstring)
                logfile.write(outstring+'\n')
                logfile.flush()
                continue
#
#            outstring = 'THIS DOC NAMELIST %s\n' % (thedocxfile.namelist())
#            logfile.write(outstring)
#            logfile.flush()

            if thedoc == 'zork':
                print('ZORK HERE')
                sys.exit()
            else:
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
## main function
def getexceptionset():
    exceptionset = set()
    exceptionfile = open('Aexceptionslist.txt')
    for line in exceptionfile:
        linesplit = line.split()
        exceptionset.add(linesplit[0])
    exceptionfile.close()
    print(exceptionset)
    return exceptionset

################################################################################
##234567890123456789012345678901234567890123456789012345678901234567890123456789
## printoutput to console and a file
def printoutput(outstring, outfile):
    print(outstring)
    outfile.write(outstring+'\n')
    outfile.flush()

################################################################################
##234567890123456789012345678901234567890123456789012345678901234567890123456789
## main function
def main(zipsdirname, logfile):
    exceptionset = getexceptionset()
    get_docx_text(zipsdirname, exceptionset, logfile)

################################################################################
##234567890123456789012345678901234567890123456789012345678901234567890123456789
##
## Main program.
checkArgs(3, 'usage: a.out zipsdirname logfile')

## Check that our zip file directory ends with 'zips'.
zipsdirname = sys.argv[1]
if zipsdirname.endswith('/'):
    zipsdirname = zipsdirname.replace('/','')
if not zipsdirname.endswith('zips'):
    print('ERROR zipfiledir %s is badly named\n' % (zipsdirname))
    sys.exit()

logfilename = sys.argv[2]
logfile = open(logfilename, 'w')

main(zipsdirname, logfile)

