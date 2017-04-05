from os.path import isdir, isfile, join, dirname, abspath
import sys
#import json
import requests
from datetime import datetime

CURRENT_DIR = dirname(abspath(__file__))
sys.path.append(dirname(CURRENT_DIR))

from msg_util import msg, msgt, msgx

INPUT_DIR = join(CURRENT_DIR, 'input')
OUTPUT_DIR = join(CURRENT_DIR, 'output')

class WhitelistChecker(object):

    def __init__(self, input_file, output_file, start_num=1, **kwargs):

        self.input_file = join(INPUT_DIR, input_file)
        self.output_file = join(OUTPUT_DIR, output_file)

        try:
            self.start_num = int(start_num)
        except (ValueError, TypeError) as ex_obj:
            msgt("That is not valid start_num (%s)\n%s" % (start_num, ex_obj))
            msgx('')

        if not isfile(self.input_file):
            msgt("Input file not found: %s" % self.input_file)
            msgx('')

        self.timeout_time = 10 # seconds; add to kwargs

    def get_output_file_handler(self):

        add_header = False
        if not isfile(self.output_file):
            add_header = True
        fh_out = open(self.output_file, 'a')

        if add_header:
            header_line = 'url_to_check,200_status_code,message,timestamp\n'
            fh_out.write(header_line)

        return fh_out

    def process_whitelist(self):
        """
        Iterate through the white list of domain names
        """
        whitelist_names = open(self.input_file, 'r').readlines()
        whitelist_names = [x.strip() for x in whitelist_names\
                           if len(x.strip()) > 0]

        fh_out = self.get_output_file_handler()

        cnt = 0
        for single_name in whitelist_names:
            cnt += 1
            msgt("(%s) Checking: %s" % (cnt, single_name))
            if cnt < self.start_num:
                msg('(skipping)')
            else:
                self.check_single_name(single_name, fh_out)

        fh_out.close()

        msgt('File written: %s' % self.output_file)

    def get_timestamp(self):

        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def write_error_to_output(self, fh_to_append, domain_name, user_message):

        self.write_to_output(fh_to_append, domain_name, user_message, False)

    def write_to_output(self, fh_to_append, url_to_check, user_message, success=True):

        if success:
            outline = '%s,True,%s,%s\n' %\
                (url_to_check, user_message, self.get_timestamp())
        else:
            outline = '%s,False,%s,%s\n' %\
                (url_to_check, user_message, self.get_timestamp())

        msg(outline)
        fh_to_append.write(outline)
        fh_to_append.flush()


    def check_single_name(self, domain_name, fh_out=None):
        """
        Check a single domain name
        """
        format_name = 'https://%s' % domain_name
        msg('url to test: %s' % format_name)

        try:
            r = requests.get(format_name, timeout=self.timeout_time)
        except requests.exceptions.ConnectionError as exception_obj:
            user_message = 'Failed to connect to site'
            self.write_error_to_output(fh_out, format_name, user_message)
            return
        except requests.exceptions.Timeout as exception_obj:
            user_message = 'Timed out after: %s second(s)' % self.timeout_time
            self.write_error_to_output(fh_out, format_name, user_message)
            return
        except:
            # Error with request
            #
            user_message = "Unexpected error: %s" % sys.exc_info()[0]
            self.write_error_to_output(fh_out, format_name, user_message)
            return

        if r.status_code == 200:
            user_message = 'Looks good!'
            self.write_to_output(fh_out, format_name, user_message)
        else:
            user_message = 'Failed with status code: %s' % r.status_code
            self.write_error_to_output(fh_out, format_name, user_message)


def show_instructions():
    msgt("white list check")
    msg(('\n\t>python check_whitelist.py (input file) (output file)'
         '\n\nExample:\n\n\t>python check_whitelist.py whitelist-domains_2017_0405.txt output_2017_0405.csv'
         '\n\nThe script may be restarted at a specific item:'
         '\n\n\t>python check_whitelist.py (input file) (output file) (item #/occurrence in whitelist)'
         '\n\nExample.  Start at 20th item in the whitelist:'
         '\n\n\t>python check_whitelist.py whitelist-domains_2017_0405.txt output_2017_0405.csv 20'
         '\n'))

if __name__ == '__main__':

    if len(sys.argv) == 4:
        print(sys.argv[1], sys.argv[2], sys.argv[3])
        wlc = WhitelistChecker(sys.argv[1], sys.argv[2], sys.argv[3])
        wlc.process_whitelist()
    elif len(sys.argv) == 3:
        wlc = WhitelistChecker(sys.argv[1], sys.argv[2])
        wlc.process_whitelist()
    else:
        show_instructions()
