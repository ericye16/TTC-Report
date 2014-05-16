from pymongo import MongoClient, ASCENDING, DESCENDING
import math, sys


def distance_lat_lon(lat2, lon2, lat1, lon1):
    delta_lat = lat2 - lat1
    delta_lon = lon2 - lon1
    delta_lat_metres = delta_lat * 111106  # http://msi.nga.mil/MSISiteContent/StaticFiles/Calculators/degree.html
    delta_lon_metres = delta_lon * 80609
    return delta_lat_metres, delta_lon_metres

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    collection = db.vehicles
    velocity_collection = db.velocity
    velocity_collection.create_index('timestamp_orig', ASCENDING)
    velocity_collection.create_index([('timestamp_orig', ASCENDING), ('vId', ASCENDING)])
    num_total = collection.count()
    for idx, vehicle in enumerate(collection.find()):
        vehicle_object_id = vehicle['_id']
        vId = vehicle['vId']
        timestamp_old = vehicle['timestamp']
        lat_old = vehicle['lat']
        long_old = vehicle['long']
        route_tag = vehicle['routeTag']
        dir_tag = vehicle['dirTag']

        next_vehicle = collection.find_one({'vId': vId,
                                            'routeTag': route_tag,
                                            'dirTag': dir_tag,
                                            'timestamp': {'$gt': timestamp_old,
                                                          '$lte': timestamp_old + 60 * 1000 * 5},
                                            }, sort=[('timestamp', ASCENDING)])
        if next_vehicle is None:
            continue
        next_vehicle_object_id = next_vehicle['_id']
        timestamp_new = next_vehicle['timestamp']
        time_delta = (timestamp_new - timestamp_old) / 1000
        lat_new = next_vehicle['lat']
        long_new = next_vehicle['long']
        vx, vy = distance_lat_lon(lat_new, long_new, lat_old, long_old)
        vx /= time_delta
        vy /= time_delta
        velocity_data = {'timestamp_orig': timestamp_old,
                         'vx': vx,
                         'vy': vy,
                         'vId': vId,
                         'route_tag': route_tag,
                         'dir_tag': dir_tag,
                         'position_old': vehicle_object_id,
                         'position_new': next_vehicle_object_id}
        spec = {'timestamp_orig': timestamp_old,
                'vId': vId}
        if idx % 1000 == 0:
            print('\rInserting %s at %1.4f%%' %(idx, (idx / num_total * 100)), end='', file=sys.stderr)
        velocity_collection.update(spec, velocity_data, upsert=True)



