__author__ = 'Francisco'

import wx
app = wx.App()

frame = wx.Frame(None, -1)
frame.SetToolTip(wx.ToolTip("Hey there"))
frame.SetTitle("Title")
frame.SetSize(wx.Size(300,300))
frame.Show(True)
app.MainLoop()
