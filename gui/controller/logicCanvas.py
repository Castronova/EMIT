__author__ = 'Mario'

import wx
import textwrap as tw

ver = 'local'
from utilities import gui

import sys

sys.path.append("..")

from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.floatcanvas.NavCanvas import NavCanvas
from wx.lib.pubsub import pub as Publisher
import numpy as N
import os
import markdown2
from gui.views.viewContext import LinkContextMenu, ModelContextMenu, GeneralContextMenu
from wrappers import odm2_data
import xml.etree.ElementTree as et
from xml.dom import minidom
from transform.space import SpatialInterpolation
from transform.time import TemporalInterpolation

import datatypes
from api.ODM2.Results.services import readResults
from api.ODM2.Core.services import readCore
from utilities.threading import EVT_CREATE_BOX, EVT_UPDATE_CONSOLE, ThreadManager
from matplotlib.pyplot import cm

from gui.views.viewCanvas import ViewCanvas
import gui.controller.logicCanvasObjects as LogicCanvasObjects
from gui.controller.logicLink import LogicLink
from coordinator import engine
from gui.controller.logicFileDrop import LogicFileDrop
import coordinator.engineManager as engineManager
import coordinator.events as engineEvent
import coordinator.engineAccessors as engine
import utilities.db as dbUtilities
import uuid

# todo: refactor
# from gui import CanvasObjects
# from ..LinkFrame import LinkStart

class LogicCanvas(ViewCanvas):
    def __init__(self, parent):

        self.cmd = engineManager.get_engine()

        self.threadManager = ThreadManager(self)

        # intialize the parent class
        ViewCanvas.__init__(self, parent)

        self.parent = parent

        # This is just to ensure that we are starting without interference from NavToolbar or drag-drop
        self.UnBindAllMouseEvents()

        self.MoveObject = None
        self.Moving = False

        self.initBindings()
        self.initSubscribers()

        defaultCursor = wx.StockCursor(wx.CURSOR_DEFAULT)
        defaultCursor.Name = 'default'
        self._Cursor = defaultCursor

        self.linkRects = []
        self.links = {}
        self.models = {}
        self.dbmodel_required_db = {}

        self.link_clicks = 0

        # self._currentDbSession = self.cmd.get_default_db()
        # self._currentDb = engine.getDefaultDb()
        # self._currentDbSession = dbUtilities.build_session_from_connection_string(self._currentDb['connection_string'])

        self.loadingpath = None

        self.model_coords = {}

    def UnBindAllMouseEvents(self):
        self.Unbind(FC.EVT_LEFT_DOWN)
        self.Unbind(FC.EVT_LEFT_UP)
        self.Unbind(FC.EVT_LEFT_DCLICK)
        self.Unbind(FC.EVT_MIDDLE_DOWN)
        self.Unbind(FC.EVT_MIDDLE_UP)
        self.Unbind(FC.EVT_MIDDLE_DCLICK)
        self.Unbind(FC.EVT_RIGHT_DOWN)
        self.Unbind(FC.EVT_RIGHT_UP)
        self.Unbind(FC.EVT_RIGHT_DCLICK)
        self.EventsAreBound = False

    def initBindings(self):
        self.FloatCanvas.Bind(FC.EVT_MOTION, self.OnMove)
        self.FloatCanvas.Bind(FC.EVT_LEFT_UP, self.OnLeftUp)
        self.FloatCanvas.Bind(FC.EVT_RIGHT_DOWN, self.LaunchContext)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(EVT_CREATE_BOX, self.onCreateBox)
        self.Bind(EVT_UPDATE_CONSOLE, self.onUpdateConsole)

        # engine bindings
        engineEvent.onModelAdded += self.draw_box
        engineEvent.onLinkAdded += self.draw_link
        # engineEvent.onDatabaseConnected += self.onDatabasesLoaded

    def initSubscribers(self):
        Publisher.subscribe(self.createBox, "createBox")
        Publisher.subscribe(self.setCursor, "setCursor")
        Publisher.subscribe(self.run, "run")
        Publisher.subscribe(self.clear, "clear")
        Publisher.subscribe(self.AddDatabaseConnection, "DatabaseConnection")
        # Publisher.subscribe(self.getDatabases, "getDatabases")
        # Publisher.subscribe(self.getCurrentDbSession, "SetCurrentDb")
        Publisher.subscribe(self.SaveSimulation, "SetSavePath")
        Publisher.subscribe(self.loadsimulation, "SetLoadPath")
        Publisher.subscribe(self.addModel, "AddModel")  # subscribes to object list view

    def onClose(self, event):
        print "In close"
        dlg = wx.MessageDialog(None, 'Are you sure you want to exit?', 'Question',
                               wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() != wx.ID_NO:

            self.threadManager.stop()

            windowsRemaining = len(wx.GetTopLevelWindows())
            if windowsRemaining > 0:
                import wx.lib.agw.aui.framemanager as aui

                for item in wx.GetTopLevelWindows():
                    if not isinstance(item, self.frame.__class__):
                        if isinstance(item, aui.AuiFloatingFrame):
                            item.Destroy()
                        elif isinstance(item, aui.AuiSingleDockingGuide):
                            item.Destroy()
                        elif isinstance(item, aui.AuiDockingHintWindow):
                            item.Destroy()
                        elif isinstance(item, wx.Dialog):
                            item.Destroy()
                        item.Close()

            self.frame.Destroy()
            wx.GetApp().ExitMainLoop()

        else:
            pass

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

    def onDatabasesLoaded(self, evt):
        pass

    def onUpdateConsole(self, evt):
        """
        Updates the output console
        """
        if evt.message:
            print "DEBUG|", evt.message

    def onCreateBox(self, evt):
        name = evt.name
        id = evt.id
        x = evt.xCoord
        y = evt.yCoord
        self.createBox(xCoord=x, yCoord=y, id=id, name=name)

    # def createBox(self, xCoord, yCoord, id=None, name=None, color='#A2CAF5'):
    def createBox(self, xCoord, yCoord, id=None, name=None, type=datatypes.ModelTypes.TimeStep):

        # set box color based on model type
        if type == datatypes.ModelTypes.TimeStep:
            color = '#B3DBG6'
        elif type == datatypes.ModelTypes.FeedForward:
            color = '#A2CAF5'
        elif type == datatypes.ModelTypes.Data:
            color = '#A2BGA5'

        if name:
            w, h = 180, 120
            x, y = xCoord, yCoord
            FontSize = 14

            # get the coordinates for the rounded rectangle
            rect_coords = LogicCanvasObjects.build_rounded_rectangle((x, y), width=w, height=h)

            R = self.FloatCanvas.AddObject(FC.Polygon(rect_coords, FillColor=color, InForeground=True))

            R.ID = id
            R.Name = name
            R.wh = (w, h)
            R.xy = (x, y)

            # set the shape type so that we can identify it later
            R.type = LogicCanvasObjects.ShapeType.Model

            width = 15
            wrappedtext = tw.wrap(unicode(name), width)

            # define the font
            font = wx.Font(16, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

            label = self.FloatCanvas.AddScaledTextBox(unicode(name), (x, y),  # (x+1, y+h/2),
                                                      Color="Black", Size=FontSize, Width=w - 10, Position="cc",
                                                      Alignment="center",
                                                      Weight=wx.BOLD, Style=wx.ITALIC, InForeground=True, Font=font,
                                                      LineWidth=0, LineColor=None)


            # set the type of this object so that we can find it later
            label.type = LogicCanvasObjects.ShapeType.Label

            # add this text as an attribute of the rectangle
            R.Text = label

            print name + ' has been added to the canvas.'

            R.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)
            R.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)

            self.models[R] = id

            self.FloatCanvas.Draw()

    def draw_box(self, evt):
        # name,id,type):
        x, y = self.get_model_coords(id=evt.id)
        self.createBox(name=evt.name, id=evt.id, xCoord=x, yCoord=y, type=evt.model_type)

    def draw_link(self, evt):
        # source_id, target_id):

        R1 = None
        R2 = None
        for R, id in self.models.iteritems():
            if id == evt.source_id:
                R1 = R
            elif id == evt.target_id:
                R2 = R

        if R1 is None or R2 is None:
            raise Exception('Could not find Model identifier in loaded models')

        # this draws the line
        self.createLine(R1, R2)

        # self.FloatCanvas.Draw()

    def set_model_coords(self, id, x, y):

        self.model_coords[id] = {'x': x, 'y': y}

    def get_model_coords(self, id):

        return (self.model_coords[id]['x'], self.model_coords[id]['y'])

    def createLine(self, R1, R2):
        # print "creating link", R1, R2
        x1, y1 = (R1.BoundingBox[0] + (R1.wh[0] / 2, R1.wh[1] / 2))
        x2, y2 = (R2.BoundingBox[0] + (R2.wh[0] / 2, R2.wh[1] / 2))

        cmap = cm.Blues
        line = LogicCanvasObjects.get_line_pts((x1, y1), (x2, y2), order=4, num=200)
        linegradient = LogicCanvasObjects.get_hex_from_gradient(cmap, len(line))
        linegradient.reverse()

        for i in range(0, len(line) - 1):
            l = FC.Line((line[i], line[i + 1]), LineColor=linegradient[i], LineWidth=2, InForeground=False)
            l.type = LogicCanvasObjects.ShapeType.Link
            self.FloatCanvas.AddObject(l)

        arrow_shape = self.createArrow(line)

        # store the link and rectangles in the self.links list
        for k, v in self.links.iteritems():
            if v == [R1, R2]:
                self.links.pop(k)
                break
        self.links[arrow_shape] = [R1, R2]

        self.FloatCanvas.Draw()

    def createArrow(self, line):

        arrow = LogicCanvasObjects.build_arrow(line, arrow_length=6)

        # create the arrowhead object
        arrow_shape = FC.Polygon(arrow, FillColor='Blue', InForeground=True)

        # set the shape type so that we can identify it later
        arrow_shape.type = LogicCanvasObjects.ShapeType.ArrowHead
        self.FloatCanvas.AddObject(arrow_shape)

        # bind the arrow to left click
        arrow_shape.Bind(FC.EVT_FC_LEFT_DOWN, self.ArrowClicked)
        arrow_shape.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)

        return arrow_shape

    def addModel(self, filepath, x, y, uid=None):
        """
        Adds a model to the canvas using x,y.  This is useful if adding by file click/dialog
        :param filename:  filename / path
        :param x: x location
        :param y: y location
        :return: None
        """


        # make sure the correct file type was dragged
        name, ext = os.path.splitext(filepath)

        # generate an ID for this model
        if uid is None:
            uid = uuid.uuid4().hex[:5]

        # save these coordinates for drawing once the model is loaded
        self.set_model_coords(uid, x=x, y=y)

        if ext == '.mdl' or ext == '.sim':

            if ext == '.mdl':
                # load the model within the engine process
                engine.addModel(id=uid, attrib={'mdl': filepath})

            elif ext == '.sim':
                # load the simulation
                self.loadsimulation(filepath[0])
        else:
            # load data model
            current_db_id = self._currentDb['id']
            attrib = dict(databaseid=current_db_id, resultid=name)
            engine.addModel(id=uid, attrib=attrib)

        return uid

    def RemoveLink(self, link_obj):

        # todo: need to warn the user that all links will be removed
        dlg = wx.MessageDialog(None,
                               'You are about to remove all data mappings that are associated with this link.  Are you sure you want to perform this action?',
                               'Question',
                               wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() != wx.ID_NO:

            # remove the link entry in self.links
            link = self.links.pop(link_obj)

            # remove the link from the cmd
            from_id = link[0].ID
            to_id = link[1].ID

            # get the link id
            links = engine.getLinksBtwnModels(from_id, to_id)

            # remove all links
            for link in links:
                success = engine.removeLinkById(link['id'])
                if not success:
                    print 'ERROR|Could not remove link: %s' % link['id']

            # redraw the canvas
            self.RedrawConfiguration()

    def RemoveModel(self, model_obj):
        """
        Removes a model component from the modeling canvas
        :param model_obj: model object that will be removed
        :return: None
        """

        updated_links = {}
        for k, v in self.links.iteritems():
            if model_obj not in v:
                updated_links[k] = v
        self.links = updated_links

        # remove the model from the engine
        success = engine.removeModelById(model_obj.ID)

        if success:
            # remove the model from the canvas
            removed_model = self.models.pop(model_obj)

            # redraw the canvas
            self.RedrawConfiguration()

    def clear(self, link_obj=None, model_obj=None):

        # clear links and models in the engine
        success = engine.clearAll()

        if success:
            # clear links and model in gui
            self.links.clear()
            self.models.clear()
            self.FloatCanvas.ClearAll()

            self.RedrawConfiguration()

    def ObjectHit(self, object):
        cur = self.getCursor()

        if cur.Name == 'link':
            self.linkRects.append(object)


        # populate model view
        if cur.Name == 'default':
            # get the model view container
            mainGui = self.GetTopLevelParent()
            mv = mainGui.Children[0].FindWindowByName('notebook').GetPage(1)

            # mv = self.Canvas.GetTopLevelParent().m_mgr.GetPane(n

            # get the model object from cmd
            obj_id = object.ID
            # obj = self.cmd.get_model_by_id(obj_id)
            model = engine.getModelById(obj_id)

            if 'params' in model:
                params = model['params']
            else:
                params = {}

            text = ''

            for arg, dict in params.iteritems():
                title = arg

                try:
                    table = ''
                    for k, v in dict[0].iteritems():
                        table += '||%s||%s||\n' % (k, v)

                    text += '###%s  \n%s  \n' % (title, table)
                except:
                    pass
            html = markdown2.markdown(text, extras=["wiki-tables"])

            css = "<style>tr:nth-child(even) " \
                  "{ background-color: #e6f1f5;} " \
                  "table {border-collapse: collapse;width:100%}" \
                  "table td, table th {border: 1px solid #e6f1f5;}" \
                  "h3 {color: #66A3E0}</style>"


            # set the model params as text
            try:
                mv.setText(css + html)

            except:
                pass

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

    def AddinkCursorClick(self):
        self.link_clicks += 1

        if self.link_clicks == 2:
            if len(self.linkRects) == 2:
                self.createLine(self.linkRects[0], self.linkRects[1])

            # reset
            self.link_clicks = 0
            self.linkRects = []

            # change the mouse cursor
            self.FloatCanvas.SetMode(self.GuiMouse)

    def GetHitObject(self, event, HitEvent):
        if self.FloatCanvas.HitDict:
            # check if there are any objects in the dict for this event
            if self.FloatCanvas.HitDict[HitEvent]:
                xy = event.GetPosition()
                color = self.FloatCanvas.GetHitTestColor(xy)
                if color in self.FloatCanvas.HitDict[HitEvent]:
                    Object = self.FloatCanvas.HitDict[HitEvent][color]
                    return Object
            return False

    def ArrowClicked(self, event):

        # get the models associated with the link
        polygons = self.links[event]

        # get r1 and r2
        r1 = polygons[0]
        r2 = polygons[1]

        # get output items from r1
        from_model = engine.getModelById(r1.ID)

        # get output items from r1
        to_model = engine.getModelById(r2.ID)

        linkstart = LogicLink(self.FloatCanvas, from_model, to_model, self.cmd)

        linkstart.Show()

    def RightClickCb(self, event):
        menu = wx.Menu()
        for (id, title) in menu_title_by_id.items():
            menu.Append(id, title)
            wx.EVT_MENU(menu, id, self.MenuSelectionCb)

        # Launcher displays menu with call to PopupMenu, invoked on the source component, passing event's GetPoint.
        self.frame.PopupMenu(menu, event.GetPoint())
        menu.Destroy()  # destroy to avoid mem leak

    def RedrawConfiguration(self):
        # clear lines from drawlist
        self.FloatCanvas._DrawList = [obj for obj in self.FloatCanvas._DrawList if
                                      obj.type != LogicCanvasObjects.ShapeType.Link]

        # remove any arrowheads from the _ForeDrawList
        self.FloatCanvas._ForeDrawList = [obj for obj in self.FloatCanvas._ForeDrawList if
                                          obj.type != LogicCanvasObjects.ShapeType.ArrowHead]

        # remove any models
        i = 0
        modelids = [model.ID for model in self.models]
        modellabels = [model.Name for model in self.models]
        self.FloatCanvas._ForeDrawList = [obj for obj in self.FloatCanvas._ForeDrawList
                                          if (obj.type == LogicCanvasObjects.ShapeType.Model and obj.ID in modelids)
                                          or (
                                              obj.type == LogicCanvasObjects.ShapeType.Label and obj.String in modellabels)]

        # redraw links
        for link in self.links.keys():
            r1, r2 = self.links[link]
            self.createLine(r1, r2)

        self.FloatCanvas.Draw(True)

    def OnLeftUp(self, event):
        if self.Moving:
            self.Moving = False
            if self.MoveObject is not None:
                dxy = event.GetPosition() - self.StartPoint
                (x, y) = self.FloatCanvas.ScalePixelToWorld(dxy)
                self.MovingObject.Move((x, y))
                self.MovingObject.Text.Move((x, y))


                # clear lines from drawlist
                self.FloatCanvas._DrawList = [obj for obj in self.FloatCanvas._DrawList if
                                              obj.type != LogicCanvasObjects.ShapeType.Link]

                # remove any arrowheads from the two FloatCanvas DrawLists
                self.FloatCanvas._ForeDrawList = [obj for obj in self.FloatCanvas._ForeDrawList if
                                                  obj.type != LogicCanvasObjects.ShapeType.ArrowHead]
                self.FloatCanvas._DrawList = [obj for obj in self.FloatCanvas._DrawList if
                                              obj.type != LogicCanvasObjects.ShapeType.ArrowHead]

                # redraw links
                for link in self.links.keys():
                    r1, r2 = self.links[link]
                    self.createLine(r1, r2)

            self.FloatCanvas.Draw(True)


        # count clicks
        cur = self.getCursor()
        if cur.Name == 'link':
            self.AddinkCursorClick()

    def getCurrentDbSession(self, dbName=None):
        if dbName is not None:
            dbs = engine.getDbConnections()
            for db in dbs.iterkeys():
                if dbs[db]['name'] == dbName:
                    self._currentDbSession = dbUtilities.build_session_from_connection_string(
                        dbs[db]['connection_string'])
                    break
        return self._currentDbSession

    def AddDatabaseConnection(self, title, desc, dbengine, address, name, user, pwd):

        # build the database connection
        # connection = gui.create_database_connections_from_args(title, desc, engine, address, name, user, pwd)

        # if type(connection) == dict and any(connection):
            # store the connection
            # self.cmd.add_db_connection(connection)
        kwargs = dict(title=title, desc=desc, engine=dbengine, address=address, name=name, user=user, pwd=pwd)
        engine.connectToDb(**kwargs)

            # if result:
            #
            #     # notify that the connection was added successfully
            #     Publisher.sendMessage('connectionAddedStatus', value=True,
            #                           connection_string=connection[connection.keys()[0]][
            #                               'connection_string'])  # sends message to mainGui
            #
            #     return True
            # else:
            #     # notify that the connection was not added successfully
            #     Publisher.sendMessage('connectionAddedStatus', value=False,
            #                           connection_string=connection)  # sends message to mainGui
            #
            #     return False

        # return False

    def DetailView(self):
        # DCV.ShowDetails()
        pass

    def SaveSimulation(self, path):

        if len(self.models.keys()) == 0:
            print 'WARNING | Nothing to save!'
            return

        # create an xml tree
        tree = et.Element('Simulation')

        db_ids = []

        # add models to the xml tree
        for shape, modelid in self.models.iteritems():
            attributes = {}
            model = engine.getModelById(modelid)
            bbox = shape.BoundingBox
            attributes['x'] = str((bbox[0][0] + bbox[1][0]) / 2)
            attributes['y'] = str((bbox[0][1] + bbox[1][1]) / 2)
            attributes['name'] = model['name']
            attributes['id'] = model['id']

            if model['type'] == datatypes.ModelTypes.FeedForward:
                attributes['mdl'] = model['attrib']['mdl']

                modelelement = et.SubElement(tree, 'Model')

                modelnameelement = et.SubElement(modelelement, "name")
                modelnameelement.text = attributes['name']
                modelidelement = et.SubElement(modelelement, "id")
                modelidelement.text = attributes['id']
                modelxelement = et.SubElement(modelelement, "xcoordinate")
                modelxelement.text = attributes['x']
                modelyelement = et.SubElement(modelelement, "ycoordinate")
                modelyelement.text = attributes['y']
                modelpathelement = et.SubElement(modelelement, "path")
                modelpathelement.text = model['attrib']['mdl']

            elif model['type'] == datatypes.ModelTypes.Data:
                attributes['databaseid'] = model['attrib']['databaseid']
                attributes['resultid'] = model['attrib']['resultid']
                dataelement = et.SubElement(tree, 'DataModel')
                datamodelnameelement = et.SubElement(dataelement, "name")
                datamodelnameelement.text = attributes['name']
                datamodelidelement = et.SubElement(dataelement, "id")
                datamodelidelement.text = attributes['id']
                datamodelxelement = et.SubElement(dataelement, "xcoordinate")
                datamodelxelement.text = attributes['x']
                datamodelyelement = et.SubElement(dataelement, "ycoordinate")
                datamodelyelement.text = attributes['y']
                datamodelidelement = et.SubElement(dataelement, "databaseid")
                datamodelidelement.text = attributes['databaseid']
                datamodelresultidelement = et.SubElement(dataelement, "resultid")
                datamodelresultidelement.text = attributes['resultid']

                # save this db id
                if model['attrib']['databaseid'] not in db_ids:
                    db_ids.append(model['attrib']['databaseid'])

        # add links to the xml tree
        links = engine.getAllLinks()
        for link in links:
            attributes = {}

            attributes['from_name'] = link['source_component_name']
            attributes['from_id'] = link['source_component_id']
            attributes['from_item'] = link['output_name']
            attributes['from_item_id'] = link['output_id']

            attributes['to_name'] = link['target_component_name']
            attributes['to_id'] = link['target_component_id']
            attributes['to_item'] = link['input_name']
            attributes['to_item_id'] = link['input_name']

            attributes['temporal_transformation'] = link['temporal_interpolation']
            attributes['spatial_transformation'] = link['spatial_interpolation']

            linkelement = et.SubElement(tree, 'Link')

            linkfromnameelement = et.SubElement(linkelement, "from_name")
            linkfromnameelement.text = attributes['from_name']
            linkfromidelement = et.SubElement(linkelement, "from_id")
            linkfromidelement.text = attributes['from_id']
            linkfromitemelement = et.SubElement(linkelement, "from_item")
            linkfromitemelement.text = attributes['from_item']
            linkfromitemidelement = et.SubElement(linkelement, "from_item_id")
            linkfromitemidelement.text = attributes['from_item_id']

            linktonameelement = et.SubElement(linkelement, "to_name")
            linktonameelement.text = attributes['to_name']
            linktoidelement = et.SubElement(linkelement, "to_id")
            linktoidelement.text = attributes['to_id']
            linktoitemelement = et.SubElement(linkelement, "to_item")
            linktoitemelement.text = attributes['to_item']
            linktoitemidelement = et.SubElement(linkelement, "to_item_id")
            linktoitemidelement.text = attributes['to_item_id']

            link_transform_element = et.SubElement(linkelement, "transformation")
            link_transform_temporal = et.SubElement(link_transform_element, "temporal")
            link_transform_temporal.text = attributes['temporal_transformation']
            link_transform_spatial = et.SubElement(link_transform_element, "spatial")
            link_transform_spatial.text = attributes['spatial_transformation']


        # save required databases
        for db_id in db_ids:
            attributes = {}

            # todo: this needs to be tested!
            # connections = self.cmd.get_db_connections()
            connections = engine.getDbConnections()

            db_conn = connections[db_id]['args']

            if db_conn:
                attributes['name'] = db_conn['name']
                attributes['address'] = db_conn['address']
                attributes['pwd'] = db_conn['pwd']
                attributes['desc'] = db_conn['desc']
                attributes['engine'] = db_conn['engine']
                attributes['db'] = db_conn['db']
                attributes['user'] = db_conn['user']
                attributes['databaseid'] = db_conn['id']
                attributes['connection_string'] = str(db_conn['connection_string'])
                connectionelement = et.SubElement(tree, 'DbConnection')

                connectionnameelement = et.SubElement(connectionelement, "name")
                connectionnameelement.text = attributes['name']
                connectionaddresselement = et.SubElement(connectionelement, "address")
                connectionaddresselement.text = attributes['address']
                connectionpwdelement = et.SubElement(connectionelement, "pwd")
                connectionpwdelement.text = attributes['pwd']
                connectiondescelement = et.SubElement(connectionelement, "desc")
                connectiondescelement.text = attributes['desc']
                connectionengineelement = et.SubElement(connectionelement, "engine")
                connectionengineelement.text = attributes['engine']
                connectiondbelement = et.SubElement(connectionelement, "db")
                connectiondbelement.text = attributes['db']
                connectionuserelement = et.SubElement(connectionelement, "user")
                connectionuserelement.text = attributes['user']
                connectiondatabaseidelement = et.SubElement(connectionelement, "databaseid")
                connectiondatabaseidelement.text = attributes['databaseid']
                connectionconnectionstringelement = et.SubElement(connectionelement, "connection_string")
                connectionconnectionstringelement.text = attributes['connection_string']

        try:

            # format the xml nicely
            rough_string = et.tostring(tree, 'utf-8')
            reparsed = minidom.parseString(rough_string)
            prettyxml = reparsed.toprettyxml(indent="  ")

            # save the xml doc
            with open(path, 'w') as f:
                f.write(prettyxml)
        except Exception, e:
            print 'ERROR | An error occurred when attempting to save the project '
            print 'ERROR | EXECPTION MESSAGE '
            print e

        print 'Configuration Saved Successfully! '

    def loadsimulation(self, file):
        # TODO: Should be part of the cmd.
        tree = et.parse(file)

        self.loadingpath = file

        tree = et.parse(file)

        # get the root
        root = tree.getroot()

        # make sure the required database connections are loaded
        # connections = self.cmd.get_db_connections()
        connections = engine.getDbConnections()
        conn_ids = {}
        elementslist = root.getchildren()

        # get all known transformations
        space = SpatialInterpolation()
        time = TemporalInterpolation()
        spatial_transformations = {i.name(): i for i in space.methods()}
        temporal_transformations = {i.name(): i for i in time.methods()}

        # databaselist = [x for x in elementslist if x.tag == 'DbConnection']
        # for db_conn in databaselist:
        for child in root._children:
            if child.tag == 'DbConnection':
                taglist = []
                textlist = []
                for data in child:
                    textlist.append(data.text)
                    taglist.append(data.tag)

                attrib = dict(zip(taglist, textlist))

                connection_string = attrib['connection_string']

                database_exists = False
                # db_elements = db_conn.getchildren()


                for id, dic in connections.iteritems():

                    if str(dic['args']['connection_string']) == connection_string:
                        # dic['args']['id'] = db_conn.attrib['id']
                        database_exists = True

                        # map the connection ids
                        conn_ids[attrib['databaseid']] = dic['args']['id']
                        break

                # if database doesn't exist, then connect to it
                if not database_exists:
                    connect = wx.MessageBox('This database connection does not currently exist.  Click OK to connect.',
                                            'Info', wx.OK | wx.CANCEL)

                    if connect == wx.OK:

                        # attempt to connect to the database
                        title = dic['args']['name']
                        desc = dic['args']['desc']
                        db_engine = dic['args']['engine']
                        address = dic['args']['address']
                        name = dic['args']['db']
                        user = dic['args']['user']
                        pwd = dic['args']['pwd']

                        if not self.AddDatabaseConnection(title, desc, db_engine, address, name, user, pwd):
                            wx.MessageBox('I was unable to connect to the database with the information provided :(',
                                          'Info', wx.OK | wx.ICON_ERROR)
                            return

                        # map the connection id
                        conn_ids[attrib['databaseid']] = attrib['databaseid']

                    else:
                        return


        # loop through each model and load it
        for child in root._children:
            if child.tag == 'Model':
                taglist = []
                textlist = []
                for data in child:
                    textlist.append(data.text)
                    taglist.append(data.tag)

                attrib = dict(zip(taglist, textlist))

                # load the model
                self.addModel(filepath=attrib['path'], x=float(attrib['xcoordinate']), y=float(attrib['ycoordinate']),
                              uid=attrib['id'])

        for child in root._children:
            if child.tag == 'DataModel':
                taglist = []
                textlist = []
                for data in child:
                    textlist.append(data.text)
                    taglist.append(data.tag)

                attrib = dict(zip(taglist, textlist))

                # get the data type
                dtype = datatypes.ModelTypes.Data

                databaseid = attrib['databaseid']
                mappedid = conn_ids[databaseid]

                attrib['databaseid'] = mappedid
                modelid = self.addModel(filepath=attrib['path'], x=attrib['xcoordinate'], y=attrib['ycoordinate'],
                                        uid=attrib['id'])

        for child in root._children:
            if child.tag == 'Link':
                taglist = []
                textlist = []
                for items in child:
                    textlist.append(items.text)
                    taglist.append(items.tag)

                attrib = dict(zip(taglist, textlist))
                R1 = None
                R2 = None
                for R, id in self.models.iteritems():
                    if id == attrib['from_id']:
                        R1 = R
                    elif id == attrib['to_id']:
                        R2 = R

                if R1 is None or R2 is None:
                    raise Exception('Could not find Model identifer in loaded models')

                temporal = None
                spatial = None
                # set the temporal and spatial interpolations
                transform = child.find("./transformation")
                for transform_child in transform:
                    if transform_child.text.upper() != 'NONE':
                        if transform_child.tag == 'temporal':
                            temporal = temporal_transformations[transform_child.text]
                        elif transform_child.tag == 'spatial':
                            spatial = spatial_transformations[transform_child.text]

                # create the link
                l = engine.addLink(source_id=attrib['from_id'],
                                   source_item=attrib['from_item'],
                                   target_id=attrib['to_id'],
                                   target_item=attrib['to_item'],
                                   spatial_interpolation=spatial,
                                   temporal_interpolation=temporal
                                   )

                # this draws the line
                self.createLine(R1, R2)

            self.FloatCanvas.Draw()

    def SetLoadingPath(self, path):
        self.loadingpath = path

    def GetLoadingPath(self):
        return self.loadingpath

    def addModelDialog(self):
        # Note that we need to make sure this passes in information from the model
        # Need to know if we are planning on using this feature or something else.
        dial = wx.MessageDialog(None, 'Added a Model', 'Info', wx.OK)
        dial.ShowModal()

    def getCursor(self):
        return self._Cursor

    def setCursor(self, value=None):
        # print "Cursor was set to value ", dir(value), value.GetHandle()
        self._Cursor = value

    def LaunchContext(self, event):

        # if canvas is selected
        if type(event) == wx.lib.floatcanvas.FloatCanvas._MouseEvent:
            self.PopupMenu(GeneralContextMenu(self), event.GetPosition())

        elif type(event) == wx.lib.floatcanvas.FloatCanvas.Polygon:
            # if object is link
            if event.type == "ArrowHead":
                self.PopupMenu(LinkContextMenu(self, event), event.HitCoordsPixel.Get())

            # if object is model
            elif event.type == 'Model':
                self.PopupMenu(ModelContextMenu(self, event), event.HitCoordsPixel.Get())

                # self.Canvas.ClearAll()
                # self.Canvas.Draw()

    def MenuSelectionCb(self, event):
        # TODO: Fix the menu selection
        operation = menu_title_by_id[event.GetId()]
        # target    = self.list_item_clicked
        print 'DEBUG | Perform "%(operation)s" on "%(target)s."' % vars()

    # THREADME
    def run(self):

        try:
            self.cmd.run_simulation()
        except Exception as e:
            wx.MessageBox(str(e.args[0]), 'Error', wx.OK | wx.ICON_ERROR)


# DELETEME
menu_titles = ["Open",
               "Properties",
               "Rename",
               "Delete"]

menu_title_by_id = {}
for title in menu_titles:
    menu_title_by_id[wx.NewId()] = title
