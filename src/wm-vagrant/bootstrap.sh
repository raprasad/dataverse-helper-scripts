#!/usr/bin/env bash

#Attempt to install cga-worldmap:
# https://github.com/cga-harvard/cga-worldmap

# ------------------------------------------------
# Install vim (for editing)
# ------------------------------------------------
sudo apt-get --assume-yes install vim

# ------------------------------------------------
# Install curl (to have)
# ------------------------------------------------
sudo apt-get --assume-yes install curl


# ------------------------------------------------
# Pip
# ------------------------------------------------
sudo apt-get -y install python-pip

# ------------------------------------------------
# Install git
# ------------------------------------------------
sudo apt-get --assume-yes install git

# ------------------------------------------------
# Install subversion
# ------------------------------------------------
sudo apt-get --assume-yes install subversion

# ------------------------------------------------
# Java 1.7
# reference: http://stackoverflow.com/questions/16263556/installing-java-7-on-ubuntu
# ------------------------------------------------
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install openjdk-7-jdk
#sudo update-alternatives --config java
#sudo apt-get install oracle-java7-set-default

export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/jre
export PATH=$PATH:$JAVA_HOME/bin

# ------------------------------------------------
# precursors for geos
# ------------------------------------------------
sudo apt-get install make
sudo apt-get --assume-yes install build-essential

# ------------------------------------------------
# for GEOS
# -  https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/
# ------------------------------------------------
wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2
tar xjf geos-3.4.2.tar.bz2
cd geos-3.4.2
./configure
make
sudo make install
cd ..
rm geos-3.4.2.tar.bz2

# ------------------------------------------------
# Precursors for GDAL/OGR
# http://askubuntu.com/questions/493460/how-to-install-add-apt-repository-using-the-terminal
# ------------------------------------------------
sudo apt-get install software-properties-common
sudo apt-get --assume-yes install python-software-properties

# ------------------------------------------------
# GDAL/OGR
# http://www.sarasafavi.com/installing-gdalogr-on-ubuntu.html
# ------------------------------------------------
sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
sudo apt-get --assume-yes install gdal-bin

# ------------------------------------------------
# Apache Maven
# ------------------------------------------------
sudo apt-get --assume-yes install maven

#sudo apt-get remove maven
#apt-get autoremove

# ------------------------------------------------
# jetty
# ------------------------------------------------
sudo apt-get install jetty
#sudo apt-get remove jetty

# ------------------------------------------------
# Apache ant
# ------------------------------------------------
sudo apt-get install ant


# ------------------------------------------------
# Pre-Postgres
# http://crohr.me/journal/2014/postgres-rails-the-chosen-lc-ctype-setting-requires-encoding-latin1.html
# ------------------------------------------------
sudo locale-gen en_US.UTF-8
sudo cat - > /etc/default/locale <<EOF
LANG=en_US.UTF-8
LANGUAGE=
LC_CTYPE="en_US.UTF-8"
LC_NUMERIC="en_US.UTF-8"
LC_TIME="en_US.UTF-8"
LC_COLLATE="en_US.UTF-8"
LC_MONETARY="en_US.UTF-8"
LC_MESSAGES="en_US.UTF-8"
LC_PAPER="en_US.UTF-8"
LC_NAME="en_US.UTF-8"
LC_ADDRESS="en_US.UTF-8"
LC_TELEPHONE="en_US.UTF-8"
LC_MEASUREMENT="en_US.UTF-8"
LC_IDENTIFICATION="en_US.UTF-8"
LC_ALL=en_US.UTF-8
EOF

# ------------------------------------------------
# Postgres
# - http://www.saintsjd.com/2014/08/13/howto-install-postgis-on-ubuntu-trusty.html
# ------------------------------------------------
sudo apt-get install -y postgresql postgresql-contrib

# test user and db
#sudo -u postgres createuser -P wmadmin
#sudo -u postgres createdb -O wmadmin testit
#psql -h localhost -U wmadmin testit

# ------------------------------------------------
# Postgis
# ------------------------------------------------
sudo apt-get install -y postgis postgresql-9.1-postgis-2.0


# test postgis
#sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" testit
#sudo su - postgres
echo "--- See post_setup.md ---"
