#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:41:44 2020

@author: CCloveHH
"""

#Task: To combine UA registar data & the Purdue registrar data
#Step1: Create a demonstration data
#Step2: Read both data
#Step3:
# add a column in Purdur_registar_data, institution, and fill the column
# ompare colum difference (UA-Purdue)
# Catalog Nbr - COURSE_NUMBER
# Class Section - COURSE_REFERENCE_NUMBER
# Registrar ID - PERSON_UID
# First Name - FIRST_NAME
# Last Name - LAST_NAME
# Acad Level - STUDENT_CLASS_BOAP_DESC (different in cell naming)
# College - COLLEGE_DESC
# Major - PROGRAM_DESC (different naming)
# Birth Country Code- NATION_OF_CITIZENSHIP (different naming) * CHN vs CN
# Gender - GENDER
# TOFEL COMPI - TIBT - TOEFL IBT Total Score
# TOEFL Listening - TIBL - TOEFL IBT Listening Score
# TOEFL Reading - TIBR - TOEFL IBT Reading Score
# TOEFL Writing - TIBW - TOEFL IBT Writing Score
# TOEFL Speaking - TIBS - TOEFL IBT Speaking Score
# Crow ID - Crow ID
# Instructor Code - Instructor_Code
# Alternate Name - PREFERRED_FIRST_NAME
# term - Semester
# mode_of_course - ???
# length_of_course -???
# institution - ??? 

import pandas as pd
import re

UA = pd.read_excel('/Users/CCloveHH/Desktop/Intern_script/raw_registrar_data/UA_registrar_demo.xlsx')
PU = pd.read_excel('/Users/CCloveHH/Desktop/Intern_script/raw_registrar_data/Purdue_registrar_demo.xlsx')
Merge = pd.ExcelWriter('Merge.xlsx', engine = 'xlsxwriter') #create a new excel file
Merge.save()

PU['institution'] = ""       # add a new empty column to Purdue Dataframe
PU['institution'] = "Purdue University"  # fill the new_created column with institution name

PU.rename(columns = {'COURSE_NUMBER':'Catalog Nbr',
                     'COURSE_REFERENCE_NUMBER':'Class Section',
                     'PERSON_UID':'Registrar ID',
                     'FIRST_NAME':'First Name',
                     'LAST_NAME':'Last Name',
                     'STUDENT_CLASS_BOAP_DESC':'Acad Level',
                     'COLLEGE_DESC':'College',
                     'PROGRAM_DESC':'Major',
                     'NATION_OF_CITIZENSHIP':'Birth Country Code',
                     'GENDER':'Gender',
                     'TIBT - TOEFL IBT Total Score':'TOEFL COMPI',
                     'TIBL - TOEFL IBT Listening Score':'TOEFL Listening',
                     'TIBR - TOEFL IBT Reading Score':'TOEFL Reading',
                     'TIBW - TOEFL IBT Writing Score':'TOEFL Writing',
                     'TIBS - TOEFL IBT Speaking Score':'TOEFL Speaking',
                     'Instructor_Code':'Instructor Code',
                     'PREFERRED_FIRST_NAME':'Alternate Name',
                     'Semester':'term'}, 
          inplace = True)  # rename the column name in Purdue data, to align with that in UA data. 

PU = PU.replace(to_replace = r'Freshman.+', value = '1', regex = True)
PU = PU.replace(to_replace = r'Sophomore.+', value = '2', regex = True)
PU = PU.replace(to_replace = r'Junior.+', value = '3', regex = True)
PU = PU.replace(to_replace = r'Senior.+', value = '4', regex = True)

PU["Catalog Nbr"] = PU["Catalog Nbr"]//100

Merge = pd.concat([UA,PU], join = "inner") #combine the two dataframe with overlapping columns



Merge.to_excel('Merge.xlsx')
print(Merge)

