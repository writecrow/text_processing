'''
Script Written: 11/16/17

Author: Nik Kirstein

Description:
Web Scrapes the FLLOC Website for Corpus Data
Downloads all available transcript and tagged zip files from the various corpus links 
that are available on the FLLOC Website

Run this script in an empty folder where you want all of the other folders created.
This script will create folders of each corpus by name and then download the zip files into them.
'''

# importing modules we'll need to run the script
import os
import time
from urllib.error import HTTPError
from urllib.error import URLError
import requests

# Beautiful Soup is a Python library that is designed to let you extract
#   information from websites, especially if they're cluttered and tough
#   to navigate
from bs4 import BeautifulSoup


def establish_scraper():
    '''
    This function uses a session object and website URL to gather and store
    source code information from the website provided.
    
    Parameters: None
    Returns: Scraper session object for http://wwww.flloc.soton.ac.uk/tasklist.html
    '''

    try:
        # uses the SCRAPER session object, that was initialized in the main method,
        #   to grab the web page's source code and store it
        flloc_session = SCRAPER.get("http://www.flloc.soton.ac.uk/tasklist.html", headers=HEADER)
    except HTTPError as err:
        print(err)
    except URLError as err:
        print("Can't find site")

    # return the session object which now includes information on the
    #   web page we want to scrape
    return flloc_session
    

    
    
    
def get_links_from_corpus():
    '''
    This function stores all of the <a> tag hrefs on "download data" webpage of the FLLOC website
    
    parameters: none
    returns: a newly created list with all <a> tag hrefs from that webpage.
    '''

    # creates a beautiful soup object with the session variable that's returned by
    #   our establish_scraper() function
    beautiful_soup_obj = BeautifulSoup(establish_scraper().text, "html.parser")

    # Create and empty list to populate with links
    atag_list = []
    
    # stores the main div in an object
    main_div = beautiful_soup_obj.find("div", {"id": "content"})
    
    for element in main_div:
        # stores all of the div elements with a class of "corpuscolumn" found on the web page
        corpus_div = main_div.find_all("div", {"class": "corpuscolumn"})
    
    # loop through the columns in the main div to find the <a> tags within them.
    # Then, append them to a list and return the list.
    for corpuscolumn in corpus_div:
        corpus_links = corpuscolumn.find_all("a")
        for link in corpus_links:
            atag_list.append(link['href'])
        
    return atag_list
            
        
def get_corpus_titles(href_list):
    '''
    This function takes the href_list built in get_links_from_corpus()
    and goes through it and extracts out all the corpus titles for use later.
    
    Parameters: href_list is a list of href strings from <a> tags
    Returns: a list with the corpus titles
    
    Note: This function ended up not being used, but is very useful to keep around.
    '''
    
    title_list = []
    for item in href_list:
        split_item_list = item.split("/")
        if ('tasklist.html' in split_item_list):
            corpus_title = split_item_list[1]
            title_list.append(corpus_title)
    return title_list
    
    
def remove_tasklist(href_list):
    '''
    This function removes the tasklist items that are un-needed in the href_list
    The links with "tasklisk" in them are the homepages of each individual corpus and 
    do not contain download links that we need, so we remove them.
    
    Parameters: href_list is a list of href string from <a> tags
    Returns: None, modifies the list that is inputted.
    '''
    for item in href_list:
        if ('tasklist.html' in item):
            href_list.remove(item)
        
    
  
    
def loop_and_populate(total_list):
    '''
    This function loops through the list of all <a> tags.
    The input list is the list that was populated
    from the get_links_from_corpus() function and cleaned from the remove_tasklist() function.
    
    This function will only work from that list, and it must be cleaned using the remove_tasklist() function
    first before running this function.
    
    Parameters: total_list is the list built from earlier functions containing all <a> tags for the various corpus websites
    available on FLLOC.
    
    Returns: None, it will create folders and download all the zip files when ran.
    
    If the server responds with a 404 for certain zip files, this is because sometimes the tagged
    or transcript file is not always available for every corpus/dataset.
    '''


    print('ATTENTION: The Script sleeps for 5 seconds after each download to avoid overflowing the website with requests')
    for corpus_link in total_list:
        
        # Specific check and skipping of this page to avoid making an empty folder
        # This is because while the webpage for this corpus exists and the download buttons for the Zip Files exist
        # However, the files do not exist on the webpage so it returns a 404
        # We want to avoid making an empty folder.
        if corpus_link == '/LANGSNAP/datasets/LanINT.html':
            pass
        
        
        # For all the other corpus links
        else:
        
            print('\nDownloading Data from: ' + str(corpus_link))
        
            try:
            # uses the SCRAPER session object, that was initialized in the main method,
            #   to grab the web page's source code and store it
                url = "http://www.flloc.soton.ac.uk" + corpus_link
                corpus_session = SCRAPER.get(url, headers=HEADER)
            except HTTPError as err:
                print(err)
            except URLError as err:
                print("Can't find site")

               
            directory = corpus_link.split('/')[1]
            if not os.path.exists(directory):
                os.makedirs(directory)
            
            '''
            We need to create a beautiful soup object for each and every corpus website so we can find
            the ZIP file links that exist in a table on each site.
            '''
     
            beautiful_soup_obj = BeautifulSoup(corpus_session.text, "html.parser")
            
            # Getting the zip file urls for both transcript and tagged
            table_footer = beautiful_soup_obj.find("tfoot")
            table_a_tags = table_footer.find_all("a")
            transcription_zip_url = "http://www.flloc.soton.ac.uk" + table_a_tags[1]['href']
            tagged_zip_url = "http://www.flloc.soton.ac.uk" + table_a_tags[2]['href']
            
            
            # indexing and splitting the url of the transcript zip file so we can get the exact file_name we want
            url_holder_transcription = table_a_tags[1]['href'].split('=')
            file_name_transcription = url_holder_transcription[1].split('&')[0] + '_' + url_holder_transcription[2]
            
            # indexing and splitting the url of the tagged zip file so we can get the exact file_name we want
            url_holder_tagged = table_a_tags[2]['href'].split('=')
            file_name_tagged = url_holder_tagged[1].split('&')[0] + '_' + url_holder_tagged[2]
           
            
            # Downloading the zip file.
            respfile = requests.get(transcription_zip_url)
            if respfile.status_code != 200:
                print('Error:', respfile, 'File not found, Web server responded with something other than a 200 response code.\n')
            else: 
                with open(directory + '/' + file_name_transcription + '.zip', 'wb') as writeback:
                    writeback.write(respfile.content)
                    print('Server response:', respfile, 'Success!')
                    time.sleep(5)
            
            # Downloading the tagged file.
            respfile_tagged = requests.get(tagged_zip_url)
            if respfile_tagged.status_code != 200:
                print('Error:', respfile_tagged, 'File not found, Web server respnded with something other than a 200 response code.\n')
            else:
                with open(directory + '/' + file_name_tagged + '.zip', 'wb') as writeback2:
                    writeback2.write(respfile_tagged.content)
                    print('Server response:', respfile_tagged, 'Success!')
                    time.sleep(5)
            
    
    
            
# the main method of our python script.
if __name__ == "__main__":



    # creating a session object that we will tell which web pages to collect the source code
    #   inforamtion from
    SCRAPER = requests.session()

    # create a dictionary that will act as header information for our session object.  This is
    #   necessary for scraping some websites that won't allow specific bots to collect information.
    #   we're using the header to fool the website into thinking a firefox user is requesting
    #   the web pages.
    HEADER = {"User-Agent": "Mozilla/5.0 (Macintosh; \
                             Intel Mac OS X 10_9_5) \
                             AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
              "Accept": "text/html,application/xhtml+xml, \
                         application/xml; q=0.9,image/webp,*/*;q=0.8"}


    total_link_list = get_links_from_corpus()
    #print(total_link_list)
    total_title_list = get_corpus_titles(total_link_list)
    #print(total_title_list)
    
    remove_tasklist(total_link_list)
    #print(total_link_list)
    loop_and_populate(total_link_list)
    print('Done with Download')  