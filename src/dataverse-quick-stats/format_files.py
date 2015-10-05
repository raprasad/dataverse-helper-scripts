import os
from os.path import isfile, isdir, join

TOTAL_CNT = 0

def process_line(l):

    global TOTAL_CNT

    items = l.strip().split('|')
    if len(items) != 2:
        return None

    # split line to date, cnt4
    date, cnt = items
    # split timestamp to date, time
    mm, tt = date.strip().split()

    cnt = cnt.strip()
    TOTAL_CNT += int(cnt)

    return '%s,%s,%s' % (mm.strip(), cnt, TOTAL_CNT)


def process_file(fname):
    assert isfile(fname), "not a file: %s" % fname

    global TOTAL_CNT
    TOTAL_CNT = 0

    flines = open(fname, 'r').readlines()
    flines = [process_line(x) for x in flines]
    flines = [x for x in flines if x is not None]

    return flines

def process_dir(dirname):
    assert isdir(dirname), 'directory does not exist: %s' % dirname

    fnames = os.listdir(dirname)
    fnames = [x for x in fnames if x.endswith('.txt')]

    for fname in fnames:
        fullname = os.path.join(dirname, fname)
        fmt_lines = process_file(fullname)
        output_name = os.path.join(dirname, 'fmt_%s' % fname.replace('.txt', '.csv'))

        open(output_name, 'w').write('\n'.join(fmt_lines))
        print 'file written: %s' % output_name

if __name__=='__main__':
    dirname = join('stats', '2015-08-19')
    process_dir(dirname)
