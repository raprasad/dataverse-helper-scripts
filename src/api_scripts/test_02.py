from datetime import datetime
import json
import random
import sys
import time
from os.path import join, isdir, isfile

import requests

def msg(m): print (m)
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

def run_replace_loop_with_publish(num_loops, dataset_id, old_file_id, force_replace=False):
    run_replace_loop(num_loops, dataset_id, old_file_id, force_replace, True)

def run_replace_loop(num_loops, dataset_id, old_file_id, force_replace=False, publish_after_replace=False):
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

        params = dict(
                    forceReplace=force_replace,
                    description="Blue skies!",
                    categories=["Data", "Glue", "Foo", "Blue", "Zoo"],
                    #dataFileTags = ['Survey', 'Time Series', 'Panel', 'Event']
                    )

        payload = dict(jsonData=json.dumps(params))

        # Prep url (currently always the same)
        #
        url = '%s/files/%s/replace?key=%s' % (url_base, old_file_id, API_KEY)

        print 'url', url
        print 'payload', payload

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
        try:
            old_file_id = result_json['data']['files'][0]['dataFile']['id']
        except:
            msgx('Could not find file id: data->files[0]->dataFile->id: \n%s' % r.text)

        msg("good replace: %s" % json.dumps(result_json, indent=4))

        # Publish
        if publish_after_replace:
            run_publish_dataset(dataset_id)

        # Sleep
        msg('Sleep...')
        time.sleep(2)

def get_random_csv_contents(num_cols=10, num_lines=10):

    csv_lines = []

    fieldnames = [ 'col_%s' % x for x in range(1,num_cols+1)]
    csv_lines.append(','.join(fieldnames))

    for x in range(1, num_lines+1):
        vals = [ `x` for x in random.sample(range(1, 100), num_cols)]
        csv_lines.append(','.join(vals))

    return '\n'.join(csv_lines)

def run_add_loop(num_loops, dataset_id):
    assert num_loops > 0, "num_loops must be a number greater than 0"

    # Run replace loop multiple times
    for x in range(1, num_loops+1):

        msgt('%s) add loop' % (x))


        # ------------------------
        # Make a text "file" with the current timestamp
        # ------------------------
        """
        file_content = 'content: %s' % datetime.now()
        fname = 'add_%s.txt' % (`x`.zfill(4))
        files = {'file': (fname, file_content)}
        """

        # ------------------------
        # Make a random csv "file"
        # ------------------------
        file_content = get_random_csv_contents(random.randint(1,10), random.randint(1,10))
        #file_content = get_random_csv_contents(90, 100000)
        fname = 'add_%s.csv' % (`x`.zfill(4))
        files = {'file': (fname, file_content)}


        # ------------------------
        # Add a test shapefile
        # ------------------------
        #files = {'file': open('input/income_in_boston_gui.zip', 'rb')}

        # ------------------------
        # Add a test .zip
        # ------------------------
        #files = {'file': open('input/4files.zip', 'rb')}

        # prep other data
        #
        categories = ["Data", "Glue", "Foo", "Blue", "Zoo", "  Data  ", "Data", ""]
        dataFileTags = ['Survey', 'Time Series', 'Panel', 'Event']

        #tags = [ 'tag_%s' % `x`.zfill(4) for x in range(1, 20) ]

        params = dict(description="Blue skies!",
                    categories=categories)
                    #dataFileTags=dataFileTags)
        payload = dict(jsonData=json.dumps(params))

        # Prep url (currently always the same)
        #
        url = '%s/datasets/%s/add?key=%s' % (url_base, dataset_id, API_KEY)

        #url = '%s/datasets/:persistentId/add?key=%s&persistentId=%s' %\
        #            (url_base, API_KEY, 'doi:10.5072/FK2/6XACVA')

        print 'url', url
        print 'payload', payload

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

        msg("good add: %s" % json.dumps(result_json, indent=4))

        # Publish
        #run_publish_dataset(dataset_id)

        # Sleep
        seconds = 2
        msg('Sleep %d seconds...' % seconds)
        time.sleep(seconds)

def get_dataset_json(dataset_id):

    url = '%s/datasets/%s?key=%s' % (url_base, dataset_id, API_KEY)

    r = requests.get(url)

    #msg("response:\n%s" % json.dumps(r.json(), indent=4))

    files_only = r.json()['data']['latestVersion']['files']
    msg("response:\n%s" % json.dumps(files_only, indent=4))

    msgt('status code: %s' % r.status_code )

def make_test_csv_files(num_files=10):


    for fnum in range(1, num_files+1):
        file_content = get_random_csv_contents(random.randint(1,10), random.randint(50000,70000))
        fname = join('output', 'test_csv_%s.csv' % `fnum`.zfill(6))
        open(fname, 'w').write(file_content)
        msg('file written: %s' % fname)


if __name__ == '__main__':
    dataset_id = 2    # ID of Dataset to add or replace files
    run_add_loop(10, dataset_id)  # (number of files to add, dataset_id)
    #run_replace_loop(1, dataset_id, 845, force_replace=True)
    #run_replace_loop_with_publish(1, dataset_id, 845, force_replace=True)
    #run_replace_test(26, 417)
    #run_replace_test(26, 417, True)
    #run_command_line_params()

    #run_publish_dataset(dataset_id)
    #get_dataset_json(dataset_id)

    #run_replace_loop_with_publish

    #make_test_csv_files(25)
