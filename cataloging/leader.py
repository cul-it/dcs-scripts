#!/usr/bin/env python3

# flagrantly copied from my previous hathitrust python code
# only this time, the leader actually refers to the right thing (sigh)

import argparse
import requests
import sys
import xml.etree.ElementTree as ET


namespaces = { 'marc' : 'http://www.loc.gov/MARC21/slim' }
baseURL = 'http://newcatalog.library.cornell.edu/catalog'
headers = {'Content-Type': 'application/xml'}


def parsexml(rawxml):
    marcxml = ET.fromstring(rawxml)
    leader = marcxml.findall('marc:leader', namespaces)[0].text
    return leader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputlist', metavar='[input_list]',
                        help='input list with BIBIDs')
    args = parser.parse_args()

    failures = []

    inputlist = open(args.inputlist).readlines()
    for item in inputlist:
        item = item.strip()
        query = '{0}/{1}.marcxml'.format(baseURL, item)
        resp = requests.get(query, headers=headers)
        if resp.status_code == 200:
            leader = parsexml(resp.content.decode('utf-8'))
        else:
            failures.append(item)
            continue
        thisformat = leader[6:8]
        print(','.join([item, thisformat]))

    sys.stderr.write('\nUNKNOWN BIBS---\n')
    sys.stderr.write('\n'.join(failures))


if __name__ == "__main__":
    main()



