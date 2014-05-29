from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import sys

from normalize_directions import normalize_tag

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative

    schedule_times_collection = db.schedule_times
    schedule_times_collection.create_index([('rt_id', ASCENDING), ('stop_tag', ASCENDING), ('stop_time', ASCENDING)])
    schedule_routes_collection = db.schedule_routes
    schedule_routes_collection.create_index([('tag', ASCENDING), ('direction', ASCENDING), ('service_class', ASCENDING)])
    stop_times_collection = db.stop_times
    stops_collection = db.stops
    vehicles_collection = db.vehicles
    direction_collection = db.directions
    total = stop_times_collection.count()

    punctuality_collection = db.punctuality

    for i, stop_time in enumerate(stop_times_collection.find()):
        # print('stop time: ',stop_time)
        stop = stops_collection.find_one({'_id': stop_time['stop_id']})
        #route = vehicles_collection.find_one({'_id': stop_time['vehicle_id']})
        stop_tag = stop['tag']
        vehicle = vehicles_collection.find_one({'_id': stop_time['vehicle_id']})
        direction_tag = vehicle['dirTag']
        direction_tag_regex = normalize_tag(direction_tag)
        direction = direction_collection.find_one({'tag': direction_tag_regex}, fields=['name', 'tag'])
        if direction is None:
            continue
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
        if schedule_route is None:
            continue
        # print(schedule_route)

        time_of_stop = datetime_of_stop.replace(year=1970, month=1, day=1)
        timestamp_of_stop = int(time_of_stop.timestamp() * 1000)
        # print('ts', timestamp_of_stop)
        # to find the previous scheduled stop time, we need to use:
        # the route (from direction)
        # the direction (from direction)
        # the stop tag
        # the timestamp
        prev_scheduled_stop_time = schedule_times_collection.find_one({'rt_id': schedule_route['_id'],
                                                                       'stop_tag': stop_tag,
                                                                       'stop_time': { '$ne': -1,
                                                                                      '$lte': timestamp_of_stop}
                                                                       }, sort=[('stop_time', DESCENDING)])
        if prev_scheduled_stop_time is None:
            continue

        punctuality = {'sched_time_id': prev_scheduled_stop_time['_id'],
                       'real_time_stop_id': stop_time['_id'],
                       'time_sched': prev_scheduled_stop_time['stop_time'],
                       'time_real': timestamp_of_stop,
                       'day_of_week': service_class,
                       'datetime_real': datetime.fromtimestamp(timestamp // 1000),
                       'rt_tag': vehicle['routeTag'],
                       'direction': direction['tag'],
                       'punctuality': timestamp_of_stop - prev_scheduled_stop_time['stop_time']
                       }

        print('Percent complete: %1.4f%%' % (i * 100 / total), file=sys.stderr)
        punctuality_collection.insert(punctuality)
        #print(punctuality)