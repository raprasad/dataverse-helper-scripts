import requests
import sys
from datetime import datetime
import time

def msg(m): print m
def dashes(): msg('-' * 40)
def msgt(m): dashes(); msg(m); dashes()
def msgx(m): msgt(m); sys.exit(0)

API_KEY = open('key_str.txt').read().strip()

url_base = 'http://127.0.0.1:8080/api'

def run_add(fname='blackbox.txt'):
    msgt('ADD')
    url = '%s/upload/add/%s?key=%s' % (url_base, fname, API_KEY)

    print 'url: ', url

    r = requests.get(url)

    print r.status_code
    print r.text


def run_replace(old_fid):
    msgt('REPLACE: %s' % old_fid)

    url = '%s/upload/replace/%s?key=%s' % (url_base, old_fid, API_KEY)

    print 'url: ', url

    r = requests.get(url)

    print r.status_code
    print r.text



def run_resave(fid):

    url = '%s/upload/resave/%s?key=%s' % (url_base, fid, API_KEY)

    print 'url: ', url

    r = requests.get(url)

    print r.status_code
    print r.text

def run_publish_dataset(ds_id):
    msgt('PUBLISH')

    url = '%s/datasets/%s?key=%s' % (url_base, ds_id, API_KEY)

    r = requests.get(url)

    if r.status_code == 200:
        print 'published!'
    else:
        print r.text
        print r.status_code
        sys.exit(-1)

def run_upload_02():
    """
    @FormDataParam("file") InputStream uploadedInputStream,
        @FormDataParam("file") FormDataContentDisposition fileDetail,
        @FormDataParam("path") String path
    """

    params = dict(path="/Users/rmp553/Documents/iqss-git/dataverse-helper-scripts/src/api_scripts/output/hullo.txt")

    files = {'file': ('howdy.txt', open('input/howdy.txt', 'rb'), 'text/plain', {'Expires': '0'})}

    url = '%s/hello?key=%s' % (url_base, API_KEY)


    print 'url', url

    r = requests.post(url, files=files)

    print r.status_code
    #print r.text
    fout = 'output/result.html'
    open(fout, 'w').write(r.text.encode('utf-8'))
    print 'file written: %s' % fout

def run_replace_loop(orig_id, ds_id):

    orig_id = int(orig_id)

    for x in range(1, 2):
        # make new output file
        fh = open('input/howdy3.txt', 'w')
        fh.write('content: %s' % datetime.now())
        fh.close()
        print 'file '
        #open('input/howdy.txt', 'w').write()

        # publish
        run_publish_dataset(ds_id)
        time.sleep(2)

        # run replace
        run_replace(orig_id)
        time.sleep(2)
        orig_id += 1



if __name__ == '__main__':
    if len(sys.argv) == 3:
        if sys.argv[1].lower() == 'add':
            run_add(sys.argv[2])
        elif sys.argv[1].lower() == 'replace':
            run_replace(sys.argv[2])
        elif sys.argv[1].lower() == 'publish':
            run_publish_dataset(sys.argv[2])
    elif len(sys.argv) == 2:
        if sys.argv[1].lower() == 'loop':
            run_replace_loop(194, 10)
    else:
        print """
python test_01.py add [new file name]
python test_01.py replace [old file id]
python test_01.py publish [dataset id]
python test_01.py loop
"""
