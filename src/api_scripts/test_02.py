import requests
import sys
from datetime import datetime
import time
import urllib

def msg(m): print m
def dashes(): msg('-' * 40)
def msgt(m): dashes(); msg(m); dashes()
def msgx(m): msgt(m); sys.exit(0)

API_KEY = open('key_str.txt').read().strip()

url_base = 'http://127.0.0.1:8080/api/v1'

def run_add(fname='blackbox.txt'):
    msgt('ADD')
    url = '%s/upload/add/%s?key=%s' % (url_base, fname, API_KEY)

    print 'url: ', url

    r = requests.get(url)

    print r.status_code
    print r.text


def run_add_test():
    msgt('run_upload_test')

    url = '%s/upload/add?key=%s' % (url_base, API_KEY)

    print 'url: ', url

    # prep file data
    #
    files = {'file': open('input/howdy3.txt', 'rb')}

    # prep other data
    #
    payload = dict(datasetId=26)

    # Make the request!
    #
    r = requests.post(url, data=payload, files=files)

    #print r.json()
    print '-' * 40
    print r.text
    print '-' * 40
    print r.status_code


def run_replace_test(old_file_id):
    msgt('run_replace_test')

    url = '%s/upload/replace?key=%s' % (url_base, API_KEY)

    print 'url: ', url

    # prep file data
    #
    files = {'file': open('input/howdy3.txt', 'rb')}

    # prep other data
    #
    payload = dict(datasetId=26, fileToReplaceId=old_file_id)

    # Make the request!
    #
    r = requests.post(url, data=payload, files=files)

    #print r.json()
    print '-' * 40
    print r.text
    print '-' * 40
    print r.status_code
    return r.json()


def run_publish_dataset(ds_id):
    msgt('PUBLISH')

    url = '%s/datasets/%s/actions/:publish?key=%s&type=major' % (url_base, ds_id, API_KEY)

    r = requests.get(url)

    if r.status_code == 200:
        print 'published!'
    else:
        print r.text
        print r.status_code
        sys.exit(-1)

def update_input_file():
    msg('updating input file')
    fh = open('input/howdy3.txt', 'w')
    fh.write('%s' % datetime.now())
    fh.close()

def run_loop(old_fid):

    for x in range(1, 150):
        msgt('%s) replace loop' % (x))
        # Update
        update_input_file()
        d = run_replace_test(old_fid)
        print d
        old_fid = d['data']['id']

        # Publish
        run_publish_dataset(26)

        # Sleep
        msg('Sleep...')
        #time.sleep(3)

if __name__ == '__main__':
    #run_publish_dataset(26)
    #run_add_test()
    #run_replace_test(232)
    #run_command_line_params()
    run_loop(409)
