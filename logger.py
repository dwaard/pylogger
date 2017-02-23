import csv
from datetime import datetime

class Logger:

    # constructor
    def __init__(self, filename='data.csv', **kwds):
        filename = "logger_%s.csv" % datetime.now().strftime("%d-%m-%Y")
        self.writer = csv.writer(open(filename, 'ab'), dialect=csv.excel, **kwds)

    def log(self, data):
        self.writer.writerow(data)