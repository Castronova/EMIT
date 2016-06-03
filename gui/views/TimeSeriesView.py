import wx
from gui.Models.CustomListCtrl import CustomListCtrl


class TimeSeriesView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Components
        self.connection_options = ["---"]
        self.connection_combo = wx.Choice(self, size=(200, -1), choices=self.connection_options)
        self.add_connection_button = wx.Button(self, label="Add Connection")
        self.refresh_button = wx.Button(self, label="Refresh")
        self.table = CustomListCtrl(self)

        # Create sizers
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add components to sizer
        button_sizer.Add(self.connection_combo, 0, wx.ALL, 5)
        button_sizer.Add(self.add_connection_button, 0, wx.ALL, 5)
        button_sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        button_sizer.Add(self.refresh_button, 0, wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 0)
        main_sizer.Add(self.table, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(main_sizer)

    def append_to_connection_combo(self, item):
        if item in self.connection_options:  # Do not add duplicate items
            return
        self.connection_options.append(item)
        self.connection_options.sort()
        self.connection_combo.SetItems(self.connection_options)
