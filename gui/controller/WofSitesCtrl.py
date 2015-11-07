__author__ = 'tonycastronova'

import os
import csv
import time
import wx
import wx.calendar as cal
from gui.views.WofSitesView import ViewWofSites
from coordinator.emitLogging import elog
import coordinator.engineAccessors as engine
import uuid
import datetime as dt

class LogicWofSites(ViewWofSites):
    def __init__(self, parent, siteObject):

        ViewWofSites.__init__(self, parent, siteObject)

        self.Bind(wx.EVT_BUTTON, self.previewPlot, self.PlotBtn)
        self.Bind(wx.EVT_BUTTON, self.startDateCalender, self.startDateBtn)
        self.Bind(wx.EVT_BUTTON, self.endDateCalender, self.endDateBtn)
        self.Bind(wx.EVT_BUTTON, self.onExport, self.exportBtn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, self.addToCanvasBtn)
        self.isCalendarOpen = False  # Used to prevent calendar being open twice

    def _preparationToGetValues(self):


        var = self.getSelectedVariableCode()
        parent = self.Parent
        siteobject = self.siteobject

        # convert wx._misc.DateTime to python datetime
        start = dt.datetime.strptime('%sT%s'%(self.startDate.FormatISODate(), self.startDate.FormatISOTime()),
                                     "%Y-%m-%dT%H:%M:%S")
        end = dt.datetime.strptime('%sT%s'%(self.endDate.FormatISODate(), self.endDate.FormatISOTime()),
                                     "%Y-%m-%dT%H:%M:%S")
        return end, parent, siteobject, start, var

    def addToCanvas(self, event):
        end, parent, siteobject, start, variable_code = self._preparationToGetValues()

        if variable_code is None:
            # no table row selected
            return

        args = dict(type = 'wof' ,
                    wsdl=self.parent.api.wsdl,
                    site = siteobject.site_code,
                    variable = variable_code,
                    start = start,
                    end = end,
                    network = siteobject.network
        )

        engine.addModel(attrib=args)


        self.Close()

    def dicToObj(self, data):
        temp = []
        for key, value in data.iteritems():
            d = {}
            d["code"] = key
            d["name"] = value[0]
            d["unit"] = value[1]
            d["category"] = value[2]
            d["type"] = value[3]
            d["begin_date"] = value[4]
            d["end_date"] = value[5]
            d["description"] = value[6]
            temp.append(dicToObj(d))
        return temp

    def endDateCalender(self, event):
        if self.isCalendarOpen:
            pass
        else:
            Calendar(self, -1, "Calendar", "end")

    def onExport(self, event):
        var = self.Parent.selectedVariables = self.getSelectedVariableSiteCode()
        if var > 0:
            save = wx.FileDialog(parent=self.GetTopLevelParent(), message="Choose Path",
                                 defaultDir=os.getcwd(),
                                 wildcard="CSV Files (*.csv)|*.csv",
                                 style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if save.ShowModal() == wx.ID_OK:
                path = save.GetPath()
                if path[-4] != '.':
                    path += '.csv'
                file = open(path, 'w')
                writer = csv.writer(file, delimiter=',')
                varInfo = self.getSelectedVariable()
                end, parent, siteobject, start, var = self._preparationToGetValues()
                values = parent.getParsedValues(siteobject, start, end)

                writer.writerow([
                                    "#-------------------------Disclaimer:  This is a data set that was exported by EMIT ... use at your own risk..."])
                writer.writerow(["#"])
                writer.writerow(["#Date Exported: %s" % getTodayDate()])
                writer.writerow(["#Site Name: %s" % siteobject.site_name])
                writer.writerow(["#Site Code: %s" % siteobject.site_code])
                writer.writerow(["#Variable Name: %s" % varInfo[0]])
                writer.writerow(["#Variable Code: %s" % var])
                writer.writerow(["#Unit: %s" % varInfo[1]])
                writer.writerow(["#Category: %s" % varInfo[2]])
                writer.writerow(["#Type: %s" % varInfo[3]])
                writer.writerow(["#Begin Date: %s" % varInfo[4]])
                writer.writerow(["#End Date: %s" % varInfo[5]])
                writer.writerow(["#Description: %s" % varInfo[6]])
                writer.writerow(["#"])
                writer.writerow(["#-------------------------End Disclaimer"])
                writer.writerow(["#"])
                writer.writerow(["#Dates", "Values"])

                for d in values:
                    writer.writerow([d[0], d[1]])

                file.close()
        else:
            elog.info("Select a variable to export")

    def getSelectedObject(self):
        code = self.getSelectedVariableSiteCode()
        for i in range(len(self._objects)):
            if code == self._objects[i].code:
                return self._objects[i]

    def getSelectedVariable(self):
        code = self.getSelectedVariableSiteCode()
        return self._data[code]

    def getSelectedVariableName(self):
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                checkedVar = self.variableList.GetItemText(i)
                return checkedVar

    def getSelectedVariableCode(self):
        variableCode = None
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                v_name = self.variableList.GetItemText(i)
                variableCode = self.getSiteCodeByVariableName(v_name)
                break
        return variableCode

    def getSelectedVariableSiteCode(self):
        # variable_name_code = []
        num = self.variableList.GetItemCount()
        # checkedVar = []
        for i in range(num):
            if self.variableList.IsSelected(i):
                v_name = self.variableList.GetItemText(i)
                # variable_name_code.append((v_name, self.getSiteCodeByVariableName(v_name)))
                return self.getSiteCodeByVariableName(v_name)
                # checkedVar.append(self.variableList.GetItemText(i))

        # print checkedVar

        # if len(checkedVar) > 0:
        #     sitecode = self.getSiteCodeByVariableName(checkedVar)
        #     return sitecode
        # else:
        #     return 0
        # return zip(*variable_name_code)

    def getSiteCodeByVariableName(self, checkedVar):
        for key, value in self._data.iteritems():
            if value[0] == checkedVar:
                return key

    def previewPlot(self, event):
        var_code = self.getSelectedVariableSiteCode()
        var_name = self.getSelectedVariableName()

        if len(var_code) > 0:
            self.plot.clearPlot()

            data = self.Parent.api.getValues(self.siteobject.site_code, var_code,
                                               self.startDate.FormatISODate(), self.endDate.FormatISODate())
            plotData = []
            noData = None
            # make sure data is found
            if data is not None:
                # get the first data element only
                if len(data[0].values[0]) > 1:
                    values = data[0].values[0].value
                else:
                    elog.info("There are no values.  Try selecting a bigger date range")
                    return

                for value in values:
                    plotData.append((value._dateTime, value.value))

                noData = data[0].variable.noDataValue

            self.plot.setTitle(self.getSelectedVariableName())
            self.plot.setAxisLabel("Date Time", data[0].variable.unit.unitName)
            self.plot.plotData(plotData, var_name, noData)

    def populateVariablesList(self, api, sitecode):
        data = api.buildAllSiteCodeVariables(sitecode)
        self._data = data
        self._objects = self.dicToObj(data)
        rowNumber = 0
        colNumber = 0
        for key, value, in data.iteritems():
            pos = self.variableList.InsertStringItem(rowNumber, str(key))
            for i in value:
                if colNumber is 4 or colNumber is 5:
                    self.variableList.SetStringItem(pos, colNumber, str(i.strftime("%m/%d/%y")))
                else:
                    self.variableList.SetStringItem(pos, colNumber, str(i))
                colNumber += 1
            colNumber = 0
            rowNumber += 1

        self.autoSizeColumns()
        self.alternateRowColor()

    def startDateCalender(self, event):
        if self.isCalendarOpen:
            pass
        else:
            Calendar(self, -1, "Calendar", "start")


class Calendar(wx.Dialog):
    def __init__(self, parent, id, title, type):
        wx.Dialog.__init__(self, parent, id, title, style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^
                                                                           wx.MAXIMIZE_BOX)
        self.type = type

        self.Parent.isCalendarOpen = True

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.calendar = cal.CalendarCtrl(self, -1, style=cal.CAL_SHOW_HOLIDAYS | cal.CAL_SEQUENTIAL_MONTH_SELECTION)

        self.rememberCalendarPos()

        vbox.Add(self.calendar, 0, wx.EXPAND | wx.ALL, 5)

        vbox.Add((-1, 20))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(self, -1, 'Date')
        hbox.Add(self.text)
        vbox.Add(hbox, 0, wx.LEFT, 8)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        btn = wx.Button(self, -1, 'Ok')
        hbox2.Add(btn, 1)
        vbox.Add(hbox2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.Bind(wx.EVT_BUTTON, self.OnQuit, id=btn.GetId())
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

        self.SetSizerAndFit(vbox)

        self.Show(True)
        self.Centre()

    def OnQuit(self, event):
        self.setCalendarDates()
        if self.validateDates():
            self.Parent.isCalendarOpen = False
            self.Destroy()
        else:
            self.text.SetLabel("Make start before end")

    def rememberCalendarPos(self):
        if self.type == "start":
            self.calendar.SetDate(self.Parent.startDate)
        else:
            self.calendar.SetDate(self.Parent.endDate)

    def setCalendarDates(self):
        if self.type == "start":
            self.Parent.startDate = self.calendar.GetDate()
            self.Parent.startDateBtn.SetLabelText(self.calendar.GetDate().FormatDate())
        else:
            self.Parent.endDate = self.calendar.GetDate()
            self.Parent.endDateBtn.SetLabelText(self.calendar.GetDate().FormatDate())

    def validateDates(self):
        if self.Parent.startDate < self.Parent.endDate:
            elog.debug("Start is before End So its GOOD ")
            return True
        else:
            elog.debug("End date must be after start date")
            return False


class dicToObj(object):
    def __init__(self, dic):
        self.__dict__ = dic

def getTodayDate():
    return time.strftime("%m/%d/%Y")
