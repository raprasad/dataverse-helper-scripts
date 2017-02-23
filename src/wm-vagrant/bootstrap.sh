#!/usr/bin/env bash

#Attempt to install cga-worldmap:
# https://github.com/cga-harvard/cga-worldmap


# ------------------------------------------------
# Install vim (for editing)
# ------------------------------------------------
echo "-- Install vim (for editing) --"
sudo apt-get --assume-yes install vim

# ------------------------------------------------
# Install c (to have)
# ------------------------------------------------
echo "-- Install curl "
sudo apt-get --assume-yes install curl


# ------------------------------------------------
# Pip + virtualenvwrapper
# ------------------------------------------------
echo "-- Install Pip + virtualenvwrapper "
sudo apt-get -y install python-pip
sudo pip install virtualenvwrapper
mkdir ~/.virtualenvs
export WORKON_HOME=~/.virtualenvs


# ------------------------------------------------
# Install git
# ------------------------------------------------
echo "-- Install git --"
sudo apt-get --assume-yes install git

# ------------------------------------------------
# Install subversion
# ------------------------------------------------
echo "-- Install subversion --"
sudo apt-get --assume-yes install subversion

# ------------------------------------------------
# Java 1.7
# reference: http://stackoverflow.com/questions/16263556/installing-java-7-on-ubuntu
# ------------------------------------------------
echo "-- Install Java 1.7 --"
sudo add-apt-repository ppa:webupd8team/java -y
sudo apt-get update
sudo apt-get --assume-yes install openjdk-7-jdk
#sudo update-alternatives --config java
#sudo apt-get install oracle-java7-set-default

export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64/jre
export PATH=$PATH:$JAVA_HOME/bin

# ------------------------------------------------
# precursors for geos
# ------------------------------------------------
echo "-- Install precursors for geos --"
sudo apt-get install make
sudo apt-get --assume-yes install build-essential

# ------------------------------------------------
# for GEOS
# -  https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/
# ------------------------------------------------
echo "-- Install GEOS --"
wget http://download.osgeo.org/geos/geos-3.6.1.tar.bz2
tar xjf geos-3.6.1.tar.bz2
cd geos-3.6.1
echo "-- Install GEOS .. configure --"
sudo ./configure
echo "-- Install GEOS .. make --"
sudo make
echo "-- Install GEOS .. make install --"
sudo make install
cd ..
rm geos-3.6.1.tar.bz2

# ------------------------------------------------
# Precursors for GDAL/OGR
# http://askubuntu.com/questions/493460/how-to-install-add-apt-repository-using-the-terminal
# ------------------------------------------------
echo "-- Install Precursors for GDAL/OGR --"
sudo apt-get install software-properties-common
sudo apt-get --assume-yes install python-software-properties

# ------------------------------------------------
# GDAL/OGR
# http://www.sarasafavi.com/installing-gdalogr-on-ubuntu.html
# ------------------------------------------------
echo "-- Install GDAL/OGR --"
sudo add-apt-repository ppa:ubuntugis/ppa -y && sudo apt-get update
sudo apt-get --assume-yes install gdal-bin

# ------------------------------------------------
# Apache Maven
# ------------------------------------------------
echo "-- Install Apache Maven --"
sudo apt-get --assume-yes install maven

#sudo apt-get remove maven
#apt-get autoremove

# ------------------------------------------------
# jetty
# ------------------------------------------------
echo "-- Install jetty --"
sudo apt-get --assume-yes install jetty
#sudo apt-get remove jetty

# ------------------------------------------------
# Apache ant
# ------------------------------------------------
echo "-- Install Apache ant --"
sudo apt-get --assume-yes install ant
#Not creating home directory `/usr/share/jetty'.
# * Not starting jetty - edit /etc/default/jetty and change #NO_START to be 0 (or comment it out).


# ------------------------------------------------
# Pre-Postgres
# http://crohr.me/journal/2014/postgres-rails-the-chosen-lc-ctype-setting-requires-encoding-latin1.html
# ------------------------------------------------
echo "-- (skip) Install Pre-Postgres --"
#sudo locale-gen en_US.UTF-8
#sudo cat - > /etc/default/locale <<EOF
#LANG=en_US.UTF-8
#LANGUAGE=
#LC_CTYPE="en_US.UTF-8"
#LC_NUMERIC="en_US.UTF-8"
#LC_TIME="en_US.UTF-8"
#LC_COLLATE="en_US.UTF-8"
#LC_MONETARY="en_US.UTF-8"
#LC_MESSAGES="en_US.UTF-8"
#LC_PAPER="en_US.UTF-8"
#LC_NAME="en_US.UTF-8"
#LC_ADDRESS="en_US.UTF-8"
#LC_TELEPHONE="en_US.UTF-8"
#LC_MEASUREMENT="en_US.UTF-8"
#LC_IDENTIFICATION="en_US.UTF-8"
#LC_ALL=en_US.UTF-8
#EOF

# ------------------------------------------------
# Postgres
# - http://www.saintsjd.com/2014/08/13/howto-install-postgis-on-ubuntu-trusty.html
# ------------------------------------------------
echo "-- Install Postgres --"
sudo apt-get install -y postgresql postgresql-contrib

# test user and db
#sudo -u postgres createuser -P wmadmin
#sudo -u postgres createdb -O wmadmin testit
#psql -h localhost -U wmadmin testit

# ------------------------------------------------
# Postgis
# ------------------------------------------------
echo "-- Install Postgis --"
sudo apt-get install -y postgis postgresql-9.3-postgis-2.2

# ------------------------------------------------
# psycopg2
#
# see: http://stackoverflow.com/questions/28253681/you-need-to-install-postgresql-server-dev-x-y-for-building-a-server-side-extensi
# ------------------------------------------------
echo "-- Install psycopg2 --"
sudo apt-get install --assume-yes python-psycopg2
sudo apt-get install --assume-yes libpq-dev


# ------------------------------------------------
# pre-reqs for Pillow
# ------------------------------------------------
echo "-- dependencies for Pillow install --"
sudo apt-get install --assume-yes libjpeg-dev
sudo apt-get build-dep --assume-yes python-imaging

# ------------------------------------------------
# fix for paver fail
# see: https://github.com/scieloorg/packtools/issues/12
# ------------------------------------------------
echo "-- dependencies for pip requirements --"
sudo apt-get install --assume-yes libxml2-dev
sudo apt-get install --assume-yes libxslt1-dev

#python-dev
#sudo pip install -e #git+git://github.com/scieloorg/packtools.git#egg=packtools


echo "--- See post_setup.md ---"
