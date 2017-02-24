
### SSH into vagrant
```
vagrant ssh
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



### Manual postgres update for encoding

```
sudo su postgres
```

```
psql
update pg_database set datistemplate=false where datname='template1';
drop database Template1;
create database template1 with owner=postgres encoding='UTF-8' lc_collate='en_US.utf8' lc_ctype='en_US.utf8' template template0;
update pg_database set datistemplate=true where datname='template1';
```

### Add WorldMap tables

- create user with password: "wm_password"

```
sudo -u postgres
createuser -P -s -E -l wm_user;
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
- NOTE: For next commands, use password "wm_password"

```
createdb -E UTF8 -U wm_user -T template_postgis wm_db
createdb -E UTF8 -U wm_user -T template_postgis wmdata
```

---
# SKIP!!! Update for dbs
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
source ~/.bashrc
mkvirtualenv worldmap
```

### Run pip install

- ~~edit: ```pip install -r shared/requirements.txt```~~
- ~~comment out: ```pip==1.0```~~
  - ~~e.g. ```#pip==1.0```~~

- Run it:

```  
pip install -r shared/requirements.txt
```

### Jetty config update

- Jetty.xml adjustment for host and port.  Note host is "0.0.0.0"

```
<Set name="host"><SystemProperty name="jetty.host" default="0.0.0.0"/></Set>
<Set name="port"><SystemProperty name="jetty.port" default="8080"/></Set>
```

### Continue on with paver steps
- Next install steps

```
workon worldmap

#pip install pip==1.0    # revert for paver build script

pip uninstall django
pip install Django==1.4.13 --no-cache-dir

paver build # see note2 below
pip install --upgrade pip

django-admin.py createsuperuser --settings=geonode.settings
```

### Start jetty and django separately

- Start jetty

```
cd /vagrant/cga-worldmap
workon worldmap
paver start_geoserver
```

- Open: http://localhost:8080  
  - admin/admin


- Start Django in another window

```
cd /vagrant/cga-worldmap
workon worldmap
python manage.py runserver 0.0.0.0:8000
```

- Open: http://localhost:8000
  - rp/123



---- OLD ----


- Temp django fix before paver build (may have been bad django install):
  - see item with 11 up votes:  http://stackoverflow.com/questions/31816158/attributeerror-nonetype-object-has-no-attribute-info
