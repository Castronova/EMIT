import wx

from gui.controller.CustomListCtrl import CustomListCtrl


class PreRunView(wx.Frame):

    def __init__(self, parent=None):
        wx.Frame.__init__(self, parent=parent, title="Pre Run",
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX)

        # Create panels
        panel = wx.Panel(self)
        top_panel = wx.Panel(panel)  # Holds text fields for input
        middle_panel = wx.Panel(panel)  # Holds the table
        lower_panel = wx.Panel(panel)  # Holds the buttons

        ###############################
        # TOP PANEL
        ###############################

        #  Create components
        self.simulation_name_static_text = wx.StaticText(top_panel, label="Simulation Name:")
        self.simulation_name_textbox = wx.TextCtrl(top_panel)
        self.database_name = wx.StaticText(top_panel, label="Database:")
        self.database_combo = wx.ComboBox(top_panel, choices=[], style=wx.CB_READONLY)
        self.account_name = wx.StaticText(top_panel, label="User Account:")
        self.account_combo = wx.ComboBox(top_panel, choices=[], style=wx.CB_READONLY)
        self.add_account_button = wx.Button(top_panel, label="Add New")

        account_button_sizer = wx.BoxSizer(wx.HORIZONTAL)  # rename to account button sizer
        account_button_sizer.Add(self.account_combo, 1, wx.EXPAND | wx.ALL, 0)
        account_button_sizer.Add(self.add_account_button, 0, wx.EXPAND | wx.ALL, 0)

        #  Adding components to grid bag sizer
        fgs = wx.FlexGridSizer(rows=3, cols=2, vgap=9, hgap=5)
        fgs.AddMany([self.simulation_name_static_text, (self.simulation_name_textbox, 1, wx.EXPAND),
                     self.database_name, (self.database_combo, 1, wx.EXPAND),
                     self.account_name, (account_button_sizer, 1, wx.EXPAND)])

        fgs.AddGrowableCol(1, 1)  # Allows the text fields to stretch and expand

        top_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_panel_sizer.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        top_panel.SetSizer(top_panel_sizer)

        ###############################
        # MIDDLE PANEL
        ###############################

        #  Create components
        lower_panel_title = wx.StaticText(middle_panel, label="Select Outputs to Save:")
        self.table = CustomListCtrl(middle_panel)

        # Creat sizer and add components
        middle_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        middle_panel_sizer.Add(lower_panel_title, 0, wx.EXPAND | wx.ALL, 2)
        middle_panel_sizer.Add(self.table, 1, wx.EXPAND | wx.ALL, 2)

        middle_panel.SetSizer(middle_panel_sizer)

        ###############################
        # BOTTOM PANEL
        ###############################

        # Create components
        self.run_button = wx.Button(lower_panel, id=wx.ID_OK, label="Run")
        self.cancel_button = wx.Button(lower_panel, id=wx.ID_CANCEL, label="Cancel")

        # Create sizers and add components
        bottom_panel_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bottom_panel_sizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)  # Align the cancel and run button to the right
        bottom_panel_sizer.Add(self.cancel_button, 0, wx.ALL, 5)
        bottom_panel_sizer.Add(self.run_button, 0, wx.ALL, 5)

        lower_panel.SetSizer(bottom_panel_sizer)

        # Organize the panels into the frame
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(top_panel, 0, wx.EXPAND | wx.ALL, 2)
        frame_sizer.Add(middle_panel, 1, wx.EXPAND | wx.ALL, 2)
        frame_sizer.Add(lower_panel, 0, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(frame_sizer)
        frame_sizer.Fit(self)
        self.Show()
