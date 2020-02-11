# Purpose: combine two tabs in a registrar-data file, and then add the selected instructor info (the output file of instructor_info.py)
# To run this script in Anaconda: python registrar_data_modify.py --input_file1=summer2017_registrar.xlsx --input_file2=instructor_selected_info.csv --output_file=modified_registrar_data.xlsx

import argparse
import csv
import pandas
from pandas import DataFrame

#Define the arguments sent to the script
parser = argparse.ArgumentParser(description='Create merged spreadsheet')
parser.add_argument('--input_file1', action='store',dest='input_file1',default='')
parser.add_argument('--input_file2',action='store',dest='input_file2',default='')
parser.add_argument('--output_file', action='store',dest='output_file',default='')
args = parser.parse_args()

#create a function to combine tabs in a registrar file, for example summer2017_registrar.xlsx
def combine_tabs(filename):
	if '.xlsx' in filename or '.xls' in filename:
		print("Opening file" + filename)
		Data = pandas.ExcelFile(filename)
		Mastertab = pandas.read_excel(Data,0) # mastertab is the first tab in an excel file
		Scoretab = pandas.read_excel(Data,1) # scoretab is the second tav in an excel file 
		Scoretab_Dict = Scoretab.set_index('ID').T.to_dict()
		
		# for each ID in the ID column in the mastertab, if a ID matches the key in Scoretab_Dict, then add values of the Scoretab_Dict to new columns in the mastertab 
		for ID in Mastertab['ID']:
			if ID in Scoretab_Dict:
				#print('match:',ID)
				# add values to the a new column is the master tab one by one
				Mastertab['A01 - ACT English'] = [Scoretab_Dict[ID]['A01 - ACT English'] for ID in Mastertab['ID']]
				Mastertab['A02 - ACT Math'] = [Scoretab_Dict[ID]['A02 - ACT Math'] for ID in Mastertab['ID']]
				Mastertab['A03 - ACT Reading'] = [Scoretab_Dict[ID]['A03 - ACT Reading'] for ID in Mastertab['ID']]
				Mastertab['A04 - ACT Science Reasoning'] = [Scoretab_Dict[ID]['A04 - ACT Science Reasoning'] for ID in Mastertab['ID']]
				Mastertab['A07 - ACT Combined English/Writing'] = [Scoretab_Dict[ID]['A07 - ACT Combined English/Writing'] for ID in Mastertab['ID']]
				Mastertab['A05 - ACT Composite'] = [Scoretab_Dict[ID]['A05 - ACT Composite'] for ID in Mastertab['ID']]
				Mastertab['S01 - SAT Critical Reading'] = [Scoretab_Dict[ID]['S01 - SAT Critical Reading'] for ID in Mastertab['ID']]
				Mastertab['S02 - SAT Mathematics'] = [Scoretab_Dict[ID]['S02 - SAT Mathematics'] for ID in Mastertab['ID']]
				Mastertab['S07 - SAT Writing'] = [Scoretab_Dict[ID]['S07 - SAT Writing'] for ID in Mastertab['ID']]
				Mastertab['TIBL - TOEFL IBT Listening Score'] = [Scoretab_Dict[ID]['TIBL - TOEFL IBT Listening Score'] for ID in Mastertab['ID']]
				Mastertab['TIBR - TOEFL IBT Reading Score'] = [Scoretab_Dict[ID]['TIBR - TOEFL IBT Reading Score'] for ID in Mastertab['ID']]
				Mastertab['TIBS - TOEFL IBT Speaking Score'] = [Scoretab_Dict[ID]['TIBS - TOEFL IBT Speaking Score'] for ID in Mastertab['ID']]
				Mastertab['TIBW - TOEFL IBT Writing Score'] = [Scoretab_Dict[ID]['TIBW - TOEFL IBT Writing Score'] for ID in Mastertab['ID']]
				Mastertab['TIBT - TOEFL IBT Total Score'] = [Scoretab_Dict[ID]['TIBT - TOEFL IBT Total Score'] for ID in Mastertab['ID']]
				Mastertab['ILT1 - IELTS Listening'] = [Scoretab_Dict[ID]['ILT1 - IELTS Listening'] for ID in Mastertab['ID']]
				Mastertab['ILT2 - IELTS Overall'] = [Scoretab_Dict[ID]['ILT2 - IELTS Overall'] for ID in Mastertab['ID']]
				Mastertab['ILT3 - IELTS Reading'] = [Scoretab_Dict[ID]['ILT3 - IELTS Reading'] for ID in Mastertab['ID']]
				Mastertab['ILT4 - IELTS Speaking'] = [Scoretab_Dict[ID]['ILT4 - IELTS Speaking'] for ID in Mastertab['ID']]
				Mastertab['ILT5 - IELTS Writing'] = [Scoretab_Dict[ID]['ILT5 - IELTS Writing'] for ID in Mastertab['ID']]
			
			# If IDs between the two tabs do not match then print NA
			else:
				Mastertab['A01 - ACT English'] = 'NA'
				Mastertab['A02 - ACT Math'] = 'NA'
				Mastertab['A03 - ACT Reading'] = 'NA'
				Mastertab['A04 - ACT Science Reasoning'] = 'NA'
				Mastertab['A07 - ACT Combined English/Writing'] = 'NA'
				Mastertab['A05 - ACT Composite'] = 'NA'
				Mastertab['S01 - SAT Critical Reading'] = 'NA'
				Mastertab['S02 - SAT Mathematics'] = 'NA'
				Mastertab['S07 - SAT Writing'] = 'NA'
				Mastertab['TIBL - TOEFL IBT Listening Score'] = 'NA'
				Mastertab['TIBR - TOEFL IBT Reading Score'] = 'NA'
				Mastertab['TIBS - TOEFL IBT Speaking Score'] = 'NA'
				Mastertab['TIBW - TOEFL IBT Writing Score'] = 'NA'
				Mastertab['TIBT - TOEFL IBT Total Score'] = 'NA'
				Mastertab['ILT1 - IELTS Listening'] = 'NA'
				Mastertab['ILT2 - IELTS Overall'] = 'NA'
				Mastertab['ILT3 - IELTS Reading'] = 'NA'
				Mastertab['ILT4 - IELTS Speaking'] = 'NA'
				Mastertab['ILT5 - IELTS Writing'] = 'NA'
		
		return (Mastertab)

# Create a function to build data frame
def build_data_frame (filename):
	File = filename
	Data = pandas.read_csv(File)
	Data_Frame = pandas.DataFrame(Data)
	return (Data_Frame)
	
# Combine the two tabs in summer2017_registrar.xlsx	
Combined_Registrar_Info = combine_tabs(args.input_file1)
#Start_Crow_ID = 11168 #the last student ID in data depot is 11167 (then plus 1 is the start_Crow_ID)
#Combined_Registrar_Info['Crow ID'] = Combined_Registrar_Info.index + Start_Crow_ID

# Create a data frame for the instructor selected info (the output file of instructor_info.py)
Instructor_Selected_Info = build_data_frame(args.input_file2)

# Build a two-dimension dictionary for the selected instructor info, see the example below
# for example {CRN1:{'semester':'fall2017','instructor_name': 'Lee Jordan', 'instructor code':'2001'},
#			  {CRN2:{'semester':'fall2018','instructor_name': 'Cody Chen', 'instructor code':'2002' ...}
Data_Dict = Instructor_Selected_Info.set_index('CRN').T.to_dict()

# for each item in the CRN column of summer2017_registrar.xlsx
for Item in Combined_Registrar_Info['COURSE_REFERENCE_NUMBER']:
	# if a CRN is in the two-dimension dictionary (built above), then assigne different info related to this CRN to different and new columns in the master sheet with the registrat info for summer 2017
	if Item in Data_Dict:
		Combined_Registrar_Info['Semester'] = [Data_Dict[Item]['Semester'] for Item in Combined_Registrar_Info['COURSE_REFERENCE_NUMBER']]
		Combined_Registrar_Info['Instructor_First_Name'] = [Data_Dict[Item]['Instructor_First_Name'] for Item in Combined_Registrar_Info['COURSE_REFERENCE_NUMBER']]
		Combined_Registrar_Info['Instructor_Last_Name'] = [Data_Dict[Item]['Instructor_Last_Name'] for Item in Combined_Registrar_Info['COURSE_REFERENCE_NUMBER']]
		Combined_Registrar_Info['Instructor_Code'] = [Data_Dict[Item]['Instructor_Code'] for Item in Combined_Registrar_Info['COURSE_REFERENCE_NUMBER']]
	# else add 'N/A' to the new columns but this is not supposed to happen.
	else:
		Combined_Registrar_Info['Semester'] = 'NA'
		Combined_Registrar_Info['Instructor_First_Name'] = 'NA'
		Combined_Registrar_Info['Instructor_Last_Name'] = 'NA'
		Combined_Registrar_Info['Instructor_Code'] = 'NA'

# Output the finalized registrar: student registar info with the selected instructor info 
Combined_Registrar_Info.to_excel(args.output_file, index = False)
print ('Done.')