import unittest

from gui import CanvasController
from gui.mainGui import MainGui
from coordinator import main as cmd


__author__ = 'mario'

import wx

from wx.lib.floatcanvas.FloatCanvas import EVT_FC_LEFT_DOWN

myNewEvent, EVT_DEMO_EVENT = wx.lib.newevent.NewEvent()

class testCanvasController(unittest.TestCase):

    def setUp(self):
        self.app = wx.App()
        self.cmd = cmd.Coordinator()
        self.assertIsNotNone(self.cmd)
        self.mainGui = MainGui(None, self.cmd)
        self.assertIsNotNone(self.mainGui)
        self.canvasController = CanvasController(self.cmd, self.mainGui.Canvas)
        self.assertIsNotNone(self.canvasController)
        self.floatCanvas = self.canvasController.Canvas
        self.assertIsNotNone(self.floatCanvas)

    def test_ArrowClicked(self):
        ## make a box to use for testing
        id = -1
        self.canvasController.createBox(0, 0, id=id , name='testBox')

        ## Get box
        box = self.canvasController.models.popitem()[0]

        ## Bind box
        box.Bind(EVT_FC_LEFT_DOWN, self.canvasController.ArrowClicked)

        ## have fun with box
        evt = wx.PyCommandEvent(EVT_FC_LEFT_DOWN)
        self.floatCanvas.GetEventHandler().ProcessEvent(evt)


