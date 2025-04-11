import os, time, datetime
from pathlib import Path

samplerate = 5

class CSVReader:

    def __init__(self):
        self.filename = os.getenv('CSVREADERFILENAME')
        if self.filename is None:
            raise Exception("CSVREADERFILENAME is not specified")
        if not Path(self.filename).exists():
            raise Exception("CSVREADERFILENAME %s does not exist" % self.filename)
            
        self.interval = float(os.getenv('CSVREADERINTERVAL', 0))

    def read(self) :
        f = open(self.filename, 'r')
        for line in f.readlines():
            yield line
            time.sleep(self.interval)

