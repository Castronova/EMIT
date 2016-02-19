import wx
from gui.controller.PlotForSiteViewerCtrl import PlotForSiteViewerCtrl


class SpatialView(wx.Frame):

    def __init__(self, parent=None):

        wx.Frame.__init__(self, parent=parent, size=(650, 700))

        panel = wx.Panel(self)

        self.plot = PlotForSiteViewerCtrl(panel)

        self.Show()


