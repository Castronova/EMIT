__author__ = 'tonycastronova'

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from gui.controller.logicPlotForSiteViewer import logicPlotForSiteViewer

class CheckListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(545, 140), style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)

class ViewWofSites(wx.Frame):
    def __init__(self, parent, siteObject):
        wx.Frame.__init__(self, parent=parent, id=-1, title=str(siteObject.site_name), pos=wx.DefaultPosition, size=(650, 700),
                          style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.siteobject = siteObject
        self.startDate = wx.DateTime_Now() - 7 * wx.DateSpan_Day()
        self.endDate = wx.DateTime_Now()
        self.parent = parent
        self.data = None

        panel = wx.Panel(self)
        self.toppanel = wx.Panel(panel)
        middlepanel = wx.Panel(panel, size=(-1, 35))
        lowerpanel = wx.Panel(panel)

        hboxTopPanel = wx.BoxSizer(wx.HORIZONTAL)


        self.plot = logicPlotForSiteViewer(panel)
        hboxTopPanel.Add(self.plot.plot, 1, wx.EXPAND | wx.ALL, 2)

        self.toppanel.SetSizer(hboxTopPanel)

        hboxMidPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.startDateBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Start Date")
        self.endDateBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="End Date")
        self.exportBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Export")
        self.addToCanvasBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Add to Canvas")
        self.PlotBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Preview")

        hboxMidPanel.Add(self.startDateBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(20)
        hboxMidPanel.Add(self.endDateBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(20)
        hboxMidPanel.Add(self.PlotBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(20)
        hboxMidPanel.Add(self.exportBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(20)
        hboxMidPanel.Add(self.addToCanvasBtn, 1, wx.EXPAND | wx.ALL, 2)
        middlepanel.SetSizer(hboxMidPanel)

        hboxLowPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Column names
        self.variableList = CheckListCtrl(lowerpanel)
        self.variableList.InsertColumn(0, "Variable Name")
        self.variableList.InsertColumn(1, "Unit")
        self.variableList.InsertColumn(2, "Category")
        self.variableList.InsertColumn(3, "Type")
        self.variableList.InsertColumn(4, "Begin Date Time")
        self.variableList.InsertColumn(5, "End Date Time")
        self.variableList.InsertColumn(6, "Description")



        hboxLowPanel.Add(self.variableList, 1, wx.EXPAND | wx.ALL, 2)
        lowerpanel.SetSizer(hboxLowPanel)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(self.toppanel, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(middlepanel, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(lowerpanel, 1, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(vbox)

        self.autoSizeColumns()

        self.Show()

    def addToCanvas(self, event):
        self.Parent.selectedVariables = self.getSelectedVariableSiteCode()

        self.Close()
        if len(self.Parent.selectedVariables) > 0:
            self.Parent.setParsedValues(self.siteobject)

    def autoSizeColumns(self):
        for i in range(self.variableList.GetColumnCount()):
            self.variableList.SetColumnWidth(i, wx.LIST_AUTOSIZE)

