import csv
import numpy as np
import matplotlib.pyplot as plt
class Route:
    def __init__(self, route_id, route_short_name, route_long_name, route_type):
        self.route_id = route_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_type = route_type
        self.trips = {}

    def __repr__(self):
        return "Route(%s,%s,%s,%s)" % (self.route_id, self.route_short_name,
                                       self.route_long_name, self.route_type)
class Trip:
    def __init__(self, trip_id, service_id, trip_headsign):
        self.trip_id = trip_id
        self.service_id = service_id
        self.trip_headsign = trip_headsign
        self.stops = {}

    def __repr__(self):
        return "Trip(%s,%s,%s)" % (self.trip_id, self.service_id,
                                   self.trip_headsign)

class Stop:
    def __init__(self, stop_id, stop_name, stop_lat, stop_lon):
        self.stop_id = stop_id
        self.stop_name = stop_name
        self.stop_lat = stop_lat
        self.stop_lon = stop_lon

    def __repr__(self):
        return "Stop(%s,%s,%s,%s)" % (self.stop_id,self.stop_name,self.stop_lat,
                                         self.stop_lon)


def show_routes_all(routes_list):
    for k, route in sorted(routes_list.items()):
        print(k, route)
        for k, trip in sorted(route.trips.items()):
            print("\t%s %s" %(k, trip))
if __name__ == '__main__':
    routes_list = {}
    stops_list = {}

    with open('schedules/routes.txt') as routes_file: 
        routes_csv = csv.reader(routes_file)
        next(routes_csv) #skip header
        for route in routes_csv:
            route_id =int(route[0])
            route_short_name = route[2]
            route_long_name = route[3]
            route_type = int(route[5])
            routes_list[route_id] = Route(route_id, route_short_name,
                                          route_long_name, route_type)

    with open('schedules/trips.txt') as trips_file:
        trips_csv = csv.reader(trips_file)
        next(trips_file)
        for trip in trips_csv:
            route_id = int(trip[0])
            service_id =int(trip[1])
            trip_id = int(trip[2])
            trip_headsign = trip[3]
            route = routes_list[route_id]
            route.trips[trip_id] = Trip(trip_id, service_id, trip_headsign)

    with open('schedules/stops.txt') as stops_file:
        stops_csv = csv.reader(stops_file)
        next(stops_file)
        for stop in stops_csv:
            stop_id = int(stop[0])
            stop_name = stop[2]
            stop_lat = float(stop[4])
            stop_lon = float(stop[5])
            stops_list[stop_id] = Stop(stop_id, stop_name, stop_lat, stop_lon)

    ## Distribution of trips vs routes
    trips_freq = []
    for route in routes_list.values():
        trips_freq.append((route.route_short_name, len(route.trips)))

    #plt.figure()
    fig, ax = plt.subplots(1,1)
    n, bins, patches = ax.hist([x[1] for x in trips_freq], bins=25,
                                align='mid', range=(0, 5000))
    plt.xlabel('Number of Trips')
    plt.ylabel('Number of Routes')
    plt.title('Distribution of trips over routes')
    plt.xticks(rotation=70)
    ax.set_xticks(bins[:-1])
    plt.subplots_adjust(bottom=0.2)
    plt.savefig('figures/trip_routes_dist.png')

    ## Geographic distribution of bus stops
    plt.figure(figsize=(8,6))
    #plt.subplots(1,1)
    lats = [x.stop_lat for x in stops_list.values()]
    longs = [x.stop_lon for x in stops_list.values()]

    plt.scatter(longs, lats, marker='.', c='b')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Geographic Distribution of All Stops')
    plt.savefig('figures/geographic_stop_dist.png', dpi=300)


    plt.show()

