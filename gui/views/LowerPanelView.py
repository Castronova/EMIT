import ConfigParser
import os
import sys
import threading

import wx
from odm2api.ODMconnection import dbconnection
from wx.lib.pubsub import pub as Publisher

import coordinator.engineAccessors as engine
import coordinator.events as engineEvent
import db.dbapi_v2 as db2
from ContextView import TimeSeriesContextMenu, SimulationContextMenu #, ConsoleContextMenu
from coordinator.emitLogging import elog
from db import dbapi as dbapi
from gui import events
from gui.controller.AddConnectionCtrl import AddConnectionCtrl
from gui.controller.ConsoleOutputCtrl import consoleCtrl
from gui.controller.DatabaseCtrl import DatabaseCtrl
from gui.controller.SimulationPlotCtrl import SimulationPlotCtrl
from gui.controller.TimeSeriesObjectCtrl import TimeSeriesObjectCtrl
from gui.controller.WofSitesCtrl import WofSitesCtrl
from utilities import db as dbUtilities
from webservice import wateroneflow
import uuid
import ConfigParser
from api_old.ODMconnection import  dbconnection, SessionFactory
import xml.etree.ElementTree



class viewLowerPanel:
    def __init__(self, notebook):

        console = consoleCtrl(notebook)
        timeseries = TimeSeriesTab(notebook)
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
        self._connection_added = True

        connection_choices = []
        self.connection_combobox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), connection_choices,
                                             0)
        self.__selected_choice_idx = 0
        self.connection_combobox.SetSelection(self.__selected_choice_idx)

        self.connection_refresh_button = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        self.addConnectionButton = wx.Button(self, wx.ID_ANY, u"Add Connection", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_olvSeries = DatabaseCtrl(self, pos=wx.DefaultPosition, size=wx.DefaultSize, id=wx.ID_ANY,
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
        self.menu = TimeSeriesContextMenu(self.m_olvSeries)
        self.m_olvSeries.setContextMenu(self.menu)

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

            wofconnections = self.get_possible_wof_connections()
            for con in wofconnections:
                for key, value in con.iteritems():
                    if key == 'name':
                        choices.append(value)

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

    def getParsedValues(self, siteObject, startDate, endDate):
        values = self.api.parseValues(siteObject.site_code, self.selectedVariables, startDate, endDate)
        return values

    def get_possible_wof_connections(self):

        currentdir = os.path.dirname(os.path.abspath(__file__))
        wof_txt = os.path.abspath(os.path.join(currentdir, '../../data/wofsites'))
        params = {}
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


        #wsdl["Red Butte Creek"] = "http://data.iutahepscor.org/RedButteCreekWOF/cuahsi_1_1.asmx?WSDL"
        #wsdl["Provo River"] = "http://data.iutahepscor.org/ProvoRiverWOF/cuahsi_1_1.asmx?WSDL"
        #wsdl["Logan River"] = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"
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
        print root
        print "testing"

    def setup_wof_table(self, api):
        self.wofsites = api.getSitesObject()
        #api.getSites()
        #self.generate_wof_data_from_XML()
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

        for con in self.get_possible_wof_connections():
            for key, value in con.iteritems():
                if selected_db == value:
                    return con

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
        self._connection_added = True

        connection_choices = []
        self.connection_combobox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), connection_choices,
                                             0)
        self.__selected_choice_idx = 0
        self.connection_combobox.SetSelection(0)

        self.connection_refresh_button = wx.Button(self, wx.ID_ANY, u"Refresh", wx.DefaultPosition, wx.DefaultSize, 0)
        self.addConnectionButton = wx.Button(self, wx.ID_ANY, u"Add Connection", wx.DefaultPosition, wx.DefaultSize, 0)

        self.table = DatabaseCtrl(self, pos=wx.DefaultPosition, size=wx.DefaultSize, id=wx.ID_ANY,
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
        #  wx.Panel.__init__(self, parent)

        super(SimulationDataTab, self).__init__(parent)
        self.parent = parent

        self.table_columns = ["Simulation ID", "Simulation Name", "Model Name", "Simulation Start", "Simulation End", "Date Created","Owner"]
        #  table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
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
