
# Test the 'add' file API

Note: For these scripts to work (tested on python 2.7), you need to install the python [requests library](http://docs.python-requests.org/en/master/) as in:
  - ```pip install requests```

## API key

- Create a file named key_str.txt in this directory and save it
  - The contents should be a valid API key with permissions to add a file
  - Example file contents: ```e97118a5-5583-4d0e-9178-af07963624fc```

## Adding files to a specific dataset
- Edit ```test_02.py```
  - After the ```if __name__ == '__main__':``` function, add these lines:
```python
if __name__ == '__main__':
  dataset_id = 2    # ID of Dataset to add or replace files
  run_add_loop(1, dataset_id)  # (number of files to add, dataset_id)
```
 - From the command line, run ```python test_02.py```

## Modifying the file added, description, categories, etc
 - Edit this function ```def run_add_loop(...)```
