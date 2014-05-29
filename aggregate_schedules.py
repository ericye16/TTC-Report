from pymongo import MongoClient, ASCENDING
import pickle

client = MongoClient()
db = client.datasummative
schedule_times_collection = db.schedule_times
schedule_times_collection.create_index([('rt_id', ASCENDING)])
schedule_routes_collection = db.schedule_routes

weekday_stop_times = []
saturday_stop_times = []
sunday_stop_times = []

for scheduled_route in schedule_routes_collection.find():
    for scheduled_time in schedule_times_collection.find({'rt_id': scheduled_route['_id']}):

        # find the service class
        if scheduled_route['service_class'] == 'wkd':
            l = weekday_stop_times
        elif scheduled_route['service_class'] == 'sat':
            l = saturday_stop_times
        elif scheduled_route['service_class'] == 'sun':
            l = sunday_stop_times
        else:
            continue

        # filter out the no-stops
        if scheduled_time['stop_time'] == -1:
            continue

        # add to list
        l.append((scheduled_time['stop_time']))

with open('schedules_times.pickle', 'wb') as schedule_pickle_file:
    pickle.dump((weekday_stop_times, saturday_stop_times, sunday_stop_times), schedule_pickle_file)