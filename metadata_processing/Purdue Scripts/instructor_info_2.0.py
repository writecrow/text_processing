# Purpose: create a instructor info sheet with required info (semester, Subject, Course#, CRN, instructor name, instructor code), which will be combined with student info sheet (the registrar data). 
# To run this script in Anaconda: python instructor_info.py --input_file1= instrucor_code.csv --input_file2=instructor_list.csv --output_file=instructor_selected_info.csv

import argparse
import csv
import pandas
from pandas import DataFrame

# Define the arguments send to the script
# The first input file is instrucor_code.csv
# The second input file is instrucor_list.csv
parser = argparse.ArgumentParser(description='Create merged spreadsheet')
parser.add_argument('--input_file1', action='store',dest='input_file1',default='')
parser.add_argument('--input_file2',action='store',dest='input_file2',default='')
parser.add_argument('--output_file', action='store',dest='output_file',default='')
args = parser.parse_args()

# Create a function to build data frame
def build_data_frame (filename):
	File = filename
	Data = pandas.read_csv(File)
	Data_Frame = pandas.DataFrame(Data)
	return (Data_Frame)

# Build a data frame based on the instrucor_code.csv
Data_Frame1 = build_data_frame(args.input_file1)

# Create a dictionary: mapping between instructor's career account (Key) and the instructor code (Value)
Selected_Data_Frame1 = Data_Frame1[['Instructor_Career_Account','Instructor_Code']]
Data_Dict = pandas.Series(Selected_Data_Frame1.Instructor_Code.values,index=Selected_Data_Frame1.Instructor_Career_Account).to_dict()
#print(Data_Dict)

# Build a data frame based on the instrucor_list.csv
Data_Frame2 = build_data_frame(args.input_file2)

# Assign instructor code to Data_Frame2
# for each item in the column of "instrucotr_career_account" in instrucotr_list.csv
for Item in Data_Frame2['Instructor_Career_Account']:
	# if the item is also in the Data_dict, then use this item as the key to map the value (instructor code) in the Data_Dict and assign the value to a new column (instructor code) in the instrucotr_list.csv
	if Item in Data_Dict:
		Data_Frame2['Instructor_Code'] = [Data_Dict[Item] for Item in Data_Frame2['Instructor_Career_Account']]
	# else, add 'N/A" to this new column
	else:
		Data_Frame2['Instructor_Code'] = 'NA'		
print(Data_Frame2)

# Output the selected instructor information to a new file, which will be combined with the student registrar information
Instructor_Selected_Info = Data_Frame2[['Semester','Subject','Course#','CRN','Instructor_First_Name','Instructor_Last_Name','Instructor_Code']]
Instructor_Selected_Info.to_csv(args.output_file, index = False) #check this new file. 
