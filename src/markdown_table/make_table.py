"""
Quick script for a markdown table
"""
import sys
import os
from os.path import isfile, isdir, join, dirname, abspath

MARKDOWN_TABLE_DIR = dirname(abspath(__file__))

# ----------------------------
# Pull in util scripts
# ----------------------------
HELPER_SCRIPTS_DIR = join(dirname(MARKDOWN_TABLE_DIR))#, 'helper_utils')
sys.path.append(HELPER_SCRIPTS_DIR)

from helper_utils.msg_util import *

INPUT_DIR = join(MARKDOWN_TABLE_DIR, 'input')


def run_as_markdown_table(table_lines, add_line_numbers=False):

    print '\n' * 5

    for cnt, tl in enumerate(table_lines):
        if cnt > 0:
            print '- [ ] %d) %s' % (cnt, tl.split('|')[0].strip())

    print '\n' * 2
    print '---'
    print '\n' * 2

    table_lines = [x.strip() for x in table_lines if len(x.strip())> 0]

    fmt_lines = []
    for cnt, tl in enumerate(table_lines):

        if add_line_numbers:
            if cnt == 0:
                tl = '|#|%s|' % tl
            else:
                tl = '|%s|%s|' % (cnt, tl)
        else:
            tl = '|%s|' % tl

        fmt_lines.append(tl)

        if cnt == 0:
            #print '[%s]' % tl[1:-1], len(tl[1:-1].split('|'))
            #break
            header_breaks = []
            for x in range(0, len(tl[1:-1].strip().split('|'))):
                #if x==0 and add_line_numbers:
                #    header_breaks.append('---')
                if x == 0:
                    header_breaks.append('---')
                else:
                    header_breaks.append(':---:')
            #print header_breaks
            fmt_lines.append('%s' % '|'.join(header_breaks))


    print ''
    print '\n'.join(fmt_lines)

    print '\n' * 5


def make_md_table_from_file(fname):

    if not isfile(fname):
        print 'file not found! ', fname

    flines = open(fname, 'r').readlines()
    flines = [x.strip() for x in flines if len(x.strip()) > 0]
    run_as_markdown_table(flines, True)

def list_input_files():

    cnt = 0
    msgt("Choose a file number.")
    for f in os.listdir(INPUT_DIR):
        cnt += 1
        print '%d) %s' % (cnt, f)
    dashes()
    if cnt == 0:
        msg("Sorry!  No input files found in: %s" % INPUT_DIR)

def run_file_number(file_num):
    assert file_num.isdigit(), "file_num must be an integer"

    file_num = int(file_num)

    cnt = 0
    for f in os.listdir(INPUT_DIR):
        cnt += 1
        if file_num == cnt:
            make_md_table_from_file(join(INPUT_DIR, f))
            return
    msgt("Sorry! file number %s was not found." % file_num)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        run_file_number(sys.argv[1])
        #make_md_table_from_file(sys.argv[1])
    else:
        list_input_files()
        print 'python make_table.py [filename]'
        print 'e.g. python make_table.py [tlines_01_replace.txt]'
