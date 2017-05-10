from os.path import abspath, dirname, isfile, join
import sys
import json
import requests
import csv

#
# Pull in util scripts
CURRENT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(CURRENT_DIR))

from helper_utils.msg_util import msg, msgt, msgx

def get_creds():
    """Get the API creds from 'creds.json'"""

    creds_fname = join(dirname(abspath(__file__)), 'creds.json')

    assert isfile(creds_fname),\
        'File not found: %s' % creds_fname

    creds_content = open(creds_fname, 'r').read()

    try:
        creds_dict = json.loads(creds_content)
    except ValueError:
        msgx('Creds file not valid JSON: %s' % creds_content)

    return (creds_dict['EZID_USERNAME'],
            creds_dict['EZID_PASSWORD'])

class UpdateRunner(object):
    """Run API updates against EZID"""

    def __init__(self, input_file):
        self.cred_info = get_creds()
        self.input_file = input_file

    def run_ez_id_file(self, start_row=1, stop_row=None):
        assert isfile(self.input_file),\
            "Input file not found: %s" % self.input_file

        with open(self.input_file, 'rb') as csvfile:
            doi_reader = csv.reader(csvfile)
            row_cnt = 0
            for single_row in doi_reader:
                row_cnt += 1
                if stop_row and row_cnt >= stop_row:
                    msgx('Stopping at row: %s' % row_cnt)

                if row_cnt == 1 or row_cnt < start_row:
                    continue    # next loop

                doi = single_row[0]
                msgt('(%s) Update DOI: %s' % (row_cnt, doi))
                self.run_single_update(\
                    doi=doi,
                    status='unavailable | withdrawn by author')



    def run_single_update(self, doi, status):

        api_url = 'https://ezid.cdlib.org/id/%s' % (doi)

        payload = ('_target=%s'
                   '&_status=%s'
                   '&_export=no') % (api_url, status)

        sess_auth = self.cred_info

        msg('api_url: %s' % api_url)
        msg('payload: %s' % payload)
        msg('make update...\n')
        r = requests.post(api_url, data=payload, auth=sess_auth)

        msg('text: %s' % r.text)
        msg('status_code: %s' % r.status_code)

        if r.status_code != 200:
            msgx('Failed to update DOI! %s' % doi)


if __name__ == '__main__':
    filename = join(CURRENT_DIR, 'input', 'bad_links.csv')

    ur = UpdateRunner(filename)
    ur.run_ez_id_file(start_row=68, stop_row=None)
    #ur.run_ez_id_file(start_row=12, stop_row=30)

    #ur.run_single_update(doi='doi:10.7910/DVN/28680',
    #              status='unavailable|withdrawn by author')
