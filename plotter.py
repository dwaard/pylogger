import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime

SAMPLES = 1000

class Plotter:

    def __init__(self, axes):
        plt.title('ZRHackathon Activity Monitor')
        # define the axes
        self.axes_humidity = axes
        self.axes_temp = self.axes_humidity.twinx()
        # format x-axis
        myFmt = mdates.DateFormatter('%H:%M:%S')
        self.axes_humidity.xaxis.set_major_formatter(myFmt)
        self.axes_humidity.xaxis.grid()  # vertical lines
        # format y-axes
        self.axes_temp.set_ylabel(u'Temperatuur (\u00b0C)')
        self.axes_humidity.set_ylabel('Rel. luchtvochtigheid (%)', color='red')
        self.axes_humidity.set_ylim([0,100])
        self.axes_humidity.tick_params('y', colors='red')
        # create the lines
        n = datetime.datetime.now()
        self.temp_1, = self.axes_temp.plot([n], [0], color='blue', label='Temp')
        self.hmdty, = self.axes_humidity.plot([n], [0], color='red', label='Corr')

    # Helper method to append some new data to some line
    def update(self, data, new_value):
        old = list(data)
        while len(old) >= SAMPLES:
            del old[0]
        return np.append(old, new_value)

    # Helper method that makes sure the new data is plotted
    def set_data(self, plot, x, new_val):
        plot.set_xdata(x)
        plot.set_ydata(self.update(plot.get_ydata(), new_val))

    # is called by the Receiver.
    def plot(self, data):
        new_x = self.update(self.temp_1.get_xdata(), data[0])
        self.set_data(self.hmdty, new_x, data[3])
        self.set_data(self.temp_1, new_x, data[4])
        # update the labels in the legend
        self.temp_1.set_label(u"St: (%.1f\u00b0C)" % data[4])
        self.hmdty.set_label(u"St: (%.1f%%)" % data[3])
        plt.legend(handles=[self.temp_1, self.hmdty], loc=4)
        # find the correct upper and lower limits
        if len(new_x)>1:
            # resize the temp limits
            upper = max(self.temp_1.get_ydata() )
            plt.xlim(new_x[0], new_x[len(new_x)-1])
            self.axes_temp.set_ylim(0, upper*1.05)
        plt.draw()
