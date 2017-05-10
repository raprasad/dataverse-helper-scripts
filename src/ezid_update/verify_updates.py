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

class UpdateCheck(object):
    """Run API updates against EZID"""

    def __init__(self, input_file):
        self.cred_info = get_creds()
        self.input_file = input_file

    def run_ez_id_check(self, start_row=1, stop_row=None):
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
                msgt('(%s) Check DOI: %s' % (row_cnt, doi))
                self.run_single_check(\
                    doi=doi,
                    desired_status='unavailable')


    def examine_status(self, doi_info, desired_status):
        if doi_info is None:
            return False, 'doi_info is None'

        # split into array of lines
        doi_text = doi_info.strip().split('\n')

        doi_dict = {}
        for line in doi_text:
            key, val = line.split(':', 1)
            doi_dict[key.strip()] = val.strip()

        doi_status = doi_dict.get('_status', 'Not found')
        doi_status = doi_status.split('|')[0].strip()

        if doi_status == desired_status:
            return True, 'looks good, status is: %s' % doi_status

        return False, 'status is [%s]' % doi_status

    def run_single_check(self, doi, desired_status):

        api_url = 'https://ezid.cdlib.org/id/%s' % (doi)

        r = requests.get(api_url)

        #msg('text: %s' % r.text)
        msg('status_code: %s' % r.status_code)

        if r.status_code != 200:
            msgx('Failed to check DOI! %s' % doi)

        doi_info = r.text

        success, err_msg = self.examine_status(doi_info, desired_status)
        if success is True:
            msg('Looks good!')
        else:
            msg('!!! Update failed: %s' % err_msg)

if __name__ == '__main__':
    filename = join(CURRENT_DIR, 'input', 'bad_links.csv')

    ur = UpdateCheck(filename)
    ur.run_ez_id_check(start_row=1, stop_row=10)
    #ur.run_ez_id_file(start_row=12, stop_row=30)
