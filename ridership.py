import csv
from pymongo import MongoClient, ASCENDING

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    ridership_collection = db.ridership
    ridership_collection.create_index([('route', ASCENDING)])

    ridership_cost = {}
    with open('ridership-data/TTC-buses-streetcar-ridership.csv', 'r') as ridership_file:
        ridership_csv = csv.reader(ridership_file)
        next(ridership_csv)  # skip header
        for line in ridership_csv:
            route = line[0].split()[0]
            riders = int(line[2])
            daily_cost = int(line[7][1:].replace(',',''))  # strip dollar sign
            ridership_cost[route] = (riders, daily_cost)
            ridership_collection.insert({'route': route,
                                         'ridership': riders,
                                         'cost': daily_cost})