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
    Gets the three/four Capital letter string(s) of the investigator from a file
    
    Parameters:
    file_input is the file to be opened and read.
    
    returns:
    investigator_str_list: a list of the three/four capital letters of the investigators
    '''
    investigator_str_list = []

    for line in f:
        if line[1:3] == 'ID' and any(x in line for x in ('Investigator', 'ShowHost', 'Teacher')):
            line_investigator_list = line.split("|")
            investigator_str_list.append(line_investigator_list[2])
        
    #Believe it or not, some files don't have any investigators.  Fill in with default string to ignore.
    #Not filling this in, breaks some of the checks.
    if len(investigator_str_list) == 0:
        investigator_str_list.append('NOINV')        
            
    return investigator_str_list
    
            
def get_participation_from_file(file_input):
    '''
    Gets the three/four capital letter strings of participants from a file into alist.
    
    Parameters:
    file_input is the file to be opened and read.
    
    returns:
    participation_list: a list of the three/four capital letter strings of participants
    '''
    participation_list = []
    
    for line in f:
        if (line[1:3] == 'ID' and any(x in line for x in ('Participant', 'Subject', 'Undergraduate', 'Student', 'Child', 'Partner'))):
            line_participation_list = line.split("|")
            #print(line_participation_list[2])
            participation_list.append(line_participation_list[2])
            #print(participation_list, line_participation_list[2])
            
    return participation_list            
            

def get_write_string(current_file):
    '''
    This function looks at the current file and reads all the lines.  
    It then processes them and edits them and produces new lines which are
    written to a string and then this function returns that writable string.
    
    It initializes an empty string, write_string that adds the new and edited lines
    to itself to be returned.
    
    prev_line is a pointer that obviously points to the previous line in the file.
    
    returns:
    write_string: the full file contents, edited and processed in one string. Ready to write.
    '''
    prev_line = ""
    write_string = ""
    
    current_investigator_list = get_investigator_from_file(current_file)
    current_file.seek(0) #reset looking in the file because we traversed it a little to get the list
    
    current_participation_list = get_participation_from_file(current_file)
    current_file.seek(0) #reset looking in the file because we traversed it a little to get the list
    
    print('Processing: ', current_file.name)
    #print('Investigator list: ', current_investigator_list)
    #print('participant list: ', current_participation_list)
    
    for line in current_file:

        line_list = list(line)
        
        if line[0] == '@':
            '''
            replace all @ with < and end the line with a >
            '''
            line_list[0] = "<"
            index_to_insert = len(line_list) - 1
            line_list.insert(index_to_insert, ">")
            new_line = "".join(line_list)
            write_string += new_line
            
        elif line[0] == "%":
            '''
            Encapsulate lines that start with % in <>
            '''
            line_list.insert(0, "<")
            index_to_insert = len(line_list) - 1
            line_list.insert(index_to_insert, ">")
            new_line = "".join(line_list)
            write_string += new_line

        elif line[1:(len(current_investigator_list[0])+1)] in current_investigator_list and line[0] == '*':
            '''
            mark off the interviewer with < > as well so we only
            really look at the speakers words 
            '''
            line_list.insert(0, "<")
            index_to_insert = len(line_list) - 1
            line_list.insert(index_to_insert, ">")
            new_line = "".join(line_list)
            write_string += new_line 
        
        elif line[1:(len(current_participation_list[0])+1)] in current_participation_list and line[0] == '*':
            '''
            mark off interviewee with <> only around the 
            ID only
            '''
            line_list.insert(0, "<")
            line_list.insert(6, ">")
            new_line = "".join(line_list)
            write_string += new_line
        
        elif line[0] == "\t" and new_line[(len(new_line)-2)] == ">":
            '''
            If the previous newly formatted line ends in >, it means the next tabbed lines
            are apart of that, so they also need to be marked off with <>
            '''
            line_list.insert(0, "<")
            index_to_insert = len(line_list) - 1
            line_list.insert(index_to_insert, ">")
            new_line = "".join(line_list)
            write_string += new_line
        
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
 