
from os.path import isdir, isfile, join, dirname, abspath
from os import makedirs
import json
import sys
import random

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
    
def get_repository_creds(repo_nickname):
    
    token_lookup = get_creds_info('GITHUB_API_ACCESS_TOKENS')

    assert repo_nickname in token_lookup\
                , "Repository nickname '%s' not found.  Available names: %s" % (repo_nickname, token_lookup.keys()) 
    
    
    api_creds = token_lookup[repo_nickname]
    assert 'API_USERNAME' in api_creds\
                , '"API_USERNAME key not found in creds: %s' % (repo_nickname, api_creds) 
    assert 'API_ACCESS_TOKEN' in api_creds\
                , '"API_ACCESS_TOKEN key not found in creds: %s' % (repo_nickname, api_creds) 

    return (api_creds['API_USERNAME'], api_creds['API_ACCESS_TOKEN'])
    

def get_repository_repo(repo_nickname):

    token_lookup = get_creds_info('GITHUB_API_ACCESS_TOKENS')

    assert repo_nickname in token_lookup\
                , "Repository nickname '%s' not found.  Available names: %s" % (repo_nickname, token_lookup.keys()) 

    api_creds = token_lookup[repo_nickname]
    assert 'REPOSITORY_NAME' in api_creds\
                , '"REPOSITORY_NAME key not found in creds: %s' % (repo_nickname, api_creds) 
 
    return api_creds['REPOSITORY_NAME']

    