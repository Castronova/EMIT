#!/usr/bin/env python2
import sys

__author__ = 'Mario'


import os

import wx
import wx.xrc
import wx.aui

import gui.log as log
from coordinator import main as cmd
from gui.mainGui import MainGui, wxStdOut
from gui.CanvasController import CanvasController
import logging
import threading

#sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../../odm2/src')))


# ##########################################################################
# # Class MainFrame
# ##########################################################################
class MyApp(wx.App):
    def OnInit(self):

        # create and instance of the coordinator engine
        self.cmd = cmd.Coordinator()

        # connect to databases and set default
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir,'./data/connections'))

        # We are terminating dependency logging errors, We may want this in the future but it
        # tends to add clutter to our console.
        wx.Log.SetLogLevel(0)

        self.frame = MainGui(None,self.cmd)
        self.frame.Show(True)
        #self.frame2 = non_blocking_gui.Frame()
        #self.frame2.Show()

        CanvasController(self.cmd, self.frame)

        self.cmd.connect_to_db([connections_txt])
        if not self.cmd.get_default_db():
            self.cmd.set_default_database()

        self.frame.Center()
        return True

class SysOutListener:
    def write(self, string):
        #sys.__stdout__.write(string)
        evt = wxStdOut(text=string)
        wx.PostEvent(wx.GetApp().frame.output, evt)


if __name__ == '__main__':

    app = MyApp()
    sys.stdout = SysOutListener()
    app.MainLoop()




