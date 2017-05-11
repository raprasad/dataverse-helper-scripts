"""
Formatting for EZID requests/responses
reference: https://ezid.cdlib.org/doc/apidoc.html#internal-metadata
"""
from __future__ import print_function
import re

STATUS_UNAVAILABLE = 'unavailable'
STATUS_PUBLIC = 'public'

STATUS_UPDATE_UNAVAILABLE_WITHDRAWN ='unavailable | withdrawn by author'

def examine_status(doi_info, desired_status):
    """Given an EZID response, examine it to see if the status is correct
    Example response:
    (start)
    success: doi:10.7910/DVN/MHGCNF
    datacite.publisher: Harvard Dataverse
    _profile: datacite
    _export: yes
    datacite.creator: Ruzhdie Bici (Phd Candidate Department of Economics University of Tirana, Albania); Prof. Dr. Ahmet Mancellari (Department of Economics University of Tirana, Albania)
    datacite.publicationyear: 2015
    datacite.resourcetype: Dataset
    _datacenter: CDL.DATAVERS
    _updated: 1494525033
    _target: https://dataverse.harvard.edu/citation?persistentId=doi:10.7910/DVN/MHGCNF
    datacite.title: Multidimensional Measurement of Poverty - Albania Case
    _ownergroup: hdataverse
    _owner: hdataverse
    _shadowedby: ark:/b7910/dvn/mhgcnf
    _created: 1437624436
    _status: public
    (end)
    """
    if doi_info is None:
        return False, 'doi_info is None'

    # split into array of lines
    doi_text = doi_info.strip().split('\n')

    doi_dict = {}
    for line in doi_text:
        key, val = line.split(':', 1)
        doi_dict[key.strip()] = val.strip()

    doi_status = doi_dict.get('_status', 'Not found')

    print('doi_status (raw): %s' % doi_status)    # e.g. unavailable | withdrawn
    doi_status = doi_status.split('|')[0].strip()

    if doi_status == desired_status:
        return True, 'looks good, status is: %s' % doi_status

    return False, 'status is [%s]' % doi_status
