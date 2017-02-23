import threading, datetime
from dateutil.parser import parse

# the Receiver is the heart of the logger. It uses the Reader to read lines of data, converts
# it to an array and sends it to the logger and plotter. It works on a separate thread btw.
class Receiver(threading.Thread):

    # constructor
    def __init__(self, reader, logger, plotter):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.reader = reader
        self.logger = logger
        self.plotter = plotter

    # starts the thread
    def start(self):
        threading.Thread.start(self)

    # this method is called once when the thread is started
    # the thread stops when the method ends.
    def run(self):
        for line in self.reader.read():
            # split the line into an array of Stiings
            data = line.rstrip().split(';')
            # parse the date
            data[0] = parse(data[0])
            # if you want, transform other items in the array
            # in this example all items >= 3 are transformed to floats.
            for index in range(3, len(data)):
                data[index] = float(data[index])

            print data # for debug purposes

            self.logger.log(data)
            self.plotter.plot(data)


