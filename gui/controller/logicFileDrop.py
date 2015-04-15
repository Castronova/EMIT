__author__ = 'tonycastronova'

import wx
from wx.lib.pubsub import pub as Publisher

class LogicFileDrop(wx.FileDropTarget):
    def __init__(self, controller, FloatCanvas):
        wx.FileDropTarget.__init__(self)
        self.controller = controller
        self.FloatCanvas = FloatCanvas
        Publisher.subscribe(self.OnDropFiles, 'toolboxclick')


    def RandomCoordinateGeneration(self, filepath):
        filenames = filepath
        x = 0
        y = 0

        self.OnDropFiles(x, y, filenames)

    def OnDropFiles(self, x, y, filenames):
        originx, originy = self.FloatCanvas.PixelToWorld((0, 0))

        x = x + originx
        y = originy - y

        self.controller.addModel(filepath=filenames[0], x=x, y=y)

