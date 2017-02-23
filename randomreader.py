import random, time, datetime

samplerate = 5

class Reader:

    # Format: {correction};{setpoint};T1;T2;...
    def read(self) :
        tset = 120
        line = "{0};{1};{2};{3};{4}"
        data = [datetime.datetime.now(), 0, tset, 0, 0]
        while True:
            data[0] = datetime.datetime.now()
            data[1] = random.uniform(0, 100)
            f1 = 1.0
            if data[3] > tset:
                f1 = -1.0
            data[3] += f1 * random.uniform(-12.0/samplerate, 20.0/samplerate)
            f2 = 1.0
            if data[4] > tset:
                f2 = -1.0
            data[4] += f2 * random.uniform(-4.0/samplerate, 12.0/samplerate)
            yield line.format(*data)
            time.sleep(1.0/samplerate)

