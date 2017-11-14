# text_processing
A repository for text_processing tools used by crow

Included below is a description of tools used:

#### conversion tools

* cp1251_to_utf8.py is a python script which converts files encoded in Windows 1251 into UTF-8

* Aextractzip2txt.py is a python script which takes a directory of zip files; assuming the name ends in 'zips' or zips/' and unzips the folder as well as converts all the docx files into txt files.  It then put the new txt into a new directory with 'zips' stripped off the dir name.  This script requires the dabfunctions.py script to run.

* Fcheckdraftandfinal.py is a python script which checks filenames for draft and final in the name and then switches them.  Draft becomes the final, and final turns into a draft.  This script requires the dabfunctions.py script to run.

* dabfunctions.py is a helper script that contains many useful functions (some are commented out).  Fcheckdraftandfinal.py and Aextractzip2txt.py both rely on this script.

#### de-identification

#### normalization

* textnormalization.py is a text cleaning script, it replaces punctuation such as smart quotes, ellipsis, dashes with a regular hyphen, and other non-english characters

#### tagging
