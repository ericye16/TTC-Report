#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from urllib import request
AGENCY = 'ttc'
##agencyList = request.urlopen(
##    'http://webservices.nextbus.com/service/publicXMLFeed?command=agencyList').read()
agencyList = open('agencyList').read()
agencyTree = ET.fromstring(agencyList)
for agency in agencyTree:
    if agency.attrib['tag'] == AGENCY:
        for k, v in agency.attrib.items():
            print(k, v)

routeList = request.urlopen(
    'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=' + AGENCY).read()

routeListTree = ET.fromstring(routeList)
