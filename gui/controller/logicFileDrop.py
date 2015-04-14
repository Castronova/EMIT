__author__ = 'tonycastronova'

import os
import wx
import datatypes
from coordinator import engine
from wx.lib.pubsub import pub as Publisher
from coordinator.engineManager import Engine
import uuid
import coordinator.engineAccessors as eng

class LogicFileDrop(wx.FileDropTarget):
    def __init__(self, controller, FloatCanvas, cmd):
        wx.FileDropTarget.__init__(self)
        self.controller = controller
        self.FloatCanvas = FloatCanvas
        self.cmd = cmd
        Publisher.subscribe(self.OnDropFiles, 'toolboxclick')

        self.ENGINE = Engine()

    def RandomCoordinateGeneration(self, filepath):
        filenames = filepath
        x = 0
        y = 0

        self.OnDropFiles(x, y, filenames)

    def OnDropFiles(self, x, y, filenames):
        originx, originy = self.FloatCanvas.PixelToWorld((0, 0))

        x = x + originx
        y = originy - y

        # make sure the correct file type was dragged
        name, ext = os.path.splitext(filenames[0])
        if ext == '.mdl' or ext == '.sim':

            # generate an ID for this model
            id = uuid.uuid4().hex[:5]

            # save these coordinates for drawing once the model is loaded
            self.controller.set_model_coords(id, x=x, y=y)

            # load the model within the engine process
            if ext == '.mdl':
                eng.addModel(id=id, attrib={'mdl': filenames[0]})

            else:
                current_db_id = self.controller._currentDbID
                attrib = dict(databaseid=current_db_id, resultid=name)
                eng.addModel(id=id, attrib=attrib)

        else:
            # load the simulation
            self.controller.loadsimulation(filenames[0])

