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
        return "Stop(%s,%s,%s,%s)" % (self.stop_id, self.stop_name, self.stop_lat,
                                      self.stop_lon)