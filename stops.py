from getRouteDataFromNextBus import StopsFromNextBus, RoutesExt, DirectionExt
from pymongo import MongoClient, ASCENDING, DESCENDING
import pickle, sys


if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    stops_collection = db.stops
    stops_collection.create_index([('tag', ASCENDING)])
    directions_collection = db.directions
    directions_collection.create_index([('tag', ASCENDING)])
    with open('routeList.pickle', 'rb') as route_list_file:
        routes = pickle.load(route_list_file)

    for route in routes.values():

        # find out about the stops
        for stop in route.stops.values():
            this_stop = {
                'stopId': stop.stopId,
                'tag': stop.tag,
                'title': stop.title,
                'lat': float(stop.lat),
                'lon': float(stop.lon),
                'directions': [],
            }
            print("Adding stop %s" % stop.tag, file=sys.stderr)
            stops_collection.update({'tag': stop.tag}, this_stop, upsert=True)
            stops_collection.update({'tag': stop.tag}, {'$push': {'routes': route.tag}})

        # add directions to stops
        for direction in route.directions.values():
            this_direction = {
                'tag': direction.tag,
                'title': direction.title,
                'name': direction.name,
                'directions': [],
            }
            print("Adding direction %s" % direction.tag, file=sys.stderr)
            direction_obj = directions_collection.update({'tag': direction.tag}, this_direction, upsert=True)
            for stop_tag in direction.stops:
                stops_collection.update({'tag': stop_tag},
                                        {'$push':
                                             {'directions': direction.tag}})
