#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

## Description
# Given a student metadata file and a separate file of spreadsheets with students and group IDs, generate a unique Crow group ID and add it to the metadata file.

# Usage example:
#    python purdue_add_crow_group_ids_to_metadata.py --metadata=metadata.xlsx --group_ids=group_ids.xlsx

import argparse
import re
import pandas

# Define the way we retrieve arguments sent to the script.
parser = argparse.ArgumentParser(description='Excel to CSV')
parser.add_argument('--metadata', action="store", dest='metadata', default='')
parser.add_argument('--group_ids', action="store", dest='group_ids', default='')
args = parser.parse_args()


if not args.metadata or not args.group_ids:
    print('You need to supply a valid master student and instructor codes files')
    exit()

if '.xls' in args.metadata:
    metadata_file = pandas.ExcelFile(args.metadata)
    metadata_dataframe = pandas.read_excel(metadata_file)
elif '.csv' in args.metadata:
    metadata_dataframe = pandas.read_csv(args.metadata)

group_ids_file = pandas.ExcelFile(args.group_ids)
group_ids = pandas.read_excel(group_ids_file, sheet_name=None)
group_dataframe = pandas.concat(group_ids, ignore_index=True)
students_with_group = group_dataframe['User_ID'].tolist()
existing_ids = metadata_dataframe['User_ID'].tolist()

# Get any existing ids from the current metadata.
if 'GROUP_ID' in metadata_dataframe.columns:
    existing_group_ids = metadata_dataframe['GROUP_ID'].tolist()
else:
    existing_group_ids = []
if 'CROW_GROUP_ID' in metadata_dataframe.columns:
    existing_crow_ids = metadata_dataframe['CROW_GROUP_ID'].tolist()
    # @todo get id_inc
else:
    id_inc = 1000

crow_inc = metadata_dataframe['Crow ID'].max()

group_dict = group_dataframe.to_dict(orient="records")
meta_dict = metadata_dataframe.to_dict(orient="records")

# Generate new Crow Group IDs
# This will provide one dictionary of IDs with original->crow pairs
# As well as "student_data" dictionary, keyed by student ID
# and containing both the original group ID and the Crow group ID.
ids = {}
student_data = {}
for row in group_dict:
    user_id = row['User_ID'].strip()
    if row['Group Number'] in ids:
        row['CROW_GROUP_ID'] = ids[row['Group Number']]
    else:
        row['CROW_GROUP_ID'] = id_inc
        ids[row['Group Number']] = id_inc
        id_inc+=1
    student_data[user_id] = {
        'GROUP_ID': row['Group Number'],
        'CROW_GROUP_ID': row['CROW_GROUP_ID']
    }
# Add new Crow Group IDs to metadata
for row in meta_dict:
    found = False
    if 'GROUP_ID' in row:
        if row['GROUP_ID'] != '' and row['GROUP_ID'] in ids:
            row['CROW_GROUP_ID'] = ids[row["GROUP_ID"]]
            found = True
    if not found:
        student_id = row['User_ID'].strip()
        if student_id in students_with_group:
            found = True
            student_id = student_id
            row['GROUP_ID'] = student_data[student_id]['GROUP_ID']
            row['CROW_GROUP_ID'] = student_data[student_id]['CROW_GROUP_ID']
    if not found:
        row['GROUP_ID'] = 'NA'
        row['CROW_GROUP_ID'] = 'NA'

# Add any students with group IDs that are NOT in the existing metadata
for row in group_dict:
    if row['User_ID'] not in existing_ids:
        print('New student found: ' + row['User_ID'] + '. Check spelling?')
        # meta_dict.append({
        #     'User_ID': row['User_ID'],
        #     'GROUP_ID': row['Group Number'],
        #     'CROW_GROUP_ID': row['CROW_GROUP_ID'],
        #     'Crow ID': crow_inc
        # })
        # crow_inc+=1

# Write to a new file.
output_filename = re.sub(r'.+\/|.+\\|\.xlsx?', r'', args.metadata)
output_filename += '_processed.csv'
output_filename = re.sub(r'_+', r'_', output_filename)
dataframe = pandas.DataFrame.from_dict(meta_dict)
crow_group_id = dataframe.pop("CROW_GROUP_ID")
user_id = dataframe.pop("User_ID")
crow_id = dataframe.pop("Crow ID")
group_id = dataframe.pop("GROUP_ID")
dataframe.insert(0, "CROW_GROUP_ID", crow_group_id)
dataframe.insert(0, "GROUP_ID", group_id)
dataframe.insert(0, "Crow ID", crow_id)
dataframe.insert(0, "User_ID", user_id)
dataframe.to_csv(output_filename, index=False, header=True)
print('Successfully processed.')
