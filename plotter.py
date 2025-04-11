import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime

SAMPLES = 3000

SETPOINT_COLOR = 'red'
INPUT_COLOR = 'blue'
OUTPUT_COLOR = 'green'
PULSE_COLOR = 'orange'

SETPOINT_STEP = 1
INPUT_STEP = 1
OUTPUT_STEP = 10
PULSE_STEP = 1

class Plotter:

    def __init__(self, axes):
        plt.title('Proofingcontroller')
        # format y-axes
        self.axes_setpoint = axes
        self.axes_setpoint.set_ylabel('Temp (\u00b0C)')
        self.axes_setpoint.tick_params('y')

        self.axes_input = self.axes_setpoint.twinx()
        self.axes_input.set_ylabel(u'Input (\u00b0C)', color=INPUT_COLOR)
        self.axes_input.yaxis.set_label_position("left")
        self.axes_input.yaxis.tick_left()
        self.axes_input.spines["left"].set_position(("outward", 60))  # schuif hem iets opzij
        self.axes_input.spines["left"].set_visible(False)
        self.axes_input.tick_params('y', colors=INPUT_COLOR)
        # Zorg dat input dezelfde limieten gebruikt als setpoint
        self.axes_input.get_yaxis().set_visible(False)  # verberg de y-as zelf
        self.axes_input.set_ylim(self.axes_setpoint.get_ylim())

        # Voeg callbacks toe om synchronisatie te waarborgen
        # self.axes_setpoint.callbacks.connect(
        #     "ylim_changed",
        #     lambda ax: self.axes_input.set_ylim(ax.get_ylim())
        #     if self.axes_input.get_ylim() != ax.get_ylim() else None
        # )

        # self.axes_input.callbacks.connect(
        #     "ylim_changed",
        #     lambda ax: self.axes_setpoint.set_ylim(ax.get_ylim())
        #     if self.axes_setpoint.get_ylim() != ax.get_ylim() else None
        # )
        self.axes_output = self.axes_setpoint.twinx()
        self.axes_output.set_ylabel(u'Output (%)', color=OUTPUT_COLOR)
        self.axes_output.tick_params('y', colors=OUTPUT_COLOR)
        self.axes_output.set_ylim(-0.1, 100.1)
        self.axes_output.set_yticks(np.arange(0, 100.1, 100/3))

        self.axes_pulse = self.axes_setpoint.twinx()
        self.axes_pulse.set_ylabel(u'Pulse (s)', color=PULSE_COLOR)
        self.axes_pulse.tick_params('y', colors=PULSE_COLOR)
        self.axes_pulse.spines["right"].set_position(("outward", 50))  # schuif hem iets opzij

        # format x-axis
        myFmt = mdates.DateFormatter('%H:%M:%S')
        self.axes_setpoint.xaxis.set_major_formatter(myFmt)
        self.axes_setpoint.xaxis.grid()  # vertical lines

        # create the lines
        data = [datetime.datetime.now(), 0, 0, 0, 0]
        new_x = data[0]
        self.firstYAxes, = self.axes_setpoint.plot(new_x, data[1], color=SETPOINT_COLOR, label='Set')
        self.secondYAxes, = self.axes_input.plot(new_x, data[2], color=INPUT_COLOR, label='In')
        self.thirdYAxes, = self.axes_output.plot(new_x, data[3], color=OUTPUT_COLOR, label='Out')
        self.fourthYAxes, = self.axes_pulse.plot(new_x, data[4], color=PULSE_COLOR, label='Pulse')

        self.isEmpty = True

    def update(self, data, new_value):
        if self.isEmpty:
            old = []
        else: 
            old = list(data)
        while len(old) >= SAMPLES:
            del old[0]
        return np.append(old, new_value)

    def set_data(self, plot, x, new_val):
        plot.set_xdata(x)
        plot.set_ydata(self.update(plot.get_ydata(), new_val))

    def plot(self, data):
        new_x = self.update(self.secondYAxes.get_xdata(), data[0])
        self.set_data(self.firstYAxes, new_x, data[1])
        self.set_data(self.secondYAxes, new_x, data[2])
        self.set_data(self.thirdYAxes, new_x, data[3])
        self.set_data(self.fourthYAxes, new_x, data[4])
        self.isEmpty = False
        self.firstYAxes.set_label(u"Set: (%.1f\u00b0C)" % data[1])
        self.secondYAxes.set_label(u"In: (%.1f\u00b0C)" % data[2])
        self.thirdYAxes.set_label(u"Out: (%.1f%%)" % data[3])
        self.fourthYAxes.set_label(u"Pulse: (%.1fs)" % data[4])
        plt.legend(handles=[self.firstYAxes, self.secondYAxes, self.thirdYAxes, self.fourthYAxes], loc=4)
        # find the correct upper and lower limits
        if len(new_x)>1:
            plt.xlim(new_x[0], new_x[len(new_x)-1])

            tempMin = min(self.lower(self.firstYAxes, SETPOINT_STEP), self.lower(self.secondYAxes, INPUT_STEP))
            tempMax = max(self.upper(self.firstYAxes, SETPOINT_STEP), self.upper(self.secondYAxes, INPUT_STEP))
            self.axes_setpoint.set_ylim(tempMin, tempMax)
            self.axes_input.set_ylim(tempMin, tempMax)
            # self.axes_output.set_ylim(self.lower(self.thirdYAxes, OUTPUT_STEP), self.upper(self.thirdYAxes, OUTPUT_STEP))
            self.axes_pulse.set_ylim(self.lower(self.fourthYAxes, PULSE_STEP), self.upper(self.fourthYAxes, PULSE_STEP))

        plt.draw()

    def upper(self, data, steps):
        step_f = steps * 1.0
        largest = max(data.get_ydata())
        return np.ceil(largest/step_f)*steps + step_f/10

    def lower(self, data, steps):
        step_f = steps * 1.0
        largest = min(data.get_ydata())
        return np.floor(largest/step_f)*steps - step_f/10