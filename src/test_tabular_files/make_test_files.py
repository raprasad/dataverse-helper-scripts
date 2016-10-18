import csv
import random
import sys
from os.path import abspath, isfile, isdir, dirname, join

OUTPUT_DIR = join(dirname(abspath(__file__)), 'output')

DEFAULT_ROW_COUNT = 1000

def make_single_file(loop_num, num_rows):

    fname = 'test_csv_%s.csv' % `loop_num`.zfill(6)
    fullname = join(OUTPUT_DIR, fname)

    with open(fullname, 'w') as csvfile:
        fieldnames = [ 'col_%s' % x for x in range(1,11)]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for x in range(1, num_rows+1):
            vals = random.sample(range(1, 100), 10)
            d = dict(zip(fieldnames, vals))
            writer.writerow(d)

    print 'file written: %s', fullname


def make_csv_files(num_files, num_rows=DEFAULT_ROW_COUNT):

    num_files = int(num_files)
    num_rows = int(num_rows)

    for x in range(1, num_files+1):
        print '%s make file' % x
        make_single_file(x, num_rows)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        make_csv_files(sys.argv[1])
    elif len(sys.argv) == 3:
        make_csv_files(sys.argv[1], sys.argv[2])
    else:
        print '''
python make_test_files [num files]
'''
