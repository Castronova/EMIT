import wx
from gui.Models.CustomListCtrl import CustomListCtrl
from emitLogging import elog
from gui.Models.SpatialTemporalPlotter import SpatialTemporalPlotter


class TimeSeriesPlotView(wx.Frame):
    def __init__(self, parent, title, table_columns):
        wx.Frame.__init__(self, parent=parent, id=-1, title=title, pos=wx.DefaultPosition, size=(680, 700),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.start_date = wx.DateTime_Now() - 7 * wx.DateSpan_Day()
        self.end_date = wx.DateTime_Now()
        self.parent = parent
        self._data = None

        panel = wx.Panel(self)
        toppanel = wx.Panel(panel)
        middlepanel = wx.Panel(panel, size=(-1, 30))
        lowerpanel = wx.Panel(panel)

        hboxTopPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.plot = SpatialTemporalPlotter(toppanel)
        hboxTopPanel.Add(self.plot.plot, 1, wx.EXPAND | wx.ALL, 2)

        toppanel.SetSizer(hboxTopPanel)

        hboxMidPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.startDateText = wx.StaticText(middlepanel, id=wx.ID_ANY, label="Start")
        self.startDatePicker = wx.DatePickerCtrl(middlepanel, id=wx.ID_ANY, dt=self.start_date)
        self.endDateText = wx.StaticText(middlepanel, id=wx.ID_ANY, label="End")
        self.endDatePicker = wx.DatePickerCtrl(middlepanel, id=wx.ID_ANY, dt=self.end_date)
        self.exportBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Export")
        self.addToCanvasBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Add to Canvas")
        self.PlotBtn = wx.Button(middlepanel, id=wx.ID_ANY, label="Preview")
        self.line_style_combo = wx.ComboBox(middlepanel, value="Line style")

        self.line_style_options = ["Line", "Scatter"]

        self.line_style_combo.AppendItems(self.line_style_options)

        hboxMidPanel.Add(self.startDateText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hboxMidPanel.Add(self.startDatePicker, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.Add(self.endDateText, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        hboxMidPanel.Add(self.endDatePicker, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.Add(self.PlotBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.Add(self.exportBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.Add(self.addToCanvasBtn, 1, wx.EXPAND | wx.ALL, 2)
        hboxMidPanel.Add(self.line_style_combo, 1, wx.EXPAND | wx.ALL, 2)
        middlepanel.SetSizer(hboxMidPanel)

        hboxLowPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Build time series table
        self.variableList = CustomListCtrl(lowerpanel)
        self.variableList.set_columns(table_columns)

        hboxLowPanel.Add(self.variableList, 1, wx.EXPAND | wx.ALL, 2)
        lowerpanel.SetSizer(hboxLowPanel)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(toppanel, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(middlepanel, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(lowerpanel, 1, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(vbox)

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("Ready")

        self.Show()

    def plotGraph(self, data, var_name, y_units=None, no_data=None):
        self.plot.clear_plot()
        if data is not None:
            self.plot.plot_dates(data, str(var_name), no_data, y_units)
        else:
            elog.info("Received no data to plot")
            elog.info("data is None")

