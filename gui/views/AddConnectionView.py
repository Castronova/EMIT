import wx
import sys
import wx.lib.scrolledpanel


class AddConnectionView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, title="Add New Connection",
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        # Create panel(s)
        panel = wx.Panel(self)
        content_panel = wx.lib.scrolledpanel.ScrolledPanel(panel)
        content_panel.SetupScrolling()
        lower_panel = wx.Panel(panel)

        if sys.platform == "darwin":
            self.SetMaxSize((-1, 300))
        elif sys.platform == "win32":
            self.SetMaxSize((-1, 320))
        else:
            self.SetMaxSize((-1, 365))

        ####################################
        # CONTENT
        ####################################

        # Create components
        # Left column
        self.connection_name_label = wx.StaticText(content_panel, label="*Connection Name:")
        self.description_label = wx.StaticText(content_panel, label="Description:")
        self.connection_type_label = wx.StaticText(content_panel, label="*Connection Type:")
        self.engine_label = wx.StaticText(content_panel, label="*Engine:")
        self.database_address_label = wx.StaticText(content_panel, label="*Database Address:")
        self.database_name_label = wx.StaticText(content_panel, label="*Database Name:")
        self.user_label = wx.StaticText(content_panel, -1, "*Username:")
        self.password_label = wx.StaticText(content_panel, -1, "Password:")

        # Right column
        self.connection_name_txt_ctrl = wx.TextCtrl(content_panel)
        self.description_txt_ctrl = wx.TextCtrl(content_panel)
        self.odm_radio = wx.RadioButton(content_panel, label="ODM2")
        self.wof_radio = wx.RadioButton(content_panel, label="WOF")
        self.engine_combo = wx.ComboBox(content_panel, value="---", choices=['PostgreSQL', 'MySQL', 'SQLite'])
        self.database_address_txt_ctrl = wx.TextCtrl(content_panel)
        self.database_name_txt_ctrl = wx.TextCtrl(content_panel)
        self.username_txt_ctrl = wx.TextCtrl(content_panel)
        self.password_txt_ctrl = wx.TextCtrl(content_panel)

        # Styling of components
        # Make required fields bold
        self.connection_name_label.SetFont(self.connection_name_label.GetFont().MakeBold())
        self.connection_type_label.SetFont(self.connection_name_label.GetFont().MakeBold())
        self.engine_label.SetFont(self.engine_label.GetFont().MakeBold())
        self.database_address_label.SetFont(self.database_address_label.GetFont().MakeBold())
        self.database_name_label.SetFont(self.database_name_label.GetFont().MakeBold())
        self.user_label.SetFont(self.user_label.GetFont().MakeBold())

        # Create sizer and add components
        content_sizer = wx.BoxSizer(wx.VERTICAL)
        fgs = wx.FlexGridSizer(8, 2, 5, 5)
        radio_sizer = wx.BoxSizer(wx.HORIZONTAL)

        radio_sizer.Add(self.odm_radio, 1, wx.EXPAND | wx.ALL, 0)
        radio_sizer.Add(self.wof_radio, 1, wx.EXPAND | wx.ALL, 0)

        fgs.AddMany([self.connection_name_label, (self.connection_name_txt_ctrl, 1, wx.EXPAND),
                     self.description_label, (self.description_txt_ctrl, 1, wx.EXPAND),
                     self.connection_type_label, (radio_sizer, 1, wx.EXPAND),
                     self.engine_label, (self.engine_combo, 1, wx.EXPAND),
                     self.database_address_label, (self.database_address_txt_ctrl, 1, wx.EXPAND),
                     self.database_name_label, (self.database_name_txt_ctrl, 1, wx.EXPAND),
                     self.user_label, (self.username_txt_ctrl, 1, wx.EXPAND),
                     self.password_label, (self.password_txt_ctrl, 1, wx.EXPAND)])

        fgs.AddGrowableCol(1, 1)

        content_sizer.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        content_panel.SetSizer(content_sizer)

        ####################################
        # LOWER
        ####################################

        # Create components
        break_line = wx.StaticLine(lower_panel)
        self.ok_btn = wx.Button(lower_panel, wx.ID_OK)

        # Styling of components
        self.ok_btn.SetDefault()
        self.ok_btn.Disable()

        # Create sizers
        lower_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.ok_btn, 0, wx.ALL | wx.EXPAND, 5)

        lower_panel_sizer.Add(break_line, 0, wx.EXPAND | wx.ALL, 0)
        lower_panel_sizer.Add(button_sizer, 0, wx.ALIGN_RIGHT, wx.ALL)

        lower_panel.SetSizer(lower_panel_sizer)

        ####################################
        # FINISHING UP
        ####################################

        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(content_panel, 1, wx.EXPAND)
        frame_sizer.Add(lower_panel, 0, wx.EXPAND | wx.ALL, 0)

        panel.SetSizer(frame_sizer)

        self.CenterOnScreen()
        self.Show()
