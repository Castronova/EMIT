__author__ = 'tonycastronova'
from api.ODM2.Core.services import readCore
from api.ODM2.Results.services import readResults
from gui.frmMatPlotLib import MatplotFrame
from utilities import spatial
from api.ODM2.Simulation.services import readSimulation
from wx.lib.pubsub import pub as Publisher, __all__
import wx
from gui.controller.logicModel import LogicModel



#todo:  this needs to be split up into view and logic code

class LinkContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(LinkContextMenu, self).__init__()

        self.cmd = parent.cmd
        self.arrow_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveLink, mmi)

    def RemoveLink(self, e):
        self.parent.RemoveLink(self.arrow_obj)


    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class ConsoleContextMenu(wx.Menu):
    """
    Context menu for when a user does a right click in the ConsoleOutput
    """

    def __init__(self, parent, event):
        wx.Menu.__init__(self)
        self.log = parent.log
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Clear Console')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClear, mmi)

    def OnClear(self, event):
        """
        User clears the
        """
        self.log.Clear()
        print 'RESET |'

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class ModelContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(ModelContextMenu, self).__init__()

        self.cmd = parent.cmd
        self.model_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.ShowModelDetails, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveModel, mmi)

    def ShowModelDetails(self, e):

        # get model id
        id = self.model_obj.ID

        # create a frame to bind the details page to
        f = wx.Frame(self.GetParent())

        # get the input geometries
        ogeoms = spatial.get_output_geoms(self.cmd, id)

        # get the output geometries
        igeoms = spatial.get_input_geoms(self.cmd, id)

        # todo: HACK! should all of this be in the LogicModel?
        # create the details view (no edit)
        # view = ViewModel(f, edit=False)
        kwargs = {'edit':False,'spatial':True}
        model_details = LogicModel(f, **kwargs)

        # load geometry data
        model_details.PopulateSpatialGeoms(ogeoms, type='output')
        model_details.PopulateSpatialGeoms(igeoms, type='input')

        atts = self.cmd.get_model_by_id(self.model_obj.ID)._Model__attrib
        if 'mdl' in atts.keys():
            mdl_path= self.cmd.get_model_by_id(self.model_obj.ID)._Model__attrib['mdl']
            model_details.PopulateSummary(mdl_path)

        model_details.Show()

    def PopupDisplay(self, e):
        self.parent.DetailView(e)

    def OnAddLink(self, e):
        self.parent.ArrowClicked(e)

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

    def RemoveModel(self, e):
        self.parent.RemoveModel(self.model_obj)

class GeneralContextMenu(wx.Menu):

    def __init__(self, parent):
        super(GeneralContextMenu, self).__init__()

        self.cmd = parent.cmd
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Add Link')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Load Configuration')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.LoadConfiguration, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Save Configuration')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.SaveConfiguration, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Save Configuration As')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.SaveConfigurationAs, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Run')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClickRun, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Clear Configuration')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClickClear, mmi)

    def OnAddLink(self, e):

        self.parent.FloatCanvas.SetMode(self.parent.Canvas.GuiLink)

    def OnClickRun(self, e):

        # switch focus of the notebook tabs
        Publisher.sendMessage('ChangePage', page='Console')  # sends message to mainGui.py

        # run the simulation
        self.parent.run()

    def OnClickClear(self, e):
        dlg = wx.MessageDialog(None, 'Are you sure you would like to clear configuration?', 'Question', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() !=wx.ID_NO:
            self.parent.clear()

    def SaveConfiguration(self,e):
        if self.parent.GetLoadingPath() == None:
            save = wx.FileDialog(self.parent.Canvas.GetTopLevelParent(), "Save Configuration","","",
                                 "Simulation Files (*.sim)|*.sim", wx.FD_SAVE  | wx.FD_OVERWRITE_PROMPT)

            if save.ShowModal() == wx.ID_OK:
                path = save.GetPath()
                self.parent.SaveSimulation(path)
                self.parent.SetLoadingPath(path)
        else:
            self.parent.SaveSimulation(self.parent.GetLoadingPath())

    def SaveConfigurationAs(self,e):

        save = wx.FileDialog(self.parent.Canvas.GetTopLevelParent(), "Save Configuration","","",
                             "Simulation Files (*.sim)|*.sim", wx.FD_SAVE  | wx.FD_OVERWRITE_PROMPT)

        if save.ShowModal() == wx.ID_OK:
            path = save.GetPath()
            self.parent.SaveSimulation(path)
            self.parent.SetLoadingPath(path)

    def LoadConfiguration(self, e):
        load = wx.FileDialog(self.parent.Canvas.GetTopLevelParent(), "Load Configuration","","",
                             "Simulation Files (*.sim)|*.sim", wx.FD_OPEN)
        if load.ShowModal() == wx.ID_OK:
            path = load.GetPath()
            self.parent.loadsimulation(path)
            self.parent.SetLoadingPath(path)

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

    def Warn(parent, message, caption = 'Warning!'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

class DirectoryContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(DirectoryContextMenu, self).__init__()

        self.cmd = parent.cmd
        self.arrow_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnViewDetails, mmi)

    def OnViewDetails(self, e):
        self.parent.ShowDetails()

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class TreeItemContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(TreeItemContextMenu, self).__init__()

        self.arrow_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnViewDetails, mmi)

    def OnViewDetails(self, e):

        self.parent.ShowDetails()

    def OnExpandAll(self, e):
        self.parent.OnExpandAll()

    def OnCollapseAll(self, e):
        self.parent.OnCollapseAll()

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class ContextMenu(wx.Menu):

    def __init__(self, parent):
        super(ContextMenu, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Add')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAdd, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Plot')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnPlot, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Delete')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnDelete, mmi)

        # this is the list event from the right click
        self.__list_obj = None
        self.__list_id = None

    def Selected(self, list_obj=None, list_id=None):
        if list_id is not None and list_obj is not None:
            self.__list_obj = list_obj
            self.__list_id = list_id
        return self.__list_obj, self.__list_id




    def OnAdd(self, event):

        obj = self.__list_obj
        id = self.__list_id
        filename = obj.GetItem(id).GetText()

        Publisher.sendMessage('AddModel',filepath=filename, x = 0, y = 0) # sends message to CanvasController

    def getData(self,resultID):



        session = self.parent.getDbSession()
        if session is not None:
            readres = readResults(session)
            results = readres.getTimeSeriesValuesByResultId(resultId=int(resultID))


            core = readCore(session)
            obj = core.getResultByID(resultID=int(resultID))

            dates = []
            values = []
            for val in results:
                dates.append(val.ValueDateTime)
                values.append(val.DataValue)

            return dates,values,obj

    def OnPlot(self, event):

        obj = self.__list_obj

        # create a plot frame
        PlotFrame = None
        xlabel = None
        title = None
        variable = None
        units = None
        warning = None
        x_series = []
        y_series = []
        labels = []
        id = self.parent.GetFirstSelected()
        while id != -1:
            # get the result
            resultID = obj.GetItem(id,0).GetText()

            # get data for this row
            x,y, resobj = self.getData(resultID)

            if PlotFrame is None:
                # set metadata based on first series
                xlabel = '%s, [%s]' % (resobj.UnitObj.UnitsName, resobj.UnitObj.UnitsAbbreviation)
                title = '%s' % (resobj.VariableObj.VariableCode)

                # save the variable and units to validate future time series
                variable = resobj.VariableObj.VariableCode
                units = resobj.UnitObj.UnitsName

                PlotFrame = MatplotFrame(self.Parent, title, ylabel=xlabel)

            if resobj.VariableObj.VariableCode == variable and resobj.UnitObj.UnitsName == units:
                # store the x and Y data
                x_series.append(x)
                y_series.append(y)
                labels.append(resultID)

                # PlotFrame.add_series(x,y)
            elif warning is None:
                warning = 'Multiple Variables/Units were selected.  I currently don\'t support plotting heterogeneous time series. ' +\
                          'Some of the selected time series will not be shown :( '

            # get the next selected item
            id = obj.GetNextSelected(id)

        if warning:
            dlg = wx.MessageDialog(self.parent, warning, '', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()

        # plot the data
        PlotFrame.plot(xlist=x_series, ylist=y_series, labels=labels)
        PlotFrame.Show()

    def OnDelete(self,event):
        dlg = wx.MessageDialog(self.parent, 'Unfortunately, delete has not been implemented yet.', '', wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

class TimeSeriesContextMenu(ContextMenu):
    def __init__(self, parent):
        super(TimeSeriesContextMenu, self).__init__(parent)

class SimulationContextMenu(ContextMenu):
    def __init__(self, parent):
        super(SimulationContextMenu, self).__init__(parent)

    def getData(self,simulationID):

        session = self.parent.getDbSession()
        if session is not None:


            readsim = readSimulation(session)
            readres = readResults(session)
            results = readsim.getResultsBySimulationID(simulationID)

            res = {}
            for r in results:

                variable_name = r.VariableObj.VariableCode
                result_values = readres.getTimeSeriesValuesByResultId(int(r.ResultID))

                dates = []
                values = []
                for val in result_values:
                    dates.append(val.ValueDateTime)
                    values.append(val.DataValue)

                # save data series based on variable
                if variable_name in res:
                    res[variable_name].append([dates,values,r])
                else:
                    res[variable_name] = [[dates,values,r]]



            return res

    def OnPlot(self, event):

        obj, id = self.Selected()

        # create a plot frame
        PlotFrame = None
        xlabel = None
        title = None
        variable = None
        units = None
        warning = None
        x_series = []
        y_series = []
        labels = []
        id = self.parent.GetFirstSelected()
        while id != -1:
            # get the result
            simulationID = obj.GetItem(id,0).GetText()

            name = obj.GetItem(id,1).GetText()

            # get data for this row
            results = self.getData(simulationID)

            if PlotFrame is None:

                # todo: plot more than just this first variable
                key = results.keys()[0]


                resobj = results[key][0][2]
                # set metadata based on first series
                ylabel = '%s, [%s]' % (resobj.UnitObj.UnitsName, resobj.UnitObj.UnitsAbbreviation)
                title = '%s' % (resobj.VariableObj.VariableCode)

                # save the variable and units to validate future time series
                variable = resobj.VariableObj.VariableNameCV
                units = resobj.UnitObj.UnitsName
                title = '%s: %s [%s]' % (name, variable,units)

                PlotFrame = MatplotFrame(self.Parent, ylabel=ylabel, title=title)

                for x,y,resobj in results[key]:
                    # store the x and Y data
                    x_series.append(x)
                    y_series.append(y)
                    labels.append(int(resobj.ResultID))


                # PlotFrame.add_series(x,y)

            elif warning is None:
                warning = 'Multiple Variables/Units were selected.  I currently don\'t support plotting heterogeneous time series. ' +\
                          'Some of the selected time series will not be shown :( '

            # get the next selected item
            id = obj.GetNextSelected(id)

        if warning:
            dlg = wx.MessageDialog(self.parent, warning, '', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()

        # plot the data
        PlotFrame.plot(xlist=x_series, ylist=y_series, labels=labels)
        PlotFrame.Show()
