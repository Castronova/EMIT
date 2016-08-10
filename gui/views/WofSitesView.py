import wx
from gui.controller.CustomListCtrl import CustomListCtrl
from gui.controller.PlotCtrl import PlotCtrl


class WofSitesView(wx.Frame):
    def __init__(self, parent, title, table_columns):
        wx.Frame.__init__(self, parent=parent, id=-1, title=title, pos=wx.DefaultPosition, size=(680, 700),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.start_date = wx.DateTime_Now() - 7 * wx.DateSpan_Day()
        self.end_date = wx.DateTime_Now()
        self.parent = parent
        self._data = None

        panel = wx.Panel(self)
        top_panel = wx.Panel(panel)
        middle_panel = wx.Panel(panel, size=(-1, 30))
        lower_panel = wx.Panel(panel)

        hboxTopPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.plot = PlotCtrl(top_panel)
        hboxTopPanel.Add(self.plot.canvas, 1, wx.EXPAND | wx.ALL, 2)

        top_panel.SetSizer(hboxTopPanel)

        hboxMidPanel = wx.BoxSizer(wx.HORIZONTAL)

        self.startDateText = wx.StaticText(middle_panel, id=wx.ID_ANY, label="Start")
        self.startDatePicker = wx.DatePickerCtrl(middle_panel, id=wx.ID_ANY, dt=self.start_date)
        self.endDateText = wx.StaticText(middle_panel, id=wx.ID_ANY, label="End")
        self.endDatePicker = wx.DatePickerCtrl(middle_panel, id=wx.ID_ANY, dt=self.end_date)
        self.exportBtn = wx.Button(middle_panel, id=wx.ID_ANY, label="Export")
        self.addToCanvasBtn = wx.Button(middle_panel, id=wx.ID_ANY, label="Add to Canvas")
        self.PlotBtn = wx.Button(middle_panel, id=wx.ID_ANY, label="Preview")
        self.line_style_combo = wx.ComboBox(middle_panel, value="Line style")

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
        middle_panel.SetSizer(hboxMidPanel)

        hboxLowPanel = wx.BoxSizer(wx.HORIZONTAL)

        # Build time series table
        self.variableList = CustomListCtrl(lower_panel)
        self.variableList.set_columns(table_columns)

        hboxLowPanel.Add(self.variableList, 1, wx.EXPAND | wx.ALL, 2)
        lower_panel.SetSizer(hboxLowPanel)

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(top_panel, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(middle_panel, 0, wx.EXPAND | wx.ALL, 2)
        vbox.Add(lower_panel, 1, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(vbox)

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("Ready")

        self.Show()
