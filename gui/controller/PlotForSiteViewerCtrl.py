__author__ = 'francisco'

from gui.views.PlotForSiteViewerView import ViewPlotForSiteViewer
import numpy

class logicPlotForSiteViewer(ViewPlotForSiteViewer):
    def __init__(self, panel):
        ViewPlotForSiteViewer.__init__(self, panel)

    def plotData(self, data, name, noDataValue):

        if len(data) == 0:
            return

        # unpack the dates, values and replace nodata with None
        dates, values = zip(*data)
        nvals = numpy.array(values, dtype=numpy.float)
        nvals[nvals == noDataValue] = None

        # plot datetime axis
        self.axes.plot_date(x=dates, y=nvals, label=name, linestyle='-', marker=None)
        self.displayLegend(0)
        self.reDraw()

    def reDraw(self):
        self.plot.draw()

    def clearPlot(self):
        self.axes.clear()
        self.axes.grid()
        self.axes.margins(0)
        self.reDraw()

