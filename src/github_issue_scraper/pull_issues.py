# variation of this gist: https://gist.github.com/unbracketed/3380407
import os
import requests
import json
import csv
import urllib

from github_scrape_settings import *


REPO = get_repository_repo('dataverse')
AUTH = get_repository_creds('dataverse')


class GithubIssueToCSV(object):

    def __init__(self, output_file_name, **kwargs):

        self.print_issue = kwargs.pop('print_issue', False)

        self.output_file_name = join(OUTPUT_DIR, output_file_name)

        self.csv_writer = None

        self.query_filter_attrs = ('labels', 'assignee', 'creator' )
        self.query_str = ''

        self.set_query_string_filters(kwargs)

    def set_query_string_filters(self, kwarg_dict):
        """
        Format optional query string.
            example: "?labels=UX,design&assignee=username"
        """
        self.query_str = ''

        if kwarg_dict is None:
            return

        qstr_parts = []
        for k, v in kwarg_dict.items():
            if v is not None:
                qstr_parts.append('%s=%s' % (k, urllib.quote(v)))

        if len(qstr_parts) > 0:
            self.query_str = '?%s' % ('&'.join(qstr_parts))


    def get_api_issues_url(self):
        """
        For the API url, use the repo specified in creds.json
        """
        return 'https://api.github.com/repos/%s/issues%s' % (REPO, self.query_str)


    def get_csv_header_row(self):
        return ('Ticket #',
                 'Title',
                 'Labels',
                 'Description',
                 'Milestone',
                 'Creator',
                 'Assignee',
                 'Created At',
                 'Updated At',
                 'HTML URL')


    def initialize_output_file(self):

        # Remove existing output file, if it exists
        if isfile(self.output_file_name):
            os.remove(self.output_file_name)

        # Init the csv writer
        self.csv_writer = csv.writer(open(self.output_file_name, 'wb'))

        # Write the header row
        self.csv_writer.writerow(self.get_csv_header_row())


    def format_label_str(self, issue):

        assert isinstance(issue, dict), "Issue must be a dict"
        assert 'labels' in issue, "'labels' not found in issue dict: %s" % issue

        label_list = issue['labels']
        if label_list is None or len(label_list) == 0:
            return ''

        label_names = []
        for label in label_list:
            label_names.append(label['name'].encode('utf-8'))   # Name should always exist

        if len(label_names) == 0:
            return ''

        return ', '.join(label_names)


    def format_milestone_title(self, issue):
        assert isinstance(issue, dict), "Issue must be a dict"

        if 'milestone' not in issue or issue['milestone'] is None:
           return 'no milestone assigned'

        # crash if title not there
        return issue['milestone']['title'].encode('utf-8')

    def format_assignee(self, issue):
        assert isinstance(issue, dict), "Issue must be a dict"

        if 'assignee' in issue and issue['assignee'] is not None:
            return issue['assignee']['login'].encode('utf-8')
        else:
            return 'Not assigned'


    def write_issues(self, response):
        """Write a list of issues to CSV"""
        assert response is not None, "response cannot be None"
        assert self.csv_writer is not None, "csv_writer was not initialized"

        if not response.status_code == 200:
            raise Exception(r.status_code)

        # Iterate through issues
        for issue in response.json():

            # Format individual issue and write to CSV
            label_str = self.format_label_str(issue)    # Format Labels
            milestone_title = self.format_milestone_title(issue)    # Format Milestone
            assignee_str = self.format_assignee(issue)  # Format Assignee

            self.csv_writer.writerow([issue['number'],
                            issue['title'].encode('utf-8'),
                            label_str,
                            issue['body'].encode('utf-8'),
                            milestone_title,
                            issue['user']['login'].encode('utf-8'),
                            assignee_str,
                            issue['created_at'],
                            issue['updated_at'],
                            issue['html_url']
                            #'<a href="%s">github link</a>' % issue['html_url']
                            ])
            if self.print_issue:
                msg(json.dumps(issue, indent=4))


    def get_pages_dict_from_headers(self, headers):

        assert headers is not None, "headers cannot be None"

        if 'link' not in headers:
            return None

        link_list = [link.split(';') for link in headers['link'].split(',')]
        rel_url_pairs_list = [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in link_list]
        page_dict = dict(rel_url_pairs_list)

        return page_dict
        #pages = dict(
        #            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
        #                [link.split(';') for link in
        #                    r.headers['link'].split(',')]])

    def run_csv_maker(self, to_csv=True):

        msgt('Create csv file')

        self.initialize_output_file()

        # Get API url
        api_url = self.get_api_issues_url()
        msg('Make request: %s' % api_url)

        # Make the request
        r = requests.get(api_url, auth=AUTH)

        if not r.status_code == 200:
            msg(r.text)
            msgx('Failed with status code: %s' % r.status_code)

        # Write results of 1st page to CSV
        #
        page_num = 1
        msgt('(%s) %s'% (page_num, api_url))
        self.write_issues(r)

        # Are there additional pages?
        #
        #if not 'link' in r.headers:
        #    return

        # Iterate through additional pages
        #
        pages_dict = self.get_pages_dict_from_headers(r.headers)
        while pages_dict is not None:

            if 'next' in pages_dict and not pages_dict['next'] == api_url:
                page_num += 1
                api_url = pages_dict['next']
                msgt('(%s) %s'% (page_num, api_url))

                r = requests.get(api_url, auth=AUTH)
                self.write_issues(r)
                pages_dict = self.get_pages_dict_from_headers(r.headers)
            else:
                break
        return
        pages=dict(next='next', last='last')

        while not pages['next'] == pages['last']:

            if 'link' in r.headers:
                pages = dict(
                    [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                        [link.split(';') for link in
                            r.headers['link'].split(',')]])
                if 'next' in pages and not pages['next'] == api_url:
                    page_num+=1
                    msgt('(%s) %s'% (page_num, pages['next']))
                    output_fname = join(OUTPUT_DIR, 'scrape_%s.json' % (str(page_num).zfill(2)))

                    r = requests.get(pages['next'], auth=AUTH)
                    if to_csv:
                        write_issues(r, csvout)
                    else:
                        open(output_fname, 'w').write(json.dumps(r.json(), indent=4))
                        print 'file written: %s' % output_fname

        return
        #-----------------------
        """
        page_num = 1

        print r.text
        print r.headers
        print r.status_code

        if to_csv:
            write_issues(r, csvout)
        else:
            open(output_fname, 'w').write(json.dumps(r.json(), indent=4))
            print 'file written: %s' % output_fname

        # Are there additional pages?
        #
        if not 'link' in r.headers:
            return

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
        """

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

    csvfile = OUTPUT_CSV_FILE_NAME #'UX-upgrade-issues-2016-0507.csv' #% (REPO.replace('/', '-'))
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
    #print r.text
    print r.headers
    print r.status_code

    if to_csv:
        write_issues(r, csvout)
    else:
        open(output_fname, 'w').write(json.dumps(r.json(), indent=4))
        print 'file written: %s' % output_fname

    # Are there additional pages?
    #
    if not 'link' in r.headers:
        return

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
    # ---------------------------------
    # (1) Output file
    # ---------------------------------
    output_file_name = 'github-critical.csv'

    # ---------------------------------
    # (2) github filters (optional)
    # ---------------------------------
    #github_filters = {}    # no filters
    github_filters = dict(assignee='username',
                          labels='Component: API,Priority: Critical')
    github_filters = dict(labels='Priority: Critical')

    # ---------------------------------
    # (3) kwargs (github filters + debug, e.g. print JSON to screen)
    # ---------------------------------
    kwargs = dict(print_issues=False) # show github JSON
    kwargs.update(github_filters)

    # ---------------------------------
    # (4) Retrieve issues and write to file
    # ---------------------------------
    github2csv = GithubIssueToCSV(output_file_name, **kwargs)
    github2csv.run_csv_maker()
