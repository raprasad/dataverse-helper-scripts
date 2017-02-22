#------------------------
# Update conf file
# ------------------------   
  - reference: http://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge
  - update: ```
sudo vim /etc/postgresql/9.1/main/pg_hba.conf
in line: local   all             postgres                                peer
Change "peer" to "md5"
sudo service postgresql restart
```

# postgres pw update, if needed: http://stackoverflow.com/questions/10845998/i-forgot-the-password-i-entered-during-postgres-installation


# ------------------------------------------------
# Manual update for encoding
# ------------------------------------------------
sudo su postgres
psql
update pg_database set datistemplate=false where datname='template1';
drop database Template1;
create database template1 with owner=postgres encoding='UTF-8' lc_collate='en_US.utf8' lc_ctype='en_US.utf8' template template0;
update pg_database set datistemplate=true where datname='template1';

# ------------------------------------------------
# Add WorldMap tables
# ------------------------------------------------
# create user
sudo -u postgres createuser -P -s -E -l wm_user;
# password: wm_password

#create PostGIS template with legacy GIST operators
sudo -u postgres createdb -E UTF8 -O wm_user template_postgis
sudo -u postgres psql -d template_postgis -c "CREATE EXTENSION postgis;"

# Assumes cga-worldmap clone into /vagrant/ directory
# git clone git@github.com:cga-harvard/cga-worldmap.git
#
cd /vagrant/cga-worldmap/

sudo -u postgres psql -d template_postgis -f geonode/static/geonode/patches/postgis/legacy_gist.sql

#

# create wm_db
sudo -u postgres createdb -E UTF8 -U wm_user -T template_postgis wm_db

# create wmdata
sudo -u postgres createdb -E UTF8 -U wm_user -T template_postgis wmdata

# ------------------------------------------------
# Geonode install steps
# ------------------------------------------------

```
git submodule update --init

mkvirtualenv worldmap

pip install -r shared/requirements.txt

paver build # see note2 below

django-admin.py createsuperuser --settings=geonode.settings
```


# ------------------------------------------------
# PIL ubuntu 12.x
# http://askubuntu.com/questions/156484/how-do-i-install-python-imaging-library-pil
# ------------------------------------------------
sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg62 libjpeg62-dev
