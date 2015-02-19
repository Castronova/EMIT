__author__ = 'tonycastronova'

import wx
import time

ID_COUNT = wx.NewId()

#-----------------------------------------------------------------------------#

class CountingFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Lets Count", size=(300, 300))

        # Attributes

        # Layout
        self.__DoLayout()
        self.CreateStatusBar()

        # Event Handlers

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(CountingPanel(self), 1, wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        self.SetMinSize((300, 300))

#-----------------------------------------------------------------------------#

class CountingPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Attributes
        self._counter = wx.StaticText(self, label="0")
        self._counter.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL))

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.Bind(wx.EVT_BUTTON, self.OnButton)

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        button = wx.Button(self, ID_COUNT, "Increment Counter")
        sizer.AddMany([(button, 0, wx.ALIGN_CENTER),
                       ((15, 15), 0),
                       (self._counter, 0, wx.ALIGN_CENTER)])
        self.SetSizer(sizer)

    def OnButton(self, evt):
        # This thread is fairly lazy by itself so it takes it
        # 10 seconds to figure out what the next value is.
        time.sleep(10)
        val = int(self._counter.GetLabel()) + 1
        self._counter.SetLabel(unicode(val))

#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    APP = wx.App(False)
    FRAME = CountingFrame(None)
    FRAME.Show()
    APP.MainLoop()