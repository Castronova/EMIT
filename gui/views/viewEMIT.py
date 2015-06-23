__author__ = 'Mario'
from gui.controller.logicDirectory import LogicDirectory
from gui.controller.logicToolbox import LogicToolbox
from gui.controller.logicCanvas import LogicCanvas

import wx
import wx.html2
import sys
from wx.lib.pubsub import pub as Publisher
import wx.lib.agw.aui as aui
# import logging
import threading
from db import dbapi as dbapi
from wx import richtext
from viewContext import TimeSeriesContextMenu, SimulationContextMenu, ConsoleContextMenu
from gui.controller.logicDatabase import LogicDatabase
import coordinator.engineAccessors as engine
from utilities import db as dbUtilities
from db import dbapi as dbapi
import coordinator.events as engineEvent
# import gui.controller.events as guiEvents
from gui import events

# todo: refactor
# from .. import objectListViewDatabase as olv

from wx.lib.newevent import NewEvent
import time

# create custom events
wxCreateBox, EVT_CREATE_BOX = NewEvent()
wxStdOut, EVT_STDDOUT= NewEvent()
wxDbChanged, EVT_DBCHANGED= NewEvent()

import ConsoleOutput

from logging import FileHandler
from coordinator.emitLogging import elog


class ViewEMIT(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Environmental Model Integration Project", pos=wx.DefaultPosition,
                          size=wx.Size(1200, 750), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        # self.SetPosition(wx.Point(200,200))

        self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(1200, 750),
                                   style=wx.TAB_TRAVERSAL)
        self.bnb = wx.Notebook(self.pnlDocking)

        self.parent = parent

        self.notebook_pages = {}

        self.initMenu()

        # creating components
        self.Directory = LogicDirectory(self.pnlDocking)
        self.Toolbox = LogicToolbox(self.pnlDocking)
        self.Canvas = LogicCanvas(self.pnlDocking)
        self.Output = consoleOutput(self.bnb)

        # deactivate the console if we are in debug mode
        # if not sys.gettrace():
            # redir = RedirectText(self.log)
            # sys.stdout = redir

            #  Thread starts here to ensure its on the main thread
        t = threading.Thread(target=ConsoleOutput.follow,args=(elog, self.Output.log))
        t.start()

        self.Toolbox.Hide()
        self.initAUIManager()
        self._init_sizers()

        # Publisher.subscribe(self.OnPageChange, 'ChangePage')

        self.filename = None
        self.loadingpath = None

        self.Center()

        self.Show()


    def _init_sizers(self):
        self.s = wx.BoxSizer(wx.VERTICAL)
        self.s.AddWindow(self.pnlDocking, 85, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.s)



    def initAUIManager(self):

        self.m_mgr = aui.AuiManager()
        self.m_mgr.SetManagedWindow(self.pnlDocking)



        # seriesoutput = OutputTimeSeries(self.bnb)
        seriesselector = TimeSeries(self.bnb)
        seriesoutput = SimulationDataTable(self.bnb)

        self.bnb.AddPage(self.Output, "Console")
        self.bnb.AddPage(seriesselector, "Time Series")
        self.bnb.AddPage(seriesoutput, "Simulations")
        # self.bnb.AddPage(seriesoutput, "Output Time Series")

        # add these to the notebook pages dictionary so that they can be looked up later
        self.notebook_pages['Console'] = 0
        self.notebook_pages['Time Series'] = 1
        self.notebook_pages['Simulations'] = 2

        self.bnb.GetPage(0).SetLabel("Console")
        self.bnb.GetPage(1).SetLabel("Time Series")
        # self.bnb.GetPage(2).SetLabel("Output Time Series")

        self.bnb.GetPage(2).SetLabel("Simulations")


        self.m_mgr.AddPane(self.Canvas,
                           aui.AuiPaneInfo().
                           Center().
                           Name("Canvas").
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           Floatable(False).
                           BestSize(wx.Size(1000, 400))
        )

        self.m_mgr.AddPane(self.Directory,
                           aui.AuiPaneInfo().
                           Left().
                           Dock().
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           BestSize(wx.Size(275, 400)).
                           Floatable(False).
                           Movable(False).
                           Show(show=False).Hide()
                           )

        self.m_mgr.AddPane(self.Toolbox,
                           aui.AuiPaneInfo().
                           Left().
                           Dock().
                           Name("Toolbox").
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           BestSize(wx.Size(275, 400)).
                           Floatable(False).
                           Movable(False).
                           Show(show=True)
                           )

        self.m_mgr.AddPane(self.bnb,
                           aui.AuiPaneInfo().
                           Bottom().
                           Name("Console").
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).
                           BestSize(wx.Size(1200, 200))
        )



        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnSelect)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.m_mgr.Update()

        self._default_perspective = self.m_mgr.SavePerspective()

    # def OnPageChange(self, page):
    #
    #     index = self.notebook_pages[page]
    #     self.bnb.SetSelection(index)

    def OnSelect(self, event):

        try:
            # update databases in a generic way
            selected_page = self.bnb.GetPage(event.GetSelection())
            if len(selected_page.connection_combobox.GetItems()) == 0:
                 selected_page.refreshConnectionsListBox()

        except: pass

    def initMenu(self):
        ## Menu stuff
        #self.m_statusBar2 = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)

        self.m_menubar = wx.MenuBar()

        self.m_fileMenu = wx.Menu()
        #exit = wx.MenuItem(self.m_fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
        Save = self.m_fileMenu.Append(wx.NewId(), '&Save Configuration\tCtrl+S', 'Save Configuration')
        SaveAs = self.m_fileMenu.Append(wx.NewId(), '&Save Configuration As', 'Save Configuration')
        Open = self.m_fileMenu.Append(wx.NewId(), '&Load Configuration\tCtrl+O', 'Load Configuration')
        exit = self.m_fileMenu.Append(wx.NewId(), '&Quit\tCtrl+Q', 'Quit application')

        self.m_menubar.Append(self.m_fileMenu, "&File")

        self.m_toolMenu = wx.Menu()
        # self.m_menubar.Append(self.m_toolMenu, "&Tools")


        self.m_viewMenu = wx.Menu()
        ShowAll = self.m_viewMenu.Append(wx.NewId(), '&Toolbox\tCtrl+A', 'Show all associated files', wx.ITEM_RADIO)
        ShowDir = self.m_viewMenu.Append(wx.NewId(), '&Directory\tCtrl+D', 'Shows file directory', wx.ITEM_RADIO)
        separator = self.m_viewMenu.Append(wx.NewId(), 'separate', 'separate', wx.ITEM_SEPARATOR)
        MinimizeConsole = self.m_viewMenu.Append(wx.NewId(), '&Console Off', 'Minimizes the Console', wx.ITEM_CHECK)

        defaultview = self.m_viewMenu.Append(wx.NewId(), '&Default View', 'Returns the view to the default (inital) state', wx.ITEM_NORMAL)

        self.m_menubar.Append(self.m_viewMenu, "&View")

        self.m_optionMenu = wx.Menu()
        ShowSim = self.m_optionMenu.Append(wx.NewId(), 'Show Configurations', 'Shows the saved configurations files in the toolbox', wx.ITEM_RADIO)
        HideSim = self.m_optionMenu.Append(wx.NewId(), 'Hide Configurations', 'Only shows Hydrology models in the toolbox', wx.ITEM_RADIO)
        self.m_menubar.Append(self.m_optionMenu, "&Options")

        self.m_runMenu = wx.Menu()
        self.applicationRun = self.m_runMenu.Append(wx.NewId(), '&Run Configuration', 'Runs the existing configurations')
        separator = self.m_runMenu.Append(wx.NewId(), 'separate', 'separate', wx.ITEM_SEPARATOR)
        databaseSave = self.m_runMenu.Append(wx.NewId(), '&Save Results to Database', 'Saves the result to the default database', wx.ITEM_CHECK)
        viewResult = self.m_runMenu.Append(wx.NewId(), '&View Results', 'View the result', wx.ITEM_CHECK)
        viewResult.Check()
        self.m_menubar.Append(self.m_runMenu, "&Run")

        self.SetMenuBar(self.m_menubar)

        wx.CallAfter(self._postStart)

        ## Events
        #File MenuBar
        self.Bind(wx.EVT_MENU, self.SaveConfiguration, Save)
        self.Bind(wx.EVT_MENU, self.SaveConfigurationAs, SaveAs)
        self.Bind(wx.EVT_MENU, self.LoadConfiguration, Open)
        self.Bind(wx.EVT_MENU, self.onClose, exit)
        events.onSaveFromCanvas += self.SaveConfigurationAs

        #View MenuBar
        self.Bind(wx.EVT_MENU, self.onDirectory, ShowDir)
        self.Bind(wx.EVT_MENU, self.onAllFiles, ShowAll)
        self.Bind(wx.EVT_MENU, self.onConsole, MinimizeConsole)
        self.Bind(wx.EVT_MENU, self.defaultview, defaultview)
        # self.Bind(wx.EVT)


    def onClose(self, event):
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dial.ShowModal() == wx.ID_YES:
            self.Destroy()

    def defaultview(self, event):
        """
        Restore previously saved perspective
        """
        self.m_mgr.LoadPerspective(self._default_perspective)


    def _postStart(self):
        ## Starts stuff after program has initiated
        self.Canvas.ZoomToFit(event=None)

    def __del__(self):
        self.m_mgr.UnInit()

    def LoadConfiguration(self,event):


        #if wx.MessageBox("This will overlay on the current configuration.", "Please confirm",
        #                 wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
        #    return

        # else: proceed asking to the user the new file to open

        openFileDialog = wx.FileDialog(self, "Open SIM file", "", "",
                                       "Simulation Files (*.sim)|*.sim", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_CANCEL:
            return     # the user changed idea...
        print "Filename is: ", openFileDialog.GetFilename()
        # proceed loading the file chosen by the user
        # this can be done with e.g. wxPython input streams:
        input_stream = (openFileDialog.GetPath())
        Publisher.sendMessage('SetLoadPath',file=input_stream) #send message to canvascontroller

        self.filename = openFileDialog.GetFilename()
        self.loadingpath = input_stream
        #
        # data = wx.FileDataObject()
        # data.AddFile(input_stream)
        #
        # obj = event.GetSelection()
        # data = wx.FileDataObject()
        #
        # dropSource = wx.DropSource(openFileDialog)
        # dropSource.SetData(data)
        # x = 0
        # y = 0
        # dropSource.DoDragDrop()

        # if not input_stream.IsOk():
        #
        #     wx.LogError("Cannot open file '%s'."%openFileDialog.GetPath())
        #     return
        # pass

    def SaveConfiguration(self,event):
        if self.loadingpath == None:
            save = wx.FileDialog(self.Canvas.GetTopLevelParent(), "Save Configuration","","",
                                 "Simulation Files (*.sim)|*.sim", wx.FD_SAVE  | wx.FD_OVERWRITE_PROMPT)

            if save.ShowModal() == wx.ID_OK:
                self.save_path = save.GetPath() + ".sim"
            else:
                save.Destroy()

            Publisher.sendMessage('SetSavePath',path=save.GetPath()) #send message to canvascontroller.SaveSimulation

            self.loadingpath = save.GetPath()
        else:
            Publisher.sendMessage('SetSavePath', path=self.loadingpath)

    def SaveConfigurationAs(self,event):
        # Executes from File ->Save As
        save = wx.FileDialog(self.Canvas.GetTopLevelParent(), "Save Configuration","","",
                             "Simulation Files (*.sim)|*.sim", wx.FD_SAVE  | wx.FD_OVERWRITE_PROMPT)

        if save.ShowModal() == wx.ID_OK:
            self.save_path = save.GetPath()
            if self.save_path[-4] != '.':  # check if extension was added
                self.save_path += '.sim'
            self.loadingpath = self.save_path
            Publisher.sendMessage('SetSavePath',path=self.save_path) #send message to canvascontroller.SaveSimulation
            txt = save.Filename.split('.sim')[0]
            e = dict(cat=self.Toolbox.cat, txt=txt, fullpath=save.Path)
            events.onSimulationSaved.fire(**e)  # calls loadSIMFile from logicToolBox
        else:
            save.Destroy()

    def onDirectory(self, event):
        ToolboxPane = self.m_mgr.GetPane(self.Toolbox)
        ToolboxPane.Hide()
        DirectoryPane = self.m_mgr.GetPane(self.Directory)
        DirectoryPane.Show(show=True)
        self.m_mgr.Update()
        pass

    def onAllFiles(self, event):
        DirectoryPane = self.m_mgr.GetPane(self.Directory)
        DirectoryPane.Hide()
        ToolboxPane = self.m_mgr.GetPane(self.Toolbox)
        ToolboxPane.Show(show=True)
        self.m_mgr.Update()
        pass

    def onConsole(self, event):
        ConsolePane = self.m_mgr.GetPane(self.bnb)
        Toggle = 1
        if event.Selection == 0:
            ConsolePane.Show(show=True)
            Toggle = 1
        if event.Selection == 1:
            ConsolePane.Hide()
            Toggle = 0
        self.m_mgr.Update()
        pass

    # todo: temporarily disabled until we fix the AUI manager bugs
    # def defaultview(self, event):
    #     self.onAllFiles(event)
    #     ConsolePane = self.m_mgr.GetPane(self.bnb)
    #     ConsolePane.Show(show=True)
    #     # self.m_mgr.ClosePane(self.bnb)
    #     # self.m_mgr.AddPane(self.bnb,
    #     #                    aui.AuiPaneInfo().
    #     #                    Center().
    #     #                    Name("Console").
    #     #                    Position(1).
    #     #                    CloseButton(False).
    #     #                    MaximizeButton(True)
    #     #                    .Movable()
    #     #                    .MinimizeButton(True).
    #     #                    PinButton(True).
    #     #                    Resizable().
    #     #                    Floatable().
    #     #                    MinSize(wx.Size(1200, 200)))
    #     self.m_mgr.Update()
    #
    #     pass

class ModelView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.contents = wx.html2.WebView.New(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.contents, 1, wx.ALL|wx.EXPAND, 5)
        parent.SetSizer(sizer)
        self.SetSizerAndFit(sizer)

    def setText(self, value=None):
        self.contents.SetPage(value, "")

class AllFileView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

class TimeSeries(wx.Panel):
    """

    """

    def __init__( self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500,500), style=wx.TAB_TRAVERSAL)

        self._databases = {}
        self._connection_added = True

        # self.__logger = logging.getLogger('root')


        connection_choices = []
        self.connection_combobox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), connection_choices, 0)
        self.__selected_choice_idx = 0
        self.connection_combobox.SetSelection(self.__selected_choice_idx)

        self.connection_refresh_button = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        self.addConnectionButton = wx.Button(self, wx.ID_ANY, u"Add Connection", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_olvSeries = LogicDatabase(self, pos=wx.DefaultPosition, size=wx.DefaultSize, id=wx.ID_ANY,
                                         style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.m_olvSeries.DefineColumns(self.table_columns)

        # Bindings
        self.addConnectionButton.Bind(wx.EVT_LEFT_DOWN, self.AddConnection)
        self.addConnectionButton.Bind(wx.EVT_MOUSEWHEEL, self.AddConnection_MouseWheel)

        self.connection_refresh_button.Bind(wx.EVT_LEFT_DOWN, self.OLVRefresh)
        self.connection_combobox.Bind(wx.EVT_CHOICE, self.DbChanged)
        self.connection_combobox.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.RefreshComboBox)


        # Sizers
        seriesSelectorSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.SetMinSize(wx.Size(-1, 45))

        buttonSizer.Add(self.connection_combobox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        buttonSizer.Add(self.addConnectionButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        buttonSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        buttonSizer.Add(self.connection_refresh_button, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        seriesSelectorSizer.Add( buttonSizer, 0, wx.ALL|wx.EXPAND, 5)
        seriesSelectorSizer.Add(self.m_olvSeries, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(seriesSelectorSizer)
        self.Layout()

        # Publisher.subscribe(self.connection_added_status, "connectionAddedStatus")

        engineEvent.onDatabaseConnected += self.refreshConnectionsListBox

        # build custom context menu
        menu = TimeSeriesContextMenu(self.m_olvSeries)
        self.m_olvSeries.setContextMenu(menu)

        # object to hold the current session
        self.__current_session = None

    def RefreshComboBox(self, event):
        pass


    def DbChanged(self, event):

        # refresh the database
        # self refresh_database
        self.OLVRefresh(event)




    def refreshConnectionsListBox(self, connection_added):

        if connection_added:
            self._databases = engine.getDbConnections()

            choices = ['---']
            for k,v in self._databases.iteritems():
                choices.append(self._databases[k]['name'])
            self.connection_combobox.SetItems(choices)

            # set the selected choice
            self.connection_combobox.SetSelection( self.__selected_choice_idx)

    def connection_added_status(self,value=None,connection_string=''):
        if value is not None:
            self._connection_added = value
            self._conection_string = connection_string
        return self._connection_added

    def AddConnection_MouseWheel(self, event):
        '''
        This is intentionally empty to disable mouse scrolling in the AddConnection combobox
        :param event: EVT_MOUSEWHEEL
        :return: None
        '''
        pass

    def AddConnection(self, event):

        params = []

        while 1:
            dlg = AddConnectionDialog(self, -1, "Sample Dialog", size=(350, 200),
                             style=wx.DEFAULT_DIALOG_STYLE,
                             )
            dlg.CenterOnScreen()

            if params:
                dlg.set_values(title=params[0],
                                  desc = params[1],
                                  engine = params[2],
                                  address = params[3],
                                  name = params[4],
                                  user = params[5],
                                  pwd = params[6])

            # this does not return until the dialog is closed.
            val = dlg.ShowModal()


            if val == 5101:
                # cancel is selected
                return
            elif val == 5100:
                params = dlg.getConnectionParams()

                dlg.Destroy()



                # create the database connection
                Publisher.sendMessage('DatabaseConnection',
                                      title=params[0],
                                      desc = params[1],
                                      dbengine = params[2],
                                      address = params[3],
                                      name = params[4],
                                      user = params[5],
                                      pwd = params[6])

                if self.connection_added_status():
                    Publisher.sendMessage('getDatabases')
                    return
                else:

                    wx.MessageBox('I was unable to connect to the database with the information provided :(', 'Info', wx.OK | wx.ICON_ERROR)

    def refresh_database(self):

        # get the name of the selected database
        selected_db = self.connection_combobox.GetStringSelection()

        #set the selected choice
        self.__selected_choice_idx = self.connection_combobox.GetSelection()

        for key, db in self._databases.iteritems():

            # get the database session associated with the selected name
            if db['name'] == selected_db:

                # query the database and get basic series info

                # TODO : session wont exist here anymore!!!
                session = dbUtilities.build_session_from_connection_string(db['connection_string'])

                u = dbapi.utils(session)
                series = u.getAllSeries()

                if series is None:
                    d = {key: value for (key, value) in
                         zip([col.lower().replace(' ','_') for col in self.table_columns],["" for c in self.table_columns])}
                    record_object = type('DataRecord', (object,), d)
                    data = [record_object]
                else:

                    # loop through all of the returned data
                    data = []
                    for s in series:
                        d = {
                            'resultid' : s.ResultID,
                            'variable' : s.VariableObj.VariableCode,
                            'unit' : s.UnitObj.UnitsName,
                            'date_created' : s.FeatureActionObj.ActionObj.BeginDateTime,
                            'type' : s.FeatureActionObj.ActionObj.ActionTypeCV,
                            'featurecode' : s.FeatureActionObj.SamplingFeatureObj.SamplingFeatureCode,
                            'organization' : s.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName
                        }

                        record_object = type('DataRecord', (object,), d)
                        data.extend([record_object])

                # set the data objects in the olv control
                self.m_olvSeries.SetObjects(data)

                # set the current database in canvas controller
                Publisher.sendMessage('SetCurrentDb',value=selected_db)  # sends to CanvasController.getCurrentDbSession

                # fire the onDbChanged Event
                kwargs = dict(dbsession=session,
                              dbname=db['name'],
                              dbid=db['id'] )
                events.onDbChanged.fire(**kwargs)

                break

        return

    def OLVRefresh(self, event):

        thr = threading.Thread(target=self.refresh_database, args=(), kwargs={})
        thr.start()

class DataSeries(wx.Panel):
    """

    """

    def __init__( self, parent ):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 500),
                          style=wx.TAB_TRAVERSAL)

        self._databases = {}
        self._connection_added = True

        connection_choices = []
        self.connection_combobox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), connection_choices,
                                             0)
        self.__selected_choice_idx = 0
        self.connection_combobox.SetSelection(0)

        self.connection_refresh_button = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        self.addConnectionButton = wx.Button(self, wx.ID_ANY, u"Add Connection", wx.DefaultPosition, wx.DefaultSize, 0)

        self.table = LogicDatabase(self, pos=wx.DefaultPosition, size=wx.DefaultSize, id=wx.ID_ANY,
                                   style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        # Bindings
        self.addConnectionButton.Bind(wx.EVT_LEFT_DOWN, self.AddConnection)
        self.addConnectionButton.Bind(wx.EVT_MOUSEWHEEL, self.AddConnection_MouseWheel)

        self.connection_refresh_button.Bind(wx.EVT_LEFT_DOWN, self.database_refresh)
        self.connection_combobox.Bind(wx.EVT_CHOICE, self.DbChanged)

        # Sizers
        seriesSelectorSizer = wx.BoxSizer( wx.VERTICAL )
        buttonSizer = wx.BoxSizer( wx.HORIZONTAL )
        buttonSizer.SetMinSize( wx.Size( -1,45 ) )

        buttonSizer.Add( self.connection_combobox, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        buttonSizer.Add( self.addConnectionButton, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        buttonSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        buttonSizer.Add( self.connection_refresh_button, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
        seriesSelectorSizer.Add( buttonSizer, 0, wx.ALL|wx.EXPAND, 5 )
        seriesSelectorSizer.Add( self.table, 1, wx.ALL|wx.EXPAND, 5 )

        self.SetSizer( seriesSelectorSizer )
        self.Layout()

        #databases = Publisher.sendMessage('getDatabases')
        # Publisher.subscribe(self.getKnownDatabases, "getKnownDatabases")  # sends message to CanvasController
        # Publisher.subscribe(self.connection_added_status, "connectionAddedStatus")
        engineEvent.onDatabaseConnected += self.refreshConnectionsListBox

    def DbChanged(self, event):
        self.database_refresh(event)

    def refreshConnectionsListBox(self, connection_added):

        if connection_added:
            self._databases = engine.getDbConnections()

            choices = ['---']
            for k,v in self._databases.iteritems():
                choices.append(self._databases[k]['name'])
            self.connection_combobox.SetItems(choices)

            # set the selected choice
            self.connection_combobox.SetSelection( self.__selected_choice_idx)

    def connection_added_status(self,value=None,connection_string=''):
        if value is not None:
            self._connection_added = value
            self._connection_string = connection_string
        return self._connection_added

    def AddConnection_MouseWheel(self, event):
        '''
        This is intentionally empty to disable mouse scrolling in the AddConnection combobox
        :param event: EVT_MOUSEWHEEL
        :return: None
        '''
        pass

    def AddConnection(self, event):

        params = []

        while 1:
            dlg = AddConnectionDialog(self, -1, "Sample Dialog", size=(350, 200),
                             style=wx.DEFAULT_DIALOG_STYLE,
                             )
            dlg.CenterOnScreen()

            if params:
                dlg.set_values(title=params[0],
                                  desc = params[1],
                                  engine = params[2],
                                  address = params[3],
                                  name = params[4],
                                  user = params[5],
                                  pwd = params[6])

            # this does not return until the dialog is closed.
            val = dlg.ShowModal()


            if val == 5101:
                # cancel is selected
                return
            elif val == 5100:
                params = dlg.getConnectionParams()

                dlg.Destroy()



                # create the database connection
                Publisher.sendMessage('DatabaseConnection',
                                      title=params[0],
                                      desc = params[1],
                                      engine = params[2],
                                      address = params[3],
                                      name = params[4],
                                      user = params[5],
                                      pwd = params[6])

                if self.connection_added_status():
                    Publisher.sendMessage('getDatabases')
                    return
                else:

                    wx.MessageBox('I was unable to connect to the database with the information provided :(', 'Info', wx.OK | wx.ICON_ERROR)

    def load_data(self):
        raise Exception('Abstract method. Must be overridden!')

    def database_refresh(self, event):

        thr = threading.Thread(target=self.load_data, args=(), kwargs={})
        thr.start()

class SimulationDataTable(DataSeries):
    def __init__(self, parent):
        #wx.Panel.__init__(self, parent)

        super(SimulationDataTable, self ).__init__(parent)

        self.table_columns = ["Simulation ID", "Simulation Name", "Model Name", "Simulation Start", "Simulation End", "Date Created","Owner"]
        #table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.table.DefineColumns(self.table_columns)

        self.__selected_choice_idx = 0

        # build custom context menu
        menu = SimulationContextMenu(self.table)
        self.table.setContextMenu(menu)

    def load_data(self):

        # get the name of the selected database
        selected_db = self.connection_combobox.GetStringSelection()

        #set the selected choice
        self.__selected_choice_idx = self.connection_combobox.GetSelection()

        for key, db in self._databases.iteritems():        # # deactivate the console if we are in debug mode
        # if not sys.gettrace():
        #     redir = RedirectText(self.log)
        #     sys.stdout = redir

            # get the database session associated with the selected name
            if db['name'] == selected_db:


                # build the database session
                session = dbUtilities.build_session_from_connection_string(db['connection_string'])

                u = dbapi.utils(session)
                simulations = u.getAllSimulations()


                sim_ids = []
                if simulations is None:
                    d = {key: value for (key, value) in
                         zip([col.lower().replace(' ','_') for col in self.table_columns],["" for c in self.table_columns])}
                    record_object = type('DataRecord', (object,), d)
                    data = [record_object]
                else:
                    data = []

                    # loop through all of the returned data

                    for s in simulations:

                        simulation_id = s.Simulation.SimulationID

                        # only add if the simulation id doesn't already exist in sim_ids
                        if simulation_id not in sim_ids:
                            sim_ids.append(simulation_id)

                            d = {
                                'simulation_id' : s.Simulation.SimulationID,
                                'simulation_name' : s.Simulation.SimulationName,
                                'model_name' : s.Model.ModelName,
                                'date_created' : s.Action.BeginDateTime,
                                'owner' : s.Person.PersonLastName,
                                'simulation_start' : s.Simulation.SimulationStartDateTime,
                                'simulation_end' : s.Simulation.SimulationEndDateTime,
                            }

                            record_object = type('DataRecord', (object,), d)
                            data.extend([record_object])

                # set the data objects in the olv control
                self.table.SetObjects(data)

                # set the current database in canvas controller
                Publisher.sendMessage('SetCurrentDb',value=selected_db)  # sends to CanvasController.getCurrentDbSession

class consoleOutput(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        # self.logger = logging.getLogger('wxApp')
        # self.elogger= logging.getLogger('ENGINE_LOG')

        # Add a panel so it looks the correct on all platforms
        # self.log = wx.TextCtrl(self, -1, size=(100,100),
        #                   style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)


        self.log = wx.richtext.RichTextCtrl(self, -1, size=(100,100),
                                            style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL|wx.SIMPLE_BORDER|wx.CURSOR_NONE)



        self.log.Bind(wx.EVT_CONTEXT_MENU, self.onRightUp)

        #
        # # deactivate the console if we are in debug mode
        # if not sys.gettrace():
        #     redir = RedirectText(self.log)
        #     sys.stdout = redir


        # Add widgets to a sizer
        sizer = wx.BoxSizer()
        sizer.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)


        self.SetSizerAndFit(sizer)

    def onRightUp(self, event):
        self.log.PopupMenu(ConsoleContextMenu(self, event))

class RedirectText(object):

    def __init__(self,TextCtrl):

        self.out=TextCtrl
        self.__line_num = 0

    def line_num(self,reset=False):
        if not reset:
            self.__line_num += 1
            return self.__line_num
        else:
            self.__line_num = 0

    def write(self,string):

        args = string.split('|')
        string = args[-1]
        args = [a.strip() for a in args[:-1]]

        if len(string.strip()) > 0:

            string += '\n'
            if 'RESET' in args:
                self.line_num(reset=True)
                return


            string = str(self.line_num())+ ':  '+string if string != '\n' else string
            self.out.SetInsertionPoint(0)
            if 'WARNING' in args:
                self.out.BeginTextColour((255, 140, 0))
            elif 'ERROR' in args:
                self.out.BeginTextColour((255, 0, 0))
            elif not 'DEBUG' in args:
                self.out.BeginTextColour((0, 0, 0))

            # self.out.Text =  self.out.Text.Insert(string+ "\n");

            self.out.WriteText(string)
            self.out.EndTextColour()

            self.out.Refresh()

    def flush(self):
        pass

class AddConnectionDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,
            ):

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        self.PostCreate(pre)

        gridsizer = wx.FlexGridSizer(rows=7,cols=2,hgap=5,vgap=5)

        titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(self, -1, "Database Connection")
        titleSizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        ######################################################

        label = wx.StaticText(self, -1, "*Title :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Title of the database connection")
        self.title = wx.TextCtrl(self, wx.ID_ANY, '', size=(200,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.title, 0, wx.EXPAND)


        label = wx.StaticText(self, -1, "Description :")
        label.SetHelpText("Description of the database connection")
        self.description = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.description, 0, wx.EXPAND)

        ######################################################


        label = wx.StaticText(self, -1, "*Engine :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Database Parsing Engine (e.g. mysql, psycopg2, etc)")
        #self.engine = wx.TextCtrl(self, -1, "", size=(80,-1))
        engine_choices = ['PostgreSQL', 'MySQL']
        self.engine = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, engine_choices, 0 )
        self.engine.SetSelection( 0 )
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.engine, 0, wx.EXPAND)


        label = wx.StaticText(self, -1, "*Address :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Database Address")
        self.address = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.address, 0, wx.EXPAND)

        label = wx.StaticText(self, -1, "*Database :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Database Name")
        self.name = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.name, 0, wx.EXPAND)

        label = wx.StaticText(self, -1, "*User :")
        label.SetFont(label.GetFont().MakeBold())
        label.SetHelpText("Database Username")
        self.user = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.user, 0, wx.EXPAND)

        label = wx.StaticText(self, -1, "Password :")
        label.SetHelpText("Database Password")
        self.password = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(label, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.password, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(titleSizer, 0, wx.CENTER)
        sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(gridsizer, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizeHints(250,300,500,400)


        btnsizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)

        self.btnok = wx.Button(self, wx.ID_OK)
        self.btnok.SetDefault()
        btnsizer.AddButton(self.btnok)
        self.btnok.Disable()

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


        #self.engine.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.address.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.name.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.user.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.title.Bind(wx.EVT_TEXT, self.OnTextEnter)


    def set_values(self,title,desc,engine, address, name, user,pwd):
        self.title.Value = title
        self.description.Value = desc
        self.engine.Value = engine
        self.address.Value = address
        self.name.Value = name
        self.user.Value = user
        self.password.Value = pwd

    def getConnectionParams(self):

        engine = self.engine.GetStringSelection().lower()

        #engine = self.engine.GetValue()
        address = self.address.GetValue()
        name = self.name.GetValue()
        user = self.user.GetValue()
        pwd = self.password.GetValue()
        title = self.title.GetValue()
        desc = self.description.GetValue()

        return title,desc, engine,address,name,user,pwd,title,desc

    def OnTextEnter(self, event):
        if self.address.GetValue() == '' or  \
                self.name.GetValue() == '' or  \
                self.user.GetValue() == '' or \
                self.title.GetValue() =='' :
            self.btnok.Disable()
        else:
            self.btnok.Enable()