# Convert to UTF-8
A command-line script for semi-intelligently converting files from known encoding formats into the UTF-8 charset.


### Sample usage
Convert a single file:

`python convert_to_utf8.py --file=myfile.txt`

Convert all files in the directory `input/` :

`python convert_to_utf8.py --directory=input`

By default, original files will be preserved and converted files will be outputted to an `output/` directory. If you wish to overwrite the existing files, use the `--overwrite` flag. Example:

`python convert_to_utf8.py --file=myfile.txt --overwrite`

### Dependencies
You will need to install chardet (e.g., `pip3 install chardet`)

### Notes
  - utf-8 is backwards-compatible with ascii, so conversion is a gesture
  - Test files came from [https://github.com/chardet/chardet/tree/master/tests](https://github.com/chardet/chardet/tree/master/tests)