__author__ = 'tonycastronova'

import os
import wx
import datatypes
from coordinator import engine
from wx.lib.pubsub import pub as Publisher


class LogicFileDrop(wx.FileDropTarget):
    def __init__(self, controller, FloatCanvas, cmd):
        wx.FileDropTarget.__init__(self)
        self.controller = controller
        self.FloatCanvas = FloatCanvas
        self.cmd = cmd
        Publisher.subscribe(self.OnDropFiles, 'toolboxclick')

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

            try:
                if ext == '.mdl':

                    dtype = datatypes.ModelTypes.FeedForward
                    kwargs = dict(x=x, y=y, type=dtype, attrib={'mdl': filenames[0]})

                    model = self.cmd.add_model(type=dtype, id=None, attrib={'mdl': filenames[0]})

                    # def createBox(self, xCoord, yCoord, id=None, name=None, color='#A2CAF5'):
                    self.controller.createBox(x, y, model.get_id(), model.get_name())

                    # hack:  this is not working anymore!?
                    #task = ('addmodel', kwargs)
                    #self.controller.threadManager.dispatcher.putTask(task)

                else:
                    # load the simulation
                    self.controller.loadsimulation(filenames[0])


            except Exception, e:
                print 'ERROR | Could not load the model. Please verify that the model file exists.'
                print 'ERROR | %s' % e

        else:
            # # -- must be a data object --

            # get the current database connection dictionary
            session = self.controller.getCurrentDbSession()

            # create odm2 instance
            inst = datatypes.odm2_data.odm2(resultid=name, session=session)

            oei = inst.outputs().values()


            # create a model instance
            thisModel = engine.Model(id=inst.id(),
                                     name=inst.name(),
                                     instance=inst,
                                     desc=inst.description(),
                                     input_exchange_items=[],
                                     output_exchange_items=oei,
                                     params=None)


            # save the result id
            att = {'resultid': name}

            # save the database connection
            dbs = self.cmd.get_db_connections()
            for id, dic in dbs.iteritems():
                if dic['session'] == self.controller.getCurrentDbSession():
                    att['databaseid'] = id
                    thisModel.attrib(att)
                    break

            thisModel.type(datatypes.ModelTypes.Data)


            # save the model
            self.cmd.Models(thisModel)

            # draw a box for this model
            self.controller.createBox(name=inst.name(), id=inst.id(), xCoord=x, yCoord=y, color='#FFFF99')
            self.FloatCanvas.Draw()

