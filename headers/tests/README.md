## Automated tests

This directory includes tests for ensuring expected output.

### Running the tests
From within this directory, run `python runtests.py`.

### Summary of design
1. Four test files are supplied, with made up student names in the filename.
2. A test metadata CSV is supplied with made up student metadata.
3. Four "expected output" files are added that have the expected result of running the header script.
4. A python script is provided that can be easily executed: "python runtests.py"
5. The script will run the add_headers_full_name.py script and then compare the actual output of the four files to the expected output and report any discrepancies.

### What to expect
If all 4 files match the expected output, you'll see something like this:

```
$ python runtests.py 
Running...

***************************************
Files found: 4
Files processed: 4
Files failed to process (no metadata match): 0
***************************************
```

If there are any discrepancies, the script will show you where the files differ:

```
$ python runtests.py 
Running...

***************************************
Files found: 4
Files processed: 4
Files failed to process (no metadata match): 0
************************************************************
There are differences between the expected and actual output for 101_GA_F_NA_1_F_11113_UA.txt
--- expected
+++ actual
@@ -16,7 +16,7 @@
 <Student 1>
 <Student ID: 11113>
 <Country: NA>
-<L1: English; Spanish>
+<L1: English;Spanish>
 <Heritage Spanish Speaker: Yes>
 <Year in School: 1>
 <Gender: F>
************************************************************
