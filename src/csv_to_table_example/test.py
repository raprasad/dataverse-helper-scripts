"""
Example of adding csv file data to a postgres table

(1) Change DB_PARAMS at top
(2) At bottom of file, within ___main__, change file name and table name
"""
from os.path import isfile
import psycopg2
import sys
from csvkit import sql
from csvkit import table

DB_PARAM_NAMES = ['NAME', 'USER', 'PASSWORD', 'PORT','HOST']
DB_PARAMS = dict(USER='dvnapp',\
            PASSWORD='secret',\
            HOST='localhost',\
            PORT='5432',\
            NAME='dvndb',\
            )

def get_db_connection_string(url_format=False):
    """
    Bit hackish, two types of connection strings
    """
    if url_format:
        conn_str = "postgresql://%s:%s@%s:%s/%s" % \
                        (DB_PARAMS['USER'], DB_PARAMS['PASSWORD'], DB_PARAMS['HOST'], DB_PARAMS['PORT'], DB_PARAMS['NAME'])
    else:
        conn_str = """dbname='%s' user='%s' password='%s' port=%s host='%s'""" % \
                    tuple([DB_PARAMS.get(x) for x in DB_PARAM_NAMES])
    return conn_str


class CSVTableBuilder(object):

    def __init__(self, filename, new_table_name):
        assert isfile(filename), 'File not found: %s' % filename
        assert new_table_name is not None, "new_table_name cannot be None"

        self.fname = filename
        self.table_name = new_table_name

        # To hold csvkit objects
        self.csv_table = None
        self.sql_table = None

        self.err_found = False
        self.err_msg = None

        # Go through the table
        self.load_file()
        self.create_table()
        self.load_table()


    def add_error(self, error_message):
        self.err_found = True

        print error_message
        self.err_msg = error_message


    def load_file(self):
        """
        (1) Use csv file to Generate csvkit Table and SQL table objects
        """
        fh = open(self.fname, 'rb')
        self.csv_table = table.Table.from_csv(fh, self.table_name)
        self.sql_table = sql.make_table(self.csv_table, self.table_name)


    def create_table(self):
        """
        (2) Make the Postgres table
        """
        if self.err_found:
            return False

        create_table_sql = sql.make_create_table_statement(self.sql_table,\
                                            dialect="postgresql")

        conn = psycopg2.connect(get_db_connection_string())

        try:
            cur = conn.cursor()
            cur.execute('drop table if exists %s CASCADE;' % self.table_name)
            cur.execute(create_table_sql)
            conn.commit()
            cur.close()
        except Exception as e:
            self.add_error("Error Creating table %s" % (str(e)))
            return False
        finally:
            conn.close()

        print 'Table created %s' % self.table_name
        return True

    def load_table(self):
        """
        (3) Load the Postgres table
        """
        if self.err_found:
            return False

        if self.csv_table.count_rows() == 0:
            self.add_error("No rows to add.")
            return False

        insert = self.sql_table.insert() # Generate insert statement
        headers = self.csv_table.headers() # Pull table headers
        rows_to_add = [dict(zip(headers, row)) for row in self.csv_table.to_rows()]

        engine, metadata = sql.get_connection(get_db_connection_string(\
                                            url_format=True))
        conn = engine.connect()
        trans = conn.begin()

        try:
            conn.execute(insert, rows_to_add)
        except:
            print "Failed to add csv DATA to table %s.\n%s" % (self.table_name, (sys.exc_info()[0]))
        finally:
            trans.commit()
            conn.close()

        print 'Added %s row(s) to table "%s"' % (len(rows_to_add), self.table_name)
        return True

        
if __name__=='__main__':
    fname = 'test_files/nhcrime_2014_08_63.csv'
    table_name = 'crime_table'
    builder = CSVTableBuilder(fname, table_name)
    if builder.err_found:
        print 'Error: %s' % builder.err_msg
