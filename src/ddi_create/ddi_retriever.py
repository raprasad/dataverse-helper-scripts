from os.path import isdir, isfile, join, dirname, abspath
import os
import sys
import json
import requests
from datetime import datetime
from slugify import slugify
# ----------------------------
# Pull in util scripts
# ----------------------------
CURRENT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(CURRENT_DIR))

from helper_utils.msg_util import *


INPUT_DIR = join(CURRENT_DIR, 'input')
OUTPUT_DIR = join(CURRENT_DIR, 'output')

creds_file_fname = join(dirname(abspath(__file__)), 'creds.json')

def get_api_key():
    if not isfile(creds_file_fname):
        msgx('Creds file not found: %s' % creds_file_fname)

    creds_content = open(creds_file_fname, 'r').read()

    try:
        creds_dict = json.loads(creds_content)
    except ValueError:
        msgx('Creds file not valid JSON: %s' % creds_content)

    return creds_dict['DV_API_KEY']


class DDIRetreiver(object):

    def __init__(self, api_key, input_fname):

        self.api_key = api_key
        self.input_fname = input_fname
        #self.ddi_output_dir = None
        self.doi_cnt = 0

    def read_doi_import_list(self):

        ddi_output_dir = join(\
                          OUTPUT_DIR,
                          'output_%s' % datetime.now().strftime('%Y-%m-%d_%H-%M'))

        if not isdir(ddi_output_dir):
            os.makedirs(ddi_output_dir)
            msg('directory created: %s' % ddi_output_dir)

        input_fname = join(INPUT_DIR, self.input_fname)
        if not isfile(input_fname):
            msgx("input file not found: [%s]" % input_fname)

        input_lines = open(input_fname, 'r').readlines()
        input_lines = [x.strip() for x in input_lines if len(x.strip()) > 0]
        input_dois = [x.split('&persistentId=')[-1] for x in input_lines]

        #doi_string = 'doi:10.7910/DVN/29917'

        self.doi_cnt = 0
        for doi_string in input_dois:
            self.doi_cnt += 1
            self.retrieve_file(ddi_output_dir, doi_string)


    def retrieve_file(self, ddi_output_dir, doi_string):

        assert isdir(ddi_output_dir), '[%s] is not a directory' % ddi_output_dir
        assert doi_string is not None, "doi_string cannot be None"
        msgt("(%d) Retrieving doi: %s" % (self.doi_cnt, doi_string))

        headers = {'X-Dataverse-key' : self.api_key}#,
                  #'Content-type':'application/json'}

        doi_fname = '%s.xml' % (slugify(unicode(\
                                doi_string.replace('/', '-').replace(':', '_'))))

        url = ('https://dataverse.harvard.edu/api/datasets/export'
               '?exporter=ddi'
               '&persistentId=%s') % doi_string
        msg('url: %s' % url)

        r = requests.get(url) #,headers=headers)

        if not r.status_code == 200:
            msg(r.text)
            msgx('Failed with status code: %s' % r.status_code)

        output_fname = join(ddi_output_dir, doi_fname)
        #output_fname = join(OUTPUT_DIR, doi_fname)

        open(output_fname, 'w').write(r.text)
        msg('file written: %s' % output_fname)


if __name__ == '__main__':

    ddi_retriever = DDIRetreiver(get_api_key(), 'doi_list.txt')
    ddi_retriever.read_doi_import_list()
