'''
Script Written: 1/30/18


Description:
Text Processor for FFLOC data.  Goes through a directory full of folders than contain cex files and cha files.  It reads these files and then takes the data and outputs it in to a newly formatted file.
'''
import io
import os
import sys
import glob

def get_investigator_from_file(file_input):
    '''
    Gets the three Capital letter string of the investigator from a file
    
    Parameters:
    file_input is the file to be opened and read.
    
    returns:
    investigator_str: a string of the three capital letters of the investigator
    '''

    for line in f:
        if line[1:3] == 'ID' and "Investigator" in line:
            line_investigator_list = line.split("|")
            investigator_str = line_investigator_list[2]
            return investigator_str



            
            
def get_participation_from_file(file_input):
    '''
    Gets the three Capital letter string of the investigator from a file
    
    Parameters:
    file_input is the file to be opened and read.
    
    returns:
    investigator_list: a string of the three capital letters of the investigator
    '''
    participation_list = []
    
    for line in f:
        if (line[1:3] == 'ID' and "Participant" in line) or (line[1:3] == 'ID' and "Subject" in line) or (line[1:3] == 'ID' and "Undergraduate" in line) or (line[1:3] == 'ID' and "Student" in line):
            line_participation_list = line.split("|")
            participation_list.append(line_participation_list[2])
            #print(participation_list, line_participation_list[2])
            
    return participation_list            
            
            


def get_write_string(current_file):
    '''
    This function looks at the current file and reads all the lines.  
    It then processes them and edits them and produces new lines which are
    written to a string and then this function returns that writable string.
    
    It initalizes an empty string, write_string that adds the new and edited lines
    to itself to be returned.
    
    prev_line is a pointer that obviously points to the previous line in the file.
    
    returns:
    write_string: the full file contents, edited and processed in one string. Ready to write.
    '''

    current_investigator_str = get_investigator_from_file(current_file)
    current_file.seek(0)
    current_participation_list = get_participation_from_file(current_file)
    
    prev_line = ""
    write_string = ""
    
    current_file.seek(0)
    
    for line in current_file:

        if line[0] == "\t" and prev_line[0:10] == "@Situation":
            '''
            This if statement exists because for some reason, there would be a line for 
            @situation which would continue on the next line, beginning with a tab, which
            would taint the data if left un-carroted off.  This basically takes care of 
            multiline @situation problems in some files.
            '''
            line_list = list(line)
            index_to_insert = len(line_list) - 1
            line_list.insert(index_to_insert, ">")
            new_line = "".join(line_list)
            write_string += new_line

        elif line[0] == '@':
            '''
            replace all @ with < and end the line with a >
            '''
            line_list2 = list(line)
            line_list2[0] = "<"
            index_to_insert2 = len(line_list2) - 1
            line_list2.insert(index_to_insert2, ">")
            new_line2 = "".join(line_list2)
            write_string += new_line2
           #print(new_line2)
           
        
        elif line[1:4] == current_investigator_str:
            '''
            mark off the interviewer with < > as well so we only
            really look at the speakers words 
            '''
            line_list3 = list(line)
            line_list3.insert(0, "<")
            index_to_insert3 = len(line_list3) - 1
            line_list3.insert(index_to_insert3, ">")
            new_line3 = "".join(line_list3)
            write_string += new_line3 
        
        elif line[1:4] in current_participation_list:
            '''
            mark off interviewee with <> only around the 
            ID only
            '''
            line_list4 = list(line)
            line_list4.insert(0, "<")
            line_list4.insert(6, ">")
            new_line4 = "".join(line_list4)
            write_string += new_line4
            
        elif line[0] == "%":
            '''
            Encapsulate lines that start with % in <>
            '''
            line_list5 = list(line)
            line_list5.insert(0, "<")
            index_to_insert5 = len(line_list5) - 1
            line_list5.insert(index_to_insert5, ">")
            new_line5 = "".join(line_list5)
            write_string += new_line5
        
        else:
            write_string += line
            
        prev_line = line
            
    #print(write_string)                  
    return write_string
    
    
    
# the main method of our python script.
if len(sys.argv) > 1:
    # for every file entered as argument in the command line
    for file in glob.iglob('**/**/*.cha', recursive=True):
        # open the file as read-only ('r')
        with io.open(file, 'r', encoding="utf8") as f:
            #print(f)
            prepared_string = get_write_string(f)

            file_name = (f.name.split(".")[0] + ".txt")
            #print(file_name)
            file_path = os.path.join('recoded', file_name)
            #print(file_path)
            path_list = []
            path = f.name.split("\\")
            for path_item in path:
                if ".cha" not in path_item:
                    path_list.append(path_item)

            output_directory = os.path.dirname(file_path)
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)
      
            writing_file = open(file_path, "w", encoding="utf8")
            writing_file.write(prepared_string)
            writing_file.close()
            
            