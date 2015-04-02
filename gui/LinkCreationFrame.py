__author__ = 'HarperMain'

import wx, wx.xrc
from pnlCreateLink import pnlCreateLink as PCL

class LinkCreationFrame(wx.Frame):

    def __init__(self, parent, from_model, to_model, inputitems, outputitems, cmd):

        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition,
                          size = wx.Size( 550,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.cmd = cmd
        from_model_name = from_model.get_name()
        to_model_name = to_model.get_name()
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        LinkFrameSizer = wx.BoxSizer( wx.VERTICAL )

        self.LinksPanel = PCL(self, from_model_name, to_model_name, inputitems, outputitems)
        LinkFrameSizer.Add( self.LinksPanel, 1, wx.EXPAND |wx.ALL, 5 )
