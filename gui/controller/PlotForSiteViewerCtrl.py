__author__ = 'francisco'

from gui.views.PlotForSiteViewerView import ViewPlotForSiteViewer
import numpy

class logicPlotForSiteViewer(ViewPlotForSiteViewer):
    def __init__(self, panel):
        ViewPlotForSiteViewer.__init__(self, panel)

    def clearPlot(self):
        self.axes.clear()
        self.axes.grid()
        self.axes.margins(0)
        self.reDraw()

    def isNan(self, values):  # if values is not a number than return true
        count = 0
        for i in range(len(values)):
            if numpy.isnan(values[i]):
                count += 1
        if count == len(values):
            return True
        else:
            return False

    def plotData(self, data, name, noDataValue):

        if len(data) == 0:
            return

        # unpack the dates, values and replace nodata with None
        dates, values = zip(*data)
        nvals = numpy.array(values, dtype=numpy.float)
        nvals[nvals == noDataValue] = None
        if self.isNan(nvals):
            print "nvals are not a number"
            return

        # plot datetime axis
        self.axes.plot_date(x=dates, y=nvals, label=name, linestyle='-', marker=None)
        self.displayLegend(0)
        self.reDraw()

    def reDraw(self):
        self.plot.draw()

