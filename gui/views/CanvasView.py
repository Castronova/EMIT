__author__ = 'Mario'

from gui.controller.NavigationCanvasCtrl import *
from wx.lib.floatcanvas import FloatCanvas
import os
import environment
from gui.Resources import icons

class CanvasView(wx.Panel):
    """
        NavCanvas.py

        This is a high level window that encloses the FloatCanvas in a panel
        and adds a Navigation toolbar.

        """
    def __init__(self, parent, id=wx.ID_ANY, **kwargs): # The rest just get passed into FloatCanvas

        wx.Panel.__init__(self, parent, id, size=wx.Size(0,0))

        self.GuiMouse = GUIMouse()
        self.GuiZoomIn = GUIZoomIn()
        self.GuiZoomOut = GUIZoomOut()
        self.GuiMove = GUIMove()
        self.GuiLink = GUILink()


        self.Modes = [("Pointer",  self.GuiMouse,   icons.Cursor.GetBitmap()),
                      ("Zoom In",  self.GuiZoomIn,  icons.Zoom_In.GetBitmap()),
                      ("Zoom Out", self.GuiZoomOut, icons.Zoom_Out.GetBitmap()),
                      ]

        # Create the vertical sizer for the toolbar and Panel
        box = wx.BoxSizer(wx.VERTICAL)

        self.FloatCanvas = FloatCanvas.FloatCanvas(self, **kwargs)
        box.Add(self.FloatCanvas, 1, wx.GROW)

        self.SetSizerAndFit(box)

    def ZoomToFit(self, event):
        self.FloatCanvas.ZoomToBB()
        self.FloatCanvas.SetFocus()  # Otherwise the focus stays on the Button, and wheel events are lost.
