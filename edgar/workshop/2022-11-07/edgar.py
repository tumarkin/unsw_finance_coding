# Note: Need to deal with errors in the get_from_edgar fn

# Edgar has an INDEX for each quarter of all the filings
# beginning with 1994Q1. Robust data doesn't begin until
# 1996Q1.

# Step 1: Get these index files
# Step 2: Get the actual filing data

from glob import glob
import gzip
import os
import pathlib
import requests # Allows us to use HTTPS requests

# Ideally, this would be in a configuration file
INDEX_DIR = 'index'
EMAIL = 'r.tumarkin@unsw.edu.au'
EDGAR = 'https://www.sec.gov/Archives'

def get_from_edgar(partial_url):
    url = '{}/{}'.format(EDGAR, partial_url)
    user_agent = { 'user-agent': 'r.tumarkin@unsw.edu.au'}
    response = requests.get(url, headers = user_agent)
    
    if response.status_code == 200:
        return response
    else:
        pass

def get_index(year, qtr):
    response = get_from_edgar('edgar/full-index/{}/QTR{}/master.gz'.format(year, qtr))
    index = gzip.decompress(response.content)
    
    if not os.path.exists(INDEX_DIR):
        os.makedirs(INDEX_DIR)
        
    with open('{}/{}.Q{}.master.txt'.format(INDEX_DIR, year, qtr), 'wb') as out:
        out.write(index)
        
def get_form(filename):
    if not os.path.exists(filename):
        response = get_from_edgar(filename)
        
        parent_dirs = pathlib.Path(filename).parent
        if not os.path.exists(parent_dirs): 
            os.makedirs(pathlib.Path(filename).parent)

        with open(filename, 'wb') as out:
            out.write(response.content)
            print('Saved {}'.format(filename))
        
def get_forms_by_type(requested_type):
    for index_file in glob('{}/*.txt'.format(INDEX_DIR)):
        for form in open(index_file).readlines():
            form_info = form.split('|')
            if len(form_info) == 5:
                cik = form_info[0]
                company_name = form_info[1]
                form_type = form_info[2]
                date_filed = form_info[3]
                filename = form_info[4][:-1]
                if form_type == requested_type:
                    get_form(filename)

    
# Main loop that gets executed when this file is run
if __name__ == '__main__':
    get_index(2021, 3)
    # get_form('edgar/data/1000045/0000950170-21-004287.txt')
    # get_forms_by_type('DEF 14A')
    
