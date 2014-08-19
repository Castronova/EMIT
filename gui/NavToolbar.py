__author__ = 'Mario'
"""
A Panel that includes the FloatCanvas and Navigation controls

"""

import wx
from wx.lib.floatcanvas import FloatCanvas
from images import icons
import GUIControl as GUIMode
from wx.lib.pubsub import pub as Publisher

class NavCanvas(wx.Panel):
    """
    NavCanvas.py

    This is a high level window that encloses the FloatCanvas in a panel
    and adds a Navigation toolbar.

    """

    def __init__(self,
                 parent,
                 id = wx.ID_ANY,
                 size = wx.DefaultSize,
                 **kwargs): # The rest just get passed into FloatCanvas
        wx.Panel.__init__(self, parent, id, size=size)

        self.GuiMouse = GUIMode.GUIMouse()
        self.GuiZoomIn = GUIMode.GUIZoomIn()
        self.GuiZoomOut = GUIMode.GUIZoomOut()
        self.GuiMove = GUIMode.GUIMove()
        self.GuiRun = GUIMode.GUIRun()
        self.GuiLink = GUIMode.GUILink()
        self.GuiDelete = GUIMode.GUIDelete()


        self.Modes = [("Pointer",  self.GuiMouse,   icons.Cursor.GetBitmap()),
                      ("Zoom In",  self.GuiZoomIn,  icons.Zoom_In.GetBitmap()),
                      ("Zoom Out", self.GuiZoomOut, icons.Zoom_Out.GetBitmap()),
                      ("Pan",      self.GuiMove,    icons.Move.GetBitmap()),
                      # ("Add Link", self.GuiLink, icons.add_link.GetBitmap()),
                      ("Run Model", self.GuiRun, icons.Run.GetBitmap()),
                      ("Clear", self.GuiDelete, icons.Trash.GetBitmap())
        ]
        self.BuildToolbar()
        ## Create the vertical sizer for the toolbar and Panel
        box = wx.BoxSizer(wx.VERTICAL)
        box.Add(self.ToolBar, 0, wx.ALL | wx.ALIGN_LEFT | wx.GROW, 4)

        self.Canvas = FloatCanvas.FloatCanvas(self, **kwargs)
        box.Add(self.Canvas, 1, wx.GROW)

        # self.output = wx.TextCtrl(self, -1, size=(100,100), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        # box.Add(self.output, 0, wx.GROW)

        self.SetSizerAndFit(box)

        # default to first mode
        #self.ToolBar.ToggleTool(self.PointerTool.GetId(), True)
        self.Canvas.SetMode(self.Modes[0][1])

    def BuildToolbar(self):
        """
        This is here so it can be over-ridden in a ssubclass, to add extra tools, etc
        """
        tb = wx.ToolBar(self)
        self.ToolBar = tb
        tb.SetToolBitmapSize((24,24))
        self.AddToolbarModeButtons(tb, self.Modes)
        #self.AddToolbarZoomButton(tb)
        tb.Realize()
        ## fixme: remove this when the bug is fixed!
        #wx.CallAfter(self.HideShowHack) # this required on wxPython 2.8.3 on OS-X

    def AddToolbarModeButtons(self, tb, Modes):
        self.ModesDict = {}
        for Mode in Modes:
            tool = tb.AddRadioTool(wx.ID_ANY, shortHelp=Mode[0], bitmap=Mode[2])
            self.Bind(wx.EVT_TOOL, self.SetMode, tool)
            # self.Bind(wx.EVT_TOOL, self.SetClear, tool)
            self.ModesDict[tool.GetId()]=Mode[1]
            #self.ZoomOutTool = tb.AddRadioTool(wx.ID_ANY, bitmap=Resources.getMagMinusBitmap(), shortHelp = "Zoom Out")
            #self.Bind(wx.EVT_TOOL, lambda evt : self.SetMode(Mode=self.GUIZoomOut), self.ZoomOutTool)

    def AddToolbarZoomButton(self, tb):
        tb.AddSeparator()

        self.ZoomButton = wx.Button(tb, label="Zoom To Fit")
        tb.AddControl(self.ZoomButton)
        self.ZoomButton.Bind(wx.EVT_BUTTON, self.ZoomToFit)


    def HideShowHack(self):
        ##fixme: remove this when the bug is fixed!
        """
        Hack to hide and show button on toolbar to get around OS-X bug on
        wxPython2.8 on OS-X
        """
        self.ZoomButton.Hide()
        self.ZoomButton.Show()

    def SetRun(self, event):
        Publisher.sendMessage("run")


    def SetMode(self, event):
        Mode = self.ModesDict[event.GetId()]

        if Mode == self.GuiRun:
            Publisher.sendMessage("run")

        if Mode == self.GuiDelete:
            Publisher.sendMessage("clear")

    def ZoomToFit(self,Event):
        self.Canvas.ZoomToBB()
        self.Canvas.SetFocus() # Otherwise the focus stays on the Button, and wheel events are lost.

