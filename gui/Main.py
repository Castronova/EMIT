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

    #canvas = Canvas(parent=self.pnlDocking, ProjectionFun=None, Debug=0, BackgroundColor="White", )

    app = wx.App(False)
    frame = MainGui(None)
    canvas = Canvas(frame)
    frame.initCanvas(canvas)
    frame.initAUIManager()
    frame.Show(True)

    CanvasController(cmd, canvas)


    app.MainLoop()
