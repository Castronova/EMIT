
__author__ = 'tonycastronova'
import wx

class FileDrop(wx.FileDropTarget):
    def __init__(self, controller, window, cmd):
        wx.FileDropTarget.__init__(self)

        self.controller = controller
        self.window = window
        self.cmd = cmd
        Publisher.subscribe(self.OnDropFiles, 'toolboxclick')

    def RandomCoordinateGeneration(self, filepath):
        filenames = filepath
        x = 0
        y = 0

        self.OnDropFiles(x,y,filenames)

    def OnDropFiles(self, x, y, filenames):
        originx, originy = self.window.Canvas.PixelToWorld((0,0))

        x = x + originx
        y = originy - y

        # make sure the correct file type was dragged
        name, ext = os.path.splitext(filenames[0])
        if ext == '.mdl' or ext =='.sim':

            try:
                if ext == '.mdl':

                    dtype = datatypes.ModelTypes.FeedForward
                    kwargs = dict(x=x, y=y, type=dtype, attrib={'mdl': filenames[0]})
                    task = ('addmodel', kwargs)
                    self.controller.threadManager.dispatcher.putTask(task)

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
            inst = odm2_data.odm2(resultid=name, session=session)

            oei = inst.outputs().values()

            from coordinator import main
            # create a model instance
            thisModel = main.Model(id=inst.id(),
                                   name=inst.name(),
                                   instance=inst,
                                   desc=inst.description(),
                                   input_exchange_items= [],
                                   output_exchange_items=  oei,
                                   params=None)


            # save the result id
            att = {'resultid':name}

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
            self.window.Canvas.Draw()


    def getObj(self,resultID):

        session = self.getDbSession()

        core = readCore(session)
        obj = core.getResultByID(resultID=int(resultID))

        session.close()

        return obj

    def getData(self,resultID):


        session = self.getDbSession()
        readres = readResults(session)
        results = readres.getTimeSeriesValuesByResultId(resultId=int(resultID))

        core = readCore(session)
        obj = core.getResultByID(resultID=int(resultID))

        dates = []
        values = []
        for val in results:
            dates.append(val.ValueDateTime)
            values.append(val.DataValue)

        session.close()

        return dates,values,obj
