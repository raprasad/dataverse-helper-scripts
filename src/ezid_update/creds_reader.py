import sys
from os.path import abspath, dirname, isfile, join
import json

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
