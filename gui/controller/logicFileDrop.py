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

        # Enable these for debugging
    """
    def OnEnter(self, x, y, d):
        print "OnEnter: %d, %d, %d\n" % (x, y, d)

    def OnLeave(self):
        print "OnLeave"
    """

    def OnDropFiles(self, x, y, filenames):
        name, ext = os.path.splitext(filenames[0])

        if ext == '.mdl' or ext == '.sim':
            originx, originy = self.FloatCanvas.WorldToPixel(self.canvas.GetPosition())
            nx = (x - originx)
            ny = (originy - y)
            self.canvas.addModel(filepath=filenames[0], x=nx, y=ny)

class filepath(object):

    def __init__(self):
        self.filepath = None
        Publisher.subscribe(self.SetFilepath, 'dragpathsent')

    def SetFilepath(self, path):
        self.filepath=path

    def GetFilepath(self):
        return self.filepath

    def DeleteFilepath(self):
        self.filepath = None
