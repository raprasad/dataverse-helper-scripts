from os.path import abspath, dirname, isfile, join
import sys
import requests
import csv
import subprocess

from ezid_formatting import STATUS_UNAVAILABLE,\
    STATUS_PUBLIC,\
    STATUS_UPDATE_UNAVAILABLE_WITHDRAWN
from creds_reader import get_creds
#
# Pull in util scripts
CURRENT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(CURRENT_DIR))

from helper_utils.msg_util import msg, msgt, msgx

class UpdateRunner(object):
    """Run API updates against EZID"""
    """Run API updates against EZID"""
    def __init__(self, input_file, **kwargs):
        self.cred_info = get_creds()
        self.input_file = input_file
        self.run_update_with_curl = kwargs.get('use_curl', False)

    def run_ez_id_file(self, start_row=1, stop_row=None):
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
                msgt('(%s) Update DOI: %s' % (row_cnt, doi))

                if self.run_update_with_curl:
                    self.run_single_update_with_curl(doi, STATUS_UNAVAILABLE)
                else:
                    self.run_single_update(\
                        doi=doi,
                        status=STATUS_UPDATE_UNAVAILABLE_WITHDRAWN)

                if stop_row and row_cnt >= stop_row:
                    msgx('Stopping at row: %s' % row_cnt)



    def run_single_update_with_curl(self, doi, status):
        """Run the update as 2 separate curl commands"""

        api_url = 'https://ezid.cdlib.org/id/%s' % (doi)

        curl_cmd1 = ("curl -u {0}:{1} -X POST -H"
                    " 'Content-Type: text/plain' --data-binary"
                    " '_target:{2}' {2}").format(\
                        self.cred_info[0],
                        self.cred_info[1],
                        api_url)

        curl_cmd1_args = ['bash','-c', curl_cmd1]
        msg('\nrun command: %s\n' % curl_cmd1)
        cmd1_output = subprocess.check_output(curl_cmd1_args, shell=False)
        msg(cmd1_output)

        curl_cmd2 = ("curl -u {0}:{1} -X POST -H"
                    " 'Content-Type: text/plain' --data-binary"
                    " '_status:  unavailable | Withdrawn' {2}").format(\
                        self.cred_info[0],
                        self.cred_info[1],
                        api_url)

        msg('\nrun command: %s\n' % curl_cmd2)
        curl_cmd2_args = ['bash','-c', curl_cmd2]
        cmd2_output = subprocess.check_output(curl_cmd2_args, shell=False)
        msg(cmd2_output)



    def run_single_update(self, doi, status):
        """Run an EZID update to change target, status, and export"""

        api_url = 'https://ezid.cdlib.org/id/%s' % (doi)

        metadata_update_dict = dict(_target=api_url,
                                    _status=status,
                                    _export='no')

        string_pairs = ['%s:%s' % (key, val)\
                        for key, val in metadata_update_dict.items()]
        doi_update_str = '\n'.join(string_pairs)

        msg('api_url: %s' % api_url)
        msg('payload:\n %s' % doi_update_str)
        msg('make update...\n')
        #msgx('reverse: %s' % reverse_formatting(doi_update_str))

        headers = {'Content-type': 'text/plain'}
        r = requests.post(api_url,
                          data=doi_update_str,
                          auth=self.cred_info,
                          headers=headers)

        #msg('headers: %s' % r.headers)
        msg('text: %s' % r.text)
        msg('status_code: %s' % r.status_code)

        if r.status_code != 200:
            msgx('Failed to update DOI! %s' % doi)


if __name__ == '__main__':
    filename = join(CURRENT_DIR, 'input', 'bad_links.csv')


    #ur = UpdateRunner(filename, **dict(use_curl=True))
    ur = UpdateRunner(filename)
    ur.run_ez_id_file(start_row=10, stop_row=100)
