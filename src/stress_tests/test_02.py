from stress_settings import *

import os, sys
import sys
import random, string
from random import randint
from locust import HttpLocust, TaskSet, task
from bs4 import BeautifulSoup


def get_locust_request_kwargs():
    return dict(verify=False)

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass
        #self.login()


    #@task(1)
    def login(self):
        msg('> login')
        random_user = 'dataverseAdmin' #''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        random_pass = 'crashtest2015' #''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        r = self.client.post('/loginpage.xhtml?redirectPage=/dataverse.xhtml'
                        , {"loginForm:credentialsContainer2:0:credValue": random_user
                        , "loginForm:credentialsContainer2:1:sCredValue": random_pass
                        , "loginForm" : "loginForm"\
                        }, **get_locust_request_kwargs())
        print 'status code: %s' % r.status_code
        print 'LOGIN SUCCESS :):):)'

        
    #def login_page(self):
    #https://dataverse.harvard.edu/loginpage.xhtml

    @task(1)
    def homepage(self):
        msg('> Go to homepage. Locust instance (%s)' % self.locust)
        r = self.client.get("/?q=&types=files", **get_locust_request_kwargs())
        #https://dataverse.harvard.edu/?q=&types=files
        #&fq0=fileTypeGroupFacet%3A%22tabulardata%22&sort=dateSort&order=desc&page=1
        """
        if r.status_code == 200:
            soup = BeautifulSoup(r.text)
            links = soup.find_all('a')
            dataset_links = [ l for l in links if l.get('href', '').find('dataset.xhtml') > -1 ]
            if len(dataset_links) > 0:
                rand_idx = randint(0, len(dataset_links)-1)
                selected_link = dataset_links[rand_idx]
                msgt('Random dataset link: %s' % selected_link)
                self.client.get(selected_link.get('href'))
        """

    @task(1)
    def random_vm5_dataset(self):
        ids = """29669 55LJ9P 6AOL3H DDDOKP MPU019 OJZKKP VZLVVI ZJNG1N""".split()
        rand_idx = randint(0, len(ids)-1)
        selected_id = ids[rand_idx]
        
        ds_url = '/dataset.xhtml?persistentId=doi:10.7910/DVN/%s' % selected_id
        
        self.client.get(ds_url, **get_locust_request_kwargs())

    @task(1)
    def download_file(self):
        """
        http://dvn-vm5.hmdc.harvard.edu:8080/api/access/datafile/2670610
        """

        id_map = dict(mb_1=2670612,
                        mb_2=2670613,
                        mb_5=2670608,
                        mb_10=2670609,
                        mb_50=2670614,
                        mb_100=2670611,
                        k_250=2670610,
                        k_500=2670615,
                        #gb_1=
                        )
        
        rand_selection = random.choice(id_map.keys())
        #rand_selection = "mb_100"
        
        assert id_map.has_key(rand_selection), "file size key not found.  Valid values: %s" % id_map.keys()
        #if randint(1,2) != 1:
        #    return

        download_url = '/api/access/datafile/%s' % id_map.get(rand_selection)

        msg("Download file (%s): %s " % (rand_selection, download_url))

        self.client.get(download_url, **get_locust_request_kwargs())


    @task(0)
    def profile_page(self):
        msg('> Go to profile page (%s)' % self.locust)
        self.client.get("/dataverseuser.xhtml", **get_locust_request_kwargs())
        

class WebsiteUser(HttpLocust):
    #host = 'https://dvn-build.hmdc.harvard.edu/'
    host = get_creds_info('SERVER')
    task_set = UserBehavior
    min_wait=5000
    max_wait=20000

"""
locust -f test_02.py
http://127.0.0.1:8089/

http://www.data.gov/
"""
