import pymongo
from pymongo import MongoClient

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    collection = db.vehicles
