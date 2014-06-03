import csv, glob
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timedelta

if __name__ == '__main__':
    client = MongoClient()
    db = client.datasummative
    weather_collection = db.weather
    weather_collection.create_index([('datetime', ASCENDING)])

    ## The file here are downloaded from Climate Canada
    files = glob.glob("weather-data/*.csv")
    daylight_adj = timedelta(hours=1)
    for fname in files:
        with open(fname, 'r', errors='ignore') as f:
            weather_csv = csv.reader(f)
            for _ in range(17): # skip the first 17 rows of the csv since they're not useful
                next(weather_csv)
            for r in weather_csv:
                year = int(r[1])
                month = int(r[2])
                day = int(r[3])
                time = datetime.strptime(r[4], "%H:%M")
                complete_time = datetime(year,month,day,time.hour,time.minute) + daylight_adj

                if r[6] != '' and r[18] != '':  # guard against missing data
                    temp = float(r[6])
                    pressure = float(r[18])
                    data = {'datetime': complete_time,
                            'temp': temp,
                            'pressure': pressure}
                    print(data)
                    weather_collection.insert(data)