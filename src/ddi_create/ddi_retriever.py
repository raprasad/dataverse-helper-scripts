"""
Convenience script for retrieving DDIs in XML format
and saving them to a file
"""
from os.path import isdir, isfile, join, dirname, abspath
import os
import sys
import json
import requests
from slugify import slugify
import time
#
# Pull in util scripts
CURRENT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(CURRENT_DIR))

from helper_utils.msg_util import msg, msgt, msgx


INPUT_DIR = join(CURRENT_DIR, 'input')
OUTPUT_DIR = join(CURRENT_DIR, 'output')

creds_file_fname = join(dirname(abspath(__file__)), 'creds.json')

def get_api_key():
    """Retrieve the API key from the creds.json file"""

    if not isfile(creds_file_fname):
        msgx('Creds file not found: %s' % creds_file_fname)

    creds_content = open(creds_file_fname, 'r').read()

    try:
        creds_dict = json.loads(creds_content)
    except ValueError:
        msgx('Creds file not valid JSON: %s' % creds_content)

    return creds_dict['DV_API_KEY']


class DDIRetreiver(object):
    """
    Iterate through a list of DOIs, retrieve the DDI XML,
    and save it to a file
    """
    def __init__(self, api_key, doi_input_file, output_dir, **kwargs):

        self.api_key = api_key
        self.input_fname = doi_input_file
        self.output_dir = output_dir
        self.failed_queries = []

        #self.ddi_output_dir = None
        self.input_start_line = kwargs.get('input_start_line', 0)
        self.doi_cnt = 0



    def read_doi_import_list(self):

        if not isdir(self.output_dir):
            os.makedirs(self.output_dir)
            msg('directory created: %s' % self.output_dir)

        input_fname = join(INPUT_DIR, self.input_fname)
        if not isfile(input_fname):
            msgx("input file not found: [%s]" % input_fname)

        input_lines = open(input_fname, 'r').readlines()
        input_lines = [x.strip() for x in input_lines if len(x.strip()) > 0]
        input_dois = [x.split('&persistentId=')[-1] for x in input_lines]

        # Iterate through the DOIs
        #
        self.doi_cnt = 0
        for doi_string in input_dois:
            self.doi_cnt += 1
            if self.doi_cnt >= self.input_start_line:
                self.retrieve_file(ddi_output_dir, doi_string)

        # Save any failed queries
        #
        if len(self.failed_queries) > 0:
            failed_ddi_fname = join(ddi_output_dir, 'failed_queries.txt')
            open(failed_ddi_fname, 'wb').write('\n'.join(self.failed_queries))
            msg('file written: %s' % failed_ddi_fname)

    def retrieve_file(self, ddi_output_dir, doi_string):
        """Retrieve the DDI in XML format and write it to a file"""
        assert isdir(ddi_output_dir), '[%s] is not a directory' % ddi_output_dir
        assert doi_string is not None, "doi_string cannot be None"
        msgt("(%d) Retrieving doi: %s" % (self.doi_cnt, doi_string))

        # Format file name for DDI
        #
        doi_fname = '%s.xml' % (slugify(unicode(\
                                doi_string.replace('/', '-').replace(':', '_'))))

        # Full file name of DDI output
        #
        output_fname = join(ddi_output_dir, doi_fname)


        # Has the DDI already been retrieved?
        # Yes, then leave
        #
        if isfile(output_fname) and os.stat(output_fname).st_size > 100:
            msg('File already retrieved')
            return

        # Format the API request
        #
        url = ('https://dataverse.harvard.edu/api/datasets/export'
               '?exporter=ddi'
               '&persistentId=%s') % doi_string

        msg('url: %s' % url)

        # Make the request to retrieve the DDI file
        #
        headers = {'X-Dataverse-key' : self.api_key}

        r = requests.get(url) #,headers=headers)

        # Was the status code 200?
        #
        if not r.status_code == 200:
            msg(r.text)
            msgt('!!!!! Failed with status code: %s' % r.status_code)
            self.failed_queries.append(url)
            msg('5 second pause')
            time.sleep(5)
            return

        # Looks good, save the file
        #
        open(output_fname, 'wb').write(r.text.encode('utf-8'))
        msg('file written: %s' % output_fname)


    def post_check(self, output_dir):
        """Check if the files look valid"""

        assert isdir(output_dir), '[%s] is not a directory' % output_dir

        fnames = [x for x in os.listdir(output_dir) if x.endswith('.xml')]
        bad_file_cnt = 0
        for fname in fnames:
            content = open(join(output_dir, fname), 'r').read()
            if content.startswith('<codeBook xmlns="ddi:codebook:2_5"'):
                continue
            else:
                bad_file_cnt += 1
                msgt('(%d) Bad file: %s' % (bad_file_cnt, fname))
        if bad_file_cnt == 0:
            msgt('Looks good!')


if __name__ == '__main__':
    ddi_output_dir = join(\
              OUTPUT_DIR,
              'output_2016-0320a')

    doi_input_file = 'doi_list_2017_0320.txt'

    ddi_kwargs = dict(input_start_line=0)

    ddi_retriever = DDIRetreiver(get_api_key(),
                                 doi_input_file,
                                 ddi_output_dir,
                                 **ddi_kwargs)

    #ddi_retriever.read_doi_import_list()
    ddi_retriever.post_check(ddi_output_dir)
