__author__ = 'francisco'

from gui.views.TimeSeriesObjectViewer import TimeSeriesObjectViewer
from coordinator.emitLogging import elog
import wx


class TimeSeriesObjectCtrl(TimeSeriesObjectViewer):

    def __init__(self, parent=None):
        TimeSeriesObjectViewer.__init__(self, parent=parent)
        self.SetTitle("Time Series Object Ctrl")

        self.Bind(wx.EVT_DATE_CHANGED, self.setstartDate, self.startDatePicker)
        self.Bind(wx.EVT_DATE_CHANGED, self.setEndDate, self.endDatePicker)
        self.Bind(wx.EVT_BUTTON, self.onExport, self.exportBtn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, self.addToCanvasBtn)

        self.autoSizeColumns()

    def addToCanvas(self, event):
        pass

    def createColumns(self, column_name_list):
        if column_name_list is not None:
            for i in range(len(column_name_list)):
                self.variableList.InsertColumn(i, column_name_list[i])
            self.autoSizeColumns()
        else:
            elog.debug("Column list received is empty")

    def onExport(self, event):
        pass

    def previewPlot(self, event):
        pass

    def plotGraph(self, data, var_name, no_data=None):
        self.plot.clearPlot()
        if data is not None:
            self.plot.plotData(data, str(var_name), no_data)
        else:
            elog.info("Received no data to plot")
            elog.info("data is None")

    def populateVariableList(self):
        pass

    def setEndDate(self, event):
        self.end_date = self.endDatePicker.GetValue()

    def setPlotLabel(self, x_label, y_label):
        self.plot.setAxisLabel(x_label, y_label)

    def setstartDate(self, event):
        self.start_date = self.startDatePicker.GetValue()

    def setPlotTitle(self, title):
        self.plot.setTitle(title)


