__author__ = 'tonycastronova'
from api.ODM2.Core.services import readCore
from api.ODM2.Results.services import readResults
from utilities import spatial
from api.ODM2.Simulation.services import readSimulation
from wx.lib.pubsub import pub as Publisher, __all__
import wx
from gui.controller.logicModel import LogicModel
from gui.controller.logicPlot import LogicPlot
import coordinator.engineAccessors as engine
from gui import events
import random

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
                print "input name: " + name
                geoms = [j['shape'] for j in o['geom']]
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

        mmi = wx.MenuItem(self, wx.NewId(), 'Run Model')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnRunModel, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Clear Configuration')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClickClear, mmi)

    def OnAddLink(self, e):
        self.parent.FloatCanvas.SetMode(self.parent.GuiLink)

    def OnClickRun(self, e):
        # switch focus of the notebook tabs
        Publisher.sendMessage('ChangePage', page='Console')  # sends message to mainGui.py

        # run the simulation
        self.parent.run()

    def OnRunModel(self, e):
        notebook = MainFrame()
        notebook.Show()


    def OnClickClear(self, e):
        dlg = wx.MessageDialog(None, 'Are you sure you would like to clear configuration?', 'Question', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() !=wx.ID_NO:
            self.parent.clear()

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
        load = wx.FileDialog(self.parent.GetTopLevelParent(), "Load Configuration", "", "",
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

class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        # ------------------This way I was trying to manually positioning everything ------------------------
        # simulationTitle = wx.StaticText(self, -1, label="Simulation Title", pos=(10, 10))
        # databaseTitle = wx.StaticText(self, id=wx.ID_ANY, label="Database Title", pos=(50, 50))
        # simulationName = wx.TextCtrl(self, id=wx.ID_ANY, value="Simulation name goes here", pos=(125, 5), size=(300, -1))
        # runButton = wx.Button(self, label='Run', pos=(400, 195), style=0)

        self.parent = parent
        sizer = wx.GridBagSizer(5, 5)

        simulationName = wx.StaticText(self, label="Simulation Name: ")
        sizer.Add(simulationName, pos=(1, 0), flag=wx.LEFT, border=10)

        simulationNameTextBox = wx.TextCtrl(self)
        sizer.Add(simulationNameTextBox, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)

        databaseName = wx.StaticText(self, label="Database Name: ")
        sizer.Add(databaseName, pos=(2, 0), flag=wx.LEFT|wx.TOP, border=10)

        databaseCombo = wx.ComboBox(self)
        sizer.Add(databaseCombo, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND, border=5)

        # browseDataBaseButton = wx.Button(self, label="Browse...")
        # sizer.Add(browseDataBaseButton, pos=(2, 4), flag=wx.TOP|wx.RIGHT, border=5)

        accountName = wx.StaticText(self, label="Account: ")
        sizer.Add(accountName, pos=(3, 0), flag=wx.TOP|wx.LEFT, border=10)

        accountCombo = wx.ComboBox(self)
        sizer.Add(accountCombo, pos=(3, 1), span=(1, 3),
            flag=wx.TOP|wx.EXPAND, border=5)

        browseAccountButton = wx.Button(self, label="Add New")
        sizer.Add(browseAccountButton, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)

        lineBreak = wx.StaticLine(self)
        sizer.Add(lineBreak, pos=(4, 0), span=(1, 5), flag=wx.EXPAND|wx.BOTTOM, border=10)

        sizerStaticBox = wx.StaticBox(self, label="Optional Features")

        boxsizer = wx.StaticBoxSizer(sizerStaticBox, wx.VERTICAL)
        boxsizer.Add(wx.CheckBox(self, label="Display Simulation Message"), flag=wx.LEFT|wx.TOP, border=5)
        boxsizer.Add(wx.CheckBox(self, label="Log Simulation Message"), flag=wx.LEFT, border=5)
        boxsizer.Add(wx.CheckBox(self, label="Checkbox 3"), flag=wx.LEFT|wx.BOTTOM, border=5)
        sizer.Add(boxsizer, pos=(5, 0), span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

        helpButton = wx.Button(self, label='Help')
        sizer.Add(helpButton, pos=(7, 0), flag=wx.LEFT, border=10)

        self.runButton = wx.Button(self, label="Run")
        sizer.Add(self.runButton, pos=(7, 4))

        self.cancelButton = wx.Button(self, label="Cancel")
        sizer.Add(self.cancelButton, pos=(7, 3), span=(1, 1), flag=wx.BOTTOM | wx.RIGHT, border=5)

        sizer.AddGrowableCol(2)

        self.SetSizer(sizer)

        self.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.runButton.Bind(wx.EVT_BUTTON, self.OnRun)

    def OnCancel(self, event):
        frame = self.GetTopLevelParent()
        frame.Close(True)

    def OnRun(self, event):
        print "Run me"


class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a Page Two", (40, 40))

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a Page Three\nThis is here in case we want to add another tab. ", (60, 60))


class MainFrame(wx.Frame):
    def __init__(self):                                                         # this style makes the window non-resizable
        wx.Frame.__init__(self, None, title="Window Title", size=(450, 425), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        # Here we create a panel and a notebook on the panel
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)

        # create the page windows as children of the notebook
        page1 = PageOne(notebook)
        page2 = PageTwo(notebook)
        page3 = PageThree(notebook)

        # add the pages to the notebook with the label to show on the tab
        notebook.AddPage(page1, "Summary")
        notebook.AddPage(page2, "Details")
        notebook.AddPage(page3, "Page 3")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        panel.SetSizer(sizer)

