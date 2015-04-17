#!/usr/bin/env python2



__author__ = 'Mario'

import os
import sys
import wx
import wx.xrc
import wx.aui

from gui.controller.logicEMIT import LogicEMIT
import coordinator.engineAccessors as engine


# todo: refactor
# from gui.mainGui import wxStdOut


# ##########################################################################
# # Class MainFrame
# ##########################################################################

class EMITApp(wx.App):
    def OnInit(self):

        # get the shared instance of the coordinator engine
        # engine = engineManager.get_engine()

        # connections = engine.getDbConnections()

        # connect to databases and set default
        #currentdir = os.path.dirname(os.path.abspath(__file__))
        #connections_txt = os.path.abspath(os.path.join(currentdir,'./data/connections'))

        # We are terminating dependency logging errors, We may want this in the future but it
        # tends to add clutter to our console.
        wx.Log.SetLogLevel(0)

        # engine.connect_to_db([connections_txt])
        # if not engine.get_default_db():
        #     engine.set_default_database()

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




