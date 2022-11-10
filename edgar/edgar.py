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
import re
import argparse

import requests # Allows us to use HTTPS requests

# Ideally, this would be in a configuration file
INDEX_DIR = 'index'
EMAIL = 'r.tumarkin@unsw.edu.au'
EDGAR = 'https://www.sec.gov/Archives'

def get_from_edgar(partial_url):
    url = '{}/{}'.format(EDGAR, partial_url)
    user_agent = { 'user-agent': 'r.tumarkin@unsw.edu.au'}
    response = requests.get(url, headers = user_agent)

    if response.status_code != 200:
        raise Exception('Invalid response from Edgar')

    return response

def get_index(year, qtr):
    print('Downloading index for {} qtr {}'.format(year, qtr))
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
                _cik = form_info[0]
                _company_name = form_info[1]
                form_type = form_info[2]
                _date_filed = form_info[3]
                filename = form_info[4][:-1]
                if form_type == requested_type:
                    get_form(filename)


def index_command(start, end):
    (start_yr, start_qtr) = parse_year_quarter(start)
    (end_yr, end_qtr) = parse_year_quarter(end)

    if start_yr > end_yr:
        raise Exception("End year is greater than start year")
    if start_yr == end_yr and start_qtr > end_qtr:
        raise Exception("End year-quarter is before start year-quarter")

    # loop over quarters
    for year in range(start_yr, end_yr+1):
        if year == end_yr:
            this_end_qtr = end_qtr
        else:
            this_end_qtr = 4

        for qtr in range(start_qtr, this_end_qtr+1):
            get_index(year, qtr)

        start_qtr = 1



def parse_year_quarter(yq_str):
    match = re.match(r'(\d{4})Q(\d)', yq_str)
    if match is None:
        raise Exception('Invalid year_quarter: {}'.format(yq_str))
    return (int(match[1]), int(match[2]))


# Main loop that gets executed when this file is run
if __name__ == '__main__':

    # Define the command line parser
    parser = argparse.ArgumentParser(prog='edgar')
    subparsers = parser.add_subparsers(dest='command', help='valid sub-commands')

    # Define the command parser for downloading index files
    index_parser = subparsers.add_parser('index', help='download index files')
    index_parser.add_argument('start', metavar='Start quarter', help='yyyyQq (e.g., 2010Q2)')
    index_parser.add_argument('end', metavar='End quarter', help='yyyyQq (e..g., 2015Q4)')

    # Definte the command parser for downloading forms by type
    form_parser = subparsers.add_parser('form', help='download forms')
    form_parser.add_argument('type', metavar='String', help='Desired form type')
    args = parser.parse_args()

    if args.command == 'index':
        index_command(args.start, args.end)
    elif args.command == 'form':
        get_forms_by_type(args.type)
