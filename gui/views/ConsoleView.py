import wx
from wx import richtext


class ConsoleView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.log = wx.richtext.RichTextCtrl(self, -1, size=(100, 100),
                                            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL | wx.SIMPLE_BORDER | wx.CURSOR_NONE)

        # Add widgets to a sizer
        sizer = wx.BoxSizer()
        sizer.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)

        self.SetSizerAndFit(sizer)
