import csv

if __name__ == '__main__':
    with open('schedules/stop_times.txt') as stop_times_file:
        stop_times = csv.reader(stop_times_file)