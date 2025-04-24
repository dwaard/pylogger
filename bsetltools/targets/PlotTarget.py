import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
import numpy as np
import datetime
from collections import deque
import warnings, logging


class PlotTarget:

  def __init__(self, config, title='BSETools plot target', max_samples=500, verbosity=0):
    fig, axis = plt.subplots()
    plt.title(title)
    with warnings.catch_warnings(action="ignore"):
      plt.legend()
    self.verbosity = verbosity
    self.axis = axis
    self.config = config
    self.max_samples = max_samples
    self.num_lines = len(config) - 1
    self.data_buffers = []
    self.rigt_outward_position = 0
    self.init()


  def init(self):
    # build the required buffers
    self.timestamps = deque(maxlen=self.max_samples)
    self.data_buffers = [deque(maxlen=self.max_samples) for _ in range(self.num_lines)]
    self.keys = []
    self.configs = []
    self.axes = []
    self.lines = []
    self.axis.get_yaxis().set_visible(False) # verberg de hoofdas
    for index, (key, cfg) in enumerate(self.config.items()):
      self.configs.append(cfg)
      if key == 'timestamp':
        self.configureXAxis(self.axis, key, **cfg['axis'])
      else:
        self.keys.append(key)
        current_axes = self.axis.twinx()
        self.configureYAxis(current_axes, index, key, **cfg['axis'])
        line, = current_axes.plot(datetime.datetime.now(), 0, **cfg['line'])
        self.lines.append(line)
    self.isEmpty = True


  def configureXAxis(self, axis, key, location, format='%H:%M:%S', color='black', 
                limits={'auto':True, 'min':0, 'max':1, 'links':[]}):
    logging.debug(f"Building the X-axis with configuration of {key}")
    # build the x-axis
    axis.xaxis_date()
    myFmt = mdates.DateFormatter(format)
    axis.xaxis.set_major_formatter(myFmt)
    axis.xaxis.grid()  # vertical lines


  def configureYAxis(self, axis, index, key, title="", location='left', format=None, color='black', 
                limits={'auto':True, 'min':0, 'max':1, 'links':[]}):
    logging.debug(f"Building the Y-axis with configuration of {key}, location {location}")
    # build the axis
    axis.set_ylabel(title, color=color)
    axis.set_label(title)
    axis.tick_params('y', colors=color)
    if location == 'none':
      axis.get_yaxis().set_visible(False)  # verberg de y-as zelf
    else:
      axis.yaxis.set_label_position(location)
      if location == 'right':
        axis.spines['right'].set_visible(True)
        axis.spines['left'].set_visible(False)
        axis.yaxis.tick_right()
        if self.rigt_outward_position > 0:
          axis.spines['right'].set_position(("outward", self.rigt_outward_position))  # schuif hem iets opzij
        self.rigt_outward_position += 50
      else:
        axis.spines['right'].set_visible(False)
        axis.spines['left'].set_visible(True)
        axis.yaxis.tick_left()
    self.axes.append(axis)
    mplcursors.cursor(axis, hover=True)


  def write(self, data):
    """
    NOTE: it is assumed that the first entry in data is the timestamp (X-value)
    """
    if not self.data_buffers:
      self.init()
    # append the data to the buffers
    for i, val in enumerate(data):
      if i == 0:
        self.timestamps.append(val)
      else:
        self.data_buffers[i-1].append(val)

    for i, line in enumerate(self.lines):
      config = self.configs[i+1]
      # update the data
      line.set_data(self.timestamps, self.data_buffers[i])
      if len(self.timestamps) > 1:
        self.axes[i].set_xlim(self.timestamps[0], self.timestamps[-1])
      # update the scale, if limits.auto==True
      if 'limits' in config['axis']:
        self.updateScaling(i, **config['axis']['limits'])
      # build the label
      self.buildLabel(self.lines[i], data[i+1], **config['label'])
    plt.legend(handles=self.lines, loc='lower center')
    plt.draw()


  def updateScaling(self, index, auto=False, links=[], ymin=0, ymax=1):
    if auto:
      indexes = [index]
      all_data = list(self.data_buffers[index])
      for key in links:
        if key in self.keys:
          index2 = self.keys.index(key)
          
          if index2 != index:
            all_data.extend(self.data_buffers[index2])
            indexes.append(index2)
      ymin, ymax = min(all_data), max(all_data)
      margin = (ymax - ymin) * 0.1 if ymax > ymin else 1
      for i in indexes:
        self.axes[i].set_ylim(ymin - margin, ymax + margin)   
    else:
      margin = (ymax - ymin) * 0.1 if ymax > ymin else 1
      self.axes[index].set_ylim(ymin - margin, ymax + margin)


  def buildLabel(self, line, value, color='black', template="{value}"):
    ylabel = template.format(value=value)
    line.set_label(ylabel)
