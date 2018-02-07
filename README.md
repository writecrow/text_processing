# text_processing
A repository for text_processing tools used by crow

Included below is a description of tools used:

#### conversion tools

* convert_to_utf8.py is a command-line script for semi-intelligently converting files from known encoding 
formats into the UTF-8 charset. It will convert entire directories or individual files, and can either
overwrite the files or put them in a parallel `output` directory

* cp1251_to_utf8.py is a python script which converts files encoded in Windows 1251 into UTF-8

* Mass_directory_unzipper.py is a python script that loops through all folders in a current directory and looks inside them for zipfiles.  If zipfiles exist, this script will unzip them and place the contents into a regular folder of the same name as the zip file.

* Aextractzip2txt.py is a python script which takes a directory of zip files; assuming the name ends in 'zips' or zips/' and unzips the folder as well as converts all the docx files into txt files.  It then put the new txt into a new directory with 'zips' stripped off the dir name.  This script requires the dabfunctions.py script to run.

* Fcheckdraftandfinal.py is a python script which checks filenames for draft and final in the name and then switches them.  Draft becomes the final, and final turns into a draft.  This script requires the dabfunctions.py script to run.

* dabfunctions.py is a helper script that contains many useful functions (some are commented out).  Fcheckdraftandfinal.py and Aextractzip2txt.py both rely on this script.

#### de-identification

#### normalization

* textnormalization.py is a text cleaning script, it replaces punctuation such as smart quotes, ellipsis, dashes with a regular hyphen, and other non-english characters

* FS_general_formatter.py is a text cleaning script, it is used to process data from FLLOC and SPLLOC files.  It replaces lines that begin @ and encases the lines in <> brackets.  It also encases the interviewer of the transcriptions in <> brackets. It should be ran with an argument specifying the kind of file and directory depth like such: **/**/*.cha or **/*.cex depending on your directory structure.  This script will read the files, and after modifying their text, write them to txt in a directory called "recoded" that mimics the initial file structure within the folder.  

#### tagging

#### text-retrieval

* FLLOC_Scraper.py is a script for downloading all zip files off of the FLLOC corpora website.  It is a slow script, last tested to take up to 17 minutes to complete all the downloads.  If this script errors for some reason, mentioning a blocked port, simply delete the data, wait a bit, and restart the script.
