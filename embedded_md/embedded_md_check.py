#!/usr/bin/env python3

# Input 1: Text file with fields to interrogate
# Input 2: Directory with files to test

# Tools: PyExifTool
# Reference: https://exiftool.org/TagNames/RIFF.html (Conversion of RIFF->Exif labels)

import exiftool
import argparse
import sys
import csv
from pathlib import Path



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mdfields', metavar='[metadata_fields]',
                        help='Text file with metadata fields to analyze')
    parser.add_argument('indir', metavar='[input_directory]',
                        help='Input directory to scan')
    parser.add_argument('csvout', metavar='[csv_output]',
                        help='Output file for data (will not overwrite).')
    args = parser.parse_args()


    # Debugging
#    print("First arg:  {}".format(args.mdfields))
#    print("Second arg: {}".format(args.indir))
#    print("Third arg:  {}".format(args.csvout))


    # Make sure output does not already exist.
    c = Path(args.csvout).resolve()
    if c.exists():
        sys.exit("The output file specified already exists.")


    # Identify fields of interest
    f = Path(args.mdfields).resolve()
    if not f.is_file():
        sys.exit("The text file with metadata fields does not exist.")

    fields = []
    with open(f, 'r') as mdfile:
        for mdline in mdfile:
            mdline = mdline.strip()
            fields.append(mdline)


    # Set up path to files to analyze
    p = Path(args.indir).resolve()
    if not p.exists():
        sys.exit("The input directory '{0}' does not exist.".format(p))
    flist = []
    plist = Path(p).rglob('*')
    for p in plist:
        if p.name == '.DS_Store' or p.name == 'Thumbs.db': # Ignore hidden files
            continue
        if p.suffix == '.xml': # Ignore XML, for example if exiftool XML already exists
            continue
        if p.is_file():
            flist.append(str(p.resolve()))


    # Retrieve metadata through exiftool
    with exiftool.ExifTool() as et:
        metadata = et.get_metadata_batch(flist)


    # Set up output file
    with open(c, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields, extrasaction='ignore',
                                quotechar='"')
        writer.writeheader()


    # Write out output
        for md in metadata:
            writer.writerow(md)


if __name__ == "__main__":
    main()
