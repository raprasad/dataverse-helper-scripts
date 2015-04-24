from stress_settings import *

import os, sys
import sys
from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass
        #self.login()

    def login(self):
        r = self.client.post('/loginpage.xhtml?redirectPage=/dataverse.xhtml'\
                        , {"loginForm:credentialsContainer2:0:credValue":"admin"
                        , "loginForm:credentialsContainer2:1:sCredValue":"admin"\
                        #, "loginForm:loginSystemSelect" : "builtin"\
                        , "loginForm" : "loginForm"\
                        })
        print 'status code: %s' % r.status_code
        print 'LOGIN SUCCESS :):):)'

    @task(2)
    def homepage(self):
        msg('> Go to homepage. Locust instance (%s)' % self.locust)
        self.client.get("/")

    @task(1)
    def profile_page(self):
        msg('> Go to profile page (%s)' % self.locust)
        self.client.get("/dataverseuser.xhtml")
        

class WebsiteUser(HttpLocust):
    host = 'https://dvn-build.hmdc.harvard.edu'
    #host = 'https://dataverse-demo.iq.harvard.edu'
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000
