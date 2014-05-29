from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    collection = db.schedule_times
    for schedule_time in collection.find():
        print(schedule_time)
        schedule_time['stop_time'] = int(schedule_time['stop_time'])
        print(schedule_time)
        collection.save(schedule_time)