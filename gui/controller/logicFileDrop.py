__author__ = 'tonycastronova'

import os

import wx
from wx.lib.pubsub import pub as Publisher


class LogicFileDrop(wx.FileDropTarget):
    def __init__(self, canvas, FloatCanvas):
        wx.FileDropTarget.__init__(self)
        self.canvas = canvas
        self.FloatCanvas = FloatCanvas
        Publisher.subscribe(self.OnDropFiles, 'toolboxclick')

    def OnDropFiles(self, x, y, filenames):
        name, ext = os.path.splitext(filenames[0])

        if ext == '.mdl' or ext == '.sim':
            originx, originy = self.FloatCanvas.WorldToPixel(self.canvas.GetPosition())
            nx = (x - originx)
            ny = (originy - y)
            self.canvas.addModel(filepath=filenames[0], x=nx, y=ny)


