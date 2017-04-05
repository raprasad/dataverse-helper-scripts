## Quick check for HTTPS

The ```check_whitelist.py``` script:

1. Reads in a list of domains
1. For each domain, it
   1. Prepends ```https://```
   1. Attempts to retrieve it via a GET
   1. Records the results in an output file

### Output/Input Files

The input file should be placed in the ```input``` directory.

### Running the script:

Make sure you have the python [requests](http://docs.python-requests.org/en/master/) library.

```
----------------------------------------
quick whitelist check
----------------------------------------

Run this command:

    >python check_whitelist.py (input file) (output file)

    Example:

        >python check_whitelist.py whitelist-domains_2017_0405.txt output_2017_0405.csv

The script may be restarted at a specific line number:

    >python check_whitelist.py (input file) (output file) (item #/occurrence in whitelist)

    Example.  Start at 20th item in the whitelist:

        >python check_whitelist.py whitelist-domains_2017_0405.txt output_2017_0405.csv 20
```
