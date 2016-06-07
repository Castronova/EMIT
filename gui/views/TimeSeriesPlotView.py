import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

from emitLogging import elog
from gui.Models.SpatialTemporalPlotter import SpatialTemporalPlotter


class CheckListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(545, 140), style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)


class TimeSeriesPlotView(wx.Frame):
    def __init__(self, parent, title, table_columns):
        wx.Frame.__init__(self, parent=parent, id=-1, title=title, pos=wx.DefaultPosition, size=(650, 700),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

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

        self.plot = SpatialTemporalPlotter(self.toppanel)
        hboxTopPanel.Add(self.plot.plot, 1, wx.EXPAND | wx.ALL, 2)

        self.toppanel.SetSizer(hboxTopPanel)

        hboxMidPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.startDateText = wx.StaticText(middlepanel, id=wx.ID_ANY, label="Start")
        self.startDatePicker = wx.DatePickerCtrl(middlepanel, id=wx.ID_ANY, dt=self.start_date)
        self.endDateText = wx.StaticText(middlepanel, id=wx.ID_ANY, label="End")
        self.endDatePicker = wx.DatePickerCtrl(middlepanel, id=wx.ID_ANY, dt=self.end_date)
        self.exportBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Export")
        self.addToCanvasBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Add to Canvas")
        self.PlotBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Preview")

        hboxMidPanel.Add(self.startDateText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hboxMidPanel.AddSpacer(2)
        hboxMidPanel.Add(self.startDatePicker, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.AddSpacer(2)
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
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("Ready")

        self.Show()


    def autoSizeColumns(self):
        for i in range(self.variableList.GetColumnCount()):
            self.variableList.SetColumnWidth(i, wx.LIST_AUTOSIZE)

    def alternateRowColor(self, color="#DCEBEE"):
        for i in range(self.variableList.GetItemCount()):
            if i % 2 == 0:
                self.variableList.SetItemBackgroundColour(i, color)

    def createColumns(self, column_name_list):
        if column_name_list is not None:
            for i in range(len(column_name_list)):
                self.variableList.InsertColumn(i, column_name_list[i])
            self.autoSizeColumns()
        else:
            elog.debug("Column list received is empty")

    def getSelectedId(self):
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                id = self.variableList.GetItemText(i)
                return int(id)

    def plotGraph(self, data, var_name, y_units=None, no_data=None):
        self.plot.clear_plot()
        if data is not None:
            self.plot.plot_dates(data, str(var_name), no_data, y_units)
        else:
            elog.info("Received no data to plot")
            elog.info("data is None")

