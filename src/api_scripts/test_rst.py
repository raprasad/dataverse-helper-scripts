
from datetime import datetime
import json
import requests  # http://docs.python-requests.org/en/master/

# --------------------------------------------------
# Update params below to run code
# --------------------------------------------------
dataverse_server = 'http://127.0.0.1:8080' # no trailing slash
api_key = 'ad4db0df-2fea-4bea-b4fa-e75462371d69'

file_id = 1401  # id of the file to replace

# --------------------------------------------------
# Prepare replacement "file"
# --------------------------------------------------
file_content = 'content: %s' % datetime.now()
files = {'file': ('replacement_file.txt', file_content)}

# --------------------------------------------------
# Using a "jsonData" parameter, add optional description + file tags
# --------------------------------------------------
params = dict(description='Sunset',
            tags=['One', 'More', 'Cup of Coffee'])

# -------------------
# IMPORTANT: If the mimetype of the replacement file differs
#   from the origina file, the replace will fail
#
#  e.g. if you try to replace a ".csv" with a ".png" or something similar
#
#  You can override this with a "forceReplace" parameter
# -------------------
params['forceReplace'] = True


params_as_json_string = json.dumps(params)

payload = dict(jsonData=params_as_json_string)

print 'payload', payload
# --------------------------------------------------
# Replace file using the id of the file to replace
# --------------------------------------------------
url_replace = '%s/api/v1/files/%s/replace?key=%s' % (dataverse_server, file_id, api_key)

# -------------------
# Make the request
# -------------------
print '-' * 40
print 'making request: %s' % url_replace
r = requests.post(url_replace, data=payload, files=files)

# -------------------
# Print the response
# -------------------
print '-' * 40
print r.json()
print r.status_code
