__author__ = 'francisco'

from gui.views.viewPlotForSiteViewer import ViewPlotForSiteViewer
import numpy

class logicPlotForSiteViewer(ViewPlotForSiteViewer):
    def __init__(self, panel):
        ViewPlotForSiteViewer.__init__(self, panel)

    def plotData(self, data, name):
        t = numpy.arange(0.0, len(data), 1.0)
        self.axes.plot(t, data, label=str(name))
        self.reDraw()

    def reDraw(self):
        self.plot.draw()

    def clearPlot(self):
        self.axes.clear()
        self.axes.grid()
        self.axes.margins(0)
        self.reDraw()

