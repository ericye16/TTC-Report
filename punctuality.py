from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    schedule_times_collection = db.schedule_times
    stop_times_collection = db.stop_times
    stops_collection = db.stops
    for stop_time in stop_times_collection.find(limit=100):
        stop = stops_collection.findOne({'_id': stop_time['stop_id']})
        stop_tag = stop['tag']
        