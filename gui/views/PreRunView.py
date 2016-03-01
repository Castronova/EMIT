__author__ = 'Francisco'

import wx
import sys
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, CheckListCtrlMixin


class CheckListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, CheckListCtrlMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(-1, -1), style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        CheckListCtrlMixin.__init__(self)


class PreRunView(wx.Frame):
    def __init__(self, parent=None):                             # this style makes the window non-resizable
        wx.Frame.__init__(self, parent=parent, id=-1, pos=wx.DefaultPosition, title="Pre Run", size=(405, 450),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        if sys.platform == 'darwin': # Darwin is Mac
            self.SetSize((405, 350))

        # define top and bottom panels
        panel = wx.Panel(self)
        top_panel = wx.Panel(panel)
        lower_panel = wx.Panel(panel)
        ################## OLD GBS ################################################################################
        grid_bag_sizer = wx.GridBagSizer(vgap=5, hgap=5)

        # build top panel
        #  Creating components for the top panel
        self.simulation_name_static_text = wx.StaticText(top_panel, label="Simulation Name:")
        self.simulation_name_textbox = wx.TextCtrl(top_panel)#, size=(500,30))
        self.database_name = wx.StaticText(top_panel, label="Database:")
        self.account_name = wx.StaticText(top_panel, label="User Account:")
        self.database_combo = wx.ComboBox(top_panel, choices=[], style=wx.CB_READONLY)#, size=(500,30))
        self.account_combo = wx.ComboBox(top_panel, choices=[], style=wx.CB_READONLY)
        self.add_account_button = wx.Button(top_panel, label="Add New")

        #  Adding components to grid bag sizer
        grid_bag_sizer.Add(self.simulation_name_static_text, pos=(1, 0), flag=wx.LEFT, border=10)
        grid_bag_sizer.Add(self.simulation_name_textbox, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        grid_bag_sizer.Add(self.database_name, pos=(2, 0), flag=wx.LEFT | wx.TOP, border=10)
        grid_bag_sizer.Add(self.database_combo, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND, border=5)
        grid_bag_sizer.Add(self.account_name, pos=(3, 0), flag=wx.TOP | wx.LEFT, border=10)
        grid_bag_sizer.Add(self.account_combo, pos=(3, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND, border=5)
        grid_bag_sizer.Add(self.add_account_button, pos=(3, 3), flag=wx.TOP|wx.RIGHT, border=5)

        top_panel.SetSizer(grid_bag_sizer)
        #Above is GBS Below is sizers

        # topPanelBase = wx.BoxSizer(wx.VERTICAL)
        #
        # simulationNameField = wx.BoxSizer(wx.VERTICAL)
        # simulationSplitter = wx.BoxSizer(wx.HORIZONTAL)
        # simulationNameField.Add(simulationSplitter)
        # topPanelBase.Add(simulationNameField)
        #
        # simulationSplitter.Add(self.simulation_name_static_text, 0, wx.EXPAND | wx.LEFT, 5)
        # simulationSplitter.Add(self.simulation_name_textbox, 0, wx.EXPAND | wx.RIGHT, 10)
        #
        # databaseInfo = wx.BoxSizer(wx.VERTICAL)
        # databaseSplitter = wx.BoxSizer(wx.HORIZONTAL)
        #
        # databaseInfo.Add(databaseSplitter)
        # topPanelBase.Add(databaseInfo)
        #
        # databaseSplitter.Add(self.database_name, 0, wx.EXPAND |wx.LEFT, 5)
        # databaseSplitter.Add(self.database_combo, 0, wx.EXPAND |wx.RIGHT, 5)
        #
        # accountInfo = wx.BoxSizer(wx.VERTICAL)
        # accountSplitter = wx.BoxSizer(wx.HORIZONTAL)
        #
        # accountInfo.Add(accountSplitter)
        # topPanelBase.Add(accountInfo)
        #
        # accountSplitter.Add(self.account_name, 0, wx.EXPAND | wx.LEFT, 5)
        # accountSplitter.Add(self.account_combo, 0, wx.EXPAND, 5)
        # accountSplitter.Add(self.add_account_button, 0, wx.EXPAND, 5)
        #
        #
        #
        # top_panel.SetSizer(topPanelBase)
        #

        # build lower panel
        self.variableList = CheckListCtrl(lower_panel)
        lower_panel_title = wx.StaticText(lower_panel, label="Select Outputs to Save:")

        # Adding buttons to the lower panel
        self.run_button = wx.Button(lower_panel, id=wx.ID_OK, label="Run")
        self.cancel_button = wx.Button(lower_panel, id=wx.ID_CANCEL, label="Cancel")

        hbox_lower_panel = wx.BoxSizer(wx.VERTICAL)

        # Using a box sizer to position buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        hbox_lower_panel.Add(lower_panel_title, 0, wx.EXPAND | wx.LEFT, 5)
        hbox_lower_panel.Add(self.variableList, 1, wx.EXPAND | wx.ALL, 2)

        # Add sizer of buttons to lower_panel sizer
        hbox_lower_panel.Add(button_sizer, 1, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=5)

        #  Add buttons to the sizer
        button_sizer.Add(self.cancel_button, 1, flag=wx.ALL, border=5)  # The flags centers the buttons
        button_sizer.Add(self.run_button, 1, flag=wx.ALL, border=5)

        self.run_button.SetDefault()

        # The flag shifts the buttons to the right
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
