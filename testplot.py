# -*- coding: utf-8 -*-
"""
Demo of how to display two scales on the left and right y axis.

This example uses the Fahrenheit and Celsius scales.
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime, time, threading, random

SAMPLES = 500

# plt.ion()  # set plot to animated CRASHES!!!

start = time.time()
# setup the plot
fig, axes = plt.subplots()


class SampleRecorder(threading.Thread):

    def __init__(self, axes, samplerate=50):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.samplerate = samplerate
        self.m1 = [0.0, 0.0, 0.0]
        plt.title('BBQduino')
        self.axes_percentage = axes
        self.axes_temp = self.axes_percentage.twinx()
        # format x-axis
        myFmt = mdates.DateFormatter('%H:%M:%S')
        self.axes_percentage.xaxis.set_major_formatter(myFmt)
        self.axes_percentage.xaxis.grid()  # vertical lines
        # format y-axes
        self.axes_temp.set_ylabel(u'Temperatuur (\u00b0C)')
        self.axes_percentage.set_ylabel('Correctie (%)', color='red')
        self.axes_percentage.set_ylim([0,100])
        self.axes_percentage.tick_params('y', colors='red')
        # create the lines
        self.corr, = self.axes_percentage.plot([], [], color='red')
        self.temp_1, = self.axes_temp.plot([], [], color='green', label='T1')
        self.temp_2, = self.axes_temp.plot([], [], color='blue', label='T2')
        self.corr, = self.axes_percentage.plot([], [], color='red', label='Corr')

    def start(self):
        self.count = 0;
        threading.Thread.start(self)

    def run(self):
        while True:
            self.tick(self.count)
            self.count = self.count+1
            time.sleep(1.0/self.samplerate)

    def update(self, data, new_value):
        old = list(data)
        while len(old) >= SAMPLES:
            del old[0]
        return np.append(old, new_value)

    def tick(self, count):
        done = time.time()
        elapsed = done - start
        print ({"tick" : elapsed})
        self.m1[0] = self.m1[0] + random.uniform(-2.5, 3)
        self.m1[1] = self.m1[1] + random.uniform(-2, 2)
        self.m1[2] = random.uniform(0, 100)

        new_x = self.update(self.temp_1.get_xdata(), datetime.datetime.now())
        new_t1 = self.update(self.temp_1.get_ydata(), self.m1[0])
        new_t2 = self.update(self.temp_2.get_ydata(), self.m1[1])
        new_cr = self.update(self.corr.get_ydata(), self.m1[2])
        self.temp_1.set_xdata(new_x)
        self.temp_1.set_ydata(new_t1)
        self.temp_2.set_xdata(new_x)
        self.temp_2.set_ydata(new_t2)
        self.corr.set_xdata(new_x)
        self.corr.set_ydata(new_cr)
        # find the correct upper and lower limits
        if len(new_x)>1:
            plt.xlim(new_x[0], new_x[len(new_x)-1])
            all = []
            all.extend(new_t1)
            all.extend(new_t2)
            self.axes_temp.set_ylim(min(all), max(all))
        plt.draw()

SampleRecorder(axes, samplerate=5).start()
plt.legend()
plt.show()
