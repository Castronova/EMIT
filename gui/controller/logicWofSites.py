__author__ = 'tonycastronova'

import wx
from gui.views.WofSitesView import ViewWofSites
from coordinator.emitLogging import elog
import wx.calendar as cal


class LogicWofSites(ViewWofSites):

    def __init__(self, parent, siteObject):

        ViewWofSites.__init__(self, parent, siteObject)

        self.Bind(wx.EVT_BUTTON, self.previewPlot, self.PlotBtn)
        self.Bind(wx.EVT_BUTTON, self.startDateCalender, self.startDateBtn)
        self.Bind(wx.EVT_BUTTON, self.endDateCalender, self.endDateBtn)
        self.Bind(wx.EVT_BUTTON, self.export, self.exportBtn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, id=self.addToCanvasBtn.GetId())
        self.isCalendarOpen = False  # Used to prevent calendar being open twice

    def addToCanvas(self, event):
        var = self.Parent.selectedVariables = self.getSelectedVariableSiteCode()
        parent = self.Parent
        siteobject = self.siteobject
        start = self.startDate.FormatISODate()
        end = self.endDate.FormatISODate()
        self.Close()
        if var > 0:
            parent.setParsedValues(siteobject, start, end)

    def endDateCalender(self, event):
        if self.isCalendarOpen:
            pass
        else:
            Calendar(self, -1, "Calendar", "end")

    def export(self, event):
        dial = wx.MessageDialog(None, message='This feature has not been implemented yet.', style=wx.OK)
        dial.ShowModal()


    def getSelectedVariableName(self):
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                checkedVar = self.variableList.GetItemText(i)
                return checkedVar

    def getSelectedVariableSiteCode(self):
        num = self.variableList.GetItemCount()
        checkedVar = []
        for i in range(num):
            if self.variableList.IsSelected(i):
                checkedVar.append(self.variableList.GetItemText(i))

        if len(checkedVar) > 0:
            sitecode = self.getSiteCodeByVariableName(checkedVar)
            return sitecode
        else:
            return 0

    def getSiteCodeByVariableName(self, checkedVar):
        for key, value in self.data.iteritems():
            if value[0] == checkedVar[0]:
                return key

    def previewPlot(self, event):
        varList = self.getSelectedVariableSiteCode()
        if varList > 0:
            self.plot.clearPlot()
            data = self.Parent.api.parseValues(self.siteobject.sitecode, varList,
                                               self.startDate.FormatISODate(), self.endDate.FormatISODate())
            self.plot.setTitle(self.getSelectedVariableName())
            self.plot.setAxisLabel("Date Time", "Units")
            self.plot.plotData(data, str(varList))

    def populateVariablesList(self, api, sitecode):
        data = api.buildAllSiteCodeVariables(sitecode)
        self.data = data
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
