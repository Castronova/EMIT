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
import math


class MousePointer():
    Default = 'default'
    Link = 'link'
    Delete = 'delete'

class Canvas(NavCanvas):

    def __init__(self, *args, **kwargs):
        NavCanvas.__init__(self, *args,**kwargs)

        self.initSubscribers()
        self.models = {}

        defaultCursor = wx.StockCursor(wx.CURSOR_DEFAULT)
        defaultCursor.Name = 'default'
        self._Cursor = defaultCursor

        self.UnBindAllMouseEvents()
        self.ZoomToFit(Event=None)
        self.MoveObject = None
        self.Moving = False
        Pointers = MousePointer()
        self.MousePointer = Pointers.Default

        #self.createLink()
        self.linkrects = []
        self.initBindings()
        self.links = []

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
        Publisher.subscribe(self.setCursor, "setCursor")

    def setCursor(self, value=None):
        #print "Cursor was set to value ", dir(value), value.GetHandle()
        self._Cursor=value

    def getCursor(self):
        return self._Cursor


    def createBox(self, xCoord, yCoord, id=None, name=None):

        if name:
            w, h = 180, 120
            WH = (w/2, h/2)
            x,y = xCoord, yCoord
            FontSize = 14
            #filename = os.path.basename(filepath)

            R = self.Canvas.AddRectangle((x,y), (w,h), LineWidth = 2, FillColor = "BLUE")
            R.HitFill = True
            R.ID = id
            R.Name = name
            R.wh = (w,h)
            R.xy = (x,y)
            wrappedtext = tw.wrap(unicode(name), 15)
            print wrappedtext, 'R:', dir(R)
            label = self.Canvas.AddText("\n".join(wrappedtext), (x+1, y+h/2),
                                        Color = "White",  Size = FontSize,
                                        Weight=wx.BOLD, Style=wx.ITALIC )
            R.Text = label
            #print dir(label), label
            #R.Bind(FC.EVT_FC_LEFT_UP, self.OnLeftUp )

            R.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)
            #self.Canvas.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit, id=R.ID)

            self.models[R]=id

            self.Canvas.Draw()

        else:
            print "Nothing Selected"

    def onLeftDown(self, event):
        #print event.GetPosition(),
       # dxy = event.GetPosition() - self.StartPoint
        dxy = self.Canvas.PixelToWorld(event.GetPosition())
        print dxy
        #Cursor = wx.CURSOR_BULLSEYE
        #cnum = wx.StockCursor(Cursor)




            #if not self.Canvas.HitTest(event, EventType):
            #    self.Canvas._RaiseMouseEvent(event, EventType)
            #else:
            #    print "Selected an object"


    def ObjectHit(self, object):
        print "Hit Object", object.Name

        cur = self.getCursor()

        if cur.Name == 'link':
            if len(self.linkrects)  > 0:
                self.linkrects.append(object)
                self.CreateLine(self.linkrects[0], self.linkrects[1])

                # save links
                self.links.append([self.linkrects[0], self.linkrects[1]])

                self.linkrects=[]
                self.Canvas.SetMode(self.Modes[0][1])
            else:
                self.linkrects.append(object)
            # obj = object.GetEventObject()
            #
            # EventType = FC.EVT_FC_LEFT_DOWN
            # obj = self.GetHitObject(object, EventType)
            #
            # if obj:
            #
            #
            #     self.selected.append(obj)
            #     if len(self.selected) == 2:
            #         self.CreateLine(self.selected[0], self.selected[1])
            #         self.selected = []

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

                # remove links
                self.Canvas._DrawList = [obj for obj in self.Canvas._DrawList if type(obj) != FC.Arrow]

                # recalculate links
                rects = [obj for obj in self.Canvas._DrawList if type(obj) != FC.Rectangle]

                # todo:  link functionality must be moved into this class so that we can redraw the links
                for link in self.links:
                    self.CreateLine(link[0], link[1])

                # using links[[r1,r2],[...]] we can iterate of the rectangles and redraw links


            self.Canvas.Draw(True)

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




        self.Canvas.Draw()


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
class ClearCanvas(NavCanvas):
    def __init__(self):
        def __init__(self, *args, **kwargs):
            NavCanvas.__init__(self, *args,**kwargs)

            self.onRightDown()

    def onRightDown(self, event):
        print "Right Click"
        self.Canvas.ClearAll()
        self.Canvas.Draw()

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

