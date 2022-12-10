# Workflow notes


## Generating a metadata spreadsheet for files with Group IDs.

- Prerequisite: a metadata spreadsheet with institutional group IDs and Crow student IDs.

1. Download  metadata spreadsheet to the `metadata_processing` folder.
2. Run a command like the following (more notes on command syntax in the python file itself). You will be prompted for a starting Crow Group ID. This will need to be the **next** number in order of any existing Crow Group IDs in the system (across all institutions):

```
 python3 purdue_add_crow_group_ids_to_metadata.py --metadata=modified_registrar_FYE_updated.xlsx

Provide a starting number for the Crow Group IDs: 1000

Successfully processed.
```

This will generate a file named something like `modified_registrar_FYE_updated_processed.csv`

3. Move this new file to the `headers` folder.

4. Download the student texts to the `headers` folder.

5. Run a command similar to the following:

```
python3 purdue_add_headers.py --directory=fye-data --master_file=modified_registrar_FYE_updated_processed.csv --cms=blackboard
```

You should get output like this (along with any reports of processing problems):

```
***************************************
Files found:     944
Files processed: 944
***************************************
```




