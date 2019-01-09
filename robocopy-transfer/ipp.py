#!/usr/bin/env python3

from pathlib import Path, PurePath
from collections import defaultdict
from datetime import datetime
import xml.etree.ElementTree as ET
import re
import os

# Pilfered from stackoverflow
def formatsize(numbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'] # Planning.
    i = 0
    while numbytes >= 1024 and i < len(suffixes)-1:
        numbytes /= 1024.0
        i += 1
    f = ('%.2f' % numbytes).rstrip('0').rstrip('.')
    formatted = '{0} {1}'.format(f, suffixes[i])
    return formatted


# TODO: Set name of input manifest.xml from IPP procedure
# Use the appropriate path constructor
# For now...
pth = os.path.expanduser('~')
mfl = PurePath('/', 'Users', pth, 'Desktop', 'manifest.xml')



manifest = ET.parse(mfl).getroot()
namespaces = {'dfxml' : 
              'http://www.forensicswiki.org/wiki/Category:Digital_Forensics_XML' }

# Reporting Variables
extlist = defaultdict(lambda: 0)
sizetotal = 0
timelist = []

for f in manifest.findall('dfxml:fileobject', namespaces):
    filename = f.find('dfxml:filename', namespaces).text
    extension = PurePath(filename).suffix
    if extension == '':
        extlist['None'] += 1
    else:
        extlist[extension] += 1

    filesize = int(f.find('dfxml:filesize', namespaces).text)
    sizetotal += filesize

    mtime = f.find('dfxml:mtime', namespaces).text
    timestamp = datetime.strptime(mtime, '%Y-%m-%dT%H:%M:%SZ')
    timelist.append(timestamp)


# TODO: Set name of robocopy log from IPP procedure
# Robocopy patterns
#relogstart = re.compile("Started : (.*)")
#relogstop = re.compile("Ended : (.*)")

#with open(f, 'r') as rlog:
#    robocopylog = rlog.readlines()
#    timein = None
#    timeout = None
#
#    for rcl in robocopylog:
#        if timein is None:
#            rstart = relogstart.search(rcl)
#            if rstart is not None:
#                timein = datetime.strptime(rstart.group(1),
#                                           '%A, %B %d, %Y %I:%M:%S %p')
#        if timeout is None:
#            rend = relogstop.search(rcl)
#            if rend is not None:
#                timeout = datetime.strptime(rend.group(1),
#                                            '%A, %B %d, %Y %I:%M:%S %p')


# PRINT EVERYTHING
print('File statistics for most recent deposit')
print('Aggregate size: {0}'.format(formatsize(sizetotal)))
print('Extensions found : Number of files found')
for k in sorted(extlist, key=str.casefold):
    print('{0:>16} : {1}'.format(k, extlist[k]))
print('Most recent timestamp: {0}'.format(datetime.isoformat(timelist[0])))
print('Latest timestamp: {0}'.format(datetime.isoformat(timelist[-1])))
print('Placeholder for Robocopy Stats')
print('\n')

