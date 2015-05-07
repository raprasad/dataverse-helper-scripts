import requests
import json
from os.path import join, isdir, isfile
import os
from github_scrape_settings import *#get_repository_creds

OUTPUT_DIR = 'output'
# If I were interested in exporting all tickets labeled with UX Upgrade into a csv, how would I do that? Additionally, if I wanted all tickets assigned to @eaquigley and @mheppler? Do you know?

"""
Exports Issues from a specified repository to a CSV file

Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import requests
import urllib

REPO = get_repository_repo('dataverse')#'iqss/dataverse'  # format is username/repo
AUTH = get_repository_creds('dataverse')  #(GITHUB_USER, GITHUB_PASSWORD)



ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?assignee=raprasad' % REPO #'?milestone=4.0.3' % REPO
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?labels=%s' % (REPO, urllib.quote('Component: UX & Upgrade'))
#ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues?milestone=3' % (REPO)
#'?milestone=4.0.3' % REPO

def write_issues(response, csvout):
    "output a list of issues to csv"
    if not response.status_code == 200:
        raise Exception(r.status_code)
    for issue in response.json():

        # Labels
        label_names = []
        for label in issue['labels']:
            label_names.append(label['name'])
        if len(label_names) == 0:
            label_str = ''
        else:
            label_str = ', '.join(label_names)

        # Milestone
        if 'milestone' in issue and issue['milestone'] is not None:#and 'title' in issue['milestone']:
            #print json.dumps(issue, indent=4)
            #msgx('blah')
            #.get('milestone', {}).get('title', None) is not None:
            mstone_title = issue['milestone']['title'].encode('utf-8')
        else:
            mstone_title = 'no milestone assigned'
        
        if 'assignee' in issue and issue['assignee'] is not None:#and 'title' in issue['milestone']:
            assignee = issue['assignee']['login'].encode('utf-8')
        else:
            assignee = 'Not assigned'
        
        csvout.writerow([issue['number'], 
                        issue['title'].encode('utf-8'), 
                        label_str.encode('utf-8'),
                        issue['body'].encode('utf-8'), 
                        mstone_title, 
                        issue['user']['login'].encode('utf-8'),
                        assignee,
                        issue['created_at'], 
                        issue['updated_at'],
                        issue['html_url']
                        #'<a href="%s">github link</a>' % issue['html_url']
                        ])
        print json.dumps(issue, indent=4)
    """
    Ticket #
    Ticket Name
    Labels
    Description
    Milestone
    Assignee
    """ 



def make_api_call(to_csv=True):

    csvfile = 'UX-upgrade-issues-2016-0507.csv' #% (REPO.replace('/', '-'))
    csvout = csv.writer(open(csvfile, 'wb'))
    csvout.writerow(('Ticket #',
                     'Title',
                     'Labels',
                     'Description',
                     'Milestone',
                     'Creator',
                     'Assignee',
                     'Created At',
                     'Updated At',
                     'HTML URL'))

    msgt('make_api_call: %s' % ISSUES_FOR_REPO_URL)
    msg(AUTH)
    page_num = 1
    output_fname = join(OUTPUT_DIR, 'scrape_%s.json' % (str(page_num).zfill(2)))
    if not isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
    print r.text
    print r.headers
    print r.status_code

    if to_csv:
        write_issues(r, csvout)
    else:
        open(output_fname, 'w').write(json.dumps(r.json(), indent=4))
        print 'file written: %s' % output_fname

    current_link = ISSUES_FOR_REPO_URL
    pages=dict(next='next', last='last')

    while not pages['next'] == pages['last']:

        if 'link' in r.headers:
            pages = dict(
                [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                    [link.split(';') for link in
                        r.headers['link'].split(',')]])
            if 'next' in pages and not pages['next'] == ISSUES_FOR_REPO_URL:
                page_num+=1
                msgt('(%s) %s'% (page_num, pages['next']))
                output_fname = join(OUTPUT_DIR, 'scrape_%s.json' % (str(page_num).zfill(2)))

                r = requests.get(pages['next'], auth=AUTH)
                if to_csv:
                    write_issues(r, csvout)
                else:
                    open(output_fname, 'w').write(json.dumps(r.json(), indent=4))
                    print 'file written: %s' % output_fname



if __name__=='__main__':
    make_api_call()
"""
 if is_closed:
        # https://github.com/IQSS/geoconnect/issues?q=is:closed+milestone:"{ milestone title }"+
        return urljoin(GITHUB_VIEW_URL_BASE\
                    , github_obj.repository.organization.github_login\
                    , github_obj.repository.github_name\
                    , 'issues?q=is:closed+milestone:"%s"' %  urllib.quote((github_obj.title))\
                )

github_scrape_settings
"""
