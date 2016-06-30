import wx
import wx.propgrid as wxpg


class SettingsView(wx.Frame):

    def __init__(self, parent):
        self.window_width = 350
        self.window_height = 400
        wx.Frame.__init__(self, parent=parent, id=-1, title="Settings", pos=wx.DefaultPosition,
                          size=wx.Size(self.window_width, self.window_height),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.panel = wx.Panel(self)

        # Define widgets
        # slightly less than the window width, # make room for buttons at bottom
        self.settings = wxpg.PropertyGrid(self.panel, id=wx.ID_ANY, pos=wx.Point(0, 0),
                                          size=wx.Size(self.window_width - 25, self.window_height - 75),
                                          style=wxpg.PG_SPLITTER_AUTO_CENTER)

        self.saveButton = wx.Button(self.panel, 1, 'Save')

        # Setup widget sizers
        vsizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.settings, 0, flag=wx.CENTER | wx.ALL, border=10)
        vsizer.Add(hsizer, 0, wx.CENTER)
        vsizer.Add(self.saveButton, 0, flag=wx.RIGHT | wx.ALIGN_RIGHT, border=20)
        self.panel.SetSizer(vsizer)

        self.Show()


