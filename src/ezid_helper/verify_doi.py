from os.path import isdir, isfile, join
import os
import json
import time
import requests

from ezid_settings import * # includes file and directory settings


def get_verfied_doi_info(output_file_fname):
    """
    Get DOI info from file, or return empty dict if file not created
    """
    if not isfile(output_file_fname):
        return {}
    
    fh = open(output_file_fname, 'r')
    contents = fh.read()
    fh.close()

    if contents.strip() == '':
        return {}
    return json.loads(contents)

def save_verified_doi_info(single_doi, output_file_fname):
    """
    single_doi { dataset_id : { "success" : true/false,
                                "current_url" : "current-target-url",
                                 "expected_url" : "expected-target-url"
                            }
                }
    """
    if single_doi is None:
        return
        
    # Get the DOI info
    doi_info = get_verfied_doi_info(output_file_fname)
    
    # Update it
    doi_info.update(single_doi)
    
    # Save it to a file
    as_json = json.dumps(doi_info, indent=4)
    
    fh = open(output_file_fname, 'w')
    fh.write(as_json)
    fh.close()
    msg('file update')
    

def check_doi_files(start_num=1, end_num=9999):
    # Iterate through input lines
    assert isfile(INPUT_FILE), 'File not found: %s' % INPUT_FILE

    flines = open(INPUT_FILE, 'r').readlines()
    flines = [ x.strip() for x in flines if len(x.strip()) > 0]

    cnt = 0

    for fline in flines:
        cnt += 1

        # Parse each input line
        #
        dataset_id, protocol, authority, identifier = fline.split('|')
        msgt('(%s) verify: %s' % (cnt, fline))

        if cnt < start_num or dataset_id.startswith('#'):
            msg('Skipping...')
            continue
        if cnt > end_num:
            msg('Break...')
            break

        expected_text = 'https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:%s/%s' % (authority, identifier)
        direct_db_link = 'https://dataverse.harvard.edu/dataset.xhtml?id=%s' % (dataset_id)

        DOI_OUTPUT_FNAME = join(DOI_OUTPUT_FOLDER, '%s.json' % dataset_id)

        if not isfile(DOI_OUTPUT_FNAME):
            not_found_doi = { int(dataset_id) : dict(input_line=fline,
                                                  dv_url=expected_text,
                                                  direct_db_url=direct_db_link)
                            }
            save_verified_doi_info(not_found_doi, VERIFY_NOT_FOUND_FILE)
            msgt("Info file not found: %s" % DOI_OUTPUT_FNAME)
            continue

        content = open(DOI_OUTPUT_FNAME, 'r').read()
        if content.find(expected_text) > -1:
            single_doi = { int(dataset_id) : dict(success=True,
                                              current_url=expected_text,
                                              expected_url=expected_text,
                                              direct_db_url=direct_db_link,
                                              input_line=fline)
                        }
        else:
            #os.remove(DOI_OUTPUT_FNAME)
            #print 'file deleted: %s' % DOI_OUTPUT_FNAME
            #continue
            actual_url = 'unknown'
            for ezid_line in content.split('\n'):
                #_target: https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/0NMD8
                items = ezid_line.split(":", 1)
                if len(items)==2 and items[0]=='_target':
                    actual_url = items[1].strip()

            single_doi ={ int(dataset_id) : dict(success=False,
                                              current_url=actual_url,
                                              expected_url=expected_text,
                                              direct_db_url=direct_db_link,
                                              input_line=fline)
                          }
            save_verified_doi_info(single_doi, VERIFY_OUTPUT_FILE)


def download_doi_metadata(start_num=1, end_num=9999):
    """
    Use the ezid API to pull down the current metadata for a DOI
    Save the info to output files for later checking.
    (This is fairly ad hoc..)
    """
    assert isfile(INPUT_FILE), 'File not found: %s' % INPUT_FILE
    
    flines = open(INPUT_FILE, 'r').readlines()
    flines = [ x.strip() for x in flines if len(x.strip()) > 0]

    cnt = 0

    login_url = 'https://ezid.cdlib.org/login'

    sess = requests.Session()
    sess.auth = (get_creds_info('EZID_USERNAME'),
                 get_creds_info('EZID_PASSWORD'))

    msgt('login: %s' % login_url)
    r = sess.get(login_url)
    
    msg('status code: %s' % r.status_code)
    msg('status text: %s' % r.text)
    if not r.status_code == 200:
        msgx('Failed to log into EZID.  Check your creds JSON file for EZID_USERNAME/EZID_PASSWORD')

    # Iterate through input lines
    for fline in flines:
        cnt += 1

        # Parse each input line
        #
        dataset_id, protocol, authority, identifier = fline.split('|')
        msgt('(%s) verify: %s' % (cnt, fline))
        
        if cnt < start_num or dataset_id.startswith('#'):
            msg('Skipping...')
            continue
        if cnt > end_num:
            msg('Break...')
            break

        persisent_url = 'http://dx.doi.org/%s/%s' % (authority, identifier)
        api_url = 'http://ezid.cdlib.org/id/doi:%s/%s' % (authority, identifier)
        expected_text = 'https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:%s/%s' % (authority, identifier)

        msg('ezid api_url: %s' % api_url)
        DOI_OUTPUT_FNAME = join(DOI_OUTPUT_FOLDER, '%s.json' % dataset_id)

        if isfile(DOI_OUTPUT_FNAME):
            if os.stat(DOI_OUTPUT_FNAME).st_size == 0:
                msg("0 byte file, remove it")
                os.remove(DOI_OUTPUT_FNAME)
            else:
                msg("Already retrieved")
                continue
            
        msgt('doi: %s' % api_url)
        r = sess.get(api_url)
        print r.status_code
        print r.text
        if r.status_code == 200:
            open(DOI_OUTPUT_FNAME, 'w').write(r.text.encode('utf-8'))
            msg('file written: %s' % DOI_OUTPUT_FNAME)
        else:    
            if isfile(DOI_OUTPUT_FNAME):
                os.remove(DOI_OUTPUT_FNAME)
            msgt('Failed at line %s\n%s' % (cnt, fline))

if __name__=='__main__':
    #check_doi_files(start_num=1, end_num=9999)
    download_doi_metadata(start_num=1, end_num=9999)


"""
Handle not found
24
"""
"""
http://ezid.cdlib.org/lookup
66319|doi|10.7910/DVN|29379
"""

"""

print r.status_code
print r.text

doi_str = '10.7910/DVN/29379'
api_url = 'https://ezid.cdlib.org/id/doi:%s' % (doi_str)

payload = { '_target' : 'https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:%s' % doi_str }
dstr = '_target=https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/29379'
r = requests.post(api_url, data=dstr, auth=('user', 'pass'))
print r.status_code
print r.text
"""
#[40, 97, 222, 424, 442, 2151, 4297, 4361, 4512, 4697, 4698, 5032, 5170, 5597, 5604, 5662, 5681, 5682, 5684, 5687, 5688, 5692, 5693, 5696, 5700, 5701, 5722, 6103, 6451]
