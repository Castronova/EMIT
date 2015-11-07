__author__ = 'francisco'

import wx

class NetcdfViewer(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, id=wx.ID_ANY, title="Netcdf Viewer", pos=wx.DefaultPosition,
                          size=(400, 500), style=wx.DEFAULT_FRAME_STYLE)
        self.parent = parent

        panel = wx.Panel(self)
        self.top_panel = wx.Panel(panel)
        self.bottom_panel = wx.Panel(panel, size=(-1, 100))
        self.bottom_panel.SetBackgroundColour("#AABBCC")

        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.tree_ctrl = wx.TreeCtrl(parent=self.top_panel)
        horizontal_sizer.Add(self.tree_ctrl, 1, wx.EXPAND | wx.ALL, 2)
        self.top_panel.SetSizer(horizontal_sizer)
        hbox_bottom_panel = wx.BoxSizer(wx.HORIZONTAL)
        vbox_bottom_panel = wx.BoxSizer(wx.VERTICAL)


        url_textbox = wx.TextCtrl(parent=self.bottom_panel, id=wx.ID_ANY, value="https://url.example")
        download_btn = wx.Button(parent=self.bottom_panel, id=wx.ID_ANY, label="Download")
        add_to_canvas_btn = wx.Button(parent=self.bottom_panel, id=wx.ID_ANY, label="Add To Canvas")

        vbox_bottom_panel.Add(url_textbox, 1, wx.EXPAND | wx.ALL, 2)

        hbox_bottom_panel.Add(download_btn, 1, wx.EXPAND | wx.ALL, 2)
        hbox_bottom_panel.Add(add_to_canvas_btn, 1, wx.EXPAND | wx.ALL, 2)

        vbox_bottom_panel.Add(hbox_bottom_panel, 1, wx.EXPAND | wx.ALL, 2)

        #  This panel has a vertical and a horitzonal box sizer.
        #  The vertical makes it so the text box and buttons are stacked
        #  While the horizontal only affects the button.

        self.bottom_panel.SetSizer(vbox_bottom_panel)

        viewer_vbox = wx.BoxSizer(wx.VERTICAL)

        viewer_vbox.Add(self.top_panel, 1, wx.EXPAND | wx.ALL, 2)
        viewer_vbox.Add(self.bottom_panel, 0, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(viewer_vbox)
        self.Show()






