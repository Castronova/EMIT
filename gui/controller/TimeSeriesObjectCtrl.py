import csv
import os
import time

import wx

from emitLogging import elog
from gui.views.TimeSeriesPlotView import TimeSeriesPlotView


class TimeSeriesObjectCtrl(TimeSeriesPlotView):

    def __init__(self, parent=None, parentClass=None, timeseries_variables={}):

        table_cols = ["Result ID", "Feature Code", "Variable", "Unit", "Type", "Organization", "Date Created"]
        TimeSeriesPlotView.__init__(self, parent, "TimeSeries Viewer", table_cols)

        self.populateVariableList(timeseries_variables)

        self.parentClass = parentClass  # used to access methods from parent class
        self.endDatePicker.Disable()
        self.startDatePicker.Disable()
        self.Bind(wx.EVT_DATE_CHANGED, self.setstartDate, self.startDatePicker)
        self.Bind(wx.EVT_DATE_CHANGED, self.setEndDate, self.endDatePicker)
        self.Bind(wx.EVT_BUTTON, self.onExport, self.exportBtn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, self.addToCanvasBtn)
        self.Bind(wx.EVT_BUTTON, self.preview_plot, self.PlotBtn)
        self.disableBtns(None)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.enableBtns)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.disableBtns)
        self.autoSizeColumns()
        self._objects = None

    def addToCanvas(self, event):
        elog.info("Add to canvas has not been implementd")  # Remove this print when it is implemented

    def disableBtns(self, event):
        self.exportBtn.Disable()
        self.addToCanvasBtn.Disable()
        self.PlotBtn.Disable()

    def enableBtns(self, event):
        self.exportBtn.Enable()
        self.PlotBtn.Enable()

    def getSelectedRow(self):
        id = self.getSelectedId()
        row = self._data[id]
        row.insert(0, id)  # Attaching the id to return value
        return row

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
            varInfo = self.getSelectedRow()
            id = self.getSelectedId()
            date_time_object, values, resojb = self.parentClass.getData(resultID=id)

            writer.writerow(["#---Disclaimer: "])
            writer.writerow(["#"])
            writer.writerow(["Date Created: %s" % str(varInfo[-1].strftime("%m/%d/%Y"))])
            writer.writerow(["Date Exported: %s" % str(time.strftime("%m/%d/%Y"))])
            writer.writerow(["ID: %s" % str(id)])
            writer.writerow(["Feature Code: %s" % str(varInfo[1])])
            writer.writerow(["Variable Name: %s" % str(varInfo[2])])
            writer.writerow(["Unit: %s" % str(varInfo[3])])
            writer.writerow(["Type: %s" % str(varInfo[4])])
            writer.writerow(["Organization: %s" % str(varInfo[5])])
            writer.writerow(["#"])
            writer.writerow(["#---End Disclaimer"])
            writer.writerow(["#"])
            writer.writerow(["Dates", "Values"])

            for i in range(len(date_time_object)):
                writer.writerow([date_time_object[i], values[i]])

            file.close()

    def preview_plot(self, event):

        id = self.getSelectedId()
        date_time_objects, value, resobj = self.parentClass.menu.getData(id)

        data = []
        for i in range(len(date_time_objects)):
            data.append((date_time_objects[i], value[i]))

        try:
            variable_name = str(resobj.VariableObj.VariableNameCV)
            unit_name = '%s [%s]' % (resobj.UnitObj.UnitsName, resobj.UnitObj.UnitsAbbreviation)
            self.plotGraph(data=data, var_name=variable_name, y_units=unit_name)

        except Exception as e:
            elog.debug("DetachedInstanceError. See resobj.VariableObj" + str(e))
            elog.error("Failed to load the graph.  Try restarting.")

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
            elog.debug("populate_variable_list()---data passed is not a dictionary")
            elog.error("Received wrong format of data")

    def setEndDate(self, event):
        self.end_date = self.endDatePicker.GetValue()

    def setPlotLabel(self, x_label, y_label):
        self.plot.setAxisLabel(x_label, y_label)

    def setstartDate(self, event):
        self.start_date = self.startDatePicker.GetValue()

    def setPlotTitle(self, title):
        self.plot.setTitle(title)
