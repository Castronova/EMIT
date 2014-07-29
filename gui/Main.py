#!/usr/bin/env python2

__author__ = 'Mario'

import os

import wx
import wx.xrc
import wx.aui

from CanvasView import Canvas
from DirectoryView import DirectoryCtrlView

import coordinator.main as cmd
from mainGui import  MainGui
from CanvasController import CanvasController
from CanvasView import Canvas

from os.path import *
import sys


# ##########################################################################
# # Class MainFrame
# ##########################################################################

if __name__ == '__main__':

    # create and instance of the coordinator engine
    cmd = cmd.Coordinator()

    # connect to databases and set default
    currentdir = dirname(abspath(__file__))
    connections_txt = abspath(join(currentdir,'../data/connections'))
    cmd.connect_to_db([connections_txt])
    cmd.set_default_database()




    wx.Log.SetLogLevel(0)
    app = wx.App(False)
    frame = MainGui(None)
    frame.Show(True)

    CanvasController(cmd, frame.Canvas)

    app.MainLoop()
