import math
import textwrap as tw
import sys
import os
import xml.etree.ElementTree as et
from xml.dom import minidom
import uuid

import wx
from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.floatcanvas.NavCanvas import NavCanvas
from wx.lib.pubsub import pub as Publisher
import numpy as N
from matplotlib.pyplot import cm

from gui.views.viewContext import LinkContextMenu, ModelContextMenu, CanvasContextMenu
from transform.space import SpatialInterpolation
from transform.time import TemporalInterpolation
import datatypes
from utilities.threading import EVT_CREATE_BOX, EVT_UPDATE_CONSOLE, ThreadManager
from gui.views.viewCanvas import ViewCanvas
import gui.controller.logicCanvasObjects as LogicCanvasObjects
from gui.controller.logicLink import LogicLink
import coordinator.engineAccessors as engine
import utilities.db as dbUtilities
import coordinator.events as engineEvent
from gui import events
from coordinator.emitLogging import elog

# Not sure if this should be here
# This creates an anti-aliased line
class SmoothLine(FC.Line):
    """
    The SmoothLine class is identical to the Line class except that it uses a
    GC rather than a DC.
    """
    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Points = WorldToPixel(self.Points)
        GC = wx.GraphicsContext.Create(dc)
        GC.SetPen(self.Pen)
        GC.DrawLines(Points)

class LogicCanvas(ViewCanvas):
    def __init__(self, parent):

        # intialize the parent class
        ViewCanvas.__init__(self, parent)

        self.parent = parent

        # This is just to ensure that we are starting without interference from NavToolbar or drag-drop
        self.UnBindAllMouseEvents()

        self.MoveObject = None
        self.Moving = False
        self.linelength = None

        self.initBindings()
        self.initSubscribers()

        defaultCursor = wx.StockCursor(wx.CURSOR_DEFAULT)
        defaultCursor.Name = 'default'
        self._Cursor = defaultCursor

        self.linkRects = []
        self.links = {}
        self.models = {}

        self.link_clicks = 0
        self._currentDbSession = None
        self._dbid = None
        self.loadingpath = None
        self.model_coords = {}
        self.uniqueId = None

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

    def initBindings(self):
        self.FloatCanvas.Bind(FC.EVT_MOTION, self.OnMove)
        self.FloatCanvas.Bind(FC.EVT_LEFT_UP, self.OnLeftUp)
        self.FloatCanvas.Bind(FC.EVT_RIGHT_DOWN, self.LaunchContext)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(EVT_CREATE_BOX, self.onCreateBox)
        self.Bind(EVT_UPDATE_CONSOLE, self.onUpdateConsole)
        self.Bind(wx.EVT_ENTER_WINDOW, self.onEnterWindow)
        self.FloatCanvas.Bind(FC.EVT_ENTER_WINDOW,self.onEnterWindow)

        # engine bindings
        engineEvent.onModelAdded += self.draw_box
        engineEvent.onLinkAdded += self.draw_link
        engineEvent.onSimulationFinished += self.simulation_finished
        events.onDbChanged += self.onDbChanged

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
        Publisher.subscribe(self.OnSetFilepath, 'dragpathsent')

    def OnSetFilepath(self, path):
        self.path = path

    def onEnterWindow(self, event):
        try:
            filenames = self.path
            x,y = event.Position
            if filenames:
                name, ext = os.path.splitext(filenames)

                if ext == '.mdl' or ext == '.sim':
                    originx, originy = self.FloatCanvas.WorldToPixel(self.GetPosition())
                    nx = (x - originx)+300
                    ny = (originy - y)
                    self.addModel(filepath=filenames, x=nx, y=ny)

        except:
            # elog.debug("onEnterWindow() in logicCanvas.py")
            pass
        self.path = None

    def onDbChanged(self, event):
        """
        This function sets current database attributes locally whenever the database is changed
        :param event: gui.controller.events.onDbChanged
        :return: None
        """
        self._currentDbSession = event.dbsession
        self._dbid = event.dbid

    def onClose(self, event):
        dlg = wx.MessageDialog(None, 'Are you sure you want to exit?', 'Question',
                               wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() != wx.ID_NO:

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
        if self.Moving:
            cursorPos = event.GetPosition()
            deltaX = cursorPos.x - self.lastPos.x
            deltaY = self.lastPos.y - cursorPos.y
            dxy = (deltaX,deltaY)

            self.MovingObject.Move(dxy)
            self.MovingObject.Text.Move(dxy)


            for link in self.links.keys():
                r1, r2 = self.links[link]
                if r1 == self.MovingObject:
                    link.Points[0] = self.MovingObject.XY
                elif r2 == self.MovingObject:
                    link.Points[1] = self.MovingObject.XY

            self.lastPos = cursorPos
            self.RedrawConfiguration()
            # self.FloatCanvas.Draw(True)

    def onUpdateConsole(self, evt):
        """
        Updates the output console
        """
        if evt.message:
            elog.debug("DEBUG|", evt.message)

    def onCreateBox(self, evt):
        name = evt.name
        id = evt.id
        x = evt.xCoord
        y = evt.yCoord
        self.createBox(xCoord=x, yCoord=y, id=id, name=name)

    def createBox(self, xCoord, yCoord, id=None, name=None, type=datatypes.ModelTypes.TimeStep):

        # set box color based on model type
        if type == datatypes.ModelTypes.TimeStep:
            color = '#B3DBG6'
            bitmap = self.TimeseriesBox
        elif type == datatypes.ModelTypes.FeedForward:
            color = '#A2CAF5'
            # bitmap = self.ModelsBox
            bitmap = self.UnassignedBox4
        elif type == datatypes.ModelTypes.Data:
            color = '#A2BGA5'
            bitmap = self.DatabaseBox

        if name:
            w, h = 180, 120
            x, y = xCoord, yCoord
            FontSize = 14

            if self.getUniqueId() is not None and type == datatypes.ModelTypes.Data:
                # Strip out last bit of the name (normally includes an id), e.g. "rainfall-5" -> "rainfall"
                sub = name.rfind('-')-name.__len__()
                name = name[:sub]
                name = name.replace("_", "  ")
                name = name + "\n" + "ID = " + self.getUniqueId()

            # get the coordinates for the rounded rectangle
            rect_coords = LogicCanvasObjects.build_rounded_rectangle((x, y), width=w, height=h)

            # R = self.FloatCanvas.AddObject(FC.Polygon(rect_coords, FillColor=color, InForeground=True))
            R = self.FloatCanvas.AddBitmap(bitmap, (x,y), Position="cc", InForeground=True)
            R.ID = id
            R.Name = name
            R.wh = (w, h)
            R.xy = (x, y)

            # set the shape type so that we can identify it later
            R.type = LogicCanvasObjects.ShapeType.Model

            # define the font
            font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

            label = self.FloatCanvas.AddScaledTextBox(unicode(name), (x,y),  # (x+1, y+h/2),
                                                      Color="Black", Size=FontSize, Width=w - 10, Position="cc",
                                                      Alignment="center",
                                                      Weight=wx.BOLD, Style=wx.ITALIC, InForeground=True, Font=font,
                                                      LineWidth=0, LineColor=None)


            # set the type of this object so that we can find it later
            label.type = LogicCanvasObjects.ShapeType.Label

            # add this text as an attribute of the rectangle
            R.Text = label

            elog.info(name + ' has been added to the canvas.')

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
        x1, y1 = (R1.BoundingBox[0] + (R1.wh[0] / 2, R1.wh[1] / 2))
        x2, y2 = (R2.BoundingBox[0] + (R2.wh[0] / 2, R2.wh[1] / 2))
        x1,y1=x1-90,y1-64
        x2,y2=x2-90,y2-64

        cmap = cm.Blues
        line = LogicCanvasObjects.get_line_pts((x1, y1), (x2, y2), order=4, num=200,)
        linegradient = LogicCanvasObjects.get_hex_from_gradient(cmap, len(line))
        linegradient.reverse()

        for i in range(0, len(line) - 1):
            l = FC.Line((line[i], line[i + 1]), LineColor=linegradient[i], LineWidth=2, InForeground=False)
            l.type = LogicCanvasObjects.ShapeType.Link
            self.FloatCanvas.AddObject(l)

        # Calculate length of line, use to show/hide arrow
        self.linelength = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        arrow_shape = self.createArrow(line)

        # store the link and rectangles in the self.links list
        for k, v in self.links.iteritems():
            if v == [R1, R2]:
                self.links.pop(k)
                break
        self.links[arrow_shape] = [R1, R2]

        self.FloatCanvas.Draw()

    def createLineNew(self, R1, R2):
        # Get the center of the objects
        x1,y1 = R1.XY
        x2,y2 = R2.XY
        points = [(x1,y1),(x2,y2)]
        line = SmoothLine(points, LineColor="Blue", LineStyle="Solid", LineWidth=4, InForeground=False)
        self.links[line] = [R1, R2]
        line.type = LogicCanvasObjects.ShapeType.Link

        arrow_shape = self.createArrow(line)
        # Calculate length of line, use to show/hide arrow
        self.linelength = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        arrow_shape = self.createArrow(line)

        self.FloatCanvas.AddObject(line)
        self.FloatCanvas.Draw()

    def createArrow(self, line):

        arrow = LogicCanvasObjects.build_arrow(line, arrow_length=6)

        # create the arrowhead object
        arrow_shape = FC.Polygon(arrow, FillColor='Blue', InForeground=True)
        if self.linelength > 230:
            arrow_shape.Show()
        else:
            arrow_shape.Hide()

        # set the shape type so that we can identify it later
        arrow_shape.type = LogicCanvasObjects.ShapeType.ArrowHead
        self.FloatCanvas.AddObject(arrow_shape)

        # bind the arrow to left click
        arrow_shape.Bind(FC.EVT_FC_LEFT_DOWN, self.ArrowClicked)
        arrow_shape.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)

        return arrow_shape

    def createArrowNew(self, line):

        arrow_shape = self.FloatCanvas.AddScaledBitmap(self.linkArrow,
                                                 (0, 0),
                                                 Height = self.linkArrow.GetHeight(),
                                                 Position = 'tl',)
        # if self.linelength > 230:
        #     arrow_shape.Show()
        # else:
        #     arrow_shape.Hide()

        arrow_shape.Bind(FC.EVT_FC_LEFT_DOWN, self.ArrowClicked)
        arrow_shape.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)

        # create the arrowhead object
        # arrow_shape = FC.Polygon(arrow, FillColor='Blue', InForeground=True)
        # if self.linelength > 230:
        #     arrow_shape.Show()
        # else:
        #     arrow_shape.Hide()

        # set the shape type so that we can identify it later
        arrow_shape.type = LogicCanvasObjects.ShapeType.ArrowHead
        self.FloatCanvas.AddObject(arrow_shape)

        # bind the arrow to left click
        arrow_shape.Bind(FC.EVT_FC_LEFT_DOWN, self.ArrowClicked)
        arrow_shape.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)

        return arrow_shape

    def getUniqueId(self):
        return self.uniqueId

    def addModel(self, filepath, x, y, uid=None, uniqueId = None, title = None):
        """
        Adds a model to the canvas using x,y.  This is useful if adding by file click/dialog
        :param filename:  filename / path
        :param x: x location
        :param y: y location
        :return: None
        """
        if uniqueId is not None:
            self.uniqueId = uniqueId
        if title is not None:
            self.title = title

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
                try:
                    self.loadsimulation(filepath)
                except Exception, e:
                    elog.error('Configuration failed to load: %s'%e.message)
                    # dlg = wx.MessageDialog(None, 'Configuration failed to load', 'Error', wx.OK)
                    # dlg.ShowModal()
        else:
            # load data model
            # current_db_id = self._currentDb['id']
            # attrib = dict(databaseid=current_db_id, resultid=name)

            attrib = dict(databaseid=self._dbid, resultid=name)
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
                    elog.error('ERROR|Could not remove link: %s' % link['id'])

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
            self.models.pop(model_obj)

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

            # get the model object from the engine
            obj_id = object.ID
            model = engine.getModelById(obj_id)


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
            self.lastPos = object.HitCoordsPixel

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

    def ArrowClicked(self, event):

        # get the models associated with the link
        models = self.links[event]

        # get r1 and r2
        r1 = models[0]
        r2 = models[1]

        # get output items from r1
        from_model = engine.getModelById(r1.ID)

        # get output items from r1
        to_model = engine.getModelById(r2.ID)

        linkstart = LogicLink(self.FloatCanvas, from_model, to_model)

        linkstart.Show()


    def RedrawConfiguration(self):
        # clear lines from drawlist
        self.FloatCanvas._DrawList = [obj for obj in self.FloatCanvas._DrawList if
                                      obj.type != LogicCanvasObjects.ShapeType.Link]

        # remove any arrowheads from the _ForeDrawList
        self.FloatCanvas._ForeDrawList = [obj for obj in self.FloatCanvas._ForeDrawList if
                                          obj.type != LogicCanvasObjects.ShapeType.ArrowHead]

        # remove any models
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

    def OnLeftUp(self, event, path=None):

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

        kwargs = dict(title=title, desc=desc, engine=dbengine, address=address, name=name, user=user, pwd=pwd)
        engine.connectToDb(**kwargs)

    def DetailView(self):
        # DCV.ShowDetails()
        pass

    def SaveSimulation(self, path):

        if len(self.models.keys()) == 0:
            elog.warning('WARNING | Nothing to save!')
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
            elog.error('ERROR | An error occurred when attempting to save the project ')
            elog.error('ERROR | EXECPTION MESSAGE ')
            elog.error(e)

        elog.info('Configuration Saved Successfully! ')

    def appendChild(self, child):
        taglist = []
        textlist = []
        for data in child:
            textlist.append(data.text)
            taglist.append(data.tag)

        attrib = dict(zip(taglist, textlist))
        return attrib

    def loadsimulation(self, file):

        # TODO: This needs to be refactored to remove 'for' looping
        tree = et.parse(file)

        self.loadingpath = file

        tree = et.parse(file)

        # get the root
        root = tree.getroot()

        # make sure the required database connections are loaded
        connections = engine.getDbConnections()
        conn_ids = {}

        # get all known transformations
        space = SpatialInterpolation()
        time = TemporalInterpolation()
        spatial_transformations = {i.name(): i for i in space.methods()}
        temporal_transformations = {i.name(): i for i in time.methods()}


        for child in root._children:
            if child.tag == 'DbConnection':
                attrib = self.appendChild(child)

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

            if child.tag == 'Model':
                attrib = self.appendChild(child)

                # load the model
                self.addModel(filepath=attrib['path'], x=float(attrib['xcoordinate']), y=float(attrib['ycoordinate']),
                              uid=attrib['id'])

            if child.tag == 'DataModel':
                attrib = self.appendChild(child)

                databaseid = attrib['databaseid']
                mappedid = conn_ids[databaseid]

                attrib['databaseid'] = mappedid
                modelid = self.addModel(filepath=attrib['path'], x=attrib['xcoordinate'], y=attrib['ycoordinate'],
                                        uid=attrib['id'])

            # todo: Link cannot be added until both models have finished loading!!!  This will throw exception on line 927
            if child.tag == 'Link':
                attrib = self.appendChild(child)

                R1 = None
                R2 = None
                for R, id in self.models.iteritems():
                    if id == attrib['from_id']:
                        R1 = R
                    elif id == attrib['to_id']:
                        R2 = R

                if R1 is None or R2 is None:
                    raise Exception('Could not find Model identifier in loaded models')

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

    def getCursor(self):
        return self._Cursor

    def setCursor(self, value=None):
        self._Cursor = value

    def LaunchContext(self, event):

        # if canvas is selected
        if type(event) == wx.lib.floatcanvas.FloatCanvas._MouseEvent:
            self.PopupMenu(CanvasContextMenu(self), event.GetPosition())

        elif type(event) == wx.lib.floatcanvas.FloatCanvas.Bitmap:
            # if object is link
            if event.type == "ArrowHead":
                self.PopupMenu(LinkContextMenu(self, event), event.HitCoordsPixel.Get())

            # if object is model
            elif event.type == 'Model':
                self.PopupMenu(ModelContextMenu(self, event), event.HitCoordsPixel.Get())

        elif type(event) == wx.lib.floatcanvas.FloatCanvas.Polygon:
            if event.type == "ArrowHead":
                self.PopupMenu(LinkContextMenu(self, event), event.HitCoordsPixel.Get())


    # THREADME
    def run(self):

        try:
            # self.cmd.run_simulation()
            engine.runSimulation()
        except Exception as e:
            wx.MessageBox(str(e.args[0]), 'Error', wx.OK | wx.ICON_ERROR)


    def simulation_finished(self, evt):
        # todo: this should open a dialog box showing the execution summary
        elog.info('Simulation finished')

# DELETEME
menu_titles = ["Open",
               "Properties",
               "Rename",
               "Delete"]

menu_title_by_id = {}
for title in menu_titles:
    menu_title_by_id[wx.NewId()] = title
