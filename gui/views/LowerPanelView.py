import wx
from gui.controller.ConsoleOutputCtrl import consoleCtrl
from gui.controller.TimeSeriesCtrl import TimeSeriesCtrl
from gui.controller.NewSimulationsTabCtrl import NewSimulationsTabCtrl


class ViewLowerPanel:
    def __init__(self, notebook):
        self.notebook = notebook
        self.current_tab = 0

        console = consoleCtrl(notebook)
        self.timeseries = TimeSeriesCtrl(notebook)
        simulations = NewSimulationsTabCtrl(notebook)
        notebook.AddPage(console, "Console")
        notebook.AddPage(self.timeseries, "Time Series")
        notebook.AddPage(simulations, "Simulations")
        self.notebook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_tab_changed)

    def on_tab_changed(self, event):
        if event.GetSelection() == self.current_tab:
            return
        self.current_tab = event.GetSelection()
        event.GetEventObject().SetSelection(self.current_tab)
        if self.current_tab == 1:
            self.timeseries.load_connection_combo()
        return


# class multidict(dict):
#     """
#     Dictionary class that has been extended for Ordering and Duplicate Keys
#     """
#
#     def __init__(self, *args, **kw):
#         self.itemlist = super(multidict, self).keys()
#         self._unique = 0
#
#     def __setitem__(self, key, val):
#         if isinstance(val, dict):
#             self._unique += 1
#             key += '^' + str(self._unique)
#         self.itemlist.append(key)
#         dict.__setitem__(self, key, val)
#
#     def __iter__(self):
#         return iter(self.itemlist)
#
#     def keys(self):
#         return self.itemlist
#
#     def values(self):
#         return [self[key] for key in self]
#
#     def itervalues(self):
#         return (self[key] for key in self)
#
# class DataSeries(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 500),
#                           style=wx.TAB_TRAVERSAL)
#
#         self._databases = {}
#
#         connection_choices = []
#         self.connection_combobox = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, -1), connection_choices,
#                                              0)
#         self.__selected_choice_idx = 0
#         self.connection_combobox.SetSelection(0)
#
#         self.connection_refresh_button = wx.Button(self, label="Refresh")
#         self.addConnectionButton = wx.Button(self, label="Add Connection")
#         self.table = DatabaseCtrl(self)
#
#         # Sizers
#         seriesSelectorSizer = wx.BoxSizer(wx.VERTICAL)
#         buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
#         buttonSizer.SetMinSize(wx.Size(-1, 45))
#
#         buttonSizer.Add(self.connection_combobox, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=2)
#         buttonSizer.Add(self.addConnectionButton, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=10)
#         buttonSizer.AddSpacer((0, 0), 1, wx.EXPAND, 5)
#         buttonSizer.Add(self.connection_refresh_button, 0, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=2)
#         seriesSelectorSizer.Add( buttonSizer, 0, wx.ALL|wx.EXPAND, 0)
#         seriesSelectorSizer.Add(self.table, 1, wx.ALL|wx.EXPAND, 0)
#
#         self.SetSizer(seriesSelectorSizer)
#
#         engineEvent.onDatabaseConnected += self.refreshConnectionsListBox
#
#         # initialize key bindings
#         self.initBindings()
#
#     def initBindings(self):
#         # Bindings
#         self.addConnectionButton.Bind(wx.EVT_LEFT_DOWN, self.AddConnection)
#         self.connection_refresh_button.Bind(wx.EVT_LEFT_DOWN, self.database_refresh)
#         self.connection_combobox.Bind(wx.EVT_CHOICE, self.DbChanged)
#
#     def DbChanged(self, event):
#         self.database_refresh(event)
#
#     def refreshConnectionsListBox(self, connection_added):
#
#         if connection_added:
#             self._databases = engine.getDbConnections()
#
#             choices = ['---']
#             for k, v in self._databases.iteritems():
#                 choices.append(self._databases[k]['name'])
#             self.connection_combobox.SetItems(choices)
#
#             # set the selected choice
#             self.connection_combobox.SetSelection( self.__selected_choice_idx)
#
#     def AddConnection(self, event):
#         AddConnectionCtrl(self)
#
#     def load_data(self):
#         elog.error('Abstract method. Must be overridden!')
#         raise Exception('Abstract method. Must be overridden!')
#
#     def database_refresh(self, event):
#         if sys.gettrace():
#             #  In debug mode
#             self.load_data()
#         else:
#             # Not in debug mode
#             thr = threading.Thread(target=self.load_data, args=(), kwargs={}, name='DataSeriesRefresh')
#             thr.start()
#
#
# class SimulationDataTab(DataSeries):
#     def __init__(self, parent):
#         super(SimulationDataTab, self).__init__(parent)
#         self.parent = parent
#
#         self.table_columns = ["Simulation ID", "Simulation Name", "Date Created","Owner"]
#         self.table.DefineColumns(self.table_columns)
#         # self.table.AutoSizeColumns()
#
#         self.__selected_choice_idx = 0
#
#         # build custom context menu
#         self.menu = SimulationContextMenu(self.table)
#         self.table.setContextMenu(self.menu)
#         self.conn = None
#
#     def open_simulation_viewer(self, object):
#         results = self.menu.getData(object.simulation_id)
#         if results:
#
#             sim_plot_ctrl = SimulationPlotCtrl(parentClass=self)
#             sim_plot_ctrl.SetTitle("Results for Simulation: " + str(object.simulation_name))
#
#             # keys = results.keys()[0]
#
#             plot_data = {}
#             variable_list_entries = {}
#
#             for variable, value in results.iteritems():
#                 sub_variables = value
#                 for sub in sub_variables:
#                     variable_list_entries[sub[2].ResultID] = [sub[2].VariableObj.VariableCode,
#                                                           sub[2].UnitsObj.UnitsAbbreviation,
#                                                           sub[2].FeatureActionObj.ActionObj.BeginDateTime,
#                                                           sub[2].FeatureActionObj.ActionObj.EndDateTime,
#                                                           sub[2].VariableObj.VariableNameCV,
#                                                           sub[2].FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName]
#
#                 # Get the data belonging to the model
#                 plot_data[sub[2].ResultID] = [sub[0], sub[1]]
#
#             sim_plot_ctrl.set_timeseries_variables(variable_list_entries)
#             sim_plot_ctrl.plot_data = plot_data
#         else:
#             elog.debug("Received no data. SimulationDataTab.open_simulation_viewer()")
#
#
#     def load_data(self):
#
#         # get the name of the selected database
#         selected_db = self.connection_combobox.GetStringSelection()
#
#         #set the selected choice
#         self.__selected_choice_idx = self.connection_combobox.GetSelection()
#
#         for key, db in self._databases.iteritems():
#
#             # get the database session associated with the selected name
#             isSqlite = False
#
#             if db['name'] == selected_db:
#                 simulations = None
#
#                 # connect to database
#                 try:
#                     dargs = db['args']
#                     if dargs['engine'] == 'sqlite':
#                         session = dbconnection2.createConnection(engine=dargs['engine'], address=dargs['address'],
#                                                             db=dargs['db'], user=dargs['user'], password=dargs['pwd'])
#                         self.conn = db2.connect(session)
#                         simulations = self.conn.getAllSimulations()
#                         isSqlite = True
#                         self.conn.getCurrentSession()
#                     else:
#                         session_factory = dbUtilities.build_session_from_connection_string(db['connection_string'])
#                         session = db2.connect(session_factory)
#                         simulations  = session.getAllSimulations()
#                 except Exception, e:
#                     msg = 'Encountered an error when connecting to database %s: %s' % (db['name'], e)
#                     elog.error(msg)
#                     sPrint(msg, MessageType.ERROR)
#
#
#                 sim_ids = []
#                 if simulations is None:
#                     d = {key: value for (key, value) in
#                          zip([col.lower().replace(' ','_') for col in self.table_columns],["" for c in self.table_columns])}
#                     record_object = type('DataRecord', (object,), d)
#                     data = [record_object]
#                 else:
#                     data = []
#
#                     # loop through all of the returned data
#
#                     for s in simulations:
#                         simulation = None
#                         if isSqlite:
#                             simulation = s.Simulations
#                             person = s.People
#                             action = s.Actions
#                         else:
#                             simulation = s.Simulation
#                             person = s.Person
#                             action = s.Action
#
#                         simulation_id = simulation.SimulationID
#
#                         # only add if the simulation id doesn't already exist in sim_ids
#                         if simulation_id not in sim_ids:
#                             sim_ids.append(simulation_id)
#
#                             d = {
#                                 'simulation_id': simulation.SimulationID,
#                                 'simulation_name': simulation.SimulationName,
#                                 'date_created': action.BeginDateTime,
#                                 'owner': person.PersonLastName,
#                             }
#
#                             record_object = type('DataRecord', (object,), d)
#                             data.extend([record_object])
#
#                 # set the data objects in the olv control
#                 self.table.SetObjects(data)
#
#                 # set the current database in canvas controller
#                 Publisher.sendMessage('SetCurrentDb', value=selected_db)  # sends to CanvasController.get_current_database_session
