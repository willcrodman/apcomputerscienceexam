from matplotlib import pyplot as plt
from matplotlib.pyplot import *

class PlotHandler:
    def __init__(self, x, y):
        plt.plot(x, y)
        grid()
        ax = plt.gca()
        ax.axes.xaxis.set_visible(False)
        ax.axes.yaxis.set_visible(True)
        plt.show()