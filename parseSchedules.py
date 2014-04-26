import csv
class Route:
    def __init__(self, route_id, route_short_name, route_long_name, route_type):
        self.route_id = route_id
        self.route_short_name = route_short_name
        self.route_long_name = route_long_name
        self.route_type = route_type

    def __repr__(self):
        return "Route(%s,%s,%s,%s)" % (self.route_id, self.route_short_name,
                                       self.route_long_name, self.route_type)
        
class Stop:
    pass

routes_list = []

with open('schedules/routes.txt') as routes_file: 
    routes_csv = csv.reader(routes_file)
    next(routes_csv) #skip header
    for route in routes_csv:
        route_id = route[0]
        route_short_name = route[2]
        route_long_name = route[3]
        route_type = route[5]
        routes_list.append(Route(route_id, route_short_name, route_long_name,
                                 route_type))
        
