from ezid_settings import *


INPUT_FILE1 = join(EZID_DIR, 'input', 'prod.landreev.2015-04-22.csv')
INPUT_FILE2 = join(EZID_DIR, 'input', 'dvn-vm5.rprasad.2015-04-21.csv')
#INPUT_FILE1 = join(EZID_DIR, 'input', 't2.txt')
#INPUT_FILE2 = join(EZID_DIR, 'input', 't1.txt')


def find_diffs():
    assert isfile(INPUT_FILE1), 'file not found: %s' % INPUT_FILE1
    assert isfile(INPUT_FILE2), 'file not found: %s' % INPUT_FILE2

    with open(INPUT_FILE1, 'r') as file1:
        with open(INPUT_FILE2, 'r') as file2:
            same = set(file1).difference(file2)
            #same = set(file1).intersection(file2)

    same.discard('\n')

    for line in same:
        print line.strip()
            #file_out.write(line)
            


if __name__=='__main__':
    find_diffs()
