__author__ = 'francisco'

from gui.views.PlotForSiteViewerView import ViewPlotForSiteViewer
import numpy

class logicPlotForSiteViewer(ViewPlotForSiteViewer):
    def __init__(self, panel):
        ViewPlotForSiteViewer.__init__(self, panel)

    def plotData(self, data, name, noDataValue):
        del data[-1] #we don't want to plot the no data value
        t = numpy.arange(0.0, len(data), 1.0)
        for i in xrange(len(t)):
            if data[i] == noDataValue:
                data[i] = None
        self.axes.plot(t, data, label=str(name))
        self.displayLegend(1)
        self.reDraw()

    def reDraw(self):
        self.plot.draw()

    def clearPlot(self):
        self.axes.clear()
        self.axes.grid()
        self.axes.margins(0)
        self.reDraw()

