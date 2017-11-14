## DEFINED FUNCTIONS
##def checkargs(number, message):
##def lowercasethelist(tokens):
##def printlist(label, thelist):
##def printlisttofile(outfile, label, thelist):
##def readfile(filepath):

##def addfiletodatabase(filename, featuredatabase):
##def addtofreqs(charlist, freqs):
##def classify(scores):
##def cleanupcharacters(text):
##def computeARI(sentences):
##def computefreqs(tokens):
##def computeletterfreqs(tokens):
##def extractauthor(filename):
##def extractcounts(sentences):
##def extractfeatures(filename):
##def flipdict(thedict):
##def getingstem(thisword, goodwordsjustwords, stopwords):
##def getngrams(tokens, n):
##def getstoplist(filename):
##def isplural(thisword, goodwordsjustwords, stopwords):
##def predictauthor(text, featuredatabase):
##def printdict(label, thedict):
##def printdictflipped(label, thedict):
##def printoutput(outString, outFile):
##def removenonalpha(charlist):
##def splitintosentences(tokens):
##def tokenize(text):
##def tostring(whatever):
##def tostringlist(label, thelist):
##def tostringdict(label, thedict):
##def tostringdictflipped(label, thedict):
##def updatecounts(author, text, featuredatabase):

######################################################################
##
import sys
from collections import defaultdict
from math import log

######################################################################
## CHECK ARGUMENTS
def checkArgs(number, message):
    if len(sys.argv) != number:
        print(message)
        sys.exit(1)

######################################################################
## LOWERCASE ALL THE WORDS IN A LIST OF TOKENS
def lowercasethelist(tokens):
    ttt = []
    for word in tokens:
        word = word.lower()
        ttt.append(word)
    return ttt

######################################################################
## PRINT A LIST WITH A LABEL (OR NOT)
def printlist(label, thelist):
    for item in thelist:
        if 0 == len(label):
            print('%s\n' % (str(item)))
        else:
            print('%s %s\n' % (label, str(item)))
    return

######################################################################
## PRINT A LIST WITH A LABEL TO A FILE (OR NOT)
def printlisttofile(outfile, label, thelist):
    for item in thelist:
        if 0 == len(label):
            outfile.write('%s\n' % (str(item)))
        else:
            outfile.write('%s %s\n' % (label, str(item)))
    return


######################################################################
## print log information to the console and the output file
def printoutput(outstring, outfile):
    print(outstring)
    outfile.write('%s\n' % (outstring))
    outfile.flush()

######################################################################
## READ A FILE AND RETURN A STRING
def readfile(filepath):
    print("readfile: Read from filepath '%s'" % (filepath))
    fileptr = open(filepath)
    text = fileptr.read()
    return text

#######################################################################
### ADD A FILE TO THE FEATURE DATABASE
#def addfiletodatabase(filename, featuredatabase):
#    return updatecounts(extractauthor(filename), extractfeatures(filename), featuredatabase)
#
#######################################################################
### THIS REQUIRES A DEFAULTDICT AND NOT JUST A DICT
#def addtofreqs(charlist, freqs):
#    for char in charlist:
#        freqs[char] = freqs[char] + 1
#    return freqs
#
#######################################################################
### CLASSIFY BASED ON A SCORES DICTIONARY
#def classify(scores):
#    currentauthor = ""
#    currentbayes = 0.0
#    for author, bayes in scores.items():
#        if bayes > currentbayes:
#            currentauthor = author
#            currentbayes = bayes
#    return currentauthor
#
#######################################################################
### CLEAN UP THE CHARACTERS, REMOVE PUNCTUATION, FIX DIACRITICALS, ETC.
#def cleanupcharacters(text):
#    charstoclean = list(",.;:()[]{}`'?!")
#    charstoclean2 = list("\xd0\xd1\xd2\xd3\xd4\xd5") # smart quotes, etc.
#    newtext = ""
#    textsplit = text.split()
#    for word in textsplit:
#        newword = ""
#        for i in range(0, len(word)):
#            char = word[i]
#            char = char.lower()
#            if char in charstoclean:
#                char = " "
#            if char in charstoclean2:
#                char = " "
#            if char == '\x88':
#                char = "a"
#            if char == '\x8e':
#                char = "e"
#            if char == '\x8f':
#                char = "e"
#            if char == '\x92':
#                char = "i"
#            newword = newword + char
#        newtext = newtext + " " + newword
#    return newtext
#
#######################################################################
### COMPUTE AUTOMATIC READABILITY INDEX
#def computeARI(sentences):
#    info = extractcounts(sentences)
#    ari = 4.71 * info[0] / info[1] + 0.5 * info[1] / info[2] - 21.43
#    return ari
#
#######################################################################
### COMPUTE THE FREQS OF TOKENS IN A LIST OF TOKENS
#def computefreqs(tokens):
#    freqs = defaultdict(int)
#    for token in tokens:
#        freqs[token] = freqs[token] + 1
#    return freqs
#
#######################################################################
### COMPUTE LETTER FREQS OF WORDS IN A TOKEN LIST
#def computeletterfreqs(tokens):
#    freqs = defaultdict(int)
#    lettercount = 0
#    for token in tokens:
#        tokensplit = list(token)
#        for letter in tokensplit:
#            if not letter.isalpha(): continue
#            freqs[letter] = freqs[letter] + 1
#            lettercount += 1
#    return (lettercount, freqs)
#
#######################################################################
### EXTRACT AUTHOR FROM FILENAME
#def extractauthor(filename):
#    name = filename
#    pos = name.rfind("/")
#    if pos >= 0:
#        name = name[pos+1:]
#    pos = name.find("-")
#    return name[0:pos]
#
#######################################################################
### EXTRACT CHARACTER, WORD, AND SENTENCE COUNTS
#def extractcounts(sentences):
#    charcount = 0
#    wordcount = 0
#    for sent in sentences:
#        for word in sent:
#            charcount = charcount + len(word)
#            wordcount = wordcount + 1
#    return ( charcount, wordcount, len(sentences) )
#
#######################################################################
### EXTRACT FEATURES FROM A FILE
#def extractfeatures(filename):
#    text = readfile(filename)
#    tokenized = tokenize(text)
#    return tokenized
#
#######################################################################
### FLIP FIRST AND SECOND ITEMS (AS NEEDED FOR FREQS)
#def flipdict(thedict):
#  newdict = defaultdict()
#  for first, second in thedict.items():
#    newdict[second] = first
#  return newdict
#
#######################################################################
### GET THE 'ING' STEM OF A WORD, OR ELSE AN EMPTY WORD
#def getingstem(thisword, goodwordsjustwords, stopwords):
#    theword = thisword[0]
#    if len(theword) < 3:
#        return ""
#    thestem = theword[0:len(theword)-3]
##    print "STEMMING", theword, thestem
#    if theword[len(theword)-3:] == "ing":
#        thestem2 = thestem + 'e'
#        if thestem in stopwords:
#            print "STEMMINGA STOPSTD", theword, thestem
#            return thestem
#        elif thestem2 in stopwords:
#            print "STEMMINGB STOPSTD", theword, thestem2
#            return thestem2
#        elif thestem in goodwordsjustwords:
#            print "STEMMINGA GOOD", theword, thestem
#            return thestem
#        elif thestem2 in goodwordsjustwords:
#            print "STEMMINGB GOOD", theword, thestem2
#            return thestem2
#        else:
#            print "STEMMINGA BAD", theword, thestem, thestem2
#            return ""
#    else:
#        return ""
#
#######################################################################
### GET NGRAMS
#def getngrams(tokens, n):
#    thengrams = []
#    i = 0
#    while i < len(tokens):
#        if i+n < len(tokens):
#            ngram = tokens[i:i+n]
#            thengrams.append(ngram)
#        i = i + 1
#    return thengrams
#
#######################################################################
### FUNCTION TO GET A STOPLIST
#def getstoplist(filename):
#    stoplistfile = open(filename)
#    stoplist = stoplistfile.read()
#    stoplistfile.close()
#    stoplist = stoplist.split()
#    return stoplist
#
#######################################################################
### TEST TO SEE IF A WORD IS A PLURAL
#def isplural(thisword, goodwordsjustwords, stopwords):
#    theword = thisword[0]
#    thestem = theword[0:len(theword)-1]
#    if theword[len(theword)-1] == "s":
#        if thestem in stopwords:
#            return True
#        elif thestem in goodwordsjustwords:
#            return True
#        else:
#            return False
#    else:
#        return False
#
#######################################################################
### LOG PROBABILITY
#def logprobability(featurecounts, featuressum, nfeatures):
#    return log((featurecounts + 1.0) / (featuressum + nfeatures))
#
#######################################################################
### PREDICT AUTHOR FROM THE FEATURES
#def predictauthor(text, featuredatabase):
#    return classify(score(extractfeatures(text), featuredatabase))
#
#######################################################################
### PRINT A DICT AS KEY AND VALUE
#def printdict(label, thedict):
#    for first, second in thedict.items():
#        print label, first, second
#    return
#
#######################################################################
### PRINT A DICT FLIPPED AS VALUE AND KEY
#def printdictflipped(label, thedict):
#    for first, second in thedict.items():
#        print label, second, first
#    return
#
#######################################################################
### REMOVE NONALPHABETIC CHARACTERS FROM A LIST OF CHARS
#def removenonalpha(charlist):
#    newlist = list()
#    for char in charlist:
#        if char.isalpha():
#            newlist = newlist + [ char ]
#    return newlist
#
#######################################################################
### SPLIT INTO SENTENCES
#def splitintosentences(tokens):
#    SENTENCEENDINGS = ( ".", "!", "?" )
#    sentenceslist = []
#    sent = [] 
#    for token in tokens:
#        sent = sent + [ token ]
#        if token in SENTENCEENDINGS:
#            sentenceslist = sentenceslist + [ sent ]
#            sent = [] 
#    if len(sent) > 0: 
#        sentenceslist = sentenceslist + [ sent ]
#    return sentenceslist
#
#######################################################################
### TOKENIZE A TEXT STRING ON PUNCTUATION AND WHITESPACE
#def tokenize(text):
#    PUNCT = ( ".", ",", ";", ":", "(", ")", "[", "]", "{", "}", "!", "?", '"', "'", "`", "/",     "\\" '\xd0', '\xd1', '\xd2', '\xd3', '\xd4', '\xd5' )
#    WHITESPACE = ( " ", "\t", "\r", "\n" )
#    texttokens = []
#    token = ""
#    for i in range(0, len(text)):
#        if text[i] in PUNCT:
#            if len(token) > 0:
#                texttokens = texttokens + [ token ]
#            texttokens = texttokens + [ text[i] ]
#            token = ""
#        elif text[i] in WHITESPACE:
#            if len(token) > 0:
#                texttokens = texttokens + [ token ]
#            token = ""
#        else:
#            token = token + text[i]
#    if len(token) > 0:
#        texttokens = texttokens + [ token ]
#    return texttokens
#
#######################################################################
### TOSTRING FUNCTION FOR A NONTRIVIAL CONSTRUCT
#def tostring(whatever):
#    return whatever.__str__() + '\n'
#
#######################################################################
### TOSTRING A LIST
#def tostringlist(label, thelist):
#    s = ""
#    for item in thelist:
#        s = s + ('%s ' % label) + item.__str__() + '\n'
#    return s
#
#######################################################################
### TOSTRING A DICT
#def tostringdict(label, thedict):
#    s = ""
#    for first, second in thedict.items():
#        s = s + ('%s ' % label) + first.__str__() + " " + second.__str__() + '\n'
#    return s
#
#######################################################################
### TOSTRING A DICT FLIPPED
#def tostringdictflipped(label, thedict):
#    s = ""
#    for first, second in thedict.items():
#        s = s + ('%s ' % label) + second.__str__() + " " + first.__str__() + '\n'
#    return s
#
#######################################################################
### UPDATE COUNTS IN FEATURE DATABASE
#def updatecounts(author, text, featuredatabase):
#   for word in text:
#       featuredatabase[author][word] += 1
#   return featuredatabase
###
