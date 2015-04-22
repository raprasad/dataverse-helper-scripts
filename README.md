# dataverse-helper-scripts

This repository contains a variety of not-often-used scripts used for Dataverse related work.


1.  [EZID DOI update/verify](#ezid-doi-updateverify) - Update EZID target urls for migrated datasets.  Verify that the DOIs point to the correct url.


## EZID DOI update/verify

* Location ```src/ezid_helper```

Scripts for two basic tasks:
  1. Update EZID target urls for migrated datasets.  
  2. Quality check: Verify that the DOIs point to the correct url.

### Input

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

### Running the script

### Output


