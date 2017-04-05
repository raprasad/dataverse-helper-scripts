## Quick check for HTTPS

The ```check_whitelist.py``` script:

1. Reads in a list of domains
1. For each domain, it
  1. Prepends ```https://```
  2. Attempts to retrieve it via a GET
  3. Records the results in an output file

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

## Prerequisites

Tested with python 2.7, should work for 3.5+

### Install [pip](http://pip.readthedocs.org/en/latest/installing.html)

* use sudo if needed  (mac users, use sudo)
* if on Windows, make sure [python](https://www.python.org/downloads/) is installed.

### Install
 [virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/install.html#basic-installation)

* The virtualenvwrapper may be installed via pip:

    ```
    pip install virtualenvwrapper
    ```

  * On windows, either install [virtualenvwrapper-win-1.1.5](https://pypi.python.org/pypi/virtualenvwrapper-win) or [cygwin](https://www.cygwin.com/).

* Set the shell/Terminal to use virtualenvwrapper.
  - For Mac users:
    1. Open a new terminal
    2. Open your ```.bash_profile``` for editing
    3. Add these lines

        ```
        export WORKON_HOME=$HOME/.virtualenvs
        export PROJECT_HOME=$HOME/Devel
        source /usr/local/bin/virtualenvwrapper.sh
        ```

    4. Reference: http://virtualenvwrapper.readthedocs.org/en/latest/install.html#shell-startup-file
  - If you're using windows, [this](http://stackoverflow.com/questions/2615968/installing-virtualenvwrapper-on-windows) might be helpful.
