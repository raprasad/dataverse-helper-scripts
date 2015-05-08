# variation of this gist: https://gist.github.com/unbracketed/3380407
import os
import requests
import json
import csv
import urllib
import dateutil.parser
from github_scrape_settings import *


REPO = get_creds_info('REPOSITORY_NAME')
AUTH = (get_creds_info('API_USERNAME'), get_creds_info('API_ACCESS_TOKEN'))
OUTPUT_FILE_NAME_FROM_CREDS = get_creds_info('OUTPUT_FILE_NAME')
GITHUB_ISSUE_FILTERS_FROM_CREDS = get_creds_info('GITHUB_ISSUE_FILTERS')


class GithubIssueToCSV(object):

    def __init__(self, output_file_name, print_issues=False, **kwargs):

        self.issue_count = 0
        self.print_issues = print_issues
        self.labels_to_exclude = kwargs.get('labels_to_exclude', None)

        self.csv_output_fname = join(OUTPUT_DIR, output_file_name)

        self.csv_writer = None

        self.query_filter_attrs = ('labels', 'assignee', 'creator' )
        self.query_str = ''

        self.set_query_string_filters(kwargs)
        self.format_labels_to_exclude()

    def format_labels_to_exclude(self):

        if self.labels_to_exclude is None or len(self.labels_to_exclude.strip()) == '':
            self.labels_to_exclude = None
            return

        self.labels_to_exclude = [label.strip() for label in self.labels_to_exclude.split(',')]




    def set_query_string_filters(self, kwarg_dict):
        """
        Format optional query string.
            example: "?labels=UX,design&assignee=username"
        """
        self.query_str = ''

        if kwarg_dict is None:
            return

        qstr_parts = []
        for k in self.query_filter_attrs:
            val_str = kwarg_dict.get(k, None)
            if val_str not in ('', None):
                vlist = [val.strip() for val in val_str.split(',')]
                val_str = ','.join(vlist)
                qstr_parts.append('%s=%s' % (k, urllib.quote(val_str)))

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
        if isfile(self.csv_output_fname):
            os.remove(self.csv_output_fname)

        # Init the csv writer
        self.csv_writer = csv.writer(open(self.csv_output_fname, 'wb'))

        # Write the header row
        self.csv_writer.writerow(self.get_csv_header_row())


    def does_issue_have_label_to_exclude(self, issue):
        if self.labels_to_exclude is None:
            return False

        assert isinstance(issue, dict), "Issue must be a dict"
        assert 'labels' in issue, "'labels' not found in issue dict: %s" % issue

        label_list = issue['labels']
        if label_list is None or len(label_list) == 0:
            return False

        for label in label_list:
            if label['name'] in self.labels_to_exclude:
                return True

        return False



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

    def format_time_str(self, time_str):
        assert time_str is not None, 'time_str cannot be None'

        # Let this blow up
        fmtdate = dateutil.parser.parse(time_str)
        return fmtdate.strftime('%Y-%m-%d %H:%M:%S')

        #msg(fmtdate)
        #msgx(fmtdate.__class__.__name__)



    def write_issues(self, response):
        """Write a list of issues to CSV"""
        assert response is not None, "response cannot be None"
        assert self.csv_writer is not None, "csv_writer was not initialized"

        if not response.status_code == 200:
            raise Exception(r.status_code)

        # Iterate through issues
        for issue in response.json():

            if self.does_issue_have_label_to_exclude(issue):
                continue    # skip this issue

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
                            self.format_time_str(issue['created_at']),
                            self.format_time_str(issue['updated_at']),
                            issue['html_url']
                            #'<a href="%s">github link</a>' % issue['html_url']
                            ])
            self.issue_count += 1

            if self.print_issues:
                msg(json.dumps(issue, indent=4))

        msg('File updated: %s' % self.csv_output_fname)
        msg('Total Issue Count: %d' % self.issue_count)

    def get_pages_dict_from_headers(self, headers):
        """
        Parse headers 'link' value
        """
        assert headers is not None, "headers cannot be None"

        if 'link' not in headers:
            return None

        """Example of 'link' in headers dict
        {'link': '<https://api.github.com/repositories/14051004/issues?labels=Priority%3A+Critical&page=2>; rel="next",
         <https://api.github.com/repositories/14051004/issues?labels=Priority%3A+Critical&page=2>; rel="last"'
        }
        """
        link_list = [link.split(';') for link in headers['link'].split(',')]
        rel_url_pairs_list = [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in link_list]
        page_dict = dict(rel_url_pairs_list)

        """Example page_dict
        {'last': 'https://api.github.com/repositories/14051004/issues?labels=Priority%3A+Critical&page=2',
         'next': 'https://api.github.com/repositories/14051004/issues?labels=Priority%3A+Critical&page=2'}
        """

        return page_dict


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

        # Iterate through additional pages (if they exist)
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


if __name__=='__main__':

    # ---------------------------------
    # (1) csv output file name
    # ---------------------------------
    #output_file_name = 'github-issues.csv'

    # ---------------------------------
    # (2) github filters (optional)
    # ---------------------------------
    #github_filters = {}    # no filters
    #github_filters = dict(assignee='username',
    #                      labels='Component: API,Priority: Critical')
    #github_filters = dict(labels='Component: API,Priority: Critical')


    # ---------------------------------
    # (3) Retrieve issues and write to file
    # ---------------------------------
    github2csv = GithubIssueToCSV(OUTPUT_FILE_NAME_FROM_CREDS, **GITHUB_ISSUE_FILTERS_FROM_CREDS)
    #github2csv = GithubIssueToCSV(output_file_name, print_issues=True, **github_filters)
    github2csv.run_csv_maker()
