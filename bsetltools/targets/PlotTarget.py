import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
from collections import deque
import logging

class PlotTarget:

  def __init__(self, axes, config, max_samples=3000):
    self.axis = axes
    self.config = config
    self.max_samples = max_samples
    self.num_lines = len(config)
    self.data_buffers = []
    self.rigt_outward_position = 0


  def init(self):
    # build the required buffers
    self.timestamps = deque([datetime.datetime.now()]*self.max_samples, maxlen=self.max_samples)
    self.data_buffers = [deque([0]*self.max_samples, maxlen=self.max_samples) for _ in range(self.num_lines)]
    self.configs = []
    self.axes = []
    self.lines = []
    is_first = True
    for index, (key, cfg) in enumerate(self.config.items()):
      if key == 'timestamp':
        self.buildXAxes(self.axis, key, cfg)
      else:
        current_axes = self.axis if is_first else self.axis.twinx()
        is_first = False
        self.buildYAxes(current_axes, index, key, cfg)
    self.isEmpty = True


  def buildConfig(self, cfg, key):
    result = cfg['plot']
    result['key'] = key
    if 'title' not in result:
      result['title'] = key
    return result


  def buildXAxes(self, axes, key, cfg):
    logging.info('Building the X-axis')
    # build the config
    config = self.buildConfig(cfg, key)
    if 'format' not in config or config['format'] is None:
      config['format'] = '%H:%M:%S'
    # self.configs.append(config)
    # build the x-axis
    axes.xaxis_date()
    myFmt = mdates.DateFormatter(config['format'])
    axes.xaxis.set_major_formatter(myFmt)
    axes.xaxis.grid()  # vertical lines
    # self.axes.append(axes.xaxis)
    # self.lines.append('no line')


  def buildYAxes(self, axes, index, key, cfg):
    # build the config
    config = self.buildConfig(cfg, key)
    if 'location' not in config or config['location'] is None:
      config['location'] = 'left' if index < 2 else 'right'
    if 'min' not in config or config['min'] is None:
      config['min'] = 0 if 'min' not in cfg['params'] else cfg['params']['min']
    if 'max' not in config or config['max'] is None:
      config['max'] = 0 if 'max' not in cfg['params'] else cfg['params']['max']
    color = config.get('color', 'black')
    line, = axes.plot(datetime.datetime.now(), 0, label=key, color=color)
    self.configs.append(config)
    # build the axis
    ylabel = config['axis_title'] if config['axis_title'] is not None else config['title'] 
    if 'unit' in config:
      ylabel = f"{ylabel} ({config['unit']})"
    axes.set_ylabel(ylabel, color=color)
    axes.set_label(ylabel)
    axes.tick_params('y', colors=color)
    axis_location = config['axis_location']
    if axis_location == 'none':
      axes.get_yaxis().set_visible(False)  # verberg de y-as zelf
    elif axis_location == 'right':
      if self.rigt_outward_position > 0:
        axes.spines[axis_location].set_position(("outward", self.rigt_outward_position))  # schuif hem iets opzij
      self.rigt_outward_position += 50
    ymin = config['min']
    ymax = config['max']
    margin = (ymax - ymin) * 0.1 if ymax > ymin else 1
    axes.set_ylim(ymin - margin, ymax + margin)
    self.axes.append(axes)
    # build the line
    line, = axes.plot([], [], color=color, label=ylabel)
    self.lines.append(line)


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
      line.set_data(self.timestamps, self.data_buffers[i])
      self.axes[i].set_xlim(self.timestamps[0], self.timestamps[-1])
      # ymin = min(self.data_buffers[i])
      # ymax = max(self.data_buffers[i])
      # margin = (ymax - ymin) * 0.1 if ymax > ymin else 1
      # self.axes[i].set_ylim(ymin - margin, ymax + margin)
      name = self.configs[i]['title']
      val = self.data_buffers[i][-1]
      unit = self.configs[i].get('unit', '')
      ylabel = f"{name}: {val}{unit}"
      self.lines[i].set_label(ylabel)
    plt.legend(handles=self.lines)
    plt.draw()


  def update(self, data, new_value):
    if self.isEmpty:
      old = []
    else: 
      old = list(data)
    while len(old) >= self.max_samples:
      del old[0]
    return np.append(old, new_value)

  def set_data(self, plot, x, new_val):
    plot.set_xdata(x)
    plot.set_ydata(self.update(plot.get_ydata(), new_val))
