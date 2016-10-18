from datetime import datetime
import json
import sys
import time

import requests

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


def run_add_test(dataset_id):
    msgt('run_upload_test')

    url = '%s/upload/add?key=%s' % (url_base, API_KEY)

    print 'url: ', url

    # prep file data
    #
    #files = {'file': open('input/howdy3.txt', 'rb')}
    files = {'file': open('input/test_01.xlsx', 'rb')}

    # prep other data
    #
    payload = dict(datasetId=dataset_id)

    # Make the request!
    #
    r = requests.post(url, data=payload, files=files)

    #print r.json()
    print '-' * 40
    print r.text
    print '-' * 40
    print r.status_code


def run_replace_test(dataset_id, old_file_id, force_replace=False):
    msgt('run_replace_test')

    url = '%s/upload/replace?key=%s' % (url_base, API_KEY)

    print 'url: ', url

    # prep file data
    #
    files = {'file': open('input/test_01.xlsx', 'rb')}
    #files = {'file': open('input/howdy3.txt', 'rb')}

    # prep other data
    #
    payload = dict(datasetId=dataset_id,
                fileToReplaceId=old_file_id,
                forceReplace=force_replace)

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

def run_replace_loop(num_loops, dataset_id, old_file_id, force_replace=False):
    assert num_loops > 0, "num_loops must be a number greater than 0"

    # Run replace loop multiple times
    for x in range(1, num_loops+1):

        msgt('%s) replace loop' % (x))

        # prep file data
        #
        file_content = 'content: %s' % datetime.now()
        fname = 'loop_%s.txt' % (`x`.zfill(4))
        files = {'file': (fname, file_content)}

        # prep other data
        #
        jData = dict(fileToReplaceId=old_file_id,
                    forceReplace=force_replace)

        payload = dict(jsonData=json.dumps(jData))

        # Prep url (currently always the same)
        #
        url = '%s/files/%s/replace?key=%s' % (url_base, old_file_id, API_KEY)

        print 'url', url

        # Make the request!
        #
        r = requests.post(url, data=payload, files=files)

        # Turn result into expected JSON
        #
        try:
            result_json = r.json()
        except:
            msgt('Error!')
            msg(r.text)
            msgx(r.status_code)

        # Retrieve the new file id from the result
        #
        old_file_id = result_json.get('data', {}).get('id')
        if old_file_id is None:
            msgx("Unexpected result.  New file id not found: %s" % r.text)

        msg("good replace: %s" % json.dumps(result_json, indent=4))
        # Publish
        run_publish_dataset(dataset_id)

        # Sleep
        msg('Sleep...')
        time.sleep(2)



def run_add_loop(num_loops, dataset_id):
    assert num_loops > 0, "num_loops must be a number greater than 0"

    # Run replace loop multiple times
    for x in range(1, num_loops+1):

        msgt('%s) add loop' % (x))

        # prep file data
        #
        file_content = 'content: %s' % datetime.now()
        fname = 'add_%s.txt' % (`x`.zfill(4))
        files = {'file': (fname, file_content)}

        #files = {'file': open('input/test.csv', 'rb')}
        #files = {'file': open('input/test_01.xlsx', 'rb')}

        # prep other data
        #
        payload = dict()

        # Prep url (currently always the same)
        #
        url = '%s/datasets/%s/add?key=%s' % (url_base, dataset_id, API_KEY)
        print 'url', url
        print 'payload', payload

        # Make the request!
        #
        #r = requests.post(url, data=payload, files=files)
        r = requests.post(url, files=files)

        # Turn result into expected JSON
        #
        try:
            result_json = r.json()
        except:
            msgt('Error!')
            msg(r.text)
            msgx(r.status_code)

        msg("good add: %s" % json.dumps(result_json, indent=4))

        # Publish
        #run_publish_dataset(dataset_id)

        # Sleep
        msg('Sleep...')
        time.sleep(2)


if __name__ == '__main__':
    #run_publish_dataset(26)
    #run_add_test(26)
    #run_replace_test(26, 417)
    #run_replace_test(26, 417, True)
    #run_command_line_params()

    #run_replace_loop(5, 26, 610)#, force_replace=True)

    run_add_loop(1, 26)
