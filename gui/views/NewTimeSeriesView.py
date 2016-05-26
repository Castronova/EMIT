import wx


class NewTimeSeriesView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Components
        self.connection_options = ["---"]
        self.connection_combo = wx.Choice(self, size=(200, -1), choices=self.connection_options)
        self.add_connection_button = wx.Button(self, label="Add Connection")
        self.refresh_button = wx.Button(self, label="Refresh")
        self.table = wx.ListCtrl(self, style=wx.LC_REPORT)

        # Message to show in the ListCtrl when it is empty
        self.empty_list_message = wx.StaticText(parent=self.table, label="This list is empty",
                                                style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE | wx.FULL_REPAINT_ON_RESIZE)
        self.empty_list_message.Hide()
        self.empty_list_message.SetForegroundColour(wx.LIGHT_GREY)
        self.empty_list_message.SetBackgroundColour(self.table.GetBackgroundColour())
        self.empty_list_message.SetFont(wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, ""))

        # Pop up menu
        self.popup_menu = wx.Menu()
        self.view_menu = self.popup_menu.Append(1, "View")

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
