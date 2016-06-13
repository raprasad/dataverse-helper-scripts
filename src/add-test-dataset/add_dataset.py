import sys
sys.path.append('/Users/rmp553/Documents/iqss-git/dataverse-client-python')
sys.path.append('/Users/rmp553/Documents/iqss-git/dataverse-client-python/dataverse')

from dataverse import Connection
from geotweet_desc import get_geotweet_description

DV_HOST = 'localhost:8080'                  # All clients >4.0 are supported
TOKEN = 'ad4db0df-2fea-4bea-b4fa-e75462371d69'  # Generated at /account/apitoken


def create_dataset():

    print 'make connection...'
    connection = Connection(DV_HOST, TOKEN, use_https=False)

    print 'connection', connection
    dataverse = connection.get_dataverse('root')
    print 'base_url', connection.base_url

    title, description, creator = get_geotweet_params()

    kwargs = dict(notes="notes go here")
    dataverse.create_dataset(title, description, creator, **kwargs)
    print 'dataset created'

def get_geotweet_params():

    title = "A Billion Streaming GeoTweets"
    description = get_geotweet_description()
    creator = 'R. Prasad'

    return (title, description, creator)
    #create_dataset(self, title, description, creator, **kwargs):

if __name__ == '__main__':
    create_dataset()
