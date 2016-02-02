__author__ = 'Francisco'

import threading
import sys
import wx
from wx.lib.pubsub import pub as Publisher
from wx import richtext
from gui.controller.DatabaseCtrl import LogicDatabase
import coordinator.events as engineEvent
from ContextView import TimeSeriesContextMenu, SimulationContextMenu, ConsoleContextMenu
import coordinator.engineAccessors as engine
from utilities import db as dbUtilities
from db import dbapi as dbapi
from gui import events
from coordinator.emitLogging import elog
from gui.controller import ConsoleOutputCtrl
from gui.controller.WofSitesCtrl import WofSitesViewerCtrl
from gui.controller.AddConnectionCtrl import AddConnectionCtrl
from webservice import wateroneflow
from gui.controller.ConsoleOutputCtrl import consoleCtrl
import db.dbapi_v2 as db2
from odm2api.ODMconnection import dbconnection

class viewLowerPanel:
    def __init__(self, notebook):

        console =  consoleCtrl(notebook)
        timeseries = TimeSeriesTab(notebook)
        simulations = SimulationDataTab(notebook)

        notebook.AddPage(console, "Console")
        notebook.AddPage(timeseries, "Time Series")
        notebook.AddPage(simulations, "Simulations")

class TimeSeriesTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._databases = {}
        self._connection_added = True

        connection_choices = []
        self.connection_combobox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), connection_choices,
                                             0)
        self.__selected_choice_idx = 0
        self.connection_combobox.SetSelection(self.__selected_choice_idx)

        self.connection_refresh_button = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        self.addConnectionButton = wx.Button(self, wx.ID_ANY, u"Add Connection", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_olvSeries = LogicDatabase(self, pos=wx.DefaultPosition, size=wx.DefaultSize, id=wx.ID_ANY,
                                         style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.m_olvSeries.DefineColumns(self.table_columns)

        seriesSelectorSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.SetMinSize(wx.Size(-1, 45))

        buttonSizer.Add(self.connection_combobox, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=2)
        buttonSizer.Add(self.addConnectionButton, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        buttonSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        buttonSizer.Add(self.connection_refresh_button, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=2)
        seriesSelectorSizer.Add( buttonSizer, 0, wx.ALL|wx.EXPAND, 0)
        seriesSelectorSizer.Add(self.m_olvSeries, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(seriesSelectorSizer)
        self.Layout()

        engineEvent.onDatabaseConnected += self.refreshConnectionsListBoxTS

        # build custom context menu
        menu = TimeSeriesContextMenu(self.m_olvSeries)
        self.m_olvSeries.setContextMenu(menu)

        # object to hold the current session
        self.__current_session = None

        # intialize key bindings
        self.initBindings()

    def initBindings(self):
        self.addConnectionButton.Bind(wx.EVT_LEFT_DOWN, self.AddConnection)
        self.connection_refresh_button.Bind(wx.EVT_LEFT_DOWN, self.OLVRefresh)
        self.connection_combobox.Bind(wx.EVT_CHOICE, self.DbChanged)


    def DbChanged(self, event):
        # refresh the database
        self.OLVRefresh(event)

    def refreshConnectionsListBoxTS(self, connection_added):

        if connection_added:
            self._databases = engine.getDbConnections()

            choices = ['---']
            for k, v in self._databases.iteritems():
                choices.append(self._databases[k]['name'])

            for key, value in self.getPossibleConnections().iteritems():
                choices.append(key)

            choices.sort()

            self.connection_combobox.SetItems(choices)


            # set the selected choice
            self.connection_combobox.SetSelection( self.__selected_choice_idx)

    def connection_added_status(self, value=None, connection_string=''):
        if value is not None:
            self._connection_added = value
            self._conection_string = connection_string
        return self._connection_added

    def AddConnection(self, event):
        connection = AddConnectionCtrl(self)


    def getPossibleConnections(self):
        wsdl = {}
        wsdl["Red Butte Creek"] = "http://data.iutahepscor.org/RedButteCreekWOF/cuahsi_1_1.asmx?WSDL"
        wsdl["Provo River"] = "http://data.iutahepscor.org/ProvoRiverWOF/cuahsi_1_1.asmx?WSDL"
        wsdl["Logan River"] = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"

        return wsdl

    def prepareODM1_Model(self, siteObject):
        self.selectedVariables = None
        siteview = WofSitesViewerCtrl(self, siteObject, self.api)
        return

    def getParsedValues(self, siteObject, startDate, endDate):
        values = self.api.parseValues(siteObject.site_code, self.selectedVariables, startDate, endDate)
        return values

    def setup_wof_table(self, api):
        self.wofsites = api.getSites()
        api.network_code = self.wofsites[0].siteInfo.siteCode[0]._network
        self.table_columns = ["Site Name", "Network", "County", "State", "Site Type", "Site Code"]
        self.m_olvSeries.DefineColumns(self.table_columns)

        output = []
        for site in self.wofsites:
            properties = {prop._name.lower(): prop.value for prop in site.siteInfo.siteProperty if 'value' in prop }
            d = {
                "site_name": site.siteInfo.siteName,  # The key MUST match one in the table_columns IN LOWERCASE. FYI
                "network": site.siteInfo.siteCode[0]._network,
                "county": properties['county'],
                "state": properties['state'],
                "site_type": properties['site type'],
                "site_code": site.siteInfo.siteCode[0].value,
            }

            record_object = type('WOFRecord', (object,), d)
            output.extend([record_object])
        self.m_olvSeries.AutoSizeColumns()
        self.m_olvSeries.SetObjects(output)
        self.m_olvSeries.SetColumnWidth(0, 500)
        self.m_olvSeries.SetColumnWidth(1, 150)
        self.m_olvSeries.SetColumnWidth(2, 150)
        self.m_olvSeries.SetColumnWidth(3, 150)
        self.m_olvSeries.SetColumnWidth(4, 165)
        self.m_olvSeries.SetColumnWidth(5, 200)

    def refresh_database(self):
        # get the name of the selected database
        selected_db = self.connection_combobox.GetStringSelection()

        for key, value in self.getPossibleConnections().iteritems():
            if selected_db == key:
                return value

        self.table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.m_olvSeries.DefineColumns(self.table_columns)

        self.__selected_choice_idx = self.connection_combobox.GetSelection()

        for key, db in self._databases.iteritems():
            # get the database session associated with the selected name
            if db['name'] == selected_db:

                # query the database and get basic series info

                series = None
                # fixme: This breaks for SQLite since it is implemented in dbapi_v2
                if db['args']['engine'] == 'sqlite':
                    session = dbconnection.createConnection(engine=db['args']['engine'], address=db['args']['address'])
                    # gui_utils.connect_to_db()
                    s = db2.connect(session)
                    series = s.getAllSeries()

                else:  # fixme: this is old api for postgresql and mysql (need to update to dbapi_v2)
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
                            'resultid': s.ResultID,
                            'variable': s.VariableObj.VariableCode,
                            'unit': s.UnitObj.UnitsName,
                            'date_created': s.FeatureActionObj.ActionObj.BeginDateTime,
                            'type': s.FeatureActionObj.ActionObj.ActionTypeCV,
                            'featurecode': s.FeatureActionObj.SamplingFeatureObj.SamplingFeatureCode,
                            'organization': s.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName
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
                              dbid=db['id'])
                events.onDbChanged.fire(**kwargs)
                break

        return

    def OLVRefresh(self, event):
        # if sys.gettrace():
        #     #  In debug mode
        #     self.refresh_database()
        # else:
        #     # Not in debug mode
        #     thr = threading.Thread(target=self.refresh_database, name='DATABASE REFRESH THREAD', args=(), kwargs={})
        #     thr.start()
        value = self.refresh_database()
        if value is not None:
            try:
                self.api = wateroneflow.WaterOneFlow(value)
                self.setup_wof_table(self.api)
            except Exception:
                elog.debug("Wof web service took to long or failed.")
                elog.info("Web service took to long. Wof may be down.")

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
        self.SetSizeHints(250, 300, 500, 400)


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
                self.title.GetValue() == '':
            self.btnok.Disable()
        else:
            self.btnok.Enable()

class DataSeries(wx.Panel):
    def __init__(self, parent):
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



        # Sizers
        seriesSelectorSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.SetMinSize(wx.Size(-1, 45))

        buttonSizer.Add(self.connection_combobox, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=2)
        buttonSizer.Add(self.addConnectionButton, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        buttonSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        buttonSizer.Add(self.connection_refresh_button, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=2)
        seriesSelectorSizer.Add( buttonSizer, 0, wx.ALL|wx.EXPAND, 0)
        seriesSelectorSizer.Add(self.table, 1, wx.ALL|wx.EXPAND, 0)

        self.SetSizer(seriesSelectorSizer)
        self.Layout()

        engineEvent.onDatabaseConnected += self.refreshConnectionsListBox

        # initialize key bindings
        self.initBindings()

    def initBindings(self):
        # Bindings
        self.addConnectionButton.Bind(wx.EVT_LEFT_DOWN, self.AddConnection)
        self.connection_refresh_button.Bind(wx.EVT_LEFT_DOWN, self.database_refresh)
        self.connection_combobox.Bind(wx.EVT_CHOICE, self.DbChanged)

    def DbChanged(self, event):
        self.database_refresh(event)

    def refreshConnectionsListBox(self, connection_added):

        if connection_added:
            self._databases = engine.getDbConnections()

            choices = ['---']
            for k, v in self._databases.iteritems():
                choices.append(self._databases[k]['name'])
            self.connection_combobox.SetItems(choices)

            # set the selected choice
            self.connection_combobox.SetSelection( self.__selected_choice_idx)

    def connection_added_status(self,value=None,connection_string=''):
        if value is not None:
            self._connection_added = value
            self._connection_string = connection_string
        return self._connection_added

    def AddConnection(self, event):

        params = []
        p = self
        newConnection = AddConnectionCtrl(p)
        """
        while 1:
            dlg = AddConnectionDialog(self, -1, "Sample Dialog2", size=(350, 200),
                             style=wx.DEFAULT_DIALOG_STYLE,
                             )
            dlg.CenterOnScreen()

            if params:
                dlg.set_values(title=params[0],
                                  desc=params[1],
                                  engine=params[2],
                                  address=params[3],
                                  name=params[4],
                                  user=params[5],
                                  pwd=params[6])

            # this does not return until the dialog is closed.
            val = dlg.ShowModal()


            if val == 5101:
                # cancel is selected
                return
            elif val == 5100:
                params = dlg.getConnectionParams()
                print len(params)
                print params[6]
                dlg.Destroy()
                pwd = params[6]

                # create the database connection
                Publisher.sendMessage('DatabaseConnection',
                                      title=params[0],
                                      desc = params[1],
                                      engine = params[2],
                                      address = params[3],
                                      name = params[4],
                                      user = params[5],
                                      pwd = pwd)

                if self.connection_added_status():
                    Publisher.sendMessage('getDatabases')
                    return
                else:

                    wx.MessageBox('I was unable to connect to the database with the information provided :(', 'Info', wx.OK | wx.ICON_ERROR)
            """

    def load_data(self):
        elog.error('Abstract method. Must be overridden!')
        raise Exception('Abstract method. Must be overridden!')

    def database_refresh(self, event):
        if sys.gettrace():
            #  In debug mode
            self.load_data()
        else:
            # Not in debug mode
            thr = threading.Thread(target=self.load_data, args=(), kwargs={}, name='DataSeriesRefresh')
            thr.start()

class SimulationDataTab(DataSeries):
    def __init__(self, parent):
        #  wx.Panel.__init__(self, parent)

        super(SimulationDataTab, self).__init__(parent)
        self.parent = parent

        self.table_columns = ["Simulation ID", "Simulation Name", "Model Name", "Simulation Start", "Simulation End", "Date Created","Owner"]
        #  table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.table.DefineColumns(self.table_columns)

        self.__selected_choice_idx = 0

        # build custom context menu
        menu = SimulationContextMenu(self.table)
        self.table.setContextMenu(menu)
        self.conn = None

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
            isSqlite = False

            if db['name'] == selected_db:
                simulations = None

                if db['args']['engine'] == 'sqlite':
                    session = dbconnection.createConnection(engine=db['args']['engine'], address=db['args']['address'])
                    self.conn = db2.connect(session)
                    simulations = self.conn.getAllSimulations()
                    isSqlite = True
                    self.conn.getCurrentSession()
                else:
                    session = dbUtilities.build_session_from_connection_string(db['connection_string'])
                    # build the database session

                    u = dbapi.utils(session)
                    simulations = u.getAllSimulations()


                #     # gui_utils.connect_to_db()
                #
                #
                # else: # fixme: this is old api for postgresql and mysql (need to update to dbapi_v2)
                #     session = dbUtilities.build_session_from_connection_string(db['connection_string'])
                #     u = dbapi.utils(session)
                #     series = u.getAllSeries()


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
                        simulation = None
                        if isSqlite:
                            simulation = s.Simulations
                            person = s.People
                            action = s.Actions
                            model = s.Models
                        else:
                            simulation = s.Simulation
                            person = s.Person
                            action = s.Action
                            model = s.Model

                        simulation_id = simulation.SimulationID

                        # only add if the simulation id doesn't already exist in sim_ids
                        if simulation_id not in sim_ids:
                            sim_ids.append(simulation_id)

                            d = {
                                'simulation_id': simulation.SimulationID,
                                'simulation_name': simulation.SimulationName,
                                'model_name': model.ModelName,
                                'date_created': action.BeginDateTime,
                                'owner': person.PersonLastName,
                                'simulation_start': simulation.SimulationStartDateTime,
                                'simulation_end': simulation.SimulationEndDateTime,
                                'model_id': simulation.ModelID
                            }

                            record_object = type('DataRecord', (object,), d)
                            data.extend([record_object])

                # set the data objects in the olv control
                self.table.SetObjects(data)

                # set the current database in canvas controller
                Publisher.sendMessage('SetCurrentDb', value=selected_db)  # sends to CanvasController.getCurrentDbSession
