#!/usr/bin/env python3

import json

manifestfilename = "_EM_RMC_RMA_RMA03487_Cornell_University_Facilities_Construction_Records.json"

with open(manifestfilename, "r") as manifest:
    data = json.load(manifest)

filecount = 0

for p in data['packages']:
    c = int(p['number_files'])
    filecount = filecount + c

print("Total number of files is {0}".format(filecount))

