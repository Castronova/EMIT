
__author__ = 'Mario'

import wx
import random
import math
import math
#from GUIControl import GUIBase
import textwrap as tw
ver = 'local'

import sys
sys.path.append("..")
from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.floatcanvas.Utilities import BBox
from wx.lib.floatcanvas.NavCanvas import NavCanvas
from wx.lib.pubsub import pub as Publisher
import numpy as N
import os
import math
import markdown2
from LinkDialogueBox import LinkBox
import CanvasObjects
import LinkWizard
from LinkStart import LinkStart
from ContextMenu import LinkContextMenu, ModelContextMenu, GeneralContextMenu

class CanvasController:
    def __init__(self, cmd, Canvas):
        self.Canvas = Canvas
        self.FloatCanvas = self.Canvas.Canvas
        self.cmd = cmd

        self.UnBindAllMouseEvents()

        self.MoveObject = None
        self.Moving = False

        self.initBindings()
        self.initSubscribers()

        defaultCursor = wx.StockCursor(wx.CURSOR_DEFAULT)
        defaultCursor.Name = 'default'
        self._Cursor = defaultCursor

        self.Canvas.ZoomToFit(Event=None)

        dt = FileDrop(self, self.Canvas, self.cmd)
        self.Canvas.SetDropTarget(dt)

        self.linkRects = []
        self.links = {}
        self.models = {}

        self.link_clicks = 0

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
        self.FloatCanvas.Bind(FC.EVT_MOTION, self.OnMove )
        self.FloatCanvas.Bind(FC.EVT_LEFT_UP, self.OnLeftUp )
        #self.FloatCanvas.Bind(FC.EVT_RIGHT_DOWN, self.onRightDown)
        self.FloatCanvas.Bind(FC.EVT_LEFT_DOWN, self.onLeftDown)
        self.FloatCanvas.Bind(FC.EVT_RIGHT_DOWN, self.LaunchContext)



    def initSubscribers(self):
        Publisher.subscribe(self.createBox, "createBox")
        Publisher.subscribe(self.setCursor, "setCursor")




    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates
        and moves the object it is clicked on

        """

        if self.Moving:
            dxy = event.GetPosition() - self.StartPoint
            # Draw the Moving Object:
            dc = wx.ClientDC(self.FloatCanvas)
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetBrush(wx.TRANSPARENT_BRUSH)
            dc.SetLogicalFunction(wx.XOR)
            if self.MoveObject is not None:
                dc.DrawPolygon(self.MoveObject)
            self.MoveObject = self.StartObject + dxy
            dc.DrawPolygon(self.MoveObject)

    def LaunchContext(self, event):

        # get hit object
        #self.GetHitObject(event, event.EventType)

        # if canvas is selected
        if type(event) == wx.lib.floatcanvas.FloatCanvas._MouseEvent:
            self.Canvas.PopupMenu(GeneralContextMenu(self), event.GetPosition())

        elif type(event) == wx.lib.floatcanvas.FloatCanvas.Polygon:
            #if object is link
            if event.type == "ArrowHead":
                self.Canvas.PopupMenu(LinkContextMenu(self), event.HitCoordsPixel.Get())

            # if object is model
            elif event.type == 'Model':
                self.Canvas.PopupMenu(ModelContextMenu(self), event.HitCoordsPixel.Get())

        # # if object is neither
        # else:
        #     self.Canvas.PopupMenu(GeneralContextMenu(self), event.GetPosition())


        #self.Canvas.ClearAll()
        #self.Canvas.Draw()

    def onLeftDown(self, event):
        pass

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

            # get the coordinates for the rounded rectangle
            rect_coords = CanvasObjects.build_rounded_rectangle((x,y), width=w, height=h)

            R = self.FloatCanvas.AddObject(FC.Polygon(rect_coords,FillColor='#A2CAF5',InForeground=True))

            #R = self.FloatCanvas.AddRectangle((x,y), (w,h), LineWidth = 2, FillColor = "BLUE",InForeground=True)
            #R.HitFill = True
            R.ID = id
            R.Name = name
            R.wh = (w,h)
            R.xy = (x,y)

            # set the shape type so that we can identify it later
            R.type = CanvasObjects.ShapeType.Model


            width = 15
            wrappedtext = tw.wrap(unicode(name), width)
            # new_line = []
            # for line in wrappedtext:
            #
            #     frontpadding = int(math.floor((width - len(line))/2))
            #     backpadding = int(math.ceil((width - len(line))/2))
            #     line = ' '*frontpadding + line
            #     line += ' '*backpadding
            #     new_line.append(line)

            #print wrappedtext, 'R:', dir(R)

            #wx.DC.DrawLabel('This is some text',R)
            #DrawLabel(self, text, rect, alignment=wxALIGN_LEFT|wxALIGN_TOP, indexAccel=-1)



            #FC.DrawLabel(self, text, rect, alignment=wxALIGN_LEFT|wxALIGN_TOP, indexAccel=-1)

            #textbox = FC.ScaledText(wrappedtext, (x,y),Size=FontSize,Color='White',InForeground=True,Position='cc',Width=w)
            #__init__(self, String, Point, Size, Color, BackgroundColor, LineColor, LineStyle, LineWidth, Width, PadSize, Family, Style, Weight, Underlined, Position, Alignment, Font, LineSpacing, InForeground)
            #textbox.type  =CanvasObjects.ShapeType.Label

            #label = self.FloatCanvas.AddObject(textbox)

            # define the font
            font = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            # print "font", font.GetPixelSize()
            #
            # textwidth =len(max(wrappedtext))*font.GetPixelSize()[1]
            # textheight = len(wrappedtext)*font.GetPixelSize()[1]
            # location = (x - .25*textwidth,y+.5*textheight)

            label = self.FloatCanvas.AddScaledTextBox(unicode(name), (x,y), #(x+1, y+h/2),
                                        Color = "Black",  Size = FontSize, Width= w-10, Position = "cc", Alignment = "center",
                                        Weight=wx.BOLD, Style=wx.ITALIC, InForeground=True, Font = font, LineWidth = 0, LineColor = None)


            # set the type of this object so that we can find it later
            label.type = CanvasObjects.ShapeType.Label

            # add this text as an attribute of the rectangle
            R.Text = label


            #print dir(label), label
            #R.Bind(FC.EVT_FC_LEFT_UP, self.OnLeftUp )

            R.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)
            R.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)

            ### R.Bind(FC.EVT_FC_RIGHT_DOWN, self.RightClickCb )
            #self.Canvas.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit, id=R.ID)

            self.models[R]=id

            self.FloatCanvas.Draw()

        else:
            print "Nothing Selected"

    def createLine(self, R1, R2):
        #print "creating link", R1, R2
        x1,y1  = (R1.BoundingBox[0] + (R1.wh[0]/2, R1.wh[1]/2))
        x2,y2  = (R2.BoundingBox[0] + (R2.wh[0]/2, R2.wh[1]/2))

        length = (((x2 - x1)**2)+(y2 - y1)**2)**.5
        dy = (y2 - y1)
        dx = (x2 - x1)
        angle = 90- math.atan2(dy,dx) *180/math.pi

        #print 'angle: ',angle
        from matplotlib.pyplot import cm
        cmap = cm.Blues
        line = CanvasObjects.get_line_pts((x1,y1),(x2,y2),order=4, num=200)
        linegradient = CanvasObjects.get_hex_from_gradient(cmap, len(line))
        linegradient.reverse()
        arrow = CanvasObjects.build_arrow(line, arrow_length=6)
       # print arrow

        for i in range(0,len(line)-1):
            l = FC.Line((line[i],line[i+1]),LineColor=linegradient[i],LineWidth=2,InForeground=False)
            l.type = CanvasObjects.ShapeType.Link
            self.FloatCanvas.AddObject(l)

        # create the arrowhead object
        arrow_shape = FC.Polygon(arrow,FillColor='Blue',InForeground=True)

        # set the shape type so that we can identify it later
        arrow_shape.type = CanvasObjects.ShapeType.ArrowHead
        self.FloatCanvas.AddObject(arrow_shape)

        # bind the arrow to left click
        arrow_shape.Bind(FC.EVT_FC_LEFT_DOWN, self.ArrowClicked)
        arrow_shape.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)


        # store the link and rectangles in the self.links list
        for k,v in self.links.iteritems():
            if v == [R1,R2]:
                self.links.pop(k)
                break
        self.links[arrow_shape] = [R1,R2]


        self.Canvas.Canvas.Draw()


    def ObjectHit(self, object):
        print "Hit Object(CanvasController)", object.Name
        #self.FloatCanvas.Bind(FC.EVT_FC_RIGHT_DOWN( list, -1, self.RightClickCb ))
        cur = self.getCursor()

        print object.Name

        if cur.Name == 'link':
            self.linkRects.append(object)
        # if cur.Name == 'link':
        #     if len(self.linkRects)  > 0:
        #         self.linkRects.append(object)
        #         self.createLine(self.linkRects[0], self.linkRects[1])
        #
        #         # reset linkrects object
        #         self.linkRects=[]
        #
        #         # change the mouse cursor
        #
        #         #self.Canvas.SetMode(self.Modes[0][1])
        #
        #     else:
        #         self.linkRects.append(object)

        # populate model view
        if cur.Name == 'default':
            # get the model view container
            mainGui = self.Canvas.GetTopLevelParent()
            mv = mainGui.Children[0].FindWindowByName('notebook').GetPage(1)

            #mv = self.Canvas.GetTopLevelParent().m_mgr.GetPane(n

            # get the model object from cmd
            obj_id = object.ID
            obj = self.cmd.get_model_by_id(obj_id)

            # format the model parameters for printing
            params = obj.get_config_params()


            text = ''

            for arg,dict in params.iteritems():
                title = arg

                try:
                    table = ''
                    for k,v in dict[0].iteritems():
                        table += '||%s||%s||\n' % (k, v)

                    text += '###%s  \n%s  \n'%(title,table)
                except: pass

            #text = '\n'.join([k for k in params.keys()])

            #text = '||a||b||\n||test||test||\n||test||test||'

            #md = "###Heading\n---\n```\nsome code\n```"
            html = markdown2.markdown(text, extras=["wiki-tables"])

            #css = "<style>h3 a{font-weight:100;color: gold;text-decoration: none;}</style>"
            css = "<style>tr:nth-child(even) " \
                    "{ background-color: #e6f1f5;} " \
                    "table {border-collapse: collapse;width:100%}" \
                    "table td, table th {border: 1px solid #e6f1f5;}" \
                    "h3 {color: #66A3E0}</style>"




            # set the model params as text
            mv.setText(css + html)



        if not self.Moving:
            self.Moving = True
            self.StartPoint = object.HitCoordsPixel

            BB = object.BoundingBox
            OutlinePoints = N.array(
            ( (BB[0, 0], BB[0, 1]), (BB[0, 0], BB[1, 1]), (BB[1, 0], BB[1, 1]), (BB[1, 0], BB[0, 1]),
            ))
            self.StartObject = self.FloatCanvas.WorldToPixel(OutlinePoints)
            self.MoveObject = None
            self.MovingObject = object


    def OnLeftUp(self, event):
        if self.Moving:
            self.Moving = False
            if self.MoveObject is not None:
                dxy = event.GetPosition() - self.StartPoint
                (x,y) = self.FloatCanvas.ScalePixelToWorld(dxy)
                self.MovingObject.Move((x,y))
                self.MovingObject.Text.Move((x, y))


                # clear lines from drawlist
                self.FloatCanvas._DrawList = [obj for obj in self.FloatCanvas._DrawList if obj.type != CanvasObjects.ShapeType.Link]
                #self.FloatCanvas._DrawList = [obj for obj in self.FloatCanvas._DrawList if type(obj) != FC.Line]

                # remove any arrowheads from the _ForeDrawList
                self.FloatCanvas._ForeDrawList = [obj for obj in self.FloatCanvas._ForeDrawList if obj.type != CanvasObjects.ShapeType.ArrowHead]
                #self.FloatCanvas._ForeDrawList = [obj for obj in self.FloatCanvas._ForeDrawList if type(obj) != FC.Polygon]

                # redraw links
                for link in self.links.keys():
                    r1,r2 = self.links[link]
                    self.createLine(r1,r2)

            self.FloatCanvas.Draw(True)


        # count clicks
        cur = self.getCursor()
        if cur.Name == 'link':
            self.AddinkCursorClick()

        #if self.link

        # create link
        #if len(self.linkRects)  > 0:
        #         self.linkRects.append(object)
        #         self.createLine(self.linkRects[0], self.linkRects[1])
        #
        #         # reset linkrects object
        #         self.linkRects=[]
        #
        #         #


    def AddinkCursorClick(self):
        self.link_clicks += 1

        if self.link_clicks == 2:
            if len(self.linkRects) == 2:
                self.createLine(self.linkRects[0], self.linkRects[1])

            # reset
            self.link_clicks = 0
            self.linkRects=[]

            #change the mouse cursor


            e = e = wx._core.CommandEvent(10013)
            e.Id = -2017
            # self.Canvas.GuiMouse.OnLeftUp(e)
            #self.Canvas.
            self.Canvas.SetMode(e)

    def GetHitObject(self, event, HitEvent):
        if self.Canvas.Canvas.HitDict:
            # check if there are any objects in the dict for this event
            if self.Canvas.Canvas.HitDict[ HitEvent ]:
                xy = event.GetPosition()
                color = self.Canvas.Canvas.GetHitTestColor( xy )
                if color in self.Canvas.Canvas.HitDict[ HitEvent ]:
                    Object = self.Canvas.Canvas.HitDict[ HitEvent ][color]
                    #self.Canvas._CallHitCallback(Object, xy, HitEvent)
                    return Object
            return False

    def ArrowClicked(self,event):

        #if event

        #self.Log("The Link was Clicked")

        # get the models associated with the link
        polygons = self.links[event]

        # get r1 and r2
        r1 = polygons[0]
        r2 = polygons[1]

        # get output items from r1
        from_model = self.cmd.get_model_by_id(r1.ID)

        # get exchange items
        inputitems = from_model.get_output_exchange_items()
        # get output items from r1
        to_model = self.cmd.get_model_by_id(r2.ID)

        # get exchange items
        outputitems = to_model.get_input_exchange_items()



        # for item in eitems:
        #     print 'Type: ', item.get_type()
        #     print "Name: ", item.name()
        #     print "Variable: ", item.variable().VariableNameCV()
        #     print "Unit: ", item.unit().UnitName()
        #     print 10*'-'
        #
        #
        #
        # for item in eitems:
        #     print 'Type: ', item.get_type()
        #     print "Name: ", item.name()
        #     print "Variable: ", item.variable().VariableNameCV()
        #     print "Unit: ", item.unit().UnitName()
        #     print 10*'-'


        # print "The Link was clicked"
        linkstart = LinkStart(self.FloatCanvas, from_model, to_model, inputitems, outputitems, self.cmd)
        linkstart.Show()
        #linkwiz = LinkWizard.wizLink(self.FloatCanvas, inputitems, outputitems)

        # dlg = LinkBox()
        # dlg.ShowModal()
        # dlg.Destroy()
        #Example()

    def RightClickCb( self, event ):
        # record what was clicked
        #self.list_item_clicked = right_click_context = event.GetText()


        # get the link object
        # get the model id's from the link
        # get the model objects from the models id's
        menu = wx.Menu()
        for (id,title) in menu_title_by_id.items():
            menu.Append( id, title )
            wx.EVT_MENU( menu, id, self.MenuSelectionCb )

        ### 5. Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint. ###
        self.frame.PopupMenu( menu, event.GetPoint() )
        menu.Destroy() # destroy to avoid mem leak
    #
    def MenuSelectionCb( self, event ):
        # do something
        operation = menu_title_by_id[ event.GetId() ]
        #target    = self.list_item_clicked
        print 'Perform "%(operation)s" on "%(target)s."' % vars()


class FileDrop(wx.FileDropTarget):
    def __init__(self, controller, window, cmd):
        wx.FileDropTarget.__init__(self)
        self.controller = controller
        self.window = window
        self.cmd = cmd

    def OnDropFiles(self, x, y, filenames):
        #print "filename: {2} x: {0} y: {1}".format(x,y, filenames)

        #Canvas = NC.NavCanvas(self, -1, size=wx.DefaultSize).Canvas
        #Canvas.AddRectangle((110, 10), (100, 100), FillColor='Red')
        #print x,y
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

                    self.controller.createBox(name=name, id=modelid, xCoord=newx, yCoord=newy)
                    self.window.Canvas.Draw()
                    offset=200
            except Exception, e:
                print 'Could not load the model :(. Hopefully this exception helps...'
                print e

        else:
            print 'I do not recognize this file type :('



menu_titles = [ "Open",
                "Properties",
                "Rename",
                "Delete" ]

menu_title_by_id = {}
for title in menu_titles:
    menu_title_by_id[ wx.NewId() ] = title
