import pickle, requests, collections, sys, time
import xml.etree.ElementTree as ET
from getRouteDataFromNextBus import RoutesExt, StopsFromNextBus, DirectionExt

Vehicle = collections.namedtuple('Vehicle',
                                 ['id', 'routeTag', 'dirTag', 'lat', 'lon',
                                  'predictable', 'heading', 'timestamp'])

with open('routeList.pickle', 'rb') as routeList:
    routes = pickle.load(routeList)


vehicles = {}
now = int(time.time())
current_last = -1
for route in routes.values():
    rt = route.tag
    print("Getting vehicles from route %s." % rt, file=sys.stderr)
    r = requests.get(
        'http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&r=%s' % rt)
    root = ET.fromstring(r.text)
    if root.find('Error'):
        print(root.find('Error').attrib, file=sys.stderr)
    lt = root.find('lastTime')
    last = int(lt.attrib['time'])
    if last < current_last or current_last == -1:
        current_last = last
    for vehicle in root.findall('vehicle'):
        vId = vehicle.attrib['id']
        if 'routeTag' in vehicle.attrib:
            routeTag = vehicle.attrib['routeTag']
        else:
            routeTag = rt
        if 'dirTag' in vehicle.attrib:
            dirTag = vehicle.attrib['dirTag']
        else:
            dirTag = None
        lat = vehicle.attrib['lat']
        lon = vehicle.attrib['lon']
        predictable = vehicle.attrib['predictable']
        heading = vehicle.attrib['heading']
        vehicles[vId] = Vehicle(vId, routeTag, dirTag, lat, lon, predictable,
                                heading, last)
with open('vehicles-data/vehicles-%s'% now, 'wb') as vehiclesFile:
    pickle.dump(vehicles, vehiclesFile)
