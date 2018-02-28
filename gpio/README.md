## General Purpose Input-Output Script
Given a single file or directory provided by the user, this script
sends each file, one at a time, to a generic `process()` function.
This `process()` function exists in `process_script.py` and may be
modified as needed for actual processing.

### Example command for processing a single file called "text.txt"
        $ python gpio.py --file=text.txt
### Example command for processing an entire directory called "input"
        $ python gpio.py --directory=input

An optional argument, `--overwrite`, may be passed along with the 
file or directory, and will save any changes to the same location
as the originating file. The default behavior, otherwise, is to
save identically named file(s) to an "output" directory.

The `process()` function receives the contents of each file as its
input, and should return the (modified) contents of the file as 
its output.