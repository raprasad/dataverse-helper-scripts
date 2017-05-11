"""
Formatting for EZID requests/responses
reference: https://ezid.cdlib.org/doc/apidoc.html#internal-metadata
"""
from __future__ import print_function
import re

STATUS_UNAVAILABLE = 'unavailable'


def anvl_unescape(item_str):
    """Reverse the ANVL format"""
    return re.sub("%([0-9A-Fa-f][0-9A-Fa-f])",
                  lambda m: chr(int(m.group(1), 16)),
                  item_str)

def reverse_formatting(anvl_str):
    """Convert an ANVL string to a dict
    source: https://ezid.cdlib.org/doc/apidoc.html#internal-metadata
    """

    metadata = dict(tuple(self.anvl_unescape(v).strip()\
                    for v in l.split(":", 1)) \
                    for l in anvl_str.decode("UTF-8").splitlines())

    return metadata

def anvl_escape(item_str):
    """
    Escape the string for ANVL formatting
    example source: https://ezid.cdlib.org/doc/apidoc.html#internal-metadata
    """
    return re.sub("[%:\r\n]", lambda c: "%%%02X" % ord(c.group(0)), item_str)


def format_for_request(metadata_dict):
    """
    Convert a dict to an ANVL string.
    DOI updates are in the ANVL format as described here:
    https://ezid.cdlib.org/doc/apidoc.html#internal-metadata
    """
    formatted_lines = ["%s: %s" %\
                       (self.anvl_escape(name), self.anvl_escape(value))\
                       for name, value in metadata_dict.items()]
    return '\n'.join(formatted_lines).encode("UTF-8")


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
