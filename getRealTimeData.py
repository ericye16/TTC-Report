#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from collections import namedtuple
import requests
import pickle
import sys

RoutesFromNextBus = namedtuple('RoutesFromNextBus',
                               ['tag', 'title'])
class RoutesExt(RoutesFromNextBus):
    pass
StopsFromNextBus = namedtuple('StopsFromNextBus',
                              ['tag', 'title', 'lat', 'lon', 'stopId'])
Direction = namedtuple('Direction',
                       ['tag', 'title', 'name'])
class DirectionExt(Direction):
    pass

if __name__ == '__main__':
    ## collect routes
    # routeList comes from:
    # http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=ttc
    with open('routeList') as routeListFile:
        routeListTree = ET.fromstring(routeListFile.read())
    routes = {}
    for route in routeListTree:
        #print(route.attrib)
        tag = route.attrib['tag']
        title = route.attrib['title']
        routes[tag] = RoutesExt(tag, title)

    ## collect stops, directions associated with routes
    for route in routes.values():
        print("Gathering data from route %s." % route.title, file=sys.stderr)
        stops = {}
        directions = {}
        tag = route.tag
        r = requests.get("http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r=" + tag + "&terse")
        routeConfigTree = ET.fromstring(r.text)
        rt = routeConfigTree[0] # the <route> tag
        assert(rt.attrib['title'] == route.title)
        assert(rt.attrib['tag'] == tag)
        route.latMin = rt.attrib['latMin']
        route.latMax = rt.attrib['latMax']
        route.lonMin = rt.attrib['lonMin']
        route.lonMax = rt.attrib['lonMax']
        for stop in rt.findall('stop'):
            tag = stop.attrib['tag']
            title = stop.attrib['title']
            lat = stop.attrib['lat']
            lon = stop.attrib['lon']
            if 'stopId' in stop.attrib:
                stopId = stop.attrib['stopId']
            else:
                stopId = None
            stops[tag] = StopsFromNextBus(tag, title, lat, lon, stopId)
        for direction in rt.findall('direction'):
            tag = direction.attrib['tag']
            title = direction.attrib['title']
            name = direction.attrib['name']
            d = DirectionExt(tag, title, name)
            d.stops = []
            for stop in direction.findall('stop'):
                d.stops.append(stop.attrib['tag'])
            directions[tag] = d
        route.stops = stops
        route.directions = directions
            

    with open('routeList.pickle', 'wb') as routeListPickleFile:
        pickle.dump(routes, routeListPickleFile)
