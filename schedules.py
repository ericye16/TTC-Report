import pickle, requests, sys

import xml.etree.ElementTree as ET

from pymongo import MongoClient, ASCENDING, DESCENDING
from getRouteDataFromNextBus import RoutesExt, StopsFromNextBus, DirectionExt

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    schedule_routes = db.schedule_routes
    if schedule_routes.count() > 0:
        print("Warning: Routes collection not empty.", file=sys.stderr)
    stop_times = db.schedule_times
    if stop_times.count() > 0:
        print("Warning: Stops collection not empty.", file=sys.stderr)
    with open('routeList.pickle','rb') as route_list_file:
        routes = pickle.load(route_list_file)
    for route in routes.values():
        route_tag = route.tag
        print("Gathering data from route %s." % route.title)
        r = requests.get('http://webservices.nextbus.com/service/publicXMLFeed?command=schedule&a=ttc&r=%s' % route_tag)
        schedule_root = ET.fromstring(r.text)
        routes_list = []
        stops_list = []
        for rt in schedule_root:  # each <route> tag
            # explicitly create the dictionary so we know if something goes wrong
            this_rt = {'tag': rt.attrib['tag'],
                       'direction': rt.attrib['direction'],
                       'title': rt.attrib['title'],
                       'service_class': rt.attrib['serviceClass'],
                       'schedule_class': rt.attrib['scheduleClass']}
            # print(this_rt, file=sys.stderr)
            routes_list.append(this_rt)
            rt_id = schedule_routes.insert(this_rt)
            for tr in rt.findall('tr'):
                block_id = tr.attrib['blockID']  # I'm not too sure what this is for
                for stop in tr.findall('stop'):
                    stop_tag = stop.attrib['tag']
                    stop_time = stop.attrib['epochTime']
                    stop_time_human = stop.text
                    stop_all = {'stop_tag': stop_tag,
                                'stop_time': int(stop_time),
                                'stop_time_h': stop_time_human,
                                'block': block_id,
                                'rt_id': rt_id}
                    # print(stop_all, file=sys.stderr)
                    stop_times.insert(stop_all)
                    stop_all['rt'] = this_rt
                    stops_list.append(stop_all)

    with open('schedules.pickle', 'wb') as schedules_file:
        pickle.dump((routes_list, stops_list), schedules_file)