
### SSH into vagrant
```
vagrant ssh
```

### Update .bashrc

- Open the .bashrc:
```
sudo vim /home/vagrant/.bashrc
```

- Add these lines to the end:
```
. /usr/local/bin/virtualenvwrapper.sh
export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/jre
export PATH=$PATH:$JAVA_HOME/bin
export WORKON_HOME=~/.virtualenvs
```

### Update pg_hba.conf conf file

- reference: http://stackoverflow.com/questions/18664074/getting-error-peer-authentication-failed-for-user-postgres-when-trying-to-ge
- open pg_hba.conf:
```
sudo vim /etc/postgresql/9.3/main/pg_hba.conf
```

- In 2 lines ending with "peer", change "peer" to "md5"

- Restart postgres:
```
sudo service postgresql restart
```

### Update postgres password:

  - http://stackoverflow.com/questions/10845998/i-forgot-the-password-i-entered-during-postgres-installation

- open config:
```
sudo vim /etc/postgresql/9.3/main/pg_hba.conf
```

- Add line to top:
```
local  all   all   trust
```

- Restart postgres:
```
sudo service postgresql restart
```

- Reset pw

```
psql -U postgres
ALTER USER postgres with password '123';
```

- Remove line from top of config and restart server again


---
### Manual update for encoding
---
sudo su postgres
psql
update pg_database set datistemplate=false where datname='template1';
drop database Template1;
create database template1 with owner=postgres encoding='UTF-8' lc_collate='en_US.utf8' lc_ctype='en_US.utf8' template template0;
update pg_database set datistemplate=true where datname='template1';

### Add WorldMap tables

- create user with password: "wm_password"

```
sudo -u postgres createuser -P -s -E -l wm_user;
```

### create PostGIS template with legacy GIST operators

```
sudo su postgres
createdb -E UTF8 -O wm_user template_postgis
psql -d template_postgis -c "CREATE EXTENSION postgis;"
```

- Make sure "cga-worldmap" is cloned into /vagrant/ directory
  - e.g. git clone git@github.com:cga-harvard/cga-worldmap.git

```
cd /vagrant/cga-worldmap/
psql -d template_postgis -f geonode/static/geonode/patches/postgis/legacy_gist.sql
```

### Create worldmap databases

- Make sure you are user "postgres", e.g. sudo su postgres

```
createdb -E UTF8 -U wm_user -T template_postgis wm_db
createdb -E UTF8 -U wm_user -T template_postgis wmdata
```

---
# Update for dbs
---
sudo -u postgres psql
\c wm_db
\c wmdata

- Run the following query for both ```wm_db``` and ```wmdata```
  - See query in file: ```index_fix.sql```
- From: http://stackoverflow.com/questions/13119040/failed-to-install-index-geodjango-related



### Geonode install steps

```
cd /vagrant/cga-worldmap/
git submodule update --init

mkvirtualenv worldmap

pip install -r shared/requirements.txt
# if fails, edit "shared/requirements.txt"
# comment out "psycopg2"

paver build # see note2 below

django-admin.py createsuperuser --settings=geonode.settings
```


---
# PIL ubuntu 12.x
# http://askubuntu.com/questions/156484/how-do-i-install-python-imaging-library-pil
---
sudo apt-get build-dep python-imaging
sudo apt-get install libjpeg62 libjpeg62-dev
