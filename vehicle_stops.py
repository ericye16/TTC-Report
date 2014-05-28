import sys

from pymongo import MongoClient, ASCENDING

from normalize_directions import extract_rdb, create_regex


if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    vehicles = db.vehicles
    vehicles.create_index([('dirTag', ASCENDING), ('lat', ASCENDING), ('long', ASCENDING)])
    stops = db.stops
    stop_times = db.stop_times
    stop_times.create_index([('vehicle_id', ASCENDING), ('stop_id', ASCENDING), ('timestamp', ASCENDING)])

    # first pass: go through each stop and check if any of the correct buses are within 10m
    # 10m corresponds to 4.5e-5 in degrees latitude and 6.2e-5 in degrees longitude
    num_stops = stops.count()
    for i, stop in enumerate(stops.find()):
        stop_lat = stop['lat']
        stop_lon = stop['lon']
        dirs = stop['directions']
        regexes = []
        for dir in dirs:
            rdb = extract_rdb(dir)
            if rdb is not None:
                route, dir, branch = rdb
                regex = create_regex(route, dir, branch)
                regexes.append(regex)
        print('%1.4f%% complete.' % (i * 100 / num_stops), regexes, file=sys.stderr)
        vehicles_sel = vehicles.find({'dirTag': {'$in': regexes},
                                      'lat': {'$gte': stop_lat - 4.5e-5,
                                              '$lte': stop_lat + 4.5e-5},
                                      'long': {'$gte': stop_lon - 6.2e-5,
                                               '$lte': stop_lon + 6.2e-5}
        })
        for vehicle in vehicles_sel:
            arrival_time_data = {'vehicle_id': vehicle['_id'],
                                 'stop_id': stop['_id'],
                                 'timestamp': vehicle['timestamp'],
                                 'route': vehicle['routeTag'],
                                 'direction': vehicle['dirTag']}
            arrival_time_spec = {'vehicle_id': vehicle['_id'],
                                 'stop_id': stop['_id'],
                                 'timestamp': vehicle['timestamp']}
            stop_times.update(arrival_time_spec, arrival_time_data, upsert=True)