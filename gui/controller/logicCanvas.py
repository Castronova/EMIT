import math
import textwrap as tw
import sys
import os
import xml.etree.ElementTree as et
from xml.dom import minidom
import uuid
import threading, time
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
from gui.controller.logicCanvasObjects import SmoothLineWithArrow
from gui.controller.logicLink import LogicLink
import coordinator.engineAccessors as engine
import utilities.db as dbUtilities
import coordinator.events as engineEvent
from gui import events
from coordinator.emitLogging import elog


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
        self.arrows = {}
        self.models = {}
        self.pairedModels = []

        self.link_clicks = 0
        self._currentDbSession = None
        self._dbid = None
        self.loadingpath = None
        self.model_coords = {}
        self.uniqueId = None
        self.defaultLoadDirectory = os.getcwd() + "/models/MyConfigurations/"

        # todo: implement a method to keep track of the models that fail loading.  A failed model event must be fired inside the engine
        self.failed_models = 0
        self.logicCanvasThreads = {}

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
        # self.Bind(wx.EVT_CLOSE, self.onClose) todo: delete this
        # self.Bind(EVT_CREATE_BOX, self.onCreateBox) todo: delete this
        self.Bind(EVT_UPDATE_CONSOLE, self.onUpdateConsole)
        # self.Bind(wx.EVT_ENTER_WINDOW, self.onEnterWindow) todo: delete this
        # self.FloatCanvas.Bind(FC.EVT_ENTER_WINDOW,self.onEnterWindow) todo: delete this

        # engine bindings
        engineEvent.onModelAdded += self.draw_box
        engineEvent.onLinkAdded += self.draw_link
        engineEvent.onSimulationFinished += self.simulation_finished
        events.onDbChanged += self.onDbChanged

    def initSubscribers(self):
        # Publisher.subscribe(self.createBox, "createBox") todo: delete this
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

    # def onEnterWindow(self, event):  # todo: Delete this
    #     try:
    #         filenames = self.path
    #         x,y = event.Position
    #         if filenames:
    #             name, ext = os.path.splitext(filenames)
    #
    #             if ext == '.mdl' or ext == '.sim':
    #                 originx, originy = self.FloatCanvas.WorldToPixel(self.GetPosition())
    #                 nx = (x - originx)+300
    #                 ny = (originy - y)
    #                 self.addModel(filepath=filenames, x=nx, y=ny)
    #
    #     except:
    #         # elog.debug("onEnterWindow() in logicCanvas.py")
    #         pass
    #     self.path = None

    def onDbChanged(self, event):
        """
        This function sets current database attributes locally whenever the database is changed
        :param event: gui.controller.events.onDbChanged
        :return: None
        """
        self._currentDbSession = event.dbsession
        self._dbid = event.dbid

    # todo: Delete this
    # def onClose(self, event):
    #     dlg = wx.MessageDialog(None, 'Are you sure you want to exit?', 'Question',
    #                            wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
    #
    #     if dlg.ShowModal() != wx.ID_NO:
    #
    #         windowsRemaining = len(wx.GetTopLevelWindows())
    #         if windowsRemaining > 0:
    #             import wx.lib.agw.aui.framemanager as aui
    #
    #             for item in wx.GetTopLevelWindows():
    #                 if not isinstance(item, self.frame.__class__):
    #                     if isinstance(item, aui.AuiFloatingFrame):
    #                         item.Destroy()
    #                     elif isinstance(item, aui.AuiSingleDockingGuide):
    #                         item.Destroy()
    #                     elif isinstance(item, aui.AuiDockingHintWindow):
    #                         item.Destroy()
    #                     elif isinstance(item, wx.Dialog):
    #                         item.Destroy()
    #                     item.Close()
    #
    #         self.frame.Destroy()
    #         wx.GetApp().ExitMainLoop()
    #
    #     else:
    #         pass

    def OnMove(self, event):
        if self.Moving:
            cursorPos = event.GetPosition()
            # The following keeps the box within the canvas
            # Right
            if cursorPos.x < self.boxBoundaries[0]:
                cursorPos.x = self.boxBoundaries[0]
            # Left
            elif cursorPos.x > self.Size.x - self.boxBoundaries[1]:
                cursorPos.x = self.Size.x - self.boxBoundaries[1]
            # Top
            if cursorPos.y < self.boxBoundaries[2]:
                cursorPos.y = self.boxBoundaries[2]
            # Bottom
            elif cursorPos.y > self.Size.y - self.boxBoundaries[3]:
                cursorPos.y = self.Size.y - self.boxBoundaries[3]

            deltaX = cursorPos.x - self.lastPos.x
            deltaY = self.lastPos.y - cursorPos.y
            dxy = (deltaX, deltaY)

            # This moves the boxes and the label together
            self.MovingObject.Move(dxy)
            self.MovingObject.Text.Move(dxy)

            # Iterate through all links on the canvas
            for link in self.links.keys():
                link.Arrow.Rotate(link.GetAngleRadians())

                # Grab both boxes on the ends of the line/link
                # Update their endpoints and set the arrow to the center of the line
                r1, r2 = self.links[link]
                if r1 == self.MovingObject:
                    link.Points[0] = self.MovingObject.XY
                    link.Arrow.XY = link.MidPoint
                elif r2 == self.MovingObject:
                    link.Points[1] = self.MovingObject.XY
                    link.Arrow.XY = link.MidPoint

            self.lastPos = cursorPos
            self.FloatCanvas.Draw(True)

    def onUpdateConsole(self, evt):
        """
        Updates the output console
        """
        if evt.message:
            elog.debug("DEBUG|", evt.message)


    # def onCreateBox(self, evt):  # todo: delete this
    #     name = evt.name
    #     id = evt.id
    #     x = evt.xCoord
    #     y = evt.yCoord
    #     self.createBox(xCoord=x, yCoord=y, id=id, name=name)

    def createBox(self, xCoord, yCoord, id=None, name=None, type=datatypes.ModelTypes.TimeStep):

        # set box color based on model type
        if type == datatypes.ModelTypes.TimeStep:
            color = '#B3DBG6'
            bitmap = self.TimeseriesBox
        elif type == datatypes.ModelTypes.FeedForward:
            color = '#A2CAF5'
            # bitmap = self.ModelsBox
            bitmap = self.UnassignedBox4
            # bitmap = bitmap.AdjustChannels(factor_red=1.0, factor_green=1.0, factor_blue=1.0, factor_alpha=0.5)
        elif type == datatypes.ModelTypes.Data:
            color = '#A2BGA5'
            bitmap = self.DatabaseBox

        if name:
            w, h = 221, 141
            x, y = xCoord, yCoord
            FontSize = 15

            if self.getUniqueId() is not None and type == datatypes.ModelTypes.Data:
                # Strip out last bit of the name (normally includes an id), e.g. "rainfall-5" -> "rainfall"
                sub = name.rfind('-')-name.__len__()
                name = name[:sub]
                name = name.replace("_", "  ")
                name = name + "\n" + "ID = " + self.getUniqueId()

            # boxBitmap = ScaledBitmapWithRotation(bitmap, (x,y), Height=h, Position='cc', InForeground=True)
            # R = self.FloatCanvas.AddObject(boxBitmap)
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
            elog.debug(name + ' has been added to the canvas.')

            R.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)
            R.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)
            self.models[R] = id
            # self.FloatCanvas.AddObject(R)
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
            elog.warning("Could not find Model identifier in loaded models")
            raise Exception('Could not find Model identifier in loaded models')

        # this draws the line
        self.createLine(R1, R2)

    def set_model_coords(self, id, x, y):

        self.model_coords[id] = {'x': x, 'y': y}

    def get_model_coords(self, id):

        return (self.model_coords[id]['x'], self.model_coords[id]['y'])

    def createLine(self, R1, R2):

        if R1 == R2:
            elog.error('Cannot link a model to itself')
            return
        else:

            # Get the center of the objects on the canvas
            x1,y1 = R1.XY
            x2,y2 = R2.XY
            points = [(x1,y1),(x2,y2)]
            # line = SmoothLine(points, LineColor="Blue", LineStyle="Solid", LineWidth=4, InForeground=False)
            line = SmoothLineWithArrow(points, self.linkArrow)
            self.links[line] = [R1, R2]
            self.arrows[line.Arrow] = [R1, R2]
            self.pairedModels.append([R1.Name, R2.Name])
            line.type = LogicCanvasObjects.ShapeType.Link

            line.Arrow.type = LogicCanvasObjects.ShapeType.ArrowHead
            # Calculate length of line, use to show/hide arrow
            self.linelength = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
            self.FloatCanvas.AddObject(line)

            # For some reason we have to add line.Arrow in order to bind to it
            self.FloatCanvas.AddObject(line.Arrow)

            # We need to add this since we're binding to line's attribute and not
            # the line itself. This fixed an issue seen in the last commit from 7/15/2015
            # line.Arrow.line = line

            line.Arrow.Bind(FC.EVT_FC_LEFT_DOWN, self.ArrowClicked)
            line.Arrow.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)
            # line.Bind(FC.EVT_FC_LEFT_DOWN, self.ArrowClicked)
            # line.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)

            self.FloatCanvas.Draw()

    # todo: Delete this
    # def createArrow(self, line):
    #
    #     print "adding arrow to ", line.MidPoint
    #     angle = line.GetAngleRadians()
    #     arrow_shape = ScaledBitmapWithRotation(self.linkArrow, line.MidPoint, Angle=angle, Position='tl', InForeground=True)
    #
    #     # set the shape type so that we can identify it later
    #     arrow_shape.type = LogicCanvasObjects.ShapeType.ArrowHead
    #     self.FloatCanvas.AddObject(arrow_shape)
    #
    #     # bind the arrow to left click
    #     arrow_shape.Bind(FC.EVT_FC_LEFT_DOWN, self.ArrowClicked)
    #     arrow_shape.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)
    #
    #     return arrow_shape

    def getUniqueId(self):
        return self.uniqueId

    def addModel(self, filepath, x, y, uid=None, uniqueId=None, title=None):
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
        else:
            #  Model is from a database
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

            self.RemovePairedLinkList(link)

            # get the link id
            links = engine.getLinksBtwnModels(from_id, to_id)

            # remove all links
            for link in links:
                success = engine.removeLinkById(link['id'])
                if not success:
                    elog.error('ERROR|Could not remove link: %s' % link['id'])

            # Using SmoothLineWithArrow's builtin remove helper function
            link_obj.Remove(self.FloatCanvas)
            self.FloatCanvas.Draw()

    def RemovePairedLinkList(self, link):
        self.pairedModels.remove([link[0].Name, link[1].Name])

    def RemoveModel(self, model_obj):
        """
        Removes a model component from the modeling canvas
        :param model_obj: model object that will be removed
        :return: None
        """

        updated_links = {}
        links_to_remove = []
        for link, models in self.links.iteritems():
            if model_obj in models:
                links_to_remove.append(link)
                self.RemovePairedLinkList(models)
            elif model_obj not in models:
                updated_links[link] = models

        self.links = updated_links

        # Remove the model from the engine
        engine.removeModelById(model_obj.ID)

        if not engine.getModelById(model_obj.ID):  # If the link no longer exists
            # Update models list
            self.models.pop(model_obj)

            # Remove selected model and text box from FloatCanvas
            self.FloatCanvas.RemoveObjects([model_obj, model_obj.Text])
            # Remove the model's SmoothLineWithArrow obj with builtin remove function
            for link in links_to_remove:
                link.Remove(self.FloatCanvas)

            self.FloatCanvas.Draw()

    def clear(self, link_obj=None, model_obj=None):

        # clear links and models in the engine
        success = engine.clearAll()

        if success:
            # clear links and model in gui
            self.links.clear()
            self.models.clear()
            self.pairedModels = []
            self.FloatCanvas.ClearAll()
            self.FloatCanvas.Draw()

    def ObjectHit(self, object):
        cur = self.getCursor()

        if cur.Name == 'link':
            self.linkRects.append(object)

        # todo: Delete this, this was breaking many things
        # populate model view
        # if cur.Name == 'default':
        #
        #     # get the model object from the engine
        #     obj_id = object.ID
        #     model = engine.getModelById(obj_id)

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

            mouse = self.ScreenToClient(wx.GetMousePosition().Get())
            mouseCenterOrigin = self.FloatCanvas.PixelToWorld(mouse)
            distFromCenter = mouseCenterOrigin - self.MovingObject.XY
            overlap = 40
            # Order: X-left, X-right, Y-top, Y-bottom
            self.boxBoundaries = N.array([self.MovingObject.Width/2 + distFromCenter[0],
                                    self.MovingObject.Width/2 - distFromCenter[0],
                                    self.MovingObject.Height/2 - distFromCenter[1],
                                    self.MovingObject.Height/2 + distFromCenter[1]]) - overlap

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
        bidirectional = False

        # get the models associated with the link
        models = self.arrows[event]

        # get r1 and r2
        r1 = models[0]
        r2 = models[1]

        # get output items from r1
        from_model = engine.getModelById(r1.ID)

        # get output items from r1
        to_model = engine.getModelById(r2.ID)

        if len(self.links) > 1:
            bidirectional = self.CheckIfBidirectionalLink(r1.Name, r2.Name)

        linkstart = LogicLink(self.FloatCanvas, from_model, to_model, bidirectional)
        linkstart.Show()

    def CheckIfBidirectionalLink(self, r1, r2):
        count = 0
        for pair in self.pairedModels:
            if r1 in pair and r2 in pair:
                count += 1

        if count >= 2:
            return True
        else:
            return False

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

    # todo: Delete this
    # def DetailView(self):
    #     DCV.ShowDetails()
    #     pass

    def SaveSimulation(self, path):

        if len(self.models.keys()) == 0:
            elog.warning('Nothing to save!')
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
            elog.error('An error occurred when attempting to save the project ')
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


        # TODO: This needs to be refactored to remove 'for' looping!
        for child in root._children:
            if child.tag == 'DbConnection':
                attrib = self.appendChild(child)

                connection_string = attrib['connection_string']

                database_exists = False
                # db_elements = db_conn.getchildren()

                for id, dic in connections.iteritems():
                    try:
                        if str(dic['args']['connection_string']) == connection_string:
                            # dic['args']['id'] = db_conn.attrib['id']
                            database_exists = True

                            # map the connection ids
                            conn_ids[attrib['databaseid']] = dic['args']['id']
                            break
                    except Exception, e:
                        elog.error(e.message)

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

        models = tree.findall("./Model")  # Returns a list of all models in the file
        datamodels = tree.findall("./DataModel")  # Returns a list of all data models in the file
        links = tree.findall("./Link")  # Returns a list of all links in the file
        transform = tree.findall("./transformation")
        total = len(models) + len(datamodels) + len(self.models) + self.failed_models

        elog.debug("There are " + str(total) + " models in the file")
        waitingThread = threading.Thread(target=self.waiting, args=(total, links, transform, temporal_transformations, spatial_transformations), name="LoadLinks")
        self.logicCanvasThreads[waitingThread.name] = waitingThread
        waitingThread.start()

        #  Models from database and non database will load async.
        t1 = threading.Thread(target=self.LoadModels, args=(models,), name="LoadModels")
        self.logicCanvasThreads[t1.name] = t1
        t1.start()

        t2 = threading.Thread(target=self.LoadDataModels, args=(datamodels, conn_ids,), name="LoadDataModel")
        self.logicCanvasThreads[t2.name] = t2
        t2.start()



    def waiting(self, total, links, transform, temporal_transformations, spatial_transformations):
        #  This method waits for all the models in the file to be loaded before linking
        elog.info("Waiting for all models to be loaded before creating link")
        while len(self.models) < total:
            time.sleep(0.5)
        self.LoadLinks(links, transform, temporal_transformations, spatial_transformations)
        elog.debug(str(len(self.models)) + " were models loaded")
        return

    def LoadModels(self, models):
        for model in models:
            attrib = self.appendChild(model)
            self.addModel(filepath=attrib['path'], x=float(attrib['xcoordinate']), y=float(attrib['ycoordinate']),
                              uid=attrib['id'])
        wx.CallAfter(self.FloatCanvas.Draw)

    def LoadDataModels(self, datamodels, conn_ids):
        for model in datamodels:
            attrib = self.appendChild(model)

            # Swapping the database id with conn_ids
            attrib['databaseid'] = conn_ids[attrib['databaseid']]
            self._dbid = attrib['databaseid']

            self.addModel(filepath=attrib['resultid'], x=float(attrib['xcoordinate']),
                              y=float(attrib['ycoordinate']),  uid=attrib['databaseid'],
                              title=attrib['name'], uniqueId=attrib['resultid'])
        wx.CallAfter(self.FloatCanvas.Draw)

    def LoadLinks(self, links, transformation, temp_trans, spat_trans):
        for link in links:
            attrib = self.appendChild(link)

            R1, R2 = None, None  # Rename R1 to From Model and R2 to To Model
            for key, value in self.models.iteritems():
                if value == attrib['from_id']:
                        R1 = key
                elif value == attrib['to_id']:
                        R2 = key
            if R1 is None or R2 is None:
                # raise Exception('Could not find Model identifier in loaded models')
                elog.error("Could not find model id in loaded models")
                return

            temporal = None
            spatial = None
            # set the temporal and spatial interpolation
            for transform_child in transformation:
                    if transform_child.text.upper() != 'NONE':
                        if transform_child.tag == 'temporal':
                            temporal = temp_trans[transform_child.text]
                        elif transform_child.tag == 'spatial':
                            spatial = spat_trans[transform_child.text]

            # create the link
            l = engine.addLink(source_id=attrib['from_id'],
                               source_item=attrib['from_item'],
                               target_id=attrib['to_id'],
                               target_item=attrib['to_item'],
                               spatial_interpolation=spatial,
                               temporal_interpolation=temporal
                               )

            # this draws the line
            wx.CallAfter(self.createLine, R1, R2)

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

        elif type(event) == LogicCanvasObjects.ScaledBitmapWithRotation:
            # if object is link
            # event should be SmoothLineWithArrow...
            if event.type == "ArrowHead":
                self.PopupMenu(LinkContextMenu(self, event.line), event.HitCoordsPixel.Get())

        elif type(event) == wx.lib.floatcanvas.FloatCanvas.Bitmap:
            # if object is model
            if event.type == "Model":
                self.PopupMenu(ModelContextMenu(self, event), event.HitCoordsPixel.Get())

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

# todo: DELETEME
menu_titles = ["Open",
               "Properties",
               "Rename",
               "Delete"]

menu_title_by_id = {}
for title in menu_titles:
    menu_title_by_id[wx.NewId()] = title
