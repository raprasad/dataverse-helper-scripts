from os.path import abspath, dirname, isfile, join
import sys
import json
import requests
import csv

from creds_reader import get_creds
from ezid_formatting import STATUS_UNAVAILABLE,\
    examine_status
#
# Pull in util scripts
CURRENT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(CURRENT_DIR))

from helper_utils.msg_util import msg, msgt, msgx


class UpdateCheck(object):
    """Run API updates against EZID"""

    def __init__(self, input_file, **kwargs):
        self.cred_info = get_creds()
        self.input_file = input_file
        self.show_full_results = kwargs.get('show_full_results', False)

    def run_ez_id_check(self, start_row=1, stop_row=None):
        assert isfile(self.input_file),\
            "Input file not found: %s" % self.input_file

        with open(self.input_file, 'rb') as csvfile:
            doi_reader = csv.reader(csvfile)
            row_cnt = 0
            for single_row in doi_reader:
                row_cnt += 1

                if row_cnt == 1 or row_cnt < start_row:
                    continue    # next loop

                doi = single_row[0]
                msgt('(%s) Check DOI: %s' % (row_cnt, doi))
                self.run_single_check(\
                    doi=doi,
                    desired_status='unavailable')

                if stop_row and row_cnt >= stop_row:
                    msgx('Stopping at row: %s' % row_cnt)


    def run_single_check(self, doi, desired_status):

        api_url = 'https://ezid.cdlib.org/id/%s' % (doi)

        r = requests.get(api_url)

        if self.show_full_results:
            msg('%s' % r.text)
        msg('status_code: %s' % r.status_code)

        if r.status_code != 200:
            msgx('Failed to check DOI! %s' % doi)

        doi_info = r.text

        success, err_msg = examine_status(doi_info, desired_status)
        if success is True:
            msg('Looks good!')
        else:
            msg('!!! Update failed: %s' % err_msg)

if __name__ == '__main__':
    filename = join(CURRENT_DIR, 'input', 'bad_links.csv')

    check_args = dict(show_full_results=False)

    ur = UpdateCheck(filename, **check_args)
    ur.run_ez_id_check(start_row=2)#, stop_row=20)
    #ur.run_ez_id_file(start_row=12, stop_row=30)
