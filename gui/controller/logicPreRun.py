__author__ = 'Francisco'

import wx
from gui.views.viewPreRun import viewPreRun

class logicPreRun(viewPreRun):
    def __init__(self, parent):

        self.parent = ""
        self.logic = ""
        self.page1 = ""

        self.logic = viewPreRun.__init__(self)
        self.parent = parent
        self.initBinding()

    def initBinding(self):
        self.page1.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.page1.runButton.Bind(wx.EVT_BUTTON, self.OnRun)

    def OnCancel(self, event):
        frame = self.GetTopLevelParent()
        frame.Close(True)

    def OnRun(self, event):
        print "Run me"
