from stress_settings import *

import os, sys
import sys
import random, string
from random import randint
from locust import HttpLocust, TaskSet, task
from bs4 import BeautifulSoup

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass
        #self.login()


    #@task(1)
    def login(self):
        msg('> login')
        random_user = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        random_pass = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        r = self.client.post('/loginpage.xhtml?redirectPage=/dataverse.xhtml'
                        , {"loginForm:credentialsContainer2:0:credValue": random_user
                        , "loginForm:credentialsContainer2:1:sCredValue": random_pass
                        , "loginForm" : "loginForm"\
                        })
        print 'status code: %s' % r.status_code
        print 'LOGIN SUCCESS :):):)'

    @task(1)
    def homepage(self):
        msg('> Go to homepage. Locust instance (%s)' % self.locust)
        r = self.client.get("/")
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
        
        self.client.get(ds_url)
        
            

    @task(1)
    def profile_page(self):
        msg('> Go to profile page (%s)' % self.locust)
        self.client.get("/dataverseuser.xhtml")
        

class WebsiteUser(HttpLocust):
    #host = 'https://dvn-build.hmdc.harvard.edu'
    host = get_creds_info('SERVER')
    task_set = UserBehavior
    min_wait=5000
    max_wait=20000
