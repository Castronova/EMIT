__author__ = 'tonycastronova'

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from gui.controller.PlotForSiteViewerCtrl import logicPlotForSiteViewer


class CheckListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(545, 140), style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)

class WofSitesViewer(wx.Frame):
    def __init__(self, parent, title, table_columns):
        wx.Frame.__init__(self, parent=parent, id=-1, title=title, pos=wx.DefaultPosition, size=(650, 700),
                          style=wx.STAY_ON_TOP | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        # self.siteobject = siteObject
        self.start_date = wx.DateTime_Now() - 7 * wx.DateSpan_Day()
        self.end_date = wx.DateTime_Now()
        self.parent = parent
        self._data = None

        panel = wx.Panel(self)
        self.toppanel = wx.Panel(panel)
        middlepanel = wx.Panel(panel, size=(-1, 35))
        lowerpanel = wx.Panel(panel)

        hboxTopPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.plot = logicPlotForSiteViewer(panel)
        hboxTopPanel.Add(self.plot.plot, 1, wx.EXPAND | wx.ALL, 2)

        self.toppanel.SetSizer(hboxTopPanel)

        hboxMidPanel = wx.BoxSizer(wx.HORIZONTAL)

        # self.startDateBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Start Date")
        self.startDateText = wx.StaticText(middlepanel, id=wx.ID_ANY, label="Start")
        self.startDatePicker = wx.DatePickerCtrl(middlepanel, id=wx.ID_ANY, dt=self.start_date)
        # self.endDateBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="End Date")
        self.endDateText = wx.StaticText(middlepanel, id=wx.ID_ANY, label="End")
        self.endDatePicker = wx.DatePickerCtrl(middlepanel, id=wx.ID_ANY, dt=self.end_date)
        self.exportBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Export")
        self.addToCanvasBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Add to Canvas")
        self.PlotBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Preview")

        # hboxMidPanel.Add(self.startDateBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.Add(self.startDateText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.startDatePicker, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(2)
        # hboxMidPanel.Add(self.endDateBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.Add(self.endDateText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.endDatePicker, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.PlotBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.exportBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.addToCanvasBtn, 1, wx.EXPAND | wx.ALL, 2)
        middlepanel.SetSizer(hboxMidPanel)

        hboxLowPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Build time series table
        self.variableList = CheckListCtrl(lowerpanel)
        for i in range(len(table_columns)):
            self.variableList.InsertColumn(i, str(table_columns[i]))

        hboxLowPanel.Add(self.variableList, 1, wx.EXPAND | wx.ALL, 2)
        lowerpanel.SetSizer(hboxLowPanel)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(self.toppanel, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(middlepanel, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(lowerpanel, 1, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(vbox)

        self.autoSizeColumns()

        self.Show()


    def autoSizeColumns(self):
        for i in range(self.variableList.GetColumnCount()):
            self.variableList.SetColumnWidth(i, wx.LIST_AUTOSIZE)

    def alternateRowColor(self, color="#DCEBEE"):
        for i in range(self.variableList.GetItemCount()):
            if i % 2 == 0:
                self.variableList.SetItemBackgroundColour(i, color)

