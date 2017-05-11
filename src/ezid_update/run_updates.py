from os.path import abspath, dirname, isfile, join
import re
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

STATUS_UNAVAILABLE = 'unavailable'

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

                if row_cnt == 1 or row_cnt < start_row:
                    continue    # next loop

                doi = single_row[0]
                msgt('(%s) Update DOI: %s' % (row_cnt, doi))
                self.run_single_update(\
                    doi=doi,
                    status=STATUS_UNAVAILABLE)
                #    status='unavailable | withdrawn by author')

                if stop_row and row_cnt >= stop_row:
                    msgx('Stopping at row: %s' % row_cnt)



    def anvl_unescape(self, item_str):
        """Reverse the ANVL format
        example source: https://ezid.cdlib.org/doc/apidoc.html#internal-metadata
        """
        return re.sub("%([0-9A-Fa-f][0-9A-Fa-f])",
                      lambda m: chr(int(m.group(1), 16)),
                      item_str)

    def reverse_formatting(self, anvl_str):
        """Convert an ANVL string to a dict
        source: https://ezid.cdlib.org/doc/apidoc.html#internal-metadata
        """

        metadata = dict(tuple(self.anvl_unescape(v).strip()\
                        for v in l.split(":", 1)) \
                        for l in anvl_str.decode("UTF-8").splitlines())

        return metadata

    def anvl_escape(self, item_str):
        """
        Escape the string for ANVL formatting
        example source: https://ezid.cdlib.org/doc/apidoc.html#internal-metadata
        """
        return re.sub("[%:\r\n]", lambda c: "%%%02X" % ord(c.group(0)), item_str)


    def format_for_request(self, metadata_dict):
        """
        Convert a dict to an ANVL string.
        DOI updates are in the ANVL format as described here:
        https://ezid.cdlib.org/doc/apidoc.html#internal-metadata
        """
        formatted_lines = ["%s: %s" %\
                           (self.anvl_escape(name), self.anvl_escape(value))\
                           for name, value in metadata_dict.items()]
        return '\n'.join(formatted_lines).encode("UTF-8")


    def run_single_update(self, doi, status):

        api_url = 'https://ezid.cdlib.org/id/%s' % (doi)

        metadata_update_dict = dict(_target=api_url,
                                    _status=status,)
                                    #_export='no')

        doi_update_str = self.format_for_request(metadata_update_dict)


        sess_auth = self.cred_info

        msg('api_url: %s' % api_url)
        msg('payload: %s' % doi_update_str)
        msg('make update...\n')
        #msgx('reverse: %s' % self.reverse_formatting(doi_update_str))

        r = requests.post(api_url, data=doi_update_str, auth=sess_auth)

        msg('text: %s' % r.text)
        msg('status_code: %s' % r.status_code)

        if r.status_code != 200:
            msgx('Failed to update DOI! %s' % doi)


if __name__ == '__main__':
    filename = join(CURRENT_DIR, 'input', 'bad_links.csv')

    ur = UpdateRunner(filename)
    ur.run_ez_id_file(start_row=10, stop_row=302)
    #ur.run_ez_id_file(start_row=12, stop_row=30)
