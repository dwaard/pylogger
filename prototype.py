import matplotlib.pyplot as plt
from receiver import Receiver
from serialreader import Reader
from logger import Logger
from plotter import Plotter

# setup the reader, logger and plotter
fig, axes = plt.subplots()
r = Receiver(Reader(), Logger(), Plotter(axes))
r.start()
plt.legend()
plt.show()
