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

# ##########################################################################
# # Class MainFrame
# ##########################################################################

if __name__ == '__main__':

    # create and instance of the coordinator engine
    cmd = cmd.Coordinator()

    app = wx.App(False)
    frame = MainGui(None)
    frame.Show(True)

    CanvasController(cmd, frame.Canvas)

    app.MainLoop()
