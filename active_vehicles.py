import glob, pickle, sys
from pymongo import MongoClient, ASCENDING, DESCENDING

from busLocations import Vehicle

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    collection = db.active_vehicles
    collection.create_index([('timestamp', ASCENDING)])
    files = glob.glob('vehicles-data/vehicles-*')
    i = 0
    total = len(files)
    for file in files:
        timestamp = int(file.split('-')[2])
        with open(file, 'rb') as p_file:
            vehicles = pickle.load(p_file)
        n = len(vehicles)
        spec = {'timestamp': timestamp}
        d = {'timestamp': timestamp,
             'count': n}
        collection.update(spec, d, upsert=True)
        print("%.2f%% done" % (i * 100 / total), end='\r', file=sys.stderr)
        i += 1