#!/usr/bin/env python3

import argparse
import sys
import pymarc
import csv
from pathlib import Path
from collections import defaultdict


namespaces = { 'marc' : 'http://www.loc.gov/MARC21/slim' }
baseURL = 'http://newcatalog.library.cornell.edu/catalog'
headers = {'Content-Type': 'application/xml'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('inputlist', metavar='[input_list]',
                        help='input list with BIBIDs')
    parser.add_argument('iteminfo', metavar='[item_info]',
                        help='list with item data')
    args = parser.parse_args()

    inputlist = Path(args.inputlist)
    if not inputlist.exists():
        sys.exit("Exiting: inputlist does not exist.")

    iteminfo = Path(args.iteminfo)
    if not iteminfo.exists():
        sys.exit("Exiting: iteminfo does not exist.")



    # Load in item information
    iteminfoDict = defaultdict(dict)
    with open(iteminfo, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            barcodeinfo = {'DISPLAY_CALL_NO': row.get('DISPLAY_CALL_NO'),
                           'ITEM_ENUM': row.get('ITEM_ENUM'),
                           'COPY': row.get('Copy')}
            iteminfoDict[row.get('BIB_ID')][row.get('ITEM_BARCODE')] = barcodeinfo


    # Get marcxml for a given BIBID
    with open(inputlist) as bibs:
        for line in bibs.readlines():
            line = line.strip()
            xmlurl = '{0}/{1}.marcxml'.format(baseURL, line)
            try:
                bibxml = pymarc.parse_xml_to_array(xmlurl, strict=True)
            except:
                continue

            # Find all barcodes for a given BIBID
            for b in iteminfoDict[line]:
                callno = iteminfoDict[line][b]['DISPLAY_CALL_NO']
                itemenum = iteminfoDict[line][b]['ITEM_ENUM']
                copy = iteminfoDict[line][b]['COPY']
            
                thisnewbib = bibxml[0] # record from catalog, unmodified                       
                thissubfields = ['a', callno, 'p', b, 't', copy, 'v', itemenum]
                thisfield = pymarc.Field(tag = '976', indicators = ['', ''], subfields = thissubfields)
                thisnewbib.add_field(thisfield)

                # TODO: Need to specify an output directory!!! For now, make it here
                xmlmrcFilename = '{0}_{1}.marcxml'.format(line,b)
                writer = pymarc.XMLWriter(open(xmlmrcFilename, 'wb'))
                writer.write(thisnewbib)
                writer.close() # documentation says this is "Important!"




if __name__ == "__main__":
    main()
