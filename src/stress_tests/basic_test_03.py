from stress_settings import get_creds_info
from dataverse_tasks import homepage,\
    random_dataset_page,\
    login_page_but_no_login,\
    homepage_files_facet,\
    login_fail_with_random_user_pw,\
    login_attempt_with_user1_from_creds,\
    login_attempt_with_random_user_from_creds,\
    random_download_file,\
    profile_page,\
    download_1g_file,\
    harvested_page,\
    assign_and_revoke_role

import requests
requests.packages.urllib3.disable_warnings()

from locust import HttpLocust, TaskSet


class BrowseAndDownloadBehavior(TaskSet):
    tasks = {assign_and_revoke_role:1,
             #homepage: 20,
             #random_dataset_page: 25,
             #harvested_page: 5,
             #profile_page: 5
             #homepage_files_facet: 5, # heavier hit on homepage
             #random_download_file: 5,
             #download_1g_file: 1,
            }

    def on_start(self):
        pass
        #login_attempt_with_random_user_from_creds(self)


class WebsiteUser(HttpLocust):
    host = get_creds_info('SERVER')
    task_set = BrowseAndDownloadBehavior
    min_wait = 5000     # min pause before new task
    max_wait = 20000    # max pause before new task

"""
locust -f basic_test_01.py
http://127.0.0.1:8089/
"""
