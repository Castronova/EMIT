__author__ = 'Mario'

import sys
import wx
import wx.xrc
import wx.aui
from gui.controller.logicEMIT import LogicEMIT
from coordinator import engineManager



class EMITApp(wx.App):
    def OnInit(self):
        # Don't delete this line, instantiating the Borg Engine main thread here
        engine = engineManager.Engine()

        # We are terminating dependency logging errors, We may want this in the future but it
        # tends to add clutter to our console.
        wx.Log.SetLogLevel(0)

        self.logicEmit = LogicEMIT(None)

        return True

class SysOutListener:
    def write(self, string):
        try:
            sys.__stdout__.write(string)
            evt = wxStdOut(text=string)
            wx.PostEvent(wx.GetApp().frame.output, evt)
        except:
            pass

if __name__ == '__main__':
    app = EMITApp()
    app.MainLoop()




