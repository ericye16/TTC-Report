#!/usr/bin/env python3
import pickle, glob, sys, pymongo
from pymongo import MongoClient
from busLocations import Vehicle


def vehicleGenerator(vehicle):
    vId = int(vehicle.id)
    routeTag = vehicle.routeTag
    dirTag = vehicle.dirTag
    lat = float(vehicle.lat)
    lon = float(vehicle.lon)
    timestamp = int(vehicle.timestamp)
    heading = int(vehicle.heading)
    return [{'vId': vId,
             'timestamp': timestamp},
            {'vId': vId,
            'routeTag': routeTag,
            'dirTag': dirTag,
            'lat': lat,
            'long': lon,
            'heading': heading,
            'timestamp': timestamp}]

if __name__ == '__main__':
    dataFiles = glob.glob('vehicles-data/vehicles-*')
    client = MongoClient()
    db = client.datasummative
    collection = db.vehicles
    collection.create_index([('vId', pymongo.ASCENDING), ('timestamp', pymongo.ASCENDING)])
    time_dist = []
    for i, dataFile in enumerate(sorted(dataFiles)):
        print("Processing file: %s with %.2f%% complete" % (dataFile, i * 100 / len(dataFiles)), file=sys.stderr)
        f = open(dataFile, 'rb')
        vehicles = pickle.load(f)
        for vehicle in vehicles.values():
            #upsert into pymongo
            spec, doc = vehicleGenerator(vehicle)
            collection.update(spec, doc, upsert=True)

        num_vehicles = len(vehicles)
        time_stamp = int(dataFile.split('-')[2])
        time_dist.append((time_stamp, num_vehicles))
        f.close()