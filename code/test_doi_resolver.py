from doiresolver import DOIResolver
import json
import csv

# iterate through list of DOIs in csv, process them and find the keys, print metadata
doiR = DOIResolver()

meta = doiR.get_meta('10.3389/fcimb.2019.00477.s003')

print('META\n\t\t', meta, '\nKEYS\n\t', meta.keys())