import pickle, glob, sys
from busLocations import Vehicle

if __name__ == '__main__':
    dataFiles = glob.glob('vehicles-data/vehicles-*')
    vehicles_dict = {}
    for i, dataFile in enumerate(sorted(dataFiles)):
        print("Processing file: %s with %.2f%% complete" % (dataFile, i * 10 / len(dataFiles)), file=sys.stderr)
        f = open(dataFile, 'rb')
        vehicles = pickle.load(f)
        for vehicle in vehicles.values():
            vId = vehicle.id
            routeTag = vehicle.routeTag
            dirTag = vehicle.dirTag
            lat = vehicle.lat
            lon = vehicle.lon
            timestamp = vehicle.timestamp
            if vId in vehicles_dict:
                if abs(vehicles_dict[vId][-1].timestamp - timestamp) < 15e3:
                    continue
                else:
                    vehicles_dict[vId].append(vehicle)
            else:
                vehicles_dict[vId] = [vehicle]
        f.close()
