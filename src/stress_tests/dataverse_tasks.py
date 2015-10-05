from stress_settings import *
import random, string
#from bs4 import BeautifulSoup


FILE_ID_MAP = dict(k_250=2670610,
                  k_500=2670615,
                  mb_1=2670612,
                  mb_2=2670613,
                  mb_5=2670608,
                  mb_10=2670609,
                  mb_50=2670614,
                  mb_100=2670611,
                  #gb_1=2670827
                  )

def get_locust_request_kwargs():
    return dict(verify=False,)   # allow a self-signed certificate

def login_page_but_no_login(l):
    msg('> login page (but no login)')
    l.client.get('/loginpage.xhtml', **get_locust_request_kwargs())

def harvested_page(l):
    msg('> harvested_page')
    l.client.get('/dataverse/harvested', **get_locust_request_kwargs())
    #rhttps://dataverse.harvard.edu/dataverse/harvested
    
def homepage(l):
    msg('> homepage')
    l.client.get('/', **get_locust_request_kwargs())

def homepage_files_facet(l):
    msg('> homepage (q=&types=files)')
    l.client.get('/?q=&types=files', **get_locust_request_kwargs())

def profile_page(l):
    msg('> profile_page')
    l.client.get('/dataverseuser.xhtml', **get_locust_request_kwargs())


def random_dataset_page(l):
    msg('> random_dataset_page')

    persistent_ids = get_creds_info(KEY_PERSISTENT_IDS)    
    assert persistent_ids is not None, 'No values found in creds file for %s' % KEY_PERSISTENT_IDS
    assert len(persistent_ids) > 0, 'No values found in creds file for list %s' % KEY_PERSISTENT_IDS
    
    random_id_info = random.choice(persistent_ids) 
    
    pid = random_id_info['id']

    dataset_url = '/dataset.xhtml?persistentId=%s' % pid

    l.client.get(dataset_url, **get_locust_request_kwargs())


def login_attempt_with_user1_from_creds(l):

    username, password = get_user_creds(1)
    
    form_vals = {"loginForm:credentialsContainer2:0:credValue": username,
                 "loginForm:credentialsContainer2:1:sCredValue": password,
                 "loginForm": "loginForm"}

    r = l.client.post('/loginpage.xhtml?redirectPage=/dataverse.xhtml',
                form_vals,
                **get_locust_request_kwargs())

    if r.status_code == 200:
        msg('login success!')
    else:
        msg('login fail')

def login_attempt_with_random_user_from_creds(l):

    username, password = get_random_user_creds()

    form_vals = {"loginForm:credentialsContainer2:0:credValue": username,
                 "loginForm:credentialsContainer2:1:sCredValue": password,
                 "loginForm": "loginForm"}

    r = l.client.post('/loginpage.xhtml?redirectPage=/dataverse.xhtml',
                form_vals,
                **get_locust_request_kwargs())

    if r.status_code == 200:
        msg('login success!')
    else:
        msg('login fail')

def login_fail_with_random_user_pw(l):
    msg('> Login Fail with random user/password')

    random_user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    random_pass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    form_vals = {"loginForm:credentialsContainer2:0:credValue": random_user,
                "loginForm:credentialsContainer2:1:sCredValue": random_pass,
                "loginForm": "loginForm"}

    r = l.client.post('/loginpage.xhtml?redirectPage=/dataverse.xhtml',
                form_vals,
                **get_locust_request_kwargs())
    
    if r.status_code == 200:
        msg('login success!')
    else:
        msg('login fail')

def download_1g_file(l):

    download_url = '/api/access/datafile/%s' % FILE_ID_MAP.get('gb_1')

    msg("> Download 1gb file: %s " % (download_url))

    l.client.get(download_url, **get_locust_request_kwargs())



def random_download_file(l):
    """
    http://dvn-vm5.hmdc.harvard.edu:8080/api/access/datafile/2670610
    """
    global FILE_ID_MAP

    #gb_1=

    rand_selection = random.choice(FILE_ID_MAP.keys())
    #rand_selection = "mb_100"
        
    assert rand_selection in FILE_ID_MAP, "file size key not found.  Valid values: %s" % id_map.keys()
    
    download_url = '/api/access/datafile/%s' % FILE_ID_MAP.get(rand_selection)

    msg("> Download file (%s): %s " % (rand_selection, download_url))

    l.client.get(download_url, **get_locust_request_kwargs())