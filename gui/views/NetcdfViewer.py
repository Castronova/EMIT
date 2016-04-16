__author__ = 'francisco'

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin


class CheckListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(545, 140), style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)


class NetcdfViewer(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, id=wx.ID_ANY, title="THREDDS File Browser", pos=wx.DefaultPosition, size=(400, 500), style= wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.parent = parent

        panel = wx.Panel(self)
        self.top_panel = wx.Panel(panel)
        self.bottom_panel = wx.Panel(panel, size=(-1, 70))
        # self.bottom_panel.SetBackgroundColour("#AABBCC")

        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.variable_list = CheckListCtrl(self.top_panel)

        horizontal_sizer.Add(self.variable_list, 1, wx.EXPAND | wx.ALL, 2)
        self.top_panel.SetSizer(horizontal_sizer)
        hbox_bottom_panel = wx.BoxSizer(wx.HORIZONTAL)
        vbox_bottom_panel = wx.BoxSizer(wx.VERTICAL)
        hbox_url = wx.BoxSizer(wx.HORIZONTAL)

        # build a list of columns for the list control
        self.list_ctrl_columns = ["File Name", "File Name", "Last Updated", "URL"]

        # insert columns to list control
        for i in range(len(self.list_ctrl_columns)):
            self.variable_list.InsertColumn(i, self.list_ctrl_columns[i])

        # self.variable_list.InsertColumn(0, "File Name")
        # self.variable_list.InsertColumn(1, "File Name")
        # self.variable_list.InsertColumn(2, "Last Updated")
        # self.variable_list.InsertColumn(3, "URL")

        self.url_textbox = wx.TextCtrl(parent=self.bottom_panel, value="http://129.123.51.203/opendap", size=(-1, 25))
        self.get_btn = wx.Button(parent=self.bottom_panel, label="Get Files", size=(-1, 27))
        self.download_btn = wx.Button(parent=self.bottom_panel, id=wx.ID_ANY, label="Download")
        self.view_btn = wx.Button(parent=self.bottom_panel, id=wx.ID_ANY, label="View")

        hbox_url.Add(self.url_textbox, 1, 0)
        hbox_url.Add(self.get_btn, 0, wx.ALL)
        vbox_bottom_panel.Add(hbox_url, 1, wx.EXPAND | wx.ALL, 2)

        hbox_bottom_panel.Add(self.download_btn, 1, wx.EXPAND | wx.ALL, 2)
        hbox_bottom_panel.Add(self.view_btn, 1, wx.EXPAND | wx.ALL, 2)

        vbox_bottom_panel.Add(hbox_bottom_panel, 1, wx.EXPAND | wx.ALL, 1)

        self.bottom_panel.SetSizer(vbox_bottom_panel)

        viewer_vbox = wx.BoxSizer(wx.VERTICAL)

        viewer_vbox.Add(self.top_panel, 1, wx.EXPAND | wx.ALL, 2)
        viewer_vbox.Add(self.bottom_panel, 0, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(viewer_vbox)

        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetStatusText("ready")
        self.Layout()
        self.Show()

    def alternateRowColor(self, color="#DCEBEE"):
        for i in range(self.variable_list.GetItemCount()):
            if i % 2 == 1:
                self.variable_list.SetItemBackgroundColour(i, color)
