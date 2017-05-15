"""
Convenience script for retrieving Dataverse files
"""
from __future__ import print_function
from os.path import isdir, isfile, join, dirname, abspath
import os
import sys
import json
import requests
#from slugify import slugify
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


class FileRetriever(object):
    """
    Iterate through a list of file ids,
    retrieve the file from Dataverse,
    and store it locally
    """
    INPUT_LINE_KEYS = ['df_id', 'owner_id',
                       'label', 'contenttype',
                       'publicationdate', 'restricted']


    def __init__(self, api_key, input_file, output_dir, **kwargs):
        """Init params"""
        assert isfile(input_file), "Input file not found: [%s]" % input_file

        self.api_key = api_key
        self.input_file = input_file
        self.output_dir = output_dir
        self.failed_lines = []

        self.input_start_line = kwargs.get('input_start_line', 2)
        self.extension_type = kwargs.get('extension_type', None)
        self.download_cnt = 0



    def download_files(self):

        if not isdir(self.output_dir):
            os.makedirs(self.output_dir)
            msg('directory created: %s' % self.output_dir)

        if not isfile(self.input_file):  # redundant check
            msgx("input file not found: [%s]" % input_fname)

        line_cnt = 0
        with open(self.input_file, 'r') as infile:
            for info_line in infile:
                info_line = info_line.strip()
                print (info_line)
                print ('*' * 40)

                line_cnt += 1
                if self.input_start_line > line_cnt:
                    continue # go to next line

                line_items = info_line.split(',')
                if len(line_items) != len(self.INPUT_LINE_KEYS):
                    self.failed_lines.append(info_line)
                    continue

                #import ipdb; ipdb.set_trace()

                line_info = dict(zip(self.INPUT_LINE_KEYS, line_items))
                if self.extension_type is None:
                    # download any file
                    self.download_file(line_info, line_cnt)
                elif line_info['label'].lower().endswith(self.extension_type):
                    self.download_file(line_info, line_cnt)

        # Save any failed queries
        #
        #if len(self.failed_lines) > 0:
        #    failed_ddi_fname = join(self.output_dir, 'failed_lines.txt')
        #    open(failed_ddi_fname, 'wb').write('\n'.join(self.failed_lines))
        #    msg('file written: %s' % failed_ddi_fname)

    def download_file(self, line_info, line_cnt=1):
        """Retrieve the file"""
        msgt('(%d) Attempt to download file: %s'\
             % (line_cnt, line_info['label']))

        # Create the directory for the file
        #
        file_id_dir = join(self.output_dir, line_info['df_id'].zfill(7))
        if not isdir(file_id_dir):
            os.makedirs(file_id_dir)

        # Format the file name
        #
        output_fname = join(file_id_dir, line_info['label'])

        # Has the file already been retrieved?
        # Yes, then leave
        #
        if isfile(output_fname) and os.stat(output_fname).st_size > 100:
            msg('File already retrieved')
            self.download_cnt += 1
            return

        # Format the API request
        #/api/access/datafile/$id
        url = ('https://dataverse.harvard.edu'
               '/api/access/datafile/%s') % line_info['df_id']

        msg('url: %s' % url)

        # Make the request to retrieve the DDI file
        #
        headers = {'X-Dataverse-key' : self.api_key}

        r = requests.get(url, stream=True, headers=headers)

        # Was the status code 200?
        #
        if not r.status_code == 200:
            msg(r.text)
            msgt('!!!!! Failed with status code: %s' % r.status_code)
            self.failed_lines.append(url)
            msg('5 second pause')
            time.sleep(5)
            return

        # Looks good, save the file
        #
        with open(output_fname, 'wb') as file_download:
            for chunk in r.iter_content(chunk_size=128):
                file_download.write(chunk)
        self.download_cnt += 1
        msg('file written: %s' % output_fname)
        msg('download cnt: %s' % self.download_cnt)

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
              'output_2016-0427')

    input_file = '/Users/rmp553/Documents/iqss-git/ingest-test/rprasad.all_list.2017.0427.csv'
    extension_type = '.xls'
    extra_kwargs = dict(extension_type = '.xls',
                        input_start_line=36041)

    file_retriever = FileRetriever(get_api_key(),
                                 input_file,
                                 ddi_output_dir,
                                 **extra_kwargs)

    file_retriever.download_files()
    #ddi_retriever.post_check(ddi_output_dir)
