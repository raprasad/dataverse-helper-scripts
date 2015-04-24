# dataverse-helper-scripts

This repository contains a variety of not-often-used scripts used for Dataverse related work.


1.  [EZID DOI update/verify](#ezid-doi-updateverify) - Update EZID target urls for migrated datasets.  Verify that the DOIs point to the correct url.
2. [Basic Stress Test](#stress-tests) - Run basic browsing scenarios

## EZID DOI update/verify

* Location ```src/ezid_helper```

Scripts for two basic tasks:
  1. Update EZID target urls for migrated datasets.  
  2. Quality check: Verify that the DOIs point to the correct url.

### Input File

- Pipe ```|``` delimited .csv file with the following data:
  1.  Dataset id (pk from the 4.0 db table *dataset*)
  2.  Protocol 
  3.  Authority
  4.  Identifier
- Sample rows
```text
66319|doi|10.7910/DVN|29379
66318|doi|10.7910/DVN|29117
66317|doi|10.7910/DVN|28746
66316|doi|10.7910/DVN|29559
```

#### Input file creation

The input file is the result of a query from the postres psql shell:

* Basic query
```sql
select id, protocol, authority, identifier from dataset where protocol='doi' and authority='10.7910/DVN' order by id desc;
```

* Basic query to pipe ```|``` delimited text file

```sql
COPY (select id, protocol, authority, identifier from dataset where protocol='doi' and authority='10.7910/DVN' order by id desc) TO
'/tmp/file-name-with-dataset-ids.csv' (format csv, delimiter '|')
```

### Running the script

### Output


## Stress Tests

These are basic tests using [locustio](http://docs.locust.io/en/latest/quickstart.html).

### Initial Setup


- Requires (virtualenvwrapper)[https://virtualenvwrapper.readthedocs.org/en/latest/install.html]
    - OS X install: ```sudo pip install virtualenvwrapper```

1. Open a Terminal    
1. cd into ```src/stress_tests```
1. Make a virtualenv: ```mkvirtualenv stress_tests```
1. Install locustio: ```pip install -r requirements/base.txt```
    - This takes a couple of minutes
1. Within ```src/stress_tests```, copy ```creds-template.json``` to ```creds.json``` (in the same folder)
1. Change the ```creds.json``` settings appropriately.

### Setup (2nd time around)

1. Open a Terminal    
1. cd into ```src/stress_tests```
1. Type ```workon stress_tests``` (and press Return)

### Run a script

1. Set your server in ```creds.son```
1. cd into ```src/stress_tests```
1. Run a test script.  In this example run **test_01.py**
    - From the Terminal: ```locust -f test_01.py```
1. Open a browser and go to: ```http://127.0.0.1:8089/```    
