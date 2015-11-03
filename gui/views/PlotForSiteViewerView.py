__author__ = 'francisco'

import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sb


class ViewPlotForSiteViewer:
    def __init__(self, panel):
        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.grid()
        self.axes.margins(0)
        self.setAxisLabel("Date Time", "Units")
        self.plot = FigureCanvas(panel, -1, self.figure)

    def setTitle(self, title=""):
        self.axes.set_title(str(title))

    def displayLegend(self, location='upper right'):
        '''
        Taken from http://matplotlib.org/api/figure_api.html
        'best' : 0,          (currently not supported for figure legends)
        'upper right'  : 1,
        'upper left'   : 2,
        'lower left'   : 3,
        'lower right'  : 4,
        'right'        : 5,
        'center left'  : 6,
        'center right' : 7,
        'lower center' : 8,
        'upper center' : 9,
        'center'       : 10,
        '''
        self.axes.legend(loc=location)

    def setAxisLabel(self, x, y):
        self.axes.set_xlabel(x)
        self.axes.set_ylabel(y)




