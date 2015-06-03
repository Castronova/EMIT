__author__ = 'Mario'

from gui.controller.logicNavigationCanvas import *

# todo: refactor
from ..images import icons
from ..images import resourcesCanvasObjects as rco


class ViewCanvas(wx.Panel):
    """
        NavCanvas.py

        This is a high level window that encloses the FloatCanvas in a panel
        and adds a Navigation toolbar.

        """
    def __init__(self, parent, id=wx.ID_ANY, **kwargs): # The rest just get passed into FloatCanvas

        wx.Panel.__init__(self, parent, id, size=wx.Size(0,0))

        # Get the Canvas Objects Resources
        self.ModelsBox = rco.EMITModelDeepBlueReflected.GetBitmap()
        self.DatabaseBox = rco.EMITModelSilver.GetBitmap()
        self.TimeseriesBox = rco.EMITModelGold.GetBitmap()
        self.UnassignedBox1 = rco.EMITModelBlue.GetBitmap()
        self.UnassignedBox2 = rco.EMITModelDeepBlue.GetBitmap()
        self.UnassignedBox3 = rco.EMITModelGreen.GetBitmap()

        self.GuiMouse = GUIMouse()
        self.GuiZoomIn = GUIZoomIn()
        self.GuiZoomOut = GUIZoomOut()
        self.GuiMove = GUIMove()
        self.GuiLink = GUILink()
        # self.GuiRun = GUIRun()
        # self.GuiDelete = GUIDelete()


        self.Modes = [("Pointer",  self.GuiMouse,   icons.Cursor.GetBitmap()),
                      ("Zoom In",  self.GuiZoomIn,  icons.Zoom_In.GetBitmap()),
                      ("Zoom Out", self.GuiZoomOut, icons.Zoom_Out.GetBitmap()),
                      # ("Pan",      self.GuiMove,    icons.Move.GetBitmap())
                      # ("Add Link", self.GuiLink, icons.add_link.GetBitmap()),
                      # ("Run Model", self.GuiRun, icons.Run.GetBitmap()),
                      # ("Clear", self.GuiDelete, icons.Trash.GetBitmap())
                      ]

        # Create the vertical sizer for the toolbar and Panel
        box = wx.BoxSizer(wx.VERTICAL)

        self.FloatCanvas = FloatCanvas.FloatCanvas(self, **kwargs)
        box.Add(self.FloatCanvas, 1, wx.GROW)

        self.SetSizerAndFit(box)

    def ZoomToFit(self, event):
        self.FloatCanvas.ZoomToBB()
        self.FloatCanvas.SetFocus()  # Otherwise the focus stays on the Button, and wheel events are lost.

    # def BuildToolbar(self):
    #     """
    #     This is here so it can be over-ridden in a ssubclass, to add extra tools, etc
    #     """
    #     tb = wx.ToolBar(self)
    #     self.ToolBar = tb
    #     tb.SetToolBitmapSize((24,24))
    #     tb.Realize()

    # def AddToolbarModeButtons(self, tb, Modes):
    #     self.ModesDict = {}
    #     for Mode in Modes:
    #         tool = tb.AddRadioTool(wx.ID_ANY, shortHelp=Mode[0], bitmap=Mode[2])
    #         self.ModesDict[tool.GetId()]=Mode[1]

    # def AddToolbarZoomButton(self, tb):
    #     tb.AddSeparator()
    #
    #     self.ZoomButton = wx.Button(tb, label="Zoom To Fit")
    #     tb.AddControl(self.ZoomButton)
    #     self.ZoomButton.Bind(wx.EVT_BUTTON, self.ZoomToFit)

    # def AddToolbarZoomButtons(self, tb):
    #     tb.AddSeparator()
    #
    #     self.ZoomInButton = tb.AddSimpleTool(1, icons.Zoom_In.GetBitmap(), 'New', '')
    #     self.ZoomOutButton = tb.AddSimpleTool(2, icons.Zoom_Out.GetBitmap(), 'New', '')
    #
    #     self.Bind(wx.EVT_TOOL, self.ZoomIn, id=1)
    #     self.Bind(wx.EVT_TOOL, self.ZoomOut, id=2)

    # def HideShowHack(self):
    #     ##fixme: remove this when the bug is fixed!
    #     """
    #     Hack to hide and show button on toolbar to get around OS-X bug on
    #     wxPython2.8 on OS-X
    #     """
    #     self.ZoomButton.Hide()
    #     self.ZoomButton.Show()



        # def ZoomIn(self, Event):
        #     self.FloatCanvas.Zoom(1.1)

        # def ZoomOut(self, Event):
        #     self.FloatCanvas.Zoom(.9)
