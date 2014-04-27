#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from collections import namedtuple
import requests

RoutesFromNextBus = namedtuple('RoutesFromNextBus',
                               ['tag', 'title'])

with open('routeList') as routeListFile:
    routeListTree = ET.fromstring(routeListFile.read())
routes = {}
for route in routeListTree:
    #print(route.attrib)
    tag = route.attrib['tag']
    title = route.attrib['title']
    routes[tag] = RoutesFromNextBus(tag, title)
