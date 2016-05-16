import random
import threading
import time
import uuid
import xml.etree.ElementTree as et
from xml.dom import minidom

import numpy as N
import wx
from wx.lib.floatcanvas import FloatCanvas as FC
from wx.lib.floatcanvas.NavCanvas import NavCanvas
from wx.lib.pubsub import pub as Publisher

import coordinator.engineAccessors as engine
import coordinator.events as engineEvent
import datatypes
import gui.controller.CanvasObjectsCtrl as LogicCanvasObjects
import utilities.db as dbUtilities
from emitLogging import elog
from gui import events
from gui.controller.CanvasObjectsCtrl import SmoothLineWithArrow, ModelBox
from gui.controller.LinkCtrl import LinkCtrl
from gui.views.CanvasView import CanvasView
from gui.views.ContextView import LinkContextMenu, ModelContextMenu #, CanvasContextMenu
from sprint import *
from transform.space import SpatialInterpolation
from transform.time import TemporalInterpolation
from gui.controller.PreRunCtrl import PreRunCtrl


class CanvasCtrl(CanvasView):
    def __init__(self, parent):

        # intialize the parent class
        CanvasView.__init__(self, parent)

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
        self.arrows = {}
        self.models = {}

        self.link_clicks = 0
        self._currentDbSession = None
        self._dbid = None
        self.model_coords = {}
        self.uniqueId = None
        self.defaultLoadDirectory = os.getcwd() + "/models/MyConfigurations/"

        self.failed_models = 0
        self.logicCanvasThreads = {}

        # Canvas Pop up menu
        self.popup_menu = wx.Menu()
        add_link_menu = self.popup_menu.Append(1, "Add Link")
        load_menu = self.popup_menu.Append(2, "Load")
        save_menu = self.popup_menu.Append(3, "Save Configuration")
        save_as_menu = self.popup_menu.Append(4, "Save Configuration As")
        run_menu = self.popup_menu.Append(5, "Run")
        clear_menu = self.popup_menu.Append(6, "Clear Configuration")

        # Context menu bindings
        self.Bind(wx.EVT_MENU, self.on_add_link, add_link_menu)
        self.Bind(wx.EVT_MENU, self.on_load, load_menu)
        self.Bind(wx.EVT_MENU, self.on_save, save_menu)
        self.Bind(wx.EVT_MENU, self.on_save_as, save_as_menu)
        self.Bind(wx.EVT_MENU, self.on_run, run_menu)
        self.Bind(wx.EVT_MENU, self.on_clear_canvas, clear_menu)
        self.FloatCanvas.Bind(FC.EVT_RIGHT_DOWN, self.on_canvas_right_click)

    def on_canvas_right_click(self, event):
        self.enable_all_context_menu()
        self.disable_some_context_menu_items()
        self.PopupMenu(self.popup_menu, event.GetPosition())

    def disable_some_context_menu_items(self):
        """
        When there are no models on the canvas disable everything but load
        When there is one model on the canvas enable everything but Add Link and Run
        When there are two or more models on the canvas enable everything
        :return:
        """
        if len(self.models) <= 1:
            self.popup_menu.GetMenuItems()[0].Enable(False)
            if len(self.models) <= 0:
                self.popup_menu.GetMenuItems()[2].Enable(False)
                self.popup_menu.GetMenuItems()[3].Enable(False)
                self.popup_menu.GetMenuItems()[5].Enable(False)

        if len(self.links) <= 0:
            self.popup_menu.GetMenuItems()[4].Enable(False)

    def enable_all_context_menu(self):
        for item in self.popup_menu.GetMenuItems():
            item.Enable()

    def on_add_link(self, event):
        self.FloatCanvas.SetMode(self.GuiLink)

    def on_load(self, event):
        self.GetTopLevelParent().on_load_configuration(event)

    def on_save(self, event):
        self.GetTopLevelParent().on_save_configuration(event)

    def on_save_as(self, event):
        self.GetTopLevelParent().on_save_configuration_as(event)

    def on_run(self, event):
        pre_run = PreRunCtrl(self)
        pre_run.Show()

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
        # self.FloatCanvas.Bind(FC.EVT_RIGHT_DOWN, self.LaunchContext)

        # engine bindings
        engineEvent.onModelAdded += self.draw_box
        engineEvent.onLinkAdded += self.draw_link
        engineEvent.onSimulationFinished += self.simulation_finished
        events.onDbChanged += self.onDbChanged

    def initSubscribers(self):
        Publisher.subscribe(self.setCursor, "setCursor")
        Publisher.subscribe(self.run, "run")
        # Publisher.subscribe(self.on_clear_canvas, "clear")
        Publisher.subscribe(self.AddDatabaseConnection, "DatabaseConnection")
        Publisher.subscribe(self.SaveSimulation, "SetSavePath")
        Publisher.subscribe(self.loadsimulation, "SetLoadPath")
        Publisher.subscribe(self.addModel, "AddModel")  # subscribes to object list view
        Publisher.subscribe(self.OnSetFilepath, 'dragpathsent')

    def OnSetFilepath(self, path):
        self.path = path

    def onDbChanged(self, event):
        """
        This function sets current database attributes locally whenever the database is changed
        :param event: gui.controller.events.onDbChanged
        :return: None
        """
        self._currentDbSession = event.dbsession
        self._dbid = event.dbid

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

            # This is what allows us to the FloatCanvas Move function
            deltaX = cursorPos.x - self.lastPos.x
            deltaY = self.lastPos.y - cursorPos.y
            dxy = (deltaX, deltaY)

            # This lets us move the boxes very easily easily
            self.MovingObject.Move(dxy)

            # Iterate through all links on the canvas
            # TODO: ModelBox objects contain an unimplemented Links attribute.
            # TODO: Iterate over that with self.MovingObject.Links exactly like below
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

    def createBox(self, xCoord, yCoord, id=None, name=None, type=datatypes.ModelTypes.TimeStep):

        if name:
            x, y = xCoord, yCoord

            if self.getUniqueId() is not None and type == datatypes.ModelTypes.Data:
                # Strip out last bit of the name (normally includes an id), e.g. "rainfall-5" -> "rainfall"
                sub = name.rfind('-')-name.__len__()
                name = name[:sub]
                name = name.replace("_", "  ")
                name = name + "\n" + "ID = " + self.getUniqueId()

            model_box = ModelBox(type, (x,y), name, id)
            self.FloatCanvas.AddObject(model_box)
            self.models[model_box] = id

            model_box.Bind(FC.EVT_FC_LEFT_DOWN, self.ObjectHit)
            model_box.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)
            self.FloatCanvas.Draw()

            elog.info(name + ' has been added to the canvas.')
            sPrint(name + ' has been added to the canvas.')

    def draw_box(self, evt):

        x, y = self.get_model_coords(id=evt.id)
        self.createBox(name=evt.name, id=evt.id, xCoord=x, yCoord=y, type=evt.model_type)

    def draw_link(self, evt):

        R1 = None
        R2 = None
        for R, id in self.models.iteritems():
            if id == evt.source_id:
                R1 = R
            elif id == evt.target_id:
                R2 = R

        if R1 is None or R2 is None:
            elog.warning("Could not find Model identifier in loaded models")
            sPrint("Could not find Model identifier in loaded models", MessageType.WARNING)
            raise Exception('Could not find Model identifier in loaded models')

        # This is what actually draws the line
        self.createLine(R1, R2)

    def set_model_coords(self, id, x, y):
        self.model_coords[id] = {'x': x, 'y': y}

    def get_model_coords(self, id):
        if id in self.model_coords:
            return (self.model_coords[id]['x'], self.model_coords[id]['y'])
        else:
            x = random.randint(-200, 200)
            y = random.randint(-200, 200)
            self.model_coords[id] = dict(x=x, y=y)
            return x, y


    def createLine(self, R1, R2, image_name="questionMark.png"):
        if R1 == R2:
            elog.error('Cannot link a model to itself')
            sPrint('Cannot link a model to itself', MessageType.ERROR)
            return
        else:

            # image_name = ''

            # Get the center of the objects on the canvas
            x1, y1 = R1.XY
            x2, y2 = R2.XY
            points = [(x1, y1), (x2, y2)]

            # No link between the two models add the first
            line = SmoothLineWithArrow(points, image_name=image_name)

            self.links[line] = [R1, R2]
            self.arrows[line.Arrow] = [R1, R2]
            line.type = LogicCanvasObjects.ShapeType.Link

            line.Arrow.type = LogicCanvasObjects.ShapeType.ArrowHead
            # Calculate length of line, use to show/hide arrow
            self.FloatCanvas.AddObject(line)

            # For some reason we have to add line.Arrow in order to bind to it
            self.FloatCanvas.AddObject(line.Arrow)
            line.Arrow.PutInBackground()

            line.Arrow.Bind(FC.EVT_FC_LEFT_DOWN, self.ArrowClicked)
            line.Arrow.Bind(FC.EVT_FC_RIGHT_DOWN, self.LaunchContext)

            self.FloatCanvas.Draw()

    def getUniqueId(self):
        return self.uniqueId

    def is_link_bidirectional(self, id1, id2):
        for pair in self.links.values():
            # get the ids of the models in this link pair
            pair_ids = [pair[0].ID, pair[1].ID]
            if id1 in pair_ids and id2 in pair_ids:
                return True

        return False

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
            uid = uuid.uuid4().hex

        # save these coordinates for drawing once the model is loaded
        self.set_model_coords(uid, x=x, y=y)

        if ext == '.mdl' or ext == '.sim':

            if ext == '.mdl':
                print 'ADDING MODEL'
                # load the model within the engine process
                engine.addModel(id=uid, attrib={'mdl': filepath})

            elif ext == '.sim':
                # load the simulation
                try:
                    self.loadsimulation(filepath)
                except Exception, e:
                    elog.error('Configuration failed to load: %s'%e.message)
                    sPrint('Configuration failed to load: %s'%e.message, MessageType.ERROR)
        else:
            #  Model is from a database
            attrib = dict(databaseid=self._dbid, resultid=name)
            engine.addModel(id=uid, attrib=attrib)

        return uid

    def remove_link(self, link_obj):

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
                    sPrint('ERROR|Could not remove link: %s' % link['id'], MessageType.ERROR)

            links = engine.getLinksBtwnModels(to_id, from_id)

            # Doing this a second time to remove bidirectional links
            for link in links:
                success = engine.removeLinkById(link['id'])
                if not success:
                    elog.error('ERROR|Could not remove link: %s' % link['id'])
                    sPrint('ERROR|Could not remove link: %s' % link['id'], MessageType.ERROR)

            self.remove_link_image(link_object=link_obj)
            self.remove_link_object_by_id(from_id, to_id)

    def remove_link_object_by_id(self, id1, id2):
        for key, value in self.links.items():
            if (value[0].ID == id1 and value[1].ID == id2) or (value[1].ID == id1 and value[0].ID == id2):
                del self.links[key]

        for key, value in self.arrows.items():
            if (value[0].ID == id1 and value[1].ID == id2) or (value[1].ID == id1 and value[0].ID == id2):
                del self.arrows[key]

    def remove_link_image(self, link_object):
        # Using SmoothLineWithArrow's builtin remove helper function
        link_object.Remove(self.FloatCanvas)
        self.FloatCanvas.Draw()

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
            elif model_obj not in models:
                updated_links[link] = models

        self.links = updated_links

        engine.removeModelById(model_obj.ID)
        # engine.removeModelById is using deprecated functions and returns None, however the link is being removed.
        # to prevent issues with the drawing the if statement makes sure the link no longer exists in the engine
        if not engine.getModelById(model_obj.ID):

            try:
                # Update models list
                self.models.pop(model_obj)

                # Remove selected model and text box from FloatCanvas
                self.FloatCanvas.RemoveObjects([model_obj])
            except Exception, e:
                msg = 'Encountered and error when removing model from canvas: %s' % e
                sPrint(msg, MessageType.ERROR)

            try:

                # Remove the model's SmoothLineWithArrow obj with builtin remove function
                for link in links_to_remove:
                    # remove the link object from the DrawList if it exists.  It may not exist in the DrawList for bidirectional links.
                    if link in self.FloatCanvas._DrawList:
                        link.Remove(self.FloatCanvas)
            except Exception, e:
                msg = 'Encountered and error when removing link from canvas: %s' % e
                sPrint(msg, MessageType.ERROR)

            self.FloatCanvas.Draw()

    def on_clear_canvas(self, event):
        print "Clear canvas called"
        # clear links and models in the engine
        success = engine.clearAll()

        if success:
            # clear links and model in gui
            self.links.clear()
            self.models.clear()
            self.FloatCanvas.ClearAll()
            self.FloatCanvas.Draw()

    def ObjectHit(self, object):
        cur = self.getCursor()

        # TODO: Not sure if this is and above used for anything
        if cur.Name == 'link':
            self.linkRects.append(object)

        if not self.Moving:

            self.Moving = True
            self.StartPoint = object.HitCoordsPixel

            BB = object.box.BoundingBox
            OutlinePoints = N.array(
                ((BB[0, 0], BB[0, 1]), (BB[0, 0], BB[1, 1]), (BB[1, 0], BB[1, 1]), (BB[1, 0], BB[0, 1]),))
            self.StartObject = self.FloatCanvas.WorldToPixel(OutlinePoints)
            self.MoveObject = None
            self.MovingObject = object

            # This is so we can calculate a mouse movement delta that will be used in the OnMove() function above
            self.lastPos = object.HitCoordsPixel

            # Now we get the distance from the click to the edges of the model box
            # This is stored as a numpy array, and overlap is what sets how far the
            # edges of boxes can be dragged across the borders.
            mouse = self.ScreenToClient(wx.GetMousePosition().Get())
            mouseCenterOrigin = self.FloatCanvas.PixelToWorld(mouse)
            distFromCenter = mouseCenterOrigin - self.MovingObject.XY

            # This is what sets how much the box edges can be dragged past the canvas boundaries
            overlap = 40

            # Order: X-left, X-right, Y-top, Y-bottom
            self.boxBoundaries = N.array([self.MovingObject.Width/2 + distFromCenter[0],
                                    self.MovingObject.Width/2 - distFromCenter[0],
                                    self.MovingObject.Height/2 - distFromCenter[1],
                                    self.MovingObject.Height/2 + distFromCenter[1]]) - overlap

    def AddinkCursorClick(self):
        self.link_clicks += 1

        if self.link_clicks == 2:
            if len(self.linkRects) == 2 and not self.is_link_bidirectional(self.linkRects[0].ID, self.linkRects[1].ID):
                # This method creates the line and places the arrow
                self.createLine(self.linkRects[0], self.linkRects[1])
            else:
                print "Did not add the link"

            # reset
            self.link_clicks = 0
            self.linkRects = []

            # change the mouse cursor
            self.FloatCanvas.SetMode(self.GuiMouse)

    def ArrowClicked(self, event):

        # get the models associated with the link
        models = self.arrows[event]

        # get r1 and r2
        r1 = models[0]
        r2 = models[1]

        # get output items from r1
        from_model = engine.getModelById(r1.ID)

        # get output items from r1
        to_model = engine.getModelById(r2.ID)

        linkstart = LinkCtrl(parent=self.FloatCanvas, outputs=from_model, inputs=to_model, link_obj=event, swap=True)
        linkstart.Show()

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
        kwargs = dict(title=title, desc=desc, engine=dbengine, address=address, dbname=name, user=user, pwd=pwd)
        engine.connectToDb(**kwargs)

    def SaveSimulation(self, path):

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

            print '-------------------------------------------\n'
            print model['name']
            print model['attrib']
            print '-------------------------------------------\n'

            x = str((bbox[0][0] + bbox[1][0]) / 2)
            y = str((bbox[0][1] + bbox[1][1]) / 2)
            name = model['name']
            id = model['id']
            args = model['attrib']

            el = et.SubElement(tree, 'Model')
            el_name = et.SubElement(el, "name")
            el_name.text = name
            el_id = et.SubElement(el, "id")
            el_id.text = id
            el_x = et.SubElement(el, "xcoordinate")
            el_x.text = x
            el_y = et.SubElement(el, "ycoordinate")
            el_y.text = y

            # encode model arguments in xml
            el_args = et.SubElement(el, 'Arguments')
            for key, value in args.iteritems():
                el_arg = et.SubElement(el_args, key)
                el_arg.text = str(value)

            # save db id if the model depends on one
            if 'databaseid' in model['attrib']:
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
        print db_ids
        for db_id in db_ids:
            attributes = {}

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
            sPrint('An error occurred when attempting to save the project', MessageType.ERROR)

        elog.info('Configuration saved: ', path)
        sPrint('Configuration was saved successfully: ' + str(path))

    def appendChild(self, child):
        taglist = []
        textlist = []
        for data in child:
            textlist.append(data.text)
            taglist.append(data.tag)

        attrib = dict(zip(taglist, textlist))
        return attrib

    def loadsimulation(self, file):

        file = os.path.abspath(file)
        sPrint('Begin loading simulation: %s\n'%file)

        self.GetTopLevelParent().loading_path = file
        tree = et.parse(file)

        # make sure the required database connections are loaded
        connections = engine.getDbConnections()
        existing_connections = {}
        for id, condict in connections.iteritems():
            conargs = condict['args']
            unique_conn = '%s:%s:%s' % (conargs['engine'],
                                     conargs['address'],
                                     conargs['db'] if conargs['db'] is not None else '')
            existing_connections[unique_conn] = id

        conn_ids = {}


        dbconnections = tree.findall("./DbConnection")
        for connection in dbconnections:

            sPrint('Adding database connections...')

            con_engine = connection.find('engine').text
            con_address = connection.find('address').text
            con_db = connection.find('db').text
            con_id = connection.find('databaseid').text
            con_name = connection.find('name').text
            con_pass = connection.find('pwd').text
            con_user = connection.find('user').text
            con_desc = connection.find('desc').text

            # build a unique connection string
            unique_conn_string = '%s:%s:%s' % (con_engine,
                                               con_address,
                                               con_db if con_db != 'None' else '')

            # if connection already exists
            if unique_conn_string in existing_connections.keys():

                # map the connection ids

                conn_ids[con_id] = existing_connections[unique_conn_string]

            # open the dialog to add a new connection
            else:
                connect = wx.MessageBox('This database connection does not currently exist.  Click OK to connect.', 'Info', wx.OK | wx.CANCEL)

                if connect == wx.OK:

                    # attempt to connect to the database
                    title = con_name
                    desc = con_desc
                    db_engine = con_engine
                    address = con_address
                    name = con_db
                    user = con_user
                    pwd = con_pass

                    if not self.AddDatabaseConnection(title, desc, db_engine, address, name, user, pwd):
                        wx.MessageBox('I was unable to connect to the database with the information provided :(', 'Info', wx.OK | wx.ICON_ERROR)
                        return

                    # map the connection id
                    conn_ids[con_id] = con_id

        models = tree.findall("./Model")  # Returns a list of all models in the file
        datamodels = tree.findall("./DataModel")  # Returns a list of all data models in the file
        links = tree.findall("./Link")  # Returns a list of all links in the file

        total = len(models) + len(datamodels) + len(self.models) + self.failed_models

        waitingThread = threading.Thread(target=self.waitForModelLoading, args=(total, links), name="LoadLinks")
        self.logicCanvasThreads[waitingThread.name] = waitingThread
        waitingThread.start()

        # loop through all of the models and load each one individually
        for model in models:
            name = model.find('name').text
            x = float(model.find('xcoordinate').text)
            y = float(model.find('ycoordinate').text)
            id = model.find('id').text
            arguments = model.find('Arguments').getchildren()
            args = {}
            for arg in arguments:
                args[arg.tag] = arg.text

            sPrint('Adding model: %s...' % name)

            # save these coordinates for drawing once the model is loaded
            self.set_model_coords(id, x=x, y=y)

            # load the model in the engine
            engine.addModel(id=id, attrib=args)

            # draw the model
            wx.CallAfter(self.FloatCanvas.Draw)

    def waitForModelLoading(self, total, links):
        #  This method waits for all the models in the file to be loaded before linking
        while len(self.models) < total:
            time.sleep(0.5)
        self.LoadLinks(links)
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

    def LoadLinks(self, links):

        # get all known transformations
        space = SpatialInterpolation()
        time = TemporalInterpolation()
        spatial_transformations = {i.name(): i for i in space.methods()}
        temporal_transformations = {i.name(): i for i in time.methods()}

        for link in links:
            # get 'from' and 'to' model attributes
            from_model_id = link.find('./from_id').text
            from_model_item = link.find('./from_item').text
            from_model_name = link.find('./from_name').text
            to_model_id = link.find('./to_id').text
            to_model_item = link.find('./to_item').text
            to_model_name = link.find('./to_name').text

            from_model = self.getModelObjectFromId(from_model_id)
            to_model = self.getModelObjectFromId(to_model_id)

            if from_model is None or to_model is None:
                elog.critical("Failed to create link between %s and %s." % (from_model_name, to_model_name))
                sPrint("Failed to create link between %s and %s." % (from_model_name, to_model_name), MessageType.CRITICAL)
                return

            sPrint('Adding link between: %s and %s... ' % (from_model_name, to_model_name))

            # get the spatial and temporal transformations
            transformation = link.find("./transformation")
            temporal_transformation_name = transformation.find('./temporal').text
            spatial_transformation_name = transformation.find('./spatial').text
            # set the transformation values
            temporal = temporal_transformations[temporal_transformation_name] if temporal_transformation_name.lower() != 'none' else None
            spatial = spatial_transformations[spatial_transformation_name] if spatial_transformation_name.lower() != 'none' else None

            # create the link
            engine.addLink(source_id=from_model_id,
                               source_item=from_model_item,
                               target_id=to_model_id,
                               target_item=to_model_item,
                               spatial_interpolation=spatial,
                               temporal_interpolation=temporal
                               )

            wx.CallAfter(self.createLoadedLinks, from_model, to_model)

    def createLoadedLinks(self, from_model, to_model):
        if self.doPairModelsHaveLink(from_model, to_model):
            #  Replace the one way arrow with a bidirectional
            line = self.getLineFromPairModel(from_model, to_model)
            self.remove_link_image(line)
            self.createLine(from_model, to_model, "multiArrow.png")
        else:
            self.createLine(from_model, to_model, "rightArrowBlue60.png")

    def doPairModelsHaveLink(self, R1, R2):
        for key, value in self.links.iteritems():
            if R1 in value and R2 in value:
                return True
        return False

    def getLineFromPairModel(self, R1, R2):
        for key, value in self.links.iteritems():
            if R1 in value and R2 in value:
                return key
        return None

    def getModelObjectFromId(self, id):
        for key, value in self.models.iteritems():
            if id == value:
                return key
        return None

    def getCursor(self):
        return self._Cursor

    def setCursor(self, value=None):
        self._Cursor = value

    def LaunchContext(self, event):
        if type(event) == LogicCanvasObjects.ScaledBitmapWithRotation:
            # if object is link
            # event should be SmoothLineWithArrow...
            if event.type == "ArrowHead":
                self.PopupMenu(LinkContextMenu(self, event.line), event.HitCoordsPixel.Get())

        elif type(event) == LogicCanvasObjects.ModelBox:
            # if object is model
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
        pass
