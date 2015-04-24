from os.path import isdir, isfile, join, dirname, abspath
from os import makedirs
import json
import sys

STRESS_TEST_DIR = dirname(abspath(__file__))

# ----------------------------
# Pull in util scripts
# ----------------------------
HELPER_SCRIPTS_DIR = join(dirname(STRESS_TEST_DIR))#, 'helper_utils')
sys.path.append(HELPER_SCRIPTS_DIR)
print HELPER_SCRIPTS_DIR
from helper_utils.msg_util import *




# ----------------------------
# Any needed credentials -
#  stored in a JSON file
# ----------------------------

CREDS_FNAME = join(STRESS_TEST_DIR, 'creds.json')
CREDS_LOOKUP = {}
def get_creds_info(key_name):
    global CREDS_LOOKUP
    assert isfile(CREDS_FNAME), 'File not found: %s' % CREDS_FNAME

    if CREDS_LOOKUP.has_key(key_name):
        return CREDS_LOOKUP.get(key_name)

    json_creds = json.loads(open(CREDS_FNAME, 'r').read())

    assert json_creds.has_key(key_name), 'Key *%s* not found in creds file' % key_name

    cred_value = json_creds.get(key_name)

    CREDS_LOOKUP[key_name] = cred_value

    return cred_value