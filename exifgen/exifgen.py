#!/usr/bin/env python3

import argparse
from pathlib import Path
import os
import sys
import subprocess

# NOTE: This script caches a lot of data before writing anything out;
#       at some point it may be necessary to re-think its strategy.

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('indir', metavar='[directory]',
                        help='name of directory with assets needing exiftool metadata')
    args = parser.parse_args()

    print('Checking input path...')
    p = Path(args.indir).resolve() # resolve to absolute path
    if not p.exists():             # check to make sure it's an actual thing
        sys.exit("The input directory selected does not exist.")

    inlist = []                    # list of tuples of work to do   
    errs = []                      # all-purpose list for errors, what could go wrong

    print('Generating XML filenames and checking for previously-created output...')
    for w in os.walk(p):
        for f in w[2]:
            if f == '.DS_Store' or f == 'Thumbs.db':
                continue
            asset = '{0}/{1}'.format(w[0],f)
            preexif = Path(asset)
            if preexif.suffix == '.xml':
                errs.append(str(preexif.relative_to(Path.cwd()))) # will list files relative to where the script was run
                exif = None
            else:
                exif = '{0}/{1}{2}_exiftool.xml'.format(preexif.parent,preexif.stem, preexif.suffix.replace('.', '_'))
            
            inlist.append((asset,exif))

    if len(errs) != 0:
        print('XML already exists; please check asset directory.')
        print('\n'.join(errs))
        print('\nExiting.')
        sys.exit()

    rlist = []                      # list of xml filenames and xml-to-be-written
                                    # I know this seems weird but I don't want any xml
                                    # written unless we're sure it's error- and warning-free

    print('Calculating output and checking for errors...')
    for i in inlist:
        print('Processing {0}...'.format(i[0]))
        try:
            exifres = subprocess.run(['exiftool', '-api', 'largefilesupport=1', '-X', i[0]], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            errs.append(str(Path(i[0]).relative_to(Path.cwd())))
            exifres = None

        if exifres is not None and str(exifres.stdout.lower()).find('warn') != -1:
            errs.append(str(Path(i[0]).relative_to(Path.cwd())))
            exifres = None

        if exifres is not None:
            rlist.append((i[1], exifres.stdout))
        
    if len(errs) != 0:
        print('The following files had problems with generating exiftool metadata; please investigate first.')
        print('\n'.join(errs))
        print('\nExiting.')
        sys.exit()

    print('Writing exiftool XML files...')
    # Finally, write out the output to the files
    for r in rlist:
        with open(r[0], 'wb') as newxml:
            newxml.write(r[1])

    # TODO REDO THIS ERROR MESSAGE
    print('\nScript complete. You are STRONGLY ENCOURAGED to review the results' +
          '\nto make sure the output files are consistent with your expectations.')

if __name__ == "__main__":
    main()
