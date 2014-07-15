
__author__ = 'Mario'

import wx
import random
import math
#from GUIControl import GUIBase

ver = 'local'

import sys

sys.path.append("..")
from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.floatcanvas.Utilities import BBox
from wx.lib.pubsub import pub as Publisher
import numpy as N
import os


class CanvasController:
    def __init__(self, cmd, Canvas):
        self.Canvas = Canvas
        self.cmd = cmd
        self.initBindings()
        self.Moving = False
        #self.initSubscribers()
                ## Drag and drop
        dt = FileDrop(self.Canvas, self.cmd)
        self.Canvas.SetDropTarget(dt)

        self.selected = []
        self.links = []


    def initBindings(self):
        self.Canvas.Bind(FC.EVT_MOTION, self.OnMove)
        self.Canvas.Bind(FC.EVT_LEFT_UP, self.OnLeftUp)
    '''
    def initSubscribers(self):
        Publisher.subscribe(self.createBox, "createBox")

    def createBox(self, filepath):
        ## Build a box with a filepath
        print "I LIVE: ", filepath
    '''
    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        and moves the object it is clicked on

        """
        # self.SetStatusText("%.4f, %.4f"%tuple(event.Coords))

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
                dxy = self.Canvas.ScalePixelToWorld(dxy)
                self.MovingObject.Move(dxy)
            self.Canvas.Draw(True)

    def OnLeftDown(self, event):
        obj = event.GetEventObject()
        #print 'left down in GUILINK event! '#, dir(event)

        EventType = FC.EVT_FC_LEFT_DOWN
        obj = self.GetHitObject(event, EventType)
        print "self.Canvas.Hittest exists? ", obj.Name
        if obj:

            '''
            while 1:
                x1,y1  = (obj.BoundingBox[0] + (obj.wh[0]/2, obj.wh[1]/2))

                x2,y2 = self.Canvas.PixelToWorld(event.GetPosition())
                length = (((x2 - x1)**2)+(y2 - y1)**2)**.5
                dy = abs(y2 - y1)
                dx = abs(x2 - x1)
                angle = math.atan(dx/dy) *180/math.pi

                self.Canvas.AddArrow((x1,y1), length, angle ,LineWidth = 5, LineColor = "Black", ArrowHeadAngle = 50)
                self.Canvas.Refresh()
                self.Canvas.Draw()

            '''
            self.selected.append(obj)
            if len(self.selected) == 2:
                self.CreateLine(self.selected[0], self.selected[1])
                self.selected = []

        #if not self.Canvas.HitTest(event, EventType):
        #    self.Canvas._RaiseMouseEvent(event, EventType)
        #else:
        #    print "Selected an object"

    def GetHitObject(self, event, HitEvent):
        if self.Canvas.HitDict:
            # check if there are any objects in the dict for this event
            if self.Canvas.HitDict[ HitEvent ]:
                xy = event.GetPosition()
                color = self.Canvas.GetHitTestColor( xy )
                if color in self.Canvas.HitDict[ HitEvent ]:
                    Object = self.Canvas.HitDict[ HitEvent ][color]
                    #self.Canvas._CallHitCallback(Object, xy, HitEvent)
                    return Object
            return False

    def CreateLine(self, R1, R2):
        print "creating link", R1, R2
        x1,y1  = (R1.BoundingBox[0] + (R1.wh[0]/2, R1.wh[1]/2))
        x2,y2  = (R2.BoundingBox[0] + (R2.wh[0]/2, R2.wh[1]/2))
        #length = (((x2 - x1)**2)+(y2 - y1)**2)**.5
        #dy = abs(y2 - y1)
        #dx = abs(x2 - x1)
        #angle = math.atan2(dx,dy) *180/math.pi

        length = (((x2 - x1)**2)+(y2 - y1)**2)**.5
        dy = (y2 - y1)
        dx = (x2 - x1)
        angle = 90- math.atan2(dy,dx) *180/math.pi

        print 'angle: ',angle


        #self.Canvas.AddArrow((x1,y1), length, angle ,LineWidth = 5, LineColor = "Black", ArrowHeadAngle = 50)#, end = 'ARROW_POSITION_MIDDLE')
        self.Canvas.AddArrow((x1,y1), length/2, angle ,LineWidth = 2, LineColor = "Black", ArrowHeadSize = 10, ArrowHeadAngle = 50)#, end = 'ARROW_POSITION_MIDDLE')
        xm = x1 + dx/2
        ym = y1 + dy/2
        self.Canvas.AddArrow((xm,ym), length/2, angle ,LineWidth = 2, LineColor = "Black", ArrowHeadSize = 10, ArrowHeadAngle = 50)#, end = 'ARROW_POSITION_MIDDLE')

        g = self.Canvas._DrawList
        g.insert(0, g.pop())
        g.insert(0, g.pop())
        self.Canvas._DrawList = g


        # save links
        self.links.append([R1,R2])

        self.Canvas.Draw()

class MovingObjectMixin:
    """
    Methods required for a Moving object

    """
    def GetOutlinePoints(self):
        """
        Returns a set of points with which to draw the outline when moving the
        object.

        Points are a NX2 array of (x,y) points in World coordinates.


        """
        BB = self.BoundingBox
        OutlinePoints = N.array(
            ( (BB[0, 0], BB[0, 1]), (BB[0, 0], BB[1, 1]), (BB[1, 0], BB[1, 1]), (BB[1, 0], BB[0, 1]),
            ))

        return OutlinePoints

class ConnectorObjectMixin:
    """
    Mixin class for DrawObjects that can be connected with lines

    Note that this version only works for Objects that have an "XY" attribute:
      that is, one that is derived from XHObjectMixin.

    """

    def GetConnectPoint(self):
        return self.XY


class MovingBitmap(FC.ScaledBitmap, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    # # All we need to do is is inherit from:
    # #  ScaledBitmap, MovingObjectMixin and ConnectorObjectMixin
    pass


class MovingCircle(FC.Circle, MovingObjectMixin, ConnectorObjectMixin):
    """
    ScaledBitmap Object that can be moved
    """
    # # All we need to do is is inherit from:
    # #  Circle MovingObjectMixin and ConnectorObjectMixin
    pass


class MovingGroup(FC.Group, MovingObjectMixin, ConnectorObjectMixin):
    def GetConnectPoint(self):
        return self.BoundingBox.Center

    def CalcBoundingBox(self):
        self.BoundingBox = BBox.fromPoints((self.Object1.GetConnectPoint(), self.Object2.GetConnectPoint()))
        if self._Canvas:
            self._Canvas.BoundingBoxDirty = True


    def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Points = N.array((self.Object1.GetConnectPoint(), self.Object2.GetConnectPoint()))
        Points = WorldToPixel(Points)
        dc.SetPen(self.Pen)
        dc.DrawLines(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.DrawLines(Points)


class TriangleShape1(FC.Polygon, MovingObjectMixin):
    def __init__(self, XY, L):
        """
        An equilateral triangle object
        XY is the middle of the triangle
        L is the length of one side of the Triangle
        """

        XY = N.asarray(XY)
        XY.shape = (2,)

        Points = self.CompPoints(XY, L)

        FC.Polygon.__init__(self, Points, LineColor="Black", LineStyle="Solid", LineWidth=2, FillColor="Red",
                            FillStyle="Solid")

    # # Override the default OutlinePoints
    #def GetOutlinePoints(self):
        #return self.Points

    def CompPoints(self, XY, L):
        c = L / N.sqrt(3)

        Points = N.array(((0, c), ( L / 2.0, -c / 2.0), (-L / 2.0, -c / 2.0)), N.float_)

        Points += XY
        return Points

class FileDrop(wx.FileDropTarget):
    def __init__(self, window, cmd):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.cmd = cmd

    def OnDropFiles(self, x, y, filenames):
        print "filename: {2} x: {0} y: {1}".format(x,y, filenames)

        #Canvas = NC.NavCanvas(self, -1, size=wx.DefaultSize).Canvas
        #Canvas.AddRectangle((110, 10), (100, 100), FillColor='Red')
        print x,y
        originx, originy = self.window.Canvas.PixelToWorld((0,0))
        #ar = self.window.Canvas.ScreenPosition
        #x-= ar[0]
        x = x +originx
        y = originy - y
        #x, y = self.window.Canvas.WorldToPixel((nx,ny))
        #print x,y
        #x = y = 0


        # make sure the correct file type was dragged
        name, ext = os.path.splitext(filenames[0])
        if ext == '.mdl' or ext =='.sim':

            models = None
            try:
                if ext == '.mdl':
                    # load the model (returns model instance
                    models = [self.cmd.add_model(filenames[0])]

                else:
                    # load the simulation
                    models, links = self.cmd.load_simulation(filenames[0])

                # draw boxes for each model
                offset = 0
                for model in list(models):
                    # get the name and id of the model
                    name = model.get_name()
                    modelid = model.get_id()

                    newx = random.randrange(-1,2)*offset + x
                    newy = random.randrange(-1,2)*offset + y

                    self.window.createBox(name=name, id=modelid, xCoord=newx, yCoord=newy)
                    self.window.Canvas.Draw()
                    offset=200
            except Exception, e:
                print 'Could not load the model :(. Hopefully this exception helps...'
                print e

        else:
            print 'I do not recognize this file type :('


class GUILink():

    def __init__(self, Canvas=None):
        self.__init__(self, Canvas)
        self.Canvas = Canvas
        self.selected = []
        self.links = []

    def GetHitObject(self, event, HitEvent):
        if self.Canvas.HitDict:
            # check if there are any objects in the dict for this event
            if self.Canvas.HitDict[ HitEvent ]:
                xy = event.GetPosition()
                color = self.Canvas.GetHitTestColor( xy )
                if color in self.Canvas.HitDict[ HitEvent ]:
                    Object = self.Canvas.HitDict[ HitEvent ][color]
                    #self.Canvas._CallHitCallback(Object, xy, HitEvent)
                    return Object
            return False

    def ObjectHit(self, event):
        #print "Hit Object in Link Mode", dir(event)
        pass

    def OnLeftDown(self, event):
        obj = event.GetEventObject()
        #print 'left down in GUILINK event! '#, dir(event)

        EventType = FC.EVT_FC_LEFT_DOWN
        obj = self.GetHitObject(event, EventType)
        print "self.Canvas.Hittest exists? ", obj.Name
        if obj:

            '''
            while 1:
                x1,y1  = (obj.BoundingBox[0] + (obj.wh[0]/2, obj.wh[1]/2))

                x2,y2 = self.Canvas.PixelToWorld(event.GetPosition())
                length = (((x2 - x1)**2)+(y2 - y1)**2)**.5
                dy = abs(y2 - y1)
                dx = abs(x2 - x1)
                angle = math.atan(dx/dy) *180/math.pi

                self.Canvas.AddArrow((x1,y1), length, angle ,LineWidth = 5, LineColor = "Black", ArrowHeadAngle = 50)
                self.Canvas.Refresh()
                self.Canvas.Draw()

            '''
            self.selected.append(obj)
            if len(self.selected) == 2:
                self.CreateLine(self.selected[0], self.selected[1])
                self.selected = []

        #if not self.Canvas.HitTest(event, EventType):
        #    self.Canvas._RaiseMouseEvent(event, EventType)
        #else:
        #    print "Selected an object"

    def CreateLine(self, R1, R2):
        print "creating link", R1, R2
        x1,y1  = (R1.BoundingBox[0] + (R1.wh[0]/2, R1.wh[1]/2))
        x2,y2  = (R2.BoundingBox[0] + (R2.wh[0]/2, R2.wh[1]/2))
        #length = (((x2 - x1)**2)+(y2 - y1)**2)**.5
        #dy = abs(y2 - y1)
        #dx = abs(x2 - x1)
        #angle = math.atan2(dx,dy) *180/math.pi

        length = (((x2 - x1)**2)+(y2 - y1)**2)**.5
        dy = (y2 - y1)
        dx = (x2 - x1)
        angle = 90- math.atan2(dy,dx) *180/math.pi

        print 'angle: ',angle


        #self.Canvas.AddArrow((x1,y1), length, angle ,LineWidth = 5, LineColor = "Black", ArrowHeadAngle = 50)#, end = 'ARROW_POSITION_MIDDLE')
        self.Canvas.AddArrow((x1,y1), length/2, angle ,LineWidth = 2, LineColor = "Black", ArrowHeadSize = 10, ArrowHeadAngle = 50)#, end = 'ARROW_POSITION_MIDDLE')
        xm = x1 + dx/2
        ym = y1 + dy/2
        self.Canvas.AddArrow((xm,ym), length/2, angle ,LineWidth = 2, LineColor = "Black", ArrowHeadSize = 10, ArrowHeadAngle = 50)#, end = 'ARROW_POSITION_MIDDLE')

        g = self.Canvas._DrawList
        g.insert(0, g.pop())
        g.insert(0, g.pop())
        self.Canvas._DrawList = g


        # save links
        self.links.append([R1,R2])

        self.Canvas.Draw()

