import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
from collections import deque
import logging

class PlotTarget:

  def __init__(self, axis, config, max_samples=3000, verbosity=0):
    self.verbosity = verbosity
    self.axis = axis
    self.config = config
    self.max_samples = max_samples
    self.num_lines = len(config) - 1
    self.data_buffers = []
    self.rigt_outward_position = 0



  def buildLine(self, axis, **kwargs):
    default_val = 0 # float('nan')
    line, = axis.plot(datetime.datetime.now(), default_val, **kwargs)
    self.lines.append(line)


  def init(self):
    # build the required buffers
    self.timestamps = deque([datetime.datetime.now()]*self.max_samples, maxlen=self.max_samples)
    self.data_buffers = [deque([0]*self.max_samples, maxlen=self.max_samples) for _ in range(self.num_lines)]
    self.keys = []
    self.configs = []
    self.axes = []
    self.lines = []
    is_first = True
    for index, (key, cfg) in enumerate(self.config.items()):
      logging.warning(f"{cfg}")
      self.configs.append(cfg)
      if key == 'timestamp':
        self.configureXAxis(self.axis, key, **cfg['axis'])
      else:
        self.keys.append(key)
        current_axes = self.axis if is_first else self.axis.twinx()
        is_first = False
        self.configureYAxis(current_axes, index, key, **cfg['axis'])
        self.buildLine(current_axes, **cfg['line'])
    self.isEmpty = True


  def configureXAxis(self, axis, key, location, format='%H:%M:%S', color='black', 
                limits={'auto':True, 'min':0, 'max':1, 'links':[]}):
    logging.info(f"Building the X-axis with configuration of {key}")
    # build the x-axis
    axis.xaxis_date()
    myFmt = mdates.DateFormatter(format)
    axis.xaxis.set_major_formatter(myFmt)
    axis.xaxis.grid()  # vertical lines
    # self.axes.append(axis.xaxis)


  def configureYAxis(self, axis, index, key, title="", location='left', format=None, color='black', 
                limits={'auto':True, 'min':0, 'max':1, 'links':[]}):
    logging.info(f"Building the Y-axis with configuration of {key}")
    # build the axis
    axis.set_ylabel(title, color=color)
    axis.set_label(title)
    axis.tick_params('y', colors=color)
    if location == 'none':
      axis.get_yaxis().set_visible(False)  # verberg de y-as zelf
    elif location == 'right':
      if self.rigt_outward_position > 0:
        axis.spines[location].set_position(("outward", self.rigt_outward_position))  # schuif hem iets opzij
      self.rigt_outward_position += 50
    # # Set the limits
    # is_auto = 'auto' in limits and limits['auto'] == True
    # ymin = 0 if is_auto else limits['ymin']
    # ymax = 1 if is_auto else limits['ymax']
    # margin = (ymax - ymin) * 0.1 if ymax > ymin else 1
    # axis.set_ylim(ymin - margin, ymax + margin)
    self.axes.append(axis)


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
      self.axes[i].set_xlim(self.timestamps[0], self.timestamps[-1])
      # update the scale, if limits.auto==True
      if 'limits' in config['axis']:
        self.updateScaling(i, **config['axis']['limits'])
      # build the label
      self.buildLabel(self.lines[i], data[i+1], **config['label'])

    plt.legend(handles=self.lines)
    plt.draw()


  def updateScaling(self, index, auto=False, links=[], ymin=0, ymax=1):
    if auto:
      indexes = [index]
      all_data = self.data_buffers[index]
      for key in links:
        if key in self.keys:
          index2 = self.keys.index(key)
          
          if index2 != index:
            all_data.extend(self.data_buffers[index2])
            indexes.append(index2)
      ymin, ymax = min(all_data), max(all_data)
      margin = (ymax - ymin) * 0.1 if ymax > ymin else 1
      for i in indexes:
        logging.warning(f"updating auto limits: {ymin - margin}-{ymax + margin}")
        self.axes[i].set_ylim(ymin - margin, ymax + margin)   
    else:
      margin = (ymax - ymin) * 0.1 if ymax > ymin else 1
      logging.warning(f"updating fixed limits: {ymin - margin}-{ymax + margin}")
      self.axes[index].set_ylim(ymin - margin, ymax + margin)
    pass


  def buildLabel(self, line, value, color='black', template="{value}"):
    ylabel = template.format(value=value)
    line.set_label(ylabel)
    pass


  # def update(self, data, new_value):
  #   if self.isEmpty:
  #     old = []
  #   else: 
  #     old = list(data)
  #   while len(old) >= self.max_samples:
  #     del old[0]
  #   return np.append(old, new_value)

  # def set_data(self, plot, x, new_val):
  #   plot.set_xdata(x)
  #   plot.set_ydata(self.update(plot.get_ydata(), new_val))
