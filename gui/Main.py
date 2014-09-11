#!/usr/bin/env python2

__author__ = 'Mario'


import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),'../../../odm2/src')))

import wx
import wx.xrc
import wx.aui

import log
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

    # setup logger
    logger = log.setup_custom_logger('root')

    # create and instance of the coordinator engine
    cmd = cmd.Coordinator()


    # connect to databases and set default
    currentdir = os.path.dirname(os.path.abspath(__file__))
    connections_txt = os.path.abspath(os.path.join(currentdir,'../data/connections'))

    cmd.connect_to_db([connections_txt])
    cmd.set_default_database()




    wx.Log.SetLogLevel(0)
    app = wx.App(False)
    frame = MainGui(None,cmd)
    frame.Show(True)

    CanvasController(cmd, frame.Canvas)

    app.MainLoop()
