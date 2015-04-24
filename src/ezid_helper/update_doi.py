from ezid_settings import *
import os
import json
import requests

FAIL_LINES = []


def get_dataset_api_url(dataset_id):
    assert dataset_id is not None, "dataset_id cannot be None"

    return '%s/api/datasets/%s/?key=%s' % \
                            (   get_creds_info('SERVER'),
                                dataset_id,
                                get_creds_info('API_KEY'),
                            )
    

def get_modify_doi_url(dataset_id):
    """
    http://localhost:8080/api/datasets/11/modifyRegistration?key=--API-KEY--
    """    
    assert dataset_id is not None, "dataset_id cannot be None"
        
    return '%s/api/datasets/%s/modifyRegistration?key=%s' % \
                            (   get_creds_info('SERVER'),
                                dataset_id,
                                get_creds_info('API_KEY'),
                            )



def run_direct_ezid_doi_update_on_json_file(json_fname):
    msgx('NEED TO REDO - WASN\'T MAKING UPDATE')
    assert isfile(json_fname), "file not found: %s" % json_fname

    json_info = json.loads(open(json_fname, 'r').read())

    cnt = 0
    for dataset_id, dict in json_info.items():
        info_line = dict.get('input_line', None)
        if info_line is None:
            msgx("info line not found in dict: %s for database_id %s" % (dict, dataset_id))
        cnt += 1
        msgt('(%s) update: %s' % (cnt, info_line))
        dataset_id, protocol, authority, identifier = info_line.split('|')


        #DOI_OUTPUT_FNAME = join(DOI_OUTPUT_FOLDER, '%s.json' % dataset_id)
        #if isfile(DOI_OUTPUT_FNAME):
        #    os.remove(DOI_OUTPUT_FNAME) 
        #continue
        api_url = 'https://ezid.cdlib.org/id/doi:%s/%s' % (authority, identifier)

        payload = '_target=https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:%s/%s' % (authority, identifier)
        sess_auth = (get_creds_info('EZID_USERNAME'),
                 get_creds_info('EZID_PASSWORD'))
        msg('payload: %s' % payload)
        msg('api_url: %s' % api_url)
        r = requests.post(api_url, data=payload, auth=sess_auth)
        msg('status_code: %s' % r.status_code)
        msg('text: %s' % r.text)


def run_dataverse_doi_update_on_json_file(json_fname):
    assert isfile(json_fname), "file not found: %s" % json_fname

    json_info = json.loads(open(json_fname, 'r').read())

    cnt = 0
    for dataset_id, dict in json_info.items():
        info_line = dict.get('input_line', None)
        if info_line is None:
            msgx("info line not found in dict: %s for database_id %s" % (dict, dataset_id))
        cnt += 1
        msgt('(%s) update: %s' % (cnt, info_line))
        dataset_id, protocol, authority, identifier = info_line.split('|')

        DOI_OUTPUT_FNAME = join(DOI_OUTPUT_FOLDER, '%s.json' % dataset_id)
        if isfile(DOI_OUTPUT_FNAME):
            os.remove(DOI_OUTPUT_FNAME) 
            msg('removed: %s' % DOI_OUTPUT_FNAME)
            continue
        
        #------------------------------------
        # Run against dataverse API
        #------------------------------------                
        api_url = get_modify_doi_url(dataset_id)
        msg('api_url: %s' % api_url)

        r = requests.get(api_url)
        msgd('r.status_code: %s' % r.status_code)
        msgd('r.text: %s' % r.text)

        msg('get_dataset_api_url:\n%s' % get_dataset_api_url(dataset_id))
        if r.status_code == 200:
            fh = open(OUTPUT_FILE_FOR_UPDATES, 'a')
            fh.write('%s|%s\n' % (info_line, 'true'))
            msg('file updated')
        else:    
            FAIL_LINES.append(cnt)
            #msgx('Failed at line %s\n%s' % (cnt, fline))
        
        msgd('FAIL_LINES: %s' % FAIL_LINES)
        

def run_direct_ezid_doi_update(protocol, authority, identifier):
    msgx('NEED TO REDO - WASN\'T MAKING UPDATE')

    assert protocol is not None, 'protocol cannot be None'
    assert authority is not None, 'authority cannot be None'
    assert identifier is not None, 'identifier cannot be None'
    
    
    doi_str = '%s:%s/%s' % (protocol, authority, identifier)
    
    api_url = 'https://ezid.cdlib.org/id/%s' % (doi_str)

    payload = '_target=https://dataverse.harvard.edu/dataset.xhtml?persistentId=%s' % (doi_str)

    sess_auth = (get_creds_info('EZID_USERNAME'),
             get_creds_info('EZID_PASSWORD'))
    msg('payload: %s' % payload)
    msg('api_url: %s' % api_url)
    r = requests.post(api_url, data=payload, auth=sess_auth)
    msg('status_code: %s' % r.status_code)
    msg('text: %s' % r.text)
    if r.status_code == 200:
        return True
        
    return False

def run_doi_update(start_num=1, end_num=9999):
    
    assert isfile(INPUT_FILE), 'File not found: %s' % INPUT_FILE
    
    flines = open(INPUT_FILE, 'r').readlines()
    flines = [ x.strip() for x in flines if len(x.strip()) > 0]

    cnt = 0
    update_cnt = 0
    for fline in flines:
        cnt += 1
        line_items = fline.split('|', 4)
        #print 'line_items', line_items
        
        assert len(line_items) >= 4, 'Line needs at least 4 items: dataset_id, protocol, authority, and identifier.  Delimiter is "|"'
        
        if len(line_items) == 4:
            dataset_id, protocol, authority, identifier = line_items       
        else:        
            dataset_id, protocol, authority, identifier, extra = line_items
        
        #print dataset_id, protocol, authority, identifier, extra
        if cnt < start_num or dataset_id.startswith('#'):
            msg('skipping')
            continue
        if cnt > end_num:
            msg('break (cnt past end_num)')            
            break
        #if authority.find('/DVN1') > -1:
        #    msg('skipping dvn1')
        #    continue

        #if not authority.endswith('/DVN1'): # for the DVN update
        #    #msg('skipping non-dvn 1')
        #    continue
        
        update_cnt +=1
        msgt('(%s)(%s) process: %s' % (update_cnt, cnt, fline))
       
        #------------------------------------
        # Run against dataverse API
        #------------------------------------                
        api_url = get_modify_doi_url(dataset_id)
        msg('api_url: %s' % api_url)

        r = requests.get(api_url)
        msgd('r.status_code: %s' % r.status_code)
        msgd('r.text: %s' % r.text)

        msg('get_dataset_api_url:\n%s' % get_dataset_api_url(dataset_id))
        if r.status_code == 200:
            fh = open(OUTPUT_FILE_FOR_UPDATES, 'a')
            fh.write('%s|%s\n' % (fline, 'true'))
            msg('file updated')
        else:    
            FAIL_LINES.append(cnt)
            #msgx('Failed at line %s\n%s' % (cnt, fline))
        
        msgd('FAIL_LINES: %s' % FAIL_LINES)
        
        break    
        

if __name__=='__main__':
    #run_doi_update(start_num=7716, end_num=7716)
    #Xrun_direct_ezid_doi_update_on_json_file(INPUT_FILE_RETRIES_03)
    run_dataverse_doi_update_on_json_file(INPUT_FILE_RETRIES_03)
"""
pip install requests[security]
"""    
    
    