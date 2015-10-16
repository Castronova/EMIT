__author__ = 'francisco'

from gui.views.viewPlotForSiteViewer import ViewPlotForSiteViewer
import numpy

class logicPlotForSiteViewer(ViewPlotForSiteViewer):
    def __init__(self, panel):
        ViewPlotForSiteViewer.__init__(self, panel)
        x_axis_value = [0.202, 0.2, 0.212, 0.208, 0.2, 0.198, 0.203, 0.199, 0.196, 0.196, 0.194, 0.199, 0.2]
        self.plotData(x_axis_value)

    def plotData(self, data):
        t = numpy.arange(0.0, len(data), 1.0)
        self.axes.plot(t, data)
        self.reDraw()

    def reDraw(self):
        self.plot.draw()

    def clearPlot(self):
        self.axes.clear()
        self.reDraw()

