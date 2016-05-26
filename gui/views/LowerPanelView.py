import ConfigParser
import sys
import threading
import xml.etree.ElementTree

import wx
from odm2api.ODMconnection import dbconnection as dbconnection2
import odm2api

from wx.lib.pubsub import pub as Publisher

import coordinator.engineAccessors as engine
import coordinator.events as engineEvent
import db.dbapi_v2 as db2
from ContextView import TimeSeriesContextMenu, SimulationContextMenu #, ConsoleContextMenu
# from api_old.ODMconnection import  dbconnection
from db import dbapi as dbapi
from emitLogging import elog
from gui import events
from gui.controller.AddConnectionCtrl import AddConnectionCtrl
from gui.controller.ConsoleOutputCtrl import consoleCtrl
from gui.controller.DatabaseCtrl import DatabaseCtrl
from gui.controller.SimulationPlotCtrl import SimulationPlotCtrl
from gui.controller.TimeSeriesObjectCtrl import TimeSeriesObjectCtrl
from gui.controller.WofSitesCtrl import WofSitesCtrl
from sprint import *
from utilities import db as dbUtilities
from webservice import wateroneflow
from gui.controller.NewTimeSeriesCtrl import NewTimeSeriesCtrl


class ViewLowerPanel:
    def __init__(self, notebook):

        console = consoleCtrl(notebook)
        timeseries = TimeSeriesTab(notebook)
        # timeseries = NewTimeSeriesCtrl(notebook)
        simulations = SimulationDataTab(notebook)
        notebook.AddPage(console, "Console")
        notebook.AddPage(timeseries, "Time Series")
        notebook.AddPage(simulations, "Simulations")


class multidict(dict):
    """
    Dictionary class that has been extended for Ordering and Duplicate Keys
    """

    def __init__(self, *args, **kw):
        self.itemlist = super(multidict, self).keys()
        self._unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^' + str(self._unique)
        self.itemlist.append(key)
        dict.__setitem__(self, key, val)

    def __iter__(self):
        return iter(self.itemlist)

    def keys(self):
        return self.itemlist

    def values(self):
        return [self[key] for key in self]

    def itervalues(self):
        return (self[key] for key in self)


class TimeSeriesTab(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self._databases = {}

        connection_choices = []
        self.connection_combobox = wx.Choice(self, size=(200, -1), choices=connection_choices)
        self.__selected_choice_idx = 0
        self.connection_combobox.SetSelection(self.__selected_choice_idx)

        self.connection_refresh_button = wx.Button(self, label="Refresh")
        self.addConnectionButton = wx.Button(self, label="Add Connection")
        self.table = DatabaseCtrl(self)
        self.table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.table.DefineColumns(self.table_columns)

        seriesSelectorSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.SetMinSize(wx.Size(-1, 45))

        buttonSizer.Add(self.connection_combobox, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=2)
        buttonSizer.Add(self.addConnectionButton, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
        buttonSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
        buttonSizer.Add(self.connection_refresh_button, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=2)
        seriesSelectorSizer.Add( buttonSizer, 0, wx.ALL | wx.EXPAND, 0)
        seriesSelectorSizer.Add(self.table, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(seriesSelectorSizer)

        engineEvent.onDatabaseConnected += self.refreshConnectionsListBoxTS

        # build custom context menu
        self.menu = TimeSeriesContextMenu(self.table)
        self.table.setContextMenu(self.menu)

        # intialize key bindings
        self.initBindings()

    def initBindings(self):
        self.addConnectionButton.Bind(wx.EVT_BUTTON, self.AddConnection)
        self.connection_refresh_button.Bind(wx.EVT_BUTTON, self.OLVRefresh)
        self.connection_combobox.Bind(wx.EVT_CHOICE, self.DbChanged)

    def DbChanged(self, event):
        # refresh the database
        self.OLVRefresh(event)

    def refreshConnectionsListBoxTS(self, connection_added):
        self._databases = engine.getDbConnections()

        choices = ['---']
        for k, v in self._databases.iteritems():
            choices.append(self._databases[k]['name'])

        wofconnections = self.get_possible_wof_connections()
        for con in wofconnections:
            for key, value in con.iteritems():
                if key == 'name':
                    choices.append(value)

        choices.sort()

        self.connection_combobox.SetItems(choices)

    def AddConnection(self, event):
        connection = AddConnectionCtrl(self)

    def getParsedValues(self, siteObject, startDate, endDate):
        values = self.api.parseValues(siteObject.site_code, self.selectedVariables, startDate, endDate)
        return values

    def get_possible_wof_connections(self):
        currentdir = os.path.dirname(os.path.abspath(__file__))
        wof_txt = os.path.abspath(os.path.join(currentdir, '../../data/wofsites'))
        cparser = ConfigParser.ConfigParser(None, multidict)
        cparser.read(wof_txt)
        sections = cparser.sections()
        wsdl = []

        for s in sections:
            d={}
            options = cparser.options(s)
            for option in options:
                d[option] = cparser.get(s, option)

            wsdl.append(d)
        return wsdl

    def open_odm2_viewer(self, object):
        variable_list_entries = {}
        variable_list_entries[object.resultid] = [object.featurecode, object.variable, object.unit, object.type, object.organization, object.date_created]
        TimeSeriesObjectCtrl(parentClass=self, timeseries_variables=variable_list_entries)

    def open_wof_viewer(self, siteObject):
        self.selectedVariables = None
        siteview = WofSitesCtrl(self, siteObject, self.api)
        return

    def generate_wof_data_from_XML(self):
        root = xml.etree.ElementTree.parse('wof.xml').getroot()
        output = []
        for child in root:
            if "site" in child.tag:
                d = []
                for step_child in child:
                    for onemore in step_child:
                        if "siteName" in onemore.tag:
                            d.append(['site_name', onemore.text])
                        if "siteCode" in onemore.tag:
                            d.append(['network', onemore.items()[1][1]])
                            d.append(['site_code', onemore.text])
                        if "siteProperty" in onemore.tag:
                            if onemore.attrib.items()[0][1] == "County":
                                d.append(['county', onemore.text])
                            if onemore.attrib.items()[0][1] == "State":
                                d.append(['state', onemore.text])
                            if onemore.attrib.items()[0][1] == "Site Type":
                                d.append(['site_type', onemore.text])
                output.append(d)
        return output

    def setup_wof_table(self, api):
        #self.wofsites = api.getSitesObject()
        api.getSites()
        self.wofsites = self.generate_wof_data_from_XML()
        api.network_code = self.wofsites[1][1][1]
        self.table_columns = ["Site Name", "Network", "County", "State", "Site Type", "Site Code"]
        self.table.DefineColumns(self.table_columns)

        output = []
        for site in self.wofsites:
            data = {
                    "site_name": site[0][1],
                    "network": site[1][1],
                    "county": site[3][1],
                    "state": site[4][1],
                    "site_type": site[5][1],
                    "site_code": site[2][1]
                }

            record_object = type('WOFRecord', (object,), data)
            output.extend([record_object])
        self.table.AutoSizeColumns()
        self.table.SetObjects(output)
        self.table.SetColumnWidth(0, 500)
        self.table.SetColumnWidth(1, 150)
        self.table.SetColumnWidth(2, 150)
        self.table.SetColumnWidth(3, 150)
        self.table.SetColumnWidth(4, 165)
        self.table.SetColumnWidth(5, 200)

    def refresh_database(self):
        # get the name of the selected database
        selected_db = self.connection_combobox.GetStringSelection()

        for con in self.get_possible_wof_connections():
            for key, value in con.iteritems():
                if selected_db == value:
                    return con

        self.table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.table.DefineColumns(self.table_columns)

        self.__selected_choice_idx = self.connection_combobox.GetSelection()

        for key, db in self._databases.iteritems():
            # get the database session associated with the selected name
            if db['name'] == selected_db:

                # query the database and get basic series info

                series = None
                # fixme: This breaks for SQLite since it is implemented in dbapi_v2
                if db['args']['engine'] == 'sqlite':
                    session = dbconnection2.createConnection(engine=db['args']['engine'], address=db['args']['address'])
                    # gui_utils.connect_to_db()
                    s = db2.connect(session)
                    series = s.getAllSeries()

                else:  # fixme: this is old api for postgresql and mysql (need to update to dbapi_v2)
                    session_factory = dbUtilities.build_session_from_connection_string(db['connection_string'])
                    session = db2.connect(session_factory)
                    series = session.getAllSeries()

                if series is None:
                    d = {key: value for (key, value) in
                         zip([col.lower().replace(' ','_') for col in self.table_columns],["" for c in self.table_columns])}
                    record_object = type('DataRecord', (object,), d)
                    data = [record_object]
                else:

                    # loop through all of the returned data
                    data = []
                    for s in series:

                        variable = s.VariableObj
                        unit = s.UnitsObj
                        action = s.FeatureActionObj.ActionObj
                        samplingfeature = s.FeatureActionObj.SamplingFeatureObj
                        organization = s.FeatureActionObj.ActionObj.MethodObj.OrganizationObj
                        d = {
                            'resultid': s.ResultID or 'N/A',
                            'variable': getattr(variable, 'VariableCode', 'N/A'),
                            'unit': getattr(unit, 'UnitsName', 'N/A'),
                            'date_created': getattr(action, 'BeginDateTime', 'N/A'),
                            'type': getattr(action, 'ActionTypeCV', 'N/A'),
                            'featurecode': getattr(samplingfeature, 'SamplingFeatureCode', 'N/A'),
                            'organization': getattr(organization, 'OrganizationName', 'N/A')
                        }

                        record_object = type('DataRecord', (object,), d)
                        data.extend([record_object])

                # set the data objects in the olv control
                self.table.SetObjects(data)

                # set the current database in canvas controller
                Publisher.sendMessage('SetCurrentDb',value=selected_db)  # sends to CanvasController.get_current_database_session

                # fire the on_database_changed Event
                kwargs = dict(dbsession=session,
                              dbname=db['name'],
                              dbid=db['id'])
                events.onDbChanged.fire(**kwargs)
                break

        return

    def OLVRefresh(self, event):
        value = self.refresh_database()
        if value is not None:
            try:
                self.api = wateroneflow.WaterOneFlow(value['wsdl'], value['network'])
                self.setup_wof_table(self.api)
            except Exception:
                elog.debug("Wof web service took to long or failed.")
                elog.info("Web service took to long. Wof may be down.")


class DataSeries(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 500),
                          style=wx.TAB_TRAVERSAL)

        self._databases = {}

        connection_choices = []
        self.connection_combobox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), connection_choices,
                                             0)
        self.__selected_choice_idx = 0
        self.connection_combobox.SetSelection(0)

        self.connection_refresh_button = wx.Button(self, label="Refresh")
        self.addConnectionButton = wx.Button(self, label="Add Connection")
        self.table = DatabaseCtrl(self)

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

    def AddConnection(self, event):
        AddConnectionCtrl(self)

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
        super(SimulationDataTab, self).__init__(parent)
        self.parent = parent

        self.table_columns = ["Simulation ID", "Simulation Name", "Model Name", "Simulation Start", "Simulation End", "Date Created","Owner"]
        self.table.DefineColumns(self.table_columns)

        self.__selected_choice_idx = 0

        # build custom context menu
        self.menu = SimulationContextMenu(self.table)
        self.table.setContextMenu(self.menu)
        self.conn = None

    def open_simulation_viewer(self, object):
        results = self.menu.getData(object.simulation_id)
        if results:
            keys = results.keys()[0]

            plot_data = {}
            variable_list_entries = {}

            sub_variables = results[keys]
            for sub in sub_variables:
                variable_list_entries[sub[2].ResultID] = [sub[2].VariableObj.VariableCode,
                                                          sub[2].UnitObj.UnitsAbbreviation,
                                                          sub[2].FeatureActionObj.ActionObj.BeginDateTime,
                                                          sub[2].FeatureActionObj.ActionObj.EndDateTime,
                                                          sub[2].VariableObj.VariableNameCV,
                                                          sub[2].FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName]

                # Get the data belonging to the model
                plot_data[sub[2].ResultID] = [sub[0], sub[1]]

            sim_plot_ctrl = SimulationPlotCtrl(parentClass=self, timeseries_variables=variable_list_entries)
            sim_plot_ctrl.SetTitle("Results for Simulation: " + str(object.model_name))
            sim_plot_ctrl.plot_data = plot_data
        else:
            elog.debug("Received no data. SimulationDataTab.open_simulation_viewer()")


    def load_data(self):

        # get the name of the selected database
        selected_db = self.connection_combobox.GetStringSelection()

        #set the selected choice
        self.__selected_choice_idx = self.connection_combobox.GetSelection()

        for key, db in self._databases.iteritems():

            # get the database session associated with the selected name
            isSqlite = False

            if db['name'] == selected_db:
                simulations = None

                # connect to database
                try:
                    dargs = db['args']
                    if dargs['engine'] == 'sqlite':
                        session = dbconnection2.createConnection(engine=dargs['engine'], address=dargs['address'],
                                                            db=dargs['db'], user=dargs['user'], password=dargs['pwd'])
                        self.conn = db2.connect(session)
                        simulations = self.conn.getAllSimulations()
                        isSqlite = True
                        self.conn.getCurrentSession()
                    else:
                        session_factory = dbUtilities.build_session_from_connection_string(db['connection_string'])
                        session = db2.connect(session_factory)
                        simulations  = session.getAllSimulations()
                except Exception, e:
                    msg = 'Encountered an error when connecting to database %s: %s' % (db['name'], e)
                    elog.error(msg)
                    sPrint(msg, MessageType.ERROR)


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
                Publisher.sendMessage('SetCurrentDb', value=selected_db)  # sends to CanvasController.get_current_database_session
