import csv
import datetime
import os
import time

import wx

from coordinator.emitLogging import elog
from gui.views.TimeSeriesPlotView import TimeSeriesPlotView


class SimulationPlotCtrl(TimeSeriesPlotView):

    def __init__(self, parent=None, parentClass=None, timeseries_variables={}):

        table_cols = ["id", "Variable", "Units", "Begin Date",
                      "End Date", "Description", "Organization"]

        TimeSeriesPlotView.__init__(self, parent, "", table_cols)

        self.populateVariableList(timeseries_variables)

        self.parentClass = parentClass  # used to access methods from parent class

        self.Bind(wx.EVT_DATE_CHANGED, self.setstartDate, self.startDatePicker)
        self.Bind(wx.EVT_DATE_CHANGED, self.setEndDate, self.endDatePicker)
        self.Bind(wx.EVT_BUTTON, self.onExport, self.exportBtn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, self.addToCanvasBtn)
        self.Bind(wx.EVT_BUTTON, self.previewPlot, self.PlotBtn)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.enableBtns)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.disableBtns)

        self.autoSizeColumns()
        self.disableBtns(None)
        self.plot_data = None
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

    def disableBtns(self, event):
        self.PlotBtn.Disable()
        self.exportBtn.Disable()
        self.addToCanvasBtn.Disable()
        self.startDatePicker.Disable()
        self.endDatePicker.Disable()

    def enableBtns(self, event):
        self.PlotBtn.Enable()
        # Commented out until implementation is complete
        # self.exportBtn.Enable()
        # self.addToCanvasBtn.Enable()

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
        save = wx.FileDialog(parent=self, message="Choose Path",
                             defaultDir=os.getcwd(),
                             wildcard="CSV Files (*.csv)|*.csv",
                             style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save.ShowModal() == wx.ID_OK:
            path = save.GetPath()
            if path[-4] != '.':
                path += '.csv'
            file = open(path, 'w')
            writer = csv.writer(file, delimiter=',')
            varInfo = self.getSelectedObject()
            id = self.getSelectedId()
            date_time_object, values, resojb = self.parentClass.getData(resultID=id)

            writer.writerow(["#---Disclaimer: "])
            writer.writerow(["#"])
            writer.writerow(["Date Created: %s" % str(varInfo.date_created.strftime("%m/%d/%Y"))])
            writer.writerow(["Date Exported: %s" % str(time.strftime("%m/%d/%Y"))])
            writer.writerow(["ID: %s" % str(id)])
            writer.writerow(["Feature Code: %s" % str(varInfo.featurecode)])
            writer.writerow(["Variable Name: %s" % str(varInfo.variable)])
            writer.writerow(["Unit: %s" % str(varInfo.unit)])
            writer.writerow(["Type: %s" % str(varInfo.type)])
            writer.writerow(["Organization: %s" % str(varInfo.organization)])
            writer.writerow(["#"])
            writer.writerow(["#---End Disclaimer"])
            writer.writerow(["#"])
            writer.writerow(["Dates", "Values"])

            for i in range(len(date_time_object)):
                writer.writerow([date_time_object[i], values[i]])

            file.close()

    def previewPlot(self, event):

        id = self.getSelectedId()

        date_time_objects, value = self.plot_data[id]

        data = []
        for i in range(len(date_time_objects)):
            data.append((date_time_objects[i], value[i]))

        try:
            name = self._data[id][0]
            units = self._data[id][1]
            self.plotGraph(data=data, var_name=name, yunits=units)

        except Exception as e:
            elog.debug("DetachedInstanceError. See resobj.VariableObj" + str(e))
            elog.error("Failed to load the graph.  Try restarting.")

    def plotGraph(self, data, var_name, yunits=None, no_data=None):
        self.plot.clearPlot()
        if data is not None:
            # self.plot.setAxisLabel(" ", yunits)
            self.plot.plotData(data, str(var_name), no_data, yunits)
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
                    if self.isDateTimeObject(value) is not None:
                        value = self.isDateTimeObject(value)
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

    def isDateTimeObject(self, object):
        if type(object) is not datetime.datetime:
            return None
        else:
            return object.strftime("%m/%d/%Y")


