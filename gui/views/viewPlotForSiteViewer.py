__author__ = 'francisco'

import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


class ViewPlotForSiteViewer:
    def __init__(self, panel):
        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.grid()
        self.axes.margins(0)
        self.plot = FigureCanvas(panel, -1, self.figure)

