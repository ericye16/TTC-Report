#!/usr/bin/env python3
import xml.etree.ElementTree as ET
##from urllib import request
##agencyList = request.urlopen(
##    'http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList').read()
agencyList = open('agencyList').read()
tree = ET.fromstring(agencyList)
for agency in tree:
    if agency.attrib['tag'] == 'ttc':
        for k, v in agency.attrib.items():
            print(k, v)
