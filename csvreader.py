import random, time, datetime

samplerate = 5

class Reader:

    # Format: {correction};{setpoint};T1;T2;...
    def read(self) :
        print "reading"
        f = open('data2.csv', 'r')
        for line in f.readlines():
            print line
            yield line
            time.sleep(1.0/samplerate)

