'''
Script Written: 12/7/17

Author: Nik Kirstein

Description:
From a directory with directories that have a bunch of zip files in them,
this script loops through all those folders and unzips all the files in them into 
regular subfolders of the same file name.
'''


import os
import zipfile


    
def get_directory_list():
    '''
    Gets a list of directories from the location the script is run.
    Checks if the items in the current directory has a . in it, which 
    probably means it is a file and not a folder, and excludes these.
    
    Parameters: None
    Returns: A newly created list of ONLY the folders in the current directory of the script.
    '''

    new_directory_list = []
    
    directory_list = os.listdir()
    for item in directory_list:
        if '.' in item:
            # skip files that contain a . which means they aren't folders but some other kind of file type
            pass
        else:
            new_directory_list.append(item)
        
    return new_directory_list
    
    
def unzip_files(file_list):
    '''
    unzips all the files in the current directory 
    into a folder with the same name as the zip file
    
    Parameters: file_list is a list of all the zip files in the directory
    Returns: None, it should have created new folders with the contents of the zip file.
    '''
    for zip in file_list:
        zip_file_name = zip.split('.')[0]
        zip_ref = zipfile.ZipFile(zip, 'r')
        zip_ref.extractall(os.getcwd() + "/" + zip_file_name)
        zip_ref.close()
    
    
    
def sub_directory_looper_unzipper(directory_list):
    '''
    Loops through all subdirectorys in the current directory using a list
    Calls the unzip_files function to unzip all zip files in that folder into 
    a folder of the same name as the zip file, which will be a subdirectory of the subdirectory
    
    Parameters: directory_list is a list of the current folders where the script is run
    Returns: None
    '''
    for folder in directory_list:
        current_path = os.getcwd()
        os.chdir(current_path + "/" + folder)
        sub_directory_list = os.listdir()
        unzip_files(sub_directory_list)
        
        # return to the directory above
        os.chdir("..")
        
    
    
    
# the main method of our python script.
if __name__ == "__main__":

    total_directory_list = get_directory_list()
    #print(total_directory_list)
    sub_directory_looper_unzipper(total_directory_list)
    
    
    