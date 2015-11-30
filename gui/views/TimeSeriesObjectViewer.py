__author__ = 'francisco'

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from gui.controller.PlotForSiteViewerCtrl import logicPlotForSiteViewer
from coordinator.emitLogging import elog


class CheckListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(545, 140), style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)  # This allows the row to extend

class TimeSeriesObjectViewer(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, size=(650, 700), style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)


        self.parent = parent
        self.start_date = wx.DateTime_Now() - 7 * wx.DateSpan_Day()
        self.end_date = wx.DateTime_Now()
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

        self.startDateText = wx.StaticText(middlepanel, id=wx.ID_ANY, label="Start")
        self.startDatePicker = wx.DatePickerCtrl(middlepanel, id=wx.ID_ANY, dt=self.start_date)
        self.endDateText = wx.StaticText(middlepanel, id=wx.ID_ANY, label="End")
        self.endDatePicker = wx.DatePickerCtrl(middlepanel, id=wx.ID_ANY, dt=self.end_date)
        self.exportBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Export")
        self.addToCanvasBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Add to Canvas")
        self.previewBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Preview")

        hboxMidPanel.Add(self.startDateText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.startDatePicker, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.endDateText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.endDatePicker, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.previewBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.exportBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.addToCanvasBtn, 1, wx.EXPAND | wx.ALL, 2)
        middlepanel.SetSizer(hboxMidPanel)

        hboxLowPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.variableList = CheckListCtrl(lowerpanel)

        hboxLowPanel.Add(self.variableList, 1, wx.EXPAND | wx.ALL, 2)
        lowerpanel.SetSizer(hboxLowPanel)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(self.toppanel, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(middlepanel, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(lowerpanel, 1, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(vbox)

        self.Show()

    def autoSizeColumns(self):
        for i in range(self.variableList.GetColumnCount()):
            self.variableList.SetColumnWidth(i, wx.LIST_AUTOSIZE)

    def alternateRowColor(self, color="#DCEBEE"):
        for i in range(self.variableList.GetItemCount()):
            if i % 2 == 0:
                self.variableList.SetItemBackgroundColour(i, color)
