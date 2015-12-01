__author__ = 'francisco'

from gui.views.PlotForSiteViewerView import ViewPlotForSiteViewer
import numpy

class logicPlotForSiteViewer(ViewPlotForSiteViewer):
    def __init__(self, panel):
        ViewPlotForSiteViewer.__init__(self, panel)
        self.displayLegend(0)

        # stores the plot objects
        self.plots = []
        self.__plot_count = 0

        # stores the axis objects
        self.__axis = []

        # matplotlib color cycle used to ensure primary and secondary axis are not displayed with the same color
        self.__color_cycle = self.axes._get_lines.color_cycle

    def plotData(self, data, name, noDataValue, ylabel):

        if len(data) == 0:
            return

        # unpack the dates, values and replace nodata with None
        dates, values = zip(*data)
        nvals = numpy.array(values, dtype=numpy.float)
        nvals[nvals == noDataValue] = None

        # get the next line color
        color = self.getNextColor()


        if self.__plot_count == 0:
            # plot data on the primary axis
            p = self.axes.plot_date(dates, nvals, label=name, color=color, linestyle='-', marker=None)
            self.axes.legend(p, [pl.get_label() for pl in self.plots], loc=0)
            self.axes.set_ylabel(ylabel)

        elif self.__plot_count > 0:
            # plot data on the secondary axis
            ax = self.axes.twinx()
            self.__axis.append(ax)
            p = ax.plot_date(dates, nvals, label=name, color=color, linestyle='-', marker=None)
            ax.set_ylabel(ylabel)

        # save each of the plots
        self.plots.extend(p)

        # rebuild the legend
        self.axes.legend(self.plots, [pl.get_label() for pl in self.plots], loc=0)

        # increment the plot counter
        self.__plot_count += 1

        # redraw the cavas
        self.reDraw()

    def reDraw(self):
        self.plot.draw()

    def clearPlot(self):

        # clear axis
        self.axes.clear()
        for ax in self.__axis:
            ax.cla()

        # reset the axis container
        self.__axis = []

        self.axes.grid()
        self.axes.margins(0)

        # clear the plot objects
        self.__plot_count = 0
        self.plots = []

        self.reDraw()

    def getNextColor(self):
         return next(self.__color_cycle)
