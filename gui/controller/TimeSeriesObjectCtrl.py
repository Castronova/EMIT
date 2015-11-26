__author__ = 'francisco'

from gui.views.TimeSeriesObjectViewer import TimeSeriesObjectViewer
from coordinator.emitLogging import elog
import wx


class TimeSeriesObjectCtrl(TimeSeriesObjectViewer):

    def __init__(self, parent=None, parentClass=None):
        TimeSeriesObjectViewer.__init__(self, parent=parent)
        self.parentClass = parentClass  # used to access methods from parent class
        self.SetTitle("Time Series Object Ctrl")

        self.Bind(wx.EVT_DATE_CHANGED, self.setstartDate, self.startDatePicker)
        self.Bind(wx.EVT_DATE_CHANGED, self.setEndDate, self.endDatePicker)
        self.Bind(wx.EVT_BUTTON, self.onExport, self.exportBtn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, self.addToCanvasBtn)
        self.Bind(wx.EVT_BUTTON, self.previewPlot, self.previewBtn)

        self.autoSizeColumns()
        self._objects = None

    def addToCanvas(self, event):
        pass

    def createColumns(self, column_name_list):
        if column_name_list is not None:
            for i in range(len(column_name_list)):
                self.variableList.InsertColumn(i, column_name_list[i])
            self.autoSizeColumns()
        else:
            elog.debug("Column list received is empty")

    def getSelectedObject(self):
        id = self.getSelectedId()
        for object in self._objects:
            if id == object.resultid:
                return object

    def getSelectedId(self):
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                id = self.variableList.GetItemText(i)
                return int(id)

    def onExport(self, event):
        pass

    def previewPlot(self, event):
        id = self.getSelectedId()
        date_time_objects, value, resobj = self.parentClass.getData(resultID=id)

        data = []
        for i in range(len(date_time_objects)):
            data.append((date_time_objects[i], value[i]))

        variable_name = str(resobj.VariableObj.VariableNameCV)
        self.plotGraph(data=data, var_name=variable_name)

    def plotGraph(self, data, var_name, no_data=None):
        self.plot.clearPlot()
        if data is not None:
            self.plot.plotData(data, str(var_name), no_data)
        else:
            elog.info("Received no data to plot")
            elog.info("data is None")

    def populateVariableList(self, data):
        if isinstance(data, dict):
            self._data = data
            rowNumber = 0
            colNumber = 0
            for key, values in data.iteritems():
                pos = self.variableList.InsertStringItem(colNumber, str(key))
                colNumber += 1
                for value in values:
                    self.variableList.SetStringItem(pos, colNumber, str(value))
                    colNumber += 1
                colNumber = 0
                rowNumber += 1

            self.autoSizeColumns()
            self.alternateRowColor()
        else:
            elog.debug("populateVariableList()---data passed is not a dictionary")
            elog.error("Received wrong format of data")

    def setEndDate(self, event):
        self.end_date = self.endDatePicker.GetValue()

    def setPlotLabel(self, x_label, y_label):
        self.plot.setAxisLabel(x_label, y_label)

    def setstartDate(self, event):
        self.start_date = self.startDatePicker.GetValue()

    def setPlotTitle(self, title):
        self.plot.setTitle(title)


