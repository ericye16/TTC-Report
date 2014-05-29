from pymongo import MongoClient, ASCENDING
from datetime import datetime

from normalize_directions import normalize_tag

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    schedule_times_collection = db.schedule_times
    schedule_routes_collection = db.schedule_routes
    schedule_routes_collection.create_index([('tag', ASCENDING), ('direction', ASCENDING), ('service_class', ASCENDING)])
    stop_times_collection = db.stop_times
    stops_collection = db.stops
    vehicles_collection = db.vehicles
    direction_collection = db.directions
    for stop_time in stop_times_collection.find(limit=100):
        stop = stops_collection.find_one({'_id': stop_time['stop_id']})
        route = vehicles_collection.find_one({'_id': stop_time['vehicle_id']})
        stop_tag = stop['tag']
        vehicle = vehicles_collection.find_one({'_id': stop_time['vehicle_id']})
        direction_tag = vehicle['dirTag']
        direction_tag_regex = normalize_tag(direction_tag)
        direction = direction_collection.find_one({'tag': direction_tag_regex}, fields=['name'])
        direction_name = direction['name']

        ## figure out the proper service class
        timestamp = stop_time['timestamp']
        datetime_of_stop = datetime.fromtimestamp(timestamp // 1000)
        day_of_week = datetime_of_stop.weekday()
        if day_of_week < 5:
            service_class = 'wkd' # weekday
        elif day_of_week == 5:
            service_class = 'sat'
        elif day_of_week == 6:
            service_class = 'sun'

        ## find the schedule route
        schedule_route = schedule_routes_collection.find_one({'direction': direction_name,
                                                              'tag': vehicle['routeTag'],
                                                              'service_class': service_class
        })
        print(schedule_route)

        # strip the timestamp of date-related info  TODO

        # to find the previous scheduled stop time, we need to use:
        # the route (from direction)
        # the direction (from direction)
        # the stop tag
        # the timestamp
        # prev_scheduled_stop_time = schedule_times_collection.find_one({'rt_id': schedule_route['_id'],
        #                                                                'stop_tag': stop_tag,
        #                                                                'stop_time': {'$ne': -1,
        #                                                                              }
        #                                                               }, sort=[('stop_time', ASCENDING)])