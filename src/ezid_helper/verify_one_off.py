from ezid_settings import *


reg_list = """46594|10.7910/DVN1/22658|registered
48658|10.7910/DVN1/22660|registered
48737|10.7910/DVN1/22659|registered
48785|10.7910/DVN1/22662|registered
53231|10.7910/DVN1/22630|test dataset
55840|10.7910/DVN1/22644|looks like a test ds
56412|10.7910/DVN/28031|not registered
56413|10.7910/DVN/28029|not registered
56417|10.7910/DVN/28022 |not registered
56430|10.7910/DVN/28032|not registered
56432|10.7910/DVN/28030|not registered
56434|10.7910/DVN/28024|not registered
56438|10.7910/DVN/28027|not registered
56440|10.7910/DVN/28026|not registered
56442|10.7910/DVN/28019|not registered
56446|10.7910/DVN/28021|not registered
56447|10.7910/DVN/28033|not registered
56456|10.7910/DVN1/22656|registered
56762|10.7910/DVN/26235|not registered
56779|10.7910/DVN1/22704|registered
59833|10.7910/DVN/25329|not registered
64946|10.7910/DVN/26305|not registered
2667870|10.7910/DVN/9ZMQ12|registered smoke test ds""".split('\n')

WRONG_URL_FILE = join(OUTPUT_DIRECTORY, 'prod-verified-dois.json')
DOI_NOT_FOUND_FILE = join(OUTPUT_DIRECTORY, 'prod-verify-not-found-dois.json')


def check_wrong_urls():

    wrong_url_json = json.loads(open(DOI_NOT_FOUND_FILE, 'r').read())
    no_doi_json = json.loads(open(DOI_NOT_FOUND_FILE, 'r').read())
    cnt =0
    for line in reg_list:
        ds_id, doi_str, note = line.split('|', 2)
        if wrong_url_json.has_key(ds_id):
            authority, identifier = doi_str.rsplit('/', 1)
            cnt +=1
            msgt('(%s) got one!' % cnt)
            msg('%s|doi|%s|%s' % (ds_id, authority, identifier))

            #msg(json.dumps(wrong_url_json[ds_id], indent=4))

        if no_doi_json.has_key(ds_id):
            no_doi_json.pop(ds_id)
            
    
    msgt(json.dumps(no_doi_json, indent=4))
            
if __name__ == '__main__':
    check_wrong_urls()