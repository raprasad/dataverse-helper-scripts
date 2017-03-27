"""
Test of Dataverse APIs to test and delete WorldMap layer objects within DV

These endpoints would only be called by DV admins, not geoconnect itself
"""
from __future__ import print_function
from os.path import isfile, join, realpath, dirname
import sys
import json
import requests
from collections import OrderedDict


TEST_API_KEY = None
DV_HOST = 'http://localhost:8080'

def get_api_key():
    global TEST_API_KEY
    if TEST_API_KEY is not None:
        return TEST_API_KEY

    current_dir = dirname(realpath(__file__))
    api_key_file = join(current_dir, 'test_api_key.txt')
    if not isfile(api_key_file):
        print(("-------------------------------"
               "\nError"
               "\n-------------------------------"
               "\nPlease make a file named 'test_api_key.txt'"
               " and place your API token within it."
               "\n\nPut your file here: \n  %s"
               "\n-------------------------------") % api_key_file )
        return None
    TEST_API_KEY = open(api_key_file, 'r').read().strip()
    return TEST_API_KEY

def get_dv_key_headers():

    api_key = get_api_key()
    if api_key is None:
        sys.exit(-1)
    headers = {'X-Dataverse-key' : api_key}

    return headers

def test_get_all_map_data():
    """Retrieve map layer metadatas"""
    print (test_get_all_map_data.__doc__)

    url = '%s/api/admin/geoconnect/mapLayerMetadatas/check' % (DV_HOST)
    print (url)

    r = requests.post(url,
                     headers=get_dv_key_headers())

    print_response(r)

def test_get_single_map(datafile_id):
    """Check a single map"""
    print (test_get_single_map.__doc__)

    url = '%s/api/files/%s/map' % (DV_HOST, datafile_id)
    print (url)

    r = requests.get(url,
                     headers=get_dv_key_headers())

    print_response(r)

def print_response(resp_obj):
    """Print the response"""
    if resp_obj is None:
        print ('error')
        return

    try:
        json_resp = resp_obj.json(object_pairs_hook=OrderedDict)
        print (json.dumps(json_resp, indent=4))
    except:
        print (resp_obj.text)
        print ('status_code: %d' % resp_obj.status_code)

def delete_single_map(datafile_id):
    """delete a single map"""
    print (delete_single_map.__doc__)
    url = '%s/api/files/%s/map' % (DV_HOST, datafile_id)
    print (url)

    r = requests.delete(url,
                        headers=get_dv_key_headers())

    print_response(r)



if __name__ == '__main__':
    #test_get_all_map_data()
    #test_get_single_map(956)
    #delete_single_map(956)
