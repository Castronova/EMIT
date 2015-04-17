__author__ = 'tonycastronova'

import wx
from wx.lib.pubsub import pub as Publisher

class LogicFileDrop(wx.FileDropTarget):
    def __init__(self, canvas, FloatCanvas):
        wx.FileDropTarget.__init__(self)
        self.canvas = canvas
        self.FloatCanvas = FloatCanvas
        Publisher.subscribe(self.OnDropFiles, 'toolboxclick')

    # Enable these for debugging
    # def OnEnter(self, x, y, d):
    #     print "OnEnter: %d, %d, %d\n" % (x, y, d)
    #
    # def OnLeave(self):
    #     print "OnLeave"

    def RandomCoordinateGeneration(self, filepath):
        filenames = filepath
        x = 0
        y = 0

        self.OnDropFiles(x, y, filenames)

    def OnDropFiles(self, x, y, filenames):
        originx, originy = self.FloatCanvas.PixelToWorld((0, 0))

        x = x + originx
        y = originy - y

        self.canvas.addModel(filepath=filenames[0], x=x, y=y)

