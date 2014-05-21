import pymongo
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    vehicles = db.vehicles
    stops = db.stops
    stop_times = db.stop_times

    # first pass: go through each stop and check if any of the correct buses are within 10m
    # 10m corresponds to 4.5e-5 in degrees latitude and 6.2e-5 in degrees longitude
    for stop in stops.find(limit=100):
        stop_lat = stop.lat
        stop_lon = stop.lon
        dirs = stop.directions
        vehicle_sel = vehicles.find()