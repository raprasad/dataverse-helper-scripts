q = '''SELECT i.relname as indname,
       idx.indrelid::regclass,
       ARRAY(
       SELECT pg_get_indexdef(idx.indexrelid, k + 1, true)
       FROM generate_subscripts(idx.indkey, 1) as k
       ORDER BY k
       ) as indkey_names
FROM   pg_index as idx
JOIN   pg_class as i
ON     i.oid = idx.indexrelid
JOIN   pg_am as am
ON     i.relam = am.oid;'''

import os
from os.path import join, isfile

flines = open('input/idx_query.txt', 'r').readlines()
flines = [x.strip().replace('"', '').replace('}', '').replace('{', '') for x in flines if len(x.strip()) > 0]
flines = [x for x in flines if x.startswith('index_')]
flines.sort()
for fline in flines:
    idx_name, tbl, attrs = fline.split(';')
    if idx_name.startswith('pg_') or tbl.startswith('pg_'):
        continue
    print 'CREATE INDEX %s ON %s (%s);' % (idx_name, tbl, attrs)
    #print 'DROP INDEX IF EXISTS  %s CASCADE;' % (idx_name)
