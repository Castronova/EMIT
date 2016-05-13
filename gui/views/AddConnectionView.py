import wx


class AddConnectionView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, title="Add New Connection",
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        # Create panel(s)
        self.panel = wx.Panel(self)

        # Create components
        # Left column
        self.connection_name_label = wx.StaticText(self.panel, label="*Connection Name:")
        self.description_label = wx.StaticText(self.panel, label="Description:")
        self.connection_type_label = wx.StaticText(self.panel, label="*Connection Type:")
        self.engine_label = wx.StaticText(self.panel, label="*Engine:")
        self.database_address_label = wx.StaticText(self.panel, label="*Database Address:")
        self.database_name_label = wx.StaticText(self.panel, label="*Database Name:")
        self.user_label = wx.StaticText(self.panel, -1, "*Username:")
        self.password_label = wx.StaticText(self.panel, -1, "Password:")
        break_line = wx.StaticLine(self.panel)

        # Right column
        self.connection_name_txt_ctrl = wx.TextCtrl(self.panel)
        self.description_txt_ctrl = wx.TextCtrl(self.panel)
        self.odm_radio = wx.RadioButton(self.panel, label="ODM2")
        self.wof_radio = wx.RadioButton(self.panel, label="WOF")
        self.engine_combo = wx.ComboBox(self.panel, value="---", choices=['PostgreSQL', 'MySQL', 'SQLite'])
        self.database_address_txt_ctrl = wx.TextCtrl(self.panel)
        self.database_name_txt_ctrl = wx.TextCtrl(self.panel)
        self.username_txt_ctrl = wx.TextCtrl(self.panel)
        self.password_txt_ctrl = wx.TextCtrl(self.panel)
        self.ok_btn = wx.Button(self.panel, wx.ID_OK)

        self.ok_btn.SetDefault()
        self.ok_btn.Disable()

        #  Make required fields bold
        self.connection_name_label.SetFont(self.connection_name_label.GetFont().MakeBold())
        self.connection_type_label.SetFont(self.connection_name_label.GetFont().MakeBold())
        self.engine_label.SetFont(self.engine_label.GetFont().MakeBold())
        self.database_address_label.SetFont(self.database_address_label.GetFont().MakeBold())
        self.database_name_label.SetFont(self.database_name_label.GetFont().MakeBold())
        self.user_label.SetFont(self.user_label.GetFont().MakeBold())

        # Create sizers
        fgs = wx.FlexGridSizer(8, 2, 5, 5)
        radio_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        radio_sizer.Add(self.odm_radio, 1, wx.EXPAND | wx.ALL, 0)
        radio_sizer.Add(self.wof_radio, 1, wx.EXPAND | wx.ALL, 0)

        button_sizer.Add(self.ok_btn, 0, wx.ALL | wx.ALIGN_RIGHT, 0)

        # Add components to sizer
        fgs.AddMany([self.connection_name_label, (self.connection_name_txt_ctrl, 1, wx.EXPAND),
                     self.description_label, (self.description_txt_ctrl, 1, wx.EXPAND),
                     self.connection_type_label, (radio_sizer, 1, wx.EXPAND),
                     self.engine_label, (self.engine_combo, 1, wx.EXPAND),
                     self.database_address_label, (self.database_address_txt_ctrl, 1, wx.EXPAND),
                     self.database_name_label, (self.database_name_txt_ctrl, 1, wx.EXPAND),
                     self.user_label, (self.username_txt_ctrl, 1, wx.EXPAND),
                     self.password_label, (self.password_txt_ctrl, 1, wx.EXPAND)])

        hbox = wx.BoxSizer(wx.VERTICAL)  # wrapping the flex grid sizer in order to put some space around the window
        hbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        hbox.Add(break_line, 0, wx.EXPAND | wx.ALL, border=5)
        hbox.Add(button_sizer, 0, wx.ALL | wx.ALIGN_RIGHT, border=5)

        fgs.AddGrowableCol(1, 1)

        self.panel.SetSizer(hbox)
        hbox.Fit(self)

        self.SetMaxSize((-1, 365))  # Set max height to disable resizing the window vertically

        self.Show()
