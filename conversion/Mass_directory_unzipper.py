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
    
def clean_nonzip_files(file_list):
    '''
    Goes through a list of file names and removes one that are not zip files from the list.
    IE: Any file without the .zip extension will be tossed from the list.
    
    Parameters:
    file_list is a list of files (or directories)
    
    returns: None, modifies the file_list in place.
    '''
    for item in file_list:
        if '.zip' not in item:
            print(item, ': non-zipfile found in directory, skipping...\n')
            file_list.remove(item)
    
def unzip_files(file_list):
    '''
    unzips all the files in the current directory 
    into a folder with the same name as the zip file
    
    Parameters: file_list is a list of all the zip files in the directory
    Returns: None, it should have created new folders with the contents of the zip file.
    '''
    for zip in file_list:
        zip_file_name = zip.split('.')[0]

        #Checking if zipfile is valid.
        if zipfile.is_zipfile(zip):
            zip_ref = zipfile.ZipFile(zip, 'r')
            zip_member_list = zip_ref.infolist()
        
            #archive_file is actually a zipinfo object that contains data about the files in the zipped directory
            for archive_file in zip_member_list:
                #print(archive_file.file_size)
                if archive_file.file_size == 0 or archive_file.file_size == 1:
                    print(': empty file in archive found, skipping file...')
                    #Check for and skip empty files within the zipped file
                    pass
                else:
                    extract_path = os.getcwd() + "/" + zip_file_name
                    zip_ref.extract(archive_file, path=extract_path)
        else:
            print(zip, ': empty zipfile in directory found, skipping zipfile...')

        
        #zip_ref.close()
            
        '''
        zip_ref.extractall(os.getcwd() + "/" + zip_file_name)
        zip_ref.close()
        '''
    
    
    
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
        clean_nonzip_files(sub_directory_list)
        unzip_files(sub_directory_list)
        
        # return to the directory above
        os.chdir("..")
        
    
    
    
# the main method of our python script.
if __name__ == "__main__":

    total_directory_list = get_directory_list()
    #print(total_directory_list)
    sub_directory_looper_unzipper(total_directory_list)
    
    
    