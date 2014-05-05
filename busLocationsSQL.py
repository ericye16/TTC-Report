import pickle, glob, sys, sqlite3
from busLocations import Vehicle

if __name__ == '__main__':
    db = sqlite3.connect("busLocations.sqlite3")
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS vehicles(vId INTEGER, routeTag TEXT, dirTag TEXT, lat REAL,"
                "lon REAL, heading INTEGER, timestamp INTEGER, UNIQUE(vId, timestamp))")
    dataFiles = glob.glob('vehicles-data/vehicles-*')
    time_dist = []
    for i, dataFile in enumerate(sorted(dataFiles)):
        print("Processing file: %s with %.2f%% complete" % (dataFile, i * 100 / len(dataFiles)), file=sys.stderr)
        f = open(dataFile, 'rb')
        vehicles = pickle.load(f)
        def vehicleGenerator(vehicles):
            for vehicle in vehicles:
                vId = int(vehicle.id)
                routeTag = vehicle.routeTag
                dirTag = vehicle.dirTag
                lat = float(vehicle.lat)
                lon = float(vehicle.lon)
                timestamp = int(vehicle.timestamp)
                heading = int(vehicle.heading)
                yield (vId, routeTag, dirTag, lat, lon, heading, timestamp)
        cur.executemany("INSERT OR IGNORE INTO vehicles VALUES(?,?,?,?,?,?,?)", vehicleGenerator(vehicles.values()))
        num_vehicles = len(vehicles)
        time_stamp = int(dataFile.split('-')[2])
        time_dist.append((time_stamp, num_vehicles))
        if (i % 10 == 0):
            db.commit()
        f.close()
    db.commit()
    db.close()
    with open('time_dist.pickle', 'wb') as time_dist_pickle:
        pickle.dump(time_dist, time_dist_pickle)