import wx
import wx.lib.scrolledpanel


class SettingsView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP)

        # Create panels
        panel = wx.Panel(self)
        menu_panel = wx.Panel(panel, size=(100, -1))
        self.details_panel = wx.lib.scrolledpanel.ScrolledPanel(panel)
        lower_panel = wx.Panel(panel)

        ###########################
        # MENU PANEL
        ###########################

        # Create components
        self.console_button = wx.Button(menu_panel, label="Console", size=(-1, 40), style=wx.BORDER_NONE)
        self.another_button = wx.Button(menu_panel, label="Another", size=(-1, 40), style=wx.BORDER_NONE)
        self.environment_button = wx.Button(menu_panel, label="Environment", size=(-1, 40), style=wx.BORDER_NONE)
        self.console_button.SetForegroundColour(wx.LIGHT_GREY)
        self.another_button.SetForegroundColour(wx.LIGHT_GREY)
        self.environment_button.SetForegroundColour(wx.LIGHT_GREY)

        # Create sizer and add components
        menu_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        menu_panel_sizer.Add(self.console_button, 0, wx.EXPAND | wx.ALL, 0)
        menu_panel_sizer.Add(self.another_button, 0, wx.EXPAND | wx.ALL, 0)
        menu_panel_sizer.Add(self.environment_button, 0, wx.EXPAND | wx.ALL, 0)
        menu_panel.SetSizer(menu_panel_sizer)

        menu_panel.SetBackgroundColour((33, 117, 155))

        ###########################
        # DETAILS PANEL
        ###########################

        self.details_panel.SetupScrolling()
        # Console controls
        self.console_panel = SettingsConsole(self.details_panel)
        self.console_panel.Show()

        # Another controls
        self.__create_another_panel()

        # Environment controls
        self.environment_panel = SettingsEnvironment(self.details_panel)
        self.environment_panel.Hide()

        ###########################
        # LOWER PANEL
        ###########################

        # Create components
        self.save_button = wx.Button(lower_panel, label="Save")
        self.cancel_button = wx.Button(lower_panel, label="Cancel")

        # Create sizer and add components
        lower_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        lower_panel_sizer.AddSpacer((0, 0), 1, wx.EXPAND, 2)
        lower_panel_sizer.Add(self.cancel_button, 0, wx.EXPAND | wx.ALL, 5)
        lower_panel_sizer.Add(self.save_button, 0, wx.EXPAND | wx.ALL, 5)

        lower_panel.SetSizer(lower_panel_sizer)

        ###########################
        # ORGANIZE FRAME
        ###########################

        self.frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.main_sizer.Add(menu_panel, 0, wx.EXPAND | wx.ALL, 0)
        self.main_sizer.Add(self.details_panel, 1, wx.EXPAND | wx.LEFT, 5)

        self.frame_sizer.Add(self.main_sizer, 1, wx.EXPAND | wx.RIGHT, 5)
        self.frame_sizer.Add(lower_panel, 0, wx.EXPAND | wx.ALL, 0)

        panel.SetSizer(self.frame_sizer)

        self.Show()

    def __create_another_panel(self):
        """
        This function should only be called by SettingsView.init()
        It simply separates all of this block of code out of the init so its more compact
        :return:
        """

        # self.another_panel = wx.Panel(self.details_panel)
        self.another_panel = wx.lib.scrolledpanel.ScrolledPanel(self.details_panel)
        self.another_text = wx.StaticText(self.another_panel, label="Another text")
        another_sizer = wx.BoxSizer(wx.VERTICAL)
        another_sizer.Add(self.another_text)
        self.another_panel.SetSizer(another_sizer)
        another_sizer.Fit(self.another_panel)
        self.another_panel.Hide()


class SettingsConsole(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Create components
        header_text = wx.StaticText(self, label="Console")
        line_break = wx.StaticLine(self)
        static_box = wx.StaticBox(self, label="Display Message")
        self.info_checkbox = wx.CheckBox(self, label="Display info message")
        self.warning_checkbox = wx.CheckBox(self, label="Display warning message")
        self.critical_checkbox = wx.CheckBox(self, label="Display critical message")
        self.debug_checkbox = wx.CheckBox(self, label="Display debug message")
        self.error_checkbox = wx.CheckBox(self, label="Display error message")

        # Style components
        header_font = wx.Font(pointSize=18, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)
        header_text.SetFont(header_font)

        # Create sizer and add components
        sizer = wx.BoxSizer(wx.VERTICAL)
        static_box_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)

        sizer.Add(header_text, 0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        sizer.Add(line_break, 0, wx.EXPAND | wx.TOP | wx.LEFT, 10)
        static_box_sizer.Add(self.info_checkbox)
        static_box_sizer.Add(self.warning_checkbox)
        static_box_sizer.Add(self.critical_checkbox)
        static_box_sizer.Add(self.debug_checkbox)
        static_box_sizer.Add(self.error_checkbox)

        sizer.Add(static_box_sizer, 1, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        self.SetSizer(sizer)
        sizer.Fit(self)


class SettingsEnvironment(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # # Create components
        header_text = wx.StaticText(self, label="Environment")
        line_break = wx.StaticLine(self)
        static_box = wx.StaticBox(self, label="Paths")
        save_directory_text = wx.StaticText(self, label="Save directory")
        database_path_text = wx.StaticText(self, label="Local database")
        gdal_text = wx.StaticText(self, label="GDAL")
        self.save_directory_textctrl = wx.TextCtrl(self)
        self.database_path_textctrl = wx.TextCtrl(self)
        self.gdal_path_textctrl = wx.TextCtrl(self)
        self.save_path_button = wx.Button(self, label="Open")
        self.database_path_button = wx.Button(self, label="Open")
        self.gdal_path_button = wx.Button(self, label="Open")
        # Must have so the file dialog buttons appear and the text fields stretch to fill
        empty_button = wx.Button(self, label="", style=wx.BORDER_NONE)

        # Style components
        header_font = wx.Font(pointSize=18, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)
        header_text.SetFont(header_font)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        static_box_sizer = wx.StaticBoxSizer(static_box, wx.VERTICAL)
        row_sizer = wx.BoxSizer(wx.HORIZONTAL)

        main_sizer.Add(header_text, 0, wx.EXPAND | wx.TOP | wx.LEFT, 15)
        main_sizer.Add(line_break, 0, wx.EXPAND | wx.TOP | wx.LEFT, 10)

        row_sizer.Add(save_directory_text, 0, wx.ALL | wx.CENTER, 5)
        row_sizer.Add(self.save_directory_textctrl, 1, wx.EXPAND | wx.ALL | wx.CENTER, 5)
        row_sizer.Add(self.save_path_button, 0, wx.ALL | wx.CENTER, 5)
        row_sizer.Add(empty_button, 0, wx.ALL | wx.CENTER, 5)
        static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(database_path_text, 0, wx.ALL | wx.CENTER, 5)
        row_sizer.Add(self.database_path_textctrl, 1, wx.EXPAND | wx.ALL | wx.CENTER, 5)
        row_sizer.Add(self.database_path_button, 0, wx.ALL | wx.CENTER, 5)
        row_sizer.Add(empty_button, 0, wx.ALL | wx.CENTER, 5)
        static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        row_sizer = wx.BoxSizer(wx.HORIZONTAL)
        row_sizer.Add(gdal_text, 0, wx.ALL | wx.CENTER, 5)
        row_sizer.Add(self.gdal_path_textctrl, 1, wx.EXPAND | wx.ALL | wx.CENTER, 5)
        row_sizer.Add(self.gdal_path_button, 0, wx.ALL | wx.CENTER, 5)
        row_sizer.Add(empty_button, 0, wx.ALL | wx.CENTER, 5)
        static_box_sizer.Add(row_sizer, 1, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(static_box_sizer, 0, wx.ALL | wx.EXPAND, 15)

        self.save_path_button.Bind(wx.EVT_BUTTON, self.on_save_open)
        self.database_path_button.Bind(wx.EVT_BUTTON, self.on_database_open)
        self.gdal_path_button.Bind(wx.EVT_BUTTON, self.on_gdal_open)

        self.SetSizer(main_sizer)
        main_sizer.Fit(self)

    def on_save_open(self, event):
        dialog = wx.FileDialog(self, message="Save Directory")
        if dialog.ShowModal() == wx.ID_OK:
            self.save_directory_textctrl.SetValue(dialog.GetDirectory())
        dialog.Destroy()

    def on_database_open(self, event):
        dialog = wx.FileDialog(self, message="Database")
        if dialog.ShowModal() == wx.ID_OK:
            self.database_path_textctrl.SetValue(dialog.Path())
        dialog.Destroy()

    def on_gdal_open(self, event):
        dialog = wx.FileDialog(self, message="GDAL")
        if dialog.ShowModal() == wx.ID_OK:
            self.gdal_path_textctrl.SetValue(dialog.GetDirectory())
        dialog.Destroy()
