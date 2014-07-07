from images import icons

__author__ = 'Mario'

import wx
import sys

sys.path.append("..")
from wx.lib.floatcanvas import Resources
from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.pubsub import pub as Publisher
from NavToolbar import NavCanvas
import os
import numpy as N
import textwrap as tw


from CanvasLogic import ConnectorLine, MovingBitmap

class TreeNode:
    dx = 15
    dy = 4
    def __init__(self, name, Children = []):
        self.Name = name
        self.Children = Children
        self.Point = None # The coords of the node.

    def __str__(self):
        return "TreeNode: %s"%self.Name
    __repr__ = __str__



class Canvas(NavCanvas):

    def __init__(self, *args, **kwargs):
        NavCanvas.__init__(self, *args,**kwargs)

        self.initSubscribers()
        self.models = {}


        self.UnBindAllMouseEvents()
        self.ZoomToFit(Event=None)
        self.MoveObject = None
        self.Moving = False

        #self.createLink()

        self.initBindings()


    def UnBindAllMouseEvents(self):
        ## Here is how you unbind FloatCanvas mouse events
        self.Canvas.Unbind(FC.EVT_LEFT_DOWN)
        self.Canvas.Unbind(FC.EVT_LEFT_UP)
        self.Canvas.Unbind(FC.EVT_LEFT_DCLICK)

        self.Canvas.Unbind(FC.EVT_MIDDLE_DOWN)
        self.Canvas.Unbind(FC.EVT_MIDDLE_UP)
        self.Canvas.Unbind(FC.EVT_MIDDLE_DCLICK)

        self.Canvas.Unbind(FC.EVT_RIGHT_DOWN)
        self.Canvas.Unbind(FC.EVT_RIGHT_UP)
        self.Canvas.Unbind(FC.EVT_RIGHT_DCLICK)

        self.EventsAreBound = False
    def initBindings(self):
        self.Canvas.Bind(FC.EVT_MOTION, self.OnMove )
        self.Canvas.Bind(FC.EVT_LEFT_UP, self.OnLeftUp )
        self.Canvas.Bind(FC.EVT_RIGHT_DOWN, self.onRightDown)
        self.Canvas.Bind(FC.EVT_LEFT_DOWN, self.onLeftDown)

    def initSubscribers(self):
        Publisher.subscribe(self.createBox, "createBox")

    def createBox(self, xCoord, yCoord, filepath=None):

        if filepath:
            w, h = 360, 240
            WH = (w/2, h/2)
            x,y = xCoord, yCoord
            FontSize = 14
            filename = os.path.basename(filepath)

            R = self.Canvas.AddRectangle((x,y), WH, LineWidth = 2, FillColor = "BLUE")
            R.HitFill = True
            R.ID = filename
            R.Name = filename
            wrappedtext = tw.wrap(unicode(filename), 15)
            print wrappedtext
            label = self.Canvas.AddText("\n".join(wrappedtext), (x+1, y+h/2),
                                        Color = "White",  Size = FontSize,
                                        Weight=wx.BOLD, Style=wx.ITALIC )
            R.Text = label
            print dir(label), label
            #R.Bind(FC.EVT_FC_LEFT_UP, self.OnLeftUp )
            R.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)

            self.models[filename]=R

            self.Canvas.Draw()

        else:
            print "Nothing Selected"

    def createLink(self):
        Bitmaps = []
        for Point in ((1,1), (-4,3)):
            Bitmaps.append(MovingBitmap(Resources.getMondrianImage(), Point, Height=1))

        Line = ConnectorLine(Bitmaps[0], Bitmaps[1], LineWidth=3, LineColor="Red")
        self.Canvas.AddObject(Line)

    def onLeftDown(self, event):
        print event.GetPosition(),
       # dxy = event.GetPosition() - self.StartPoint
        dxy = self.Canvas.PixelToWorld(event.GetPosition())
        print dxy

    def ObjectHit(self, object):
        if not self.Moving:
            self.Moving = True
            self.StartPoint = object.HitCoordsPixel

            BB = object.BoundingBox
            OutlinePoints = N.array(
            ( (BB[0, 0], BB[0, 1]), (BB[0, 0], BB[1, 1]), (BB[1, 0], BB[1, 1]), (BB[1, 0], BB[0, 1]),
            ))
            self.StartObject = self.Canvas.WorldToPixel(OutlinePoints)
            self.MoveObject = None
            self.MovingObject = object

    def OnMove(self, event):

        if self.Moving:
            dxy = event.GetPosition() - self.StartPoint
            # Draw the Moving Object:
            dc = wx.ClientDC(self.Canvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.MoveObject is not None:
                dc.DrawPolygon(self.MoveObject)
            self.MoveObject = self.StartObject + dxy
            dc.DrawPolygon(self.MoveObject)

    def OnLeftUp(self, event):
        if self.Moving:
            self.Moving = False
            if self.MoveObject is not None:
                dxy = event.GetPosition() - self.StartPoint
                (x,y) = self.Canvas.ScalePixelToWorld(dxy)
                self.MovingObject.Move((x,y))
                self.MovingObject.Text.Move((x, y))
            self.Canvas.Draw(True)

    def onRightDown(self, event):
        print "Right Click"
        self.Canvas.ClearAll()
        self.Canvas.Draw()


#class DrawFrame(wx.Frame):
class MyFrame2(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                        title = wx.EmptyString, pos = wx.DefaultPosition,
                        size = wx.Size( 900,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        draw = Canvas(self )
        '''
        canvas = NavCanvas.NavCanvas(id=wx.ID_ANY,parent=self,
                          ProjectionFun = None,
                          Debug = 0,
                          BackgroundColor = "White",
                          )
        '''

class Link:
    def __init__(self):
        pass


def SimpleFrame(parent):
    return MyFrame2(parent)
'''
app = wx.App(False)
frame = SimpleFrame(None)
frame.Show(True)

app.MainLoop()
'''

