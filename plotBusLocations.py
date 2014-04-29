import matplotlib.pyplot as plt
from time import strftime, gmtime

def plot(vehicles, figure_filename="vehicles-data/figure-tmp.png"):
    vehicles_filtered = [x for x in vehicles.values() if (
        float(x.lat) > 43.55 and float(x.lat) < 43.95 and
        float(x.lon) < -79.05 and float(x.lon) > -79.7)]
    lats = [x.lat for x in vehicles_filtered]
    lons = [x.lon for x in vehicles_filtered]
    latest_time = max([x.timestamp for x in vehicles.values()])
    plt.scatter(lons, lats)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    t = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime(latest_time // 1000))
    plt.title("Geographic distribution of buses at %s" % t)
    plt.savefig(figure_filename)
    plt.show()
