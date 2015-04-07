#!/usr/bin/env python2
from gui.controller.logicEMIT import LogicEMIT

__author__ = 'Mario'


import os
import sys
import wx
import wx.xrc
import wx.aui

from coordinator import main as cmd

#sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../../odm2/src')))

# todo: refactor
from gui.mainGui import wxStdOut


# ##########################################################################
# # Class MainFrame
# ##########################################################################

class EMITApp(wx.App):
    def OnInit(self):

        # create and instance of the coordinator engine
        self.cmd = cmd.Coordinator()

        # connect to databases and set default
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir,'./data/connections'))

        # We are terminating dependency logging errors, We may want this in the future but it
        # tends to add clutter to our console.
        wx.Log.SetLogLevel(0)

        # self.frame = MainGui(None,self.cmd)
        # self.frame.Show(True)
        # # sys.stdout = SysOutListener()
        #
        # #self.frame2 = non_blocking_gui.Frame()
        # #self.frame2.Show()
        #
        # CanvasController(self.cmd, self.frame)

        parent = None

        # self.logicEmit = LogicEMIT(parent, self.cmd)
        self.cmd.connect_to_db([connections_txt])
        if not self.cmd.get_default_db():
            self.cmd.set_default_database()

        self.logicEmit = LogicEMIT(None, self.cmd)


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




