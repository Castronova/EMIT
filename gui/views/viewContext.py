__author__ = 'tonycastronova'
import wx

from api_old.ODM2.Core.services import readCore
from api_old.ODM2.Results.services import readResults
from utilities import spatial
from api_old.ODM2.Simulation.services import readSimulation
from wx.lib.pubsub import pub as Publisher, __all__
from gui.controller.logicModel import LogicModel
from gui.controller.logicPlot import LogicPlot
from gui.controller.logicPreRun import logicPreRun
import coordinator.engineAccessors as engine
from gui import events
from coordinator.emitLogging import elog
import csv
import time

#todo:  this needs to be split up into view and logic code

class LinkContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(LinkContextMenu, self).__init__()

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
        User clears the gui console
        """
        self.log.Clear()

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class ModelContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(ModelContextMenu, self).__init__()

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

        kwargs = {'edit':False,'spatial':True}
        model_details = LogicModel(f, **kwargs)

        # get the output geometries
        oei = engine.getOutputExchangeItems(id)
        ogeoms = {}
        # disable dropdown box if empty
        if not oei:
            model_details.outputSelections.Enable(False)
        else:
            model_details.outputSelections.Append('---')
            for o in oei:
                name = o['name']
                model_details.outputSelections.Append(name)
                geoms = [i['shape'] for i in o['geom']]
                ogeoms[name] = geoms

        # get the input geometries
        igeoms = {}
        iei = engine.getInputExchangeItems(id)
        # disable dropdown box if empty
        if not iei:
            model_details.inputSelections.Enable(False)
        else:
            model_details.inputSelections.Append('---')
            for i in iei:
                name = i['name']
                model_details.inputSelections.Append(name)
                elog.info("input name: " + name)
                geoms = [j['shape'] for j in i['geom']]
                igeoms[name] = geoms

        # todo: HACK! should all of this be in the LogicModel?
        # kwargs = {'edit':False,'spatial':True}
        # model_details = LogicModel(f, **kwargs)

        # load geometry data
        model_details.PopulateSpatialGeoms(ogeoms, type='output')
        model_details.PopulateSpatialGeoms(igeoms, type='input')

        # model_details.inputSelections.Clear()
        # model_details.inputSelections.Append("test2")
        # populate model metadata from MDL file
        atts = engine.getModelById(self.model_obj.ID)['attrib']
        if 'mdl' in atts.keys():
            model_details.PopulateSummary(atts['mdl'])
        else:  # This means the model is coming from a database.
            model_details.PopulateProperties(engine.getModelById(self.model_obj.ID), iei=iei, oei=oei)

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

class CanvasContextMenu(wx.Menu):

    def __init__(self, parent):
        super(CanvasContextMenu, self).__init__()
        self.parent = parent

        addLink = wx.MenuItem(self, wx.NewId(), 'Add Link')
        self.AppendItem(addLink)
        self.Bind(wx.EVT_MENU, self.OnAddLink, addLink)

        load = wx.MenuItem(self, wx.NewId(), 'Load')
        self.AppendItem(load)
        self.Bind(wx.EVT_MENU, self.LoadConfiguration, load)

        save = wx.MenuItem(self, wx.NewId(), 'Save Configuration')
        self.AppendItem(save)
        self.Bind(wx.EVT_MENU, self.SaveConfiguration, save)

        saveAs = wx.MenuItem(self, wx.NewId(), 'Save Configuration As')
        self.AppendItem(saveAs)
        self.Bind(wx.EVT_MENU, self.SaveConfigurationAs, saveAs)

        run = wx.MenuItem(self, wx.NewId(), 'Run')
        self.AppendItem(run)
        self.Bind(wx.EVT_MENU, self.OnRunModel, run)
        events.onClickRun += self.OnClickRun

        clear = wx.MenuItem(self, wx.NewId(), 'Clear Configuration')
        self.AppendItem(clear)
        self.Bind(wx.EVT_MENU, self.OnClickClear, clear)

        # Disable certain options if there aren't any models present
        if len(self.parent.models) <= 1:
            addLink.Enable(False)
            if len(self.parent.models) <= 0:
                save.Enable(False)
                saveAs.Enable(False)
                clear.Enable(False)

        if len(self.parent.links) <= 0:
            run.Enable(False)

    def OnAddLink(self, e):
        self.parent.FloatCanvas.SetMode(self.parent.GuiLink)

    def OnClickRun(self, e):
        # switch focus of the notebook tabs
        Publisher.sendMessage('ChangePage', page='Console')  # sends message to mainGui.py

        # run the simulation
        self.parent.run()

    def OnRunModel(self, e):
        preRunDialog = logicPreRun()
        preRunDialog.Show()


    def OnClickClear(self, e):
        dlg = wx.MessageDialog(None, 'Are you sure you would like to clear configuration?', 'Question', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() !=wx.ID_NO:
            self.parent.clear()
            elog.info("Configurations have been cleared")

    def SaveConfiguration(self,e):
        if self.parent.GetLoadingPath() == None:
            save = wx.FileDialog(self.parent.GetTopLevelParent(), "Save Configuration","","",
                                 "Simulation Files (*.sim)|*.sim", wx.FD_SAVE  | wx.FD_OVERWRITE_PROMPT)

            if save.ShowModal() == wx.ID_OK:
                path = save.GetPath()
                self.parent.SaveSimulation(path)
                self.parent.SetLoadingPath(path)
        else:
            self.parent.SaveSimulation(self.parent.GetLoadingPath())

    def SaveConfigurationAs(self, e):
        # Executes from Float Canvas -> right click -> Save As
        e = dict()
        events.onSaveFromCanvas.fire(**e)  # calls SaveConfigurationsAs in ViewEMIT.py

    def LoadConfiguration(self, e):
        load = wx.FileDialog(self.parent.GetTopLevelParent(), "Load File", "", "",
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

class ToolboxContextMenu(wx.Menu):

    def __init__(self, parent, e, removable, folder):
        super(ToolboxContextMenu, self).__init__()

        self.arrow_obj = e
        self.parent = parent
        if not folder:
            mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
            self.AppendItem(mmi)
            self.Bind(wx.EVT_MENU, self.OnViewDetails, mmi)

        if removable:
            # mr stands for menu remove
            mr = wx.MenuItem(self, wx.NewId(), 'Remove')
            self.AppendItem(mr)
            self.Bind(wx.EVT_MENU, self.OnRemove, mr)

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

    def OnRemove(self, e):
        self.parent.Remove(e)

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

        mmi = wx.MenuItem(self, wx.NewId(), 'Export')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.onExport, mmi)

        # this is the list event from the right click
        self.__list_obj = None
        self.__list_id = None

    def onExport(self, event):
        #  User will choose where to save the csv file
        save = wx.FileDialog(self.parent.GetTopLevelParent(), message="Choose Path",
                             wildcard="CSV Files (*.csv)|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save.ShowModal() == wx.ID_OK:
            path = save.GetPath()
            if path[-4] != '.':
                path += '.csv'
            file = open(path, 'w')

            writer = csv.writer(file, delimiter=',')

            obj = self.__list_obj
            id = self.parent.GetFirstSelected()
            resultID = obj.GetItem(id, 0).GetText()
            dates, values, resobj = self.getData(resultID)

            writer.writerow(["#-------------------------Disclaimer:  This is a data set that was exported by EMIT ... use at your own risk..."])
            writer.writerow(["#"])
            writer.writerow(["#Date Created: %s" % str(resobj.FeatureActionObj.ActionObj.BeginDateTime.strftime("%m/%d/%Y"))])
            writer.writerow(["#Date Exported: %s" % str(getTodayDate())])
            writer.writerow(["Result ID: %s" % str(resobj.ResultID)])
            writer.writerow(["#Variable: %s" % str(resobj.VariableObj.VariableCode)])
            writer.writerow(["#Unit: %s" % str(resobj.UnitObj.UnitsAbbreviation)])
            writer.writerow(["#Organization: %s" % str(resobj.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName)])
            writer.writerow(["#"])
            writer.writerow(["#-------------------------End Disclaimer"])
            writer.writerow(["#"])
            writer.writerow(["Dates", "Values"])

            data = []
            j = 0  # j acts like i but its for the values variable
            for i in dates:
                data.append([i, values[j]])  # its done this way to dates and values are two different columns
                j += 1
            writer.writerows(data)

            file.close()


    def Selected(self, list_obj=None, list_id=None):
        if list_id is not None and list_obj is not None:
            self.__list_obj = list_obj
            self.__list_id = list_id
        return self.__list_obj, self.__list_id

    def OnAdd(self, event):

        obj = self.__list_obj
        id = self.__list_id
        filename = obj.GetItem(id).GetText()

        Publisher.sendMessage('AddModel', filepath=filename, x=0, y=0) # sends message to CanvasController

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
            resultID = obj.GetItem(id, 0).GetText()

            # get data for this row
            x,y, resobj = self.getData(resultID)

            if PlotFrame is None:
                # set metadata based on first series
                ylabel = '%s, [%s]' % (resobj.UnitObj.UnitsName, resobj.UnitObj.UnitsAbbreviation)

                # todo: this needs to change based on the axis format decided by matplotlib
                xlabel = 'DateTime'

                # todo: this title must be more specific.  e.g. include gage location?
                title = '%s' % (resobj.VariableObj.VariableCode)

                # save the variable and units to validate future time series
                variable = resobj.VariableObj.VariableCode
                units = resobj.UnitObj.UnitsName
                PlotFrame = LogicPlot(self.Parent, title=title, ylabel=ylabel, xlabel=xlabel)

            if resobj.VariableObj.VariableCode == variable and resobj.UnitObj.UnitsName == units:
                # store the x and Y data
                x_series.append(x)
                y_series.append(y)
                labels.append(resultID)

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

                PlotFrame = LogicPlot(self.Parent, ylabel=ylabel, title=title)

                for x,y,resobj in results[key]:
                    # store the x and Y data
                    x_series.append(x)
                    y_series.append(y)
                    labels.append(int(resobj.ResultID))

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

    def onExport(self, event):
        #  User will choose where to save the csv file
        save = wx.FileDialog(self.parent.GetTopLevelParent(), message="Choose Path",
                             wildcard="CSV Files (*.csv)|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save.ShowModal() == wx.ID_OK:
            path = save.GetPath()
            if path[-4] != '.':
                path += '.csv'
            file = open(path, 'w')
            convert = csv.writer(file, delimiter=',')

            obj, id = self.Selected()
            id = self.parent.GetFirstSelected()
            simulationID = obj.GetItem(id, 0).GetText()

            #  The if below was taken from self.getData
            session = self.parent.getDbSession()
            if session is not None:

                readsim = readSimulation(session)
                readres = readResults(session)
                results = readsim.getResultsBySimulationID(simulationID)

                for r in results:

                    variable_name = r.VariableObj.VariableCode
                    result_values = readres.getTimeSeriesValuesByResultId(int(r.ResultID))

                    dates = []
                    values = []
                    for val in result_values:
                        dates.append(val.ValueDateTime)
                        values.append(val.DataValue)

                    #  Organzing data so its in two columns
                    data = []
                    j = 0  # j acts like i but its for the values variable
                    for i in dates:
                        data.append([i, values[j]])
                        j += 1

                    #  Writing to CSV file
                    convert.writerows([[variable_name]])
                    convert.writerows(data)

            file.close()

def getTodayDate():
    return time.strftime("%m/%d/%Y")