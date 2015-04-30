from stress_settings import get_creds_info
from dataverse_tasks import homepage,\
    random_dataset_page,\
    login_page_but_no_login,\
    homepage_files_facet,\
    login_fail_with_random_user_pw,\
    login_attempt_with_user1_from_creds,\
    login_attempt_with_random_user_from_creds,\
    download_file

from locust import HttpLocust, TaskSet


class BrowsingBehavior(TaskSet):
    tasks = {homepage: 25,
             random_dataset_page: 25,
             #login_page_but_no_login: 10,
             homepage_files_facet: 25,
             #login_fail_with_random_user_pw: 5,
             download_file: 25,
            }
    def on_start(self):
        login_attempt_with_random_user_from_creds(self)

class WebsiteUser(HttpLocust):
    host = get_creds_info('SERVER')
    task_set = BrowsingBehavior
    min_wait = 5000
    max_wait = 20000

"""
locust -f basic_test_01.py
http://127.0.0.1:8089/
"""