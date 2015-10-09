from os.path import isdir, join
import urllib2
import shutil
from datetime import datetime

class LogReader:

    STRINGS_TO_SKIP = ['.css', '.js', '.jpg', '.png', '.gif'\
                    , '.svg', '.woff', '.ico', 'atmosphere-tracking-id'\
                    , 'fontcustom/fontcustom_', 'resources/socicon-font'\
                    , 'fonts/glyphicons'\
                    , 'robots.txt']

    def __init__(self, log_fname, **kwargs):
        self.log_fname = log_fname
        self.hr_cnts = {}   # { hr : cnt }
        self.selected_minute = kwargs.get('selected_minute', None)
        self.list_requests = kwargs.get('list_requests', False)
        self.request_list = []
        self.read_lines()

    def skip_this_line(self, line):
        fline = line.lower()
        for skip_it in self.STRINGS_TO_SKIP:
            if fline.find(skip_it) > -1:
                return True
        return False

    def add_request_info(self, req_info):
        if req_info is None:
            return
        req_parts = req_info.split()
        if len(req_parts) < 2:
            return
        self.request_list.append(req_parts[1])

    def write_requests(self):
        unique_requests = {}
        for req in self.request_list:
            unique_requests[req]  = unique_requests.get(req, 0) + 1

        #print len(self.request_list)
        #for k, v in unique_requests.items():
        #    print v, k
        print len(unique_requests)

        keys = unique_requests.keys()
        keys.sort()
        open('test-data/request_list.txt', 'w').write('\n'.join(keys))

    def read_lines(self):
        line_cnt = 0
        new_fh = open('test-data/server_dv_only.txt', 'w')
        with open(self.log_fname) as infile:
            for line in infile:
                line_cnt += 1
                if self.skip_this_line(line):
                    continue

                new_fh.write(line)
                #print 'line_cnt: {0}'.format(line_cnt)
                line_parts = line.strip()[1:-1].split('" "')
                #print line_parts
                if len(line_parts) >= 3:

                    print line_parts

                    # Pull out the time string
                    # ---------------------------
                    tm = line_parts[1]  # "08/Oct/2015:17:34:52 -0500


                    # ---------------------------
                    # Group by time string
                    #
                    if self.selected_minute:    # group by minute
                        hr_sub = tm[:17]
                        if hr_sub.startswith(self.selected_minute):
                            self.hr_cnts[hr_sub] = self.hr_cnts.get(hr_sub, 0) + 1
                            # Save the url called
                            self.add_request_info(line_parts[2])

                    else:                       # group by hour
                        hr_sub = tm[:15]
                        self.hr_cnts[hr_sub] = self.hr_cnts.get(hr_sub, 0) + 1
                        # Save the url called
                        self.add_request_info(line_parts[2])

                    #print hr_sub
                #if line_cnt > 1:
                #    break

        if self.list_requests is True:
            self.write_requests()


if __name__ == '__main__':
    #log_fname = 'test-data/server_access_log.2015-10-08.txt'
    log_fname = 'test-data/server_access_log.2015-10-08.txt'
    #lr = LogReader(log_fname, selected_minute='09/Oct/2015:08')
    #lr = LogReader(log_fname, list_requests=True)
    lr = LogReader(log_fname, list_requests=True, selected_minute='09/Oct/2015:08')
