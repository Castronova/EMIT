import wx
import wx.propgrid as wxpg


class NASViewer(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, id=-1, title=str("Netcdf file information"), pos=wx.DefaultPosition, size=(650, 700),
                          style = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        panel = wx.Panel(self)
        self.topPanel = wx.Panel(panel)


        #self.button = wx.Button(self.topPanel, id=wx.ID_ANY, label="Woot Woot")
        self.PropertyGrid = MyPropertyGrid(self.topPanel, id=wx.ID_ANY,
                                               pos=wx.Point(0, 0),
                                               # size=wx.Size(700,500))
                                               size=wx.Size(423, 319))
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.topPanel)
        panel.SetSizer(vbox)
        self.Show()



class MyPropertyGrid(wx.propgrid.PropertyGrid):
    def __init__(self, *args, **kwargs):
        wxpg.PropertyGrid.__init__(self, *args, **kwargs)
