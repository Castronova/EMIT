__author__ = 'Francisco'

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, CheckListCtrlMixin


class CheckListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, CheckListCtrlMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(350, 400), style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        CheckListCtrlMixin.__init__(self)

class viewPreRun(wx.Frame):
    def __init__(self, parent=None):                             # this style makes the window non-resizable
        wx.Frame.__init__(self, parent=parent, title="Pre Run", size=(405, 375),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        # define top and bottom panels
        panel = wx.Panel(self)
        top_panel = wx.Panel(panel)
        lower_panel = wx.Panel(panel)

        grid_bag_sizer = wx.GridBagSizer(vgap=5, hgap=5)

        # build top panel
        #  Creating components for the top panel
        self.simulation_name_static_text = wx.StaticText(top_panel, label="Simulation Name:")
        self.simulation_name_textbox = wx.TextCtrl(top_panel)
        self.database_name = wx.StaticText(top_panel, label="Database:")
        self.account_name = wx.StaticText(top_panel, label="User Account:")
        self.database_combo = wx.ComboBox(top_panel, choices=[], style=wx.CB_READONLY)
        self.account_combo = wx.ComboBox(top_panel, choices=[], style=wx.CB_READONLY)
        self.add_account_button = wx.Button(top_panel, label="Add New")
        self.run_button = wx.Button(top_panel, id=wx.ID_OK, label="Run")
        self.cancel_button = wx.Button(top_panel, id=wx.ID_CANCEL, label="Cancel")

        #  Adding components to grid bag sizer
        grid_bag_sizer.Add(self.simulation_name_static_text, pos=(1, 0), flag=wx.LEFT, border=10)
        grid_bag_sizer.Add(self.simulation_name_textbox, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        grid_bag_sizer.Add(self.database_name, pos=(2, 0), flag=wx.LEFT | wx.TOP, border=10)
        grid_bag_sizer.Add(self.database_combo, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND, border=5)
        grid_bag_sizer.Add(self.account_name, pos=(3, 0), flag=wx.TOP | wx.LEFT, border=10)
        grid_bag_sizer.Add(self.account_combo, pos=(3, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND, border=5)
        grid_bag_sizer.Add(self.add_account_button, pos=(3, 3), flag=wx.TOP|wx.RIGHT, border=5)
        grid_bag_sizer.Add(self.run_button, pos=(4, 3), flag=wx.BOTTOM | wx.RIGHT, border=5)
        grid_bag_sizer.Add(self.cancel_button, pos=(4, 2), flag=wx.BOTTOM | wx.RIGHT, border=5)

        self.run_button.SetDefault()
        top_panel.SetSizer(grid_bag_sizer)

        # build lower panel
        self.variableList = CheckListCtrl(lower_panel)
        lower_panel_title = wx.StaticText(lower_panel, label="Select Outputs to Save:")
        hbox_lower_panel = wx.BoxSizer(wx.VERTICAL)
        hbox_lower_panel.Add(lower_panel_title, 0, wx.EXPAND | wx.LEFT, 5)
        hbox_lower_panel.Add(self.variableList, 1, wx.EXPAND | wx.ALL, 2)
        lower_panel.SetSizer(hbox_lower_panel)

        #  Add top and lower panel to the sizer
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(top_panel, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(lower_panel, 1, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(vbox)
        self.Show()

    def autoSizeColumns(self):
        for i in range(self.variableList.GetColumnCount()):
            self.variableList.SetColumnWidth(i, wx.LIST_AUTOSIZE)

    def alternateRowColor(self, color="#DCEBEE"):
        for i in range(self.variableList.GetItemCount()):
            if i % 2 == 0:
                self.variableList.SetItemBackgroundColour(i, color)
