from gui.views.TimeSeriesView import TimeSeriesView
import wx
import coordinator.events as engineEvents
import coordinator.engineAccessors as engineAccessors
import db.dbapi_v2 as db2
from utilities import db as dbUtilities
from gui.controller.SimulationPlotCtrl import SimulationPlotCtrl
from odm2api.ODMconnection import dbconnection
from gui.controller.AddConnectionCtrl import AddConnectionCtrl


class SimulationsTabCtrl(TimeSeriesView):
    def __init__(self, parent):
        TimeSeriesView.__init__(self, parent)

        table_columns = ["Simulation ID", "Simulation Name", "Date Created","Owner"]
        self.set_columns(table_columns)
        self.alternate_row_color()

        # Bind Events
        self.Bind(wx.EVT_MENU, self.on_view_menu, self.view_menu)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_right_click)
        self.connection_combo.Bind(wx.EVT_CHOICE, self.on_connection_combo)
        self.add_connection_button.Bind(wx.EVT_BUTTON, self.on_add_connection)
        self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        self.table.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_double_click)
        engineEvents.onDatabaseConnected += self.on_refresh_connection_combo

    def get_database_session(self):
        """
        Connect to the respective database and return the session
        Exception is raised if it is not a sqlite or postresql
        :return:
        """
        db = self.get_selected_database()
        if db["args"]['engine'] == "sqlite":
            session_factory = dbconnection.createConnection(engine=db["args"]["engine"], address=db["args"]["address"],
                                                     db=db["args"]["db"], user=db["args"]["user"],
                                                     password=db["args"]["pwd"])
            session = db2.connect(session_factory)
            return session
        elif db["args"]["engine"] == "postgresql":
            session_factory = dbUtilities.build_session_from_connection_string(db['connection_string'])
            session = db2.connect(session_factory)
            return session
        else:
            raise Exception("Failed to load simulations database")

    def get_row_data(self, simulation_id):
        session = self.get_database_session()

        results = session.read.getResults(simulationid=simulation_id)

        if len(results) == 0:
            self.empty_list_message.Show()  # No results were returned
            return None

        res = {}
        for r in results:
            variable_name = r.VariableObj.VariableCode
            result_values = session.read.getResultValues(resultid=r.ResultID)

            dates = list(result_values.ValueDateTime)
            values = list(result_values.DataValue)

            if variable_name in res:
                res[variable_name].append([dates, values, r])
            else:
                res[variable_name] = [[dates, values, r]]

        return res

    def get_selected_database(self):
        for key, value in engineAccessors.getDbConnections().iteritems():
            if self.connection_combo.GetStringSelection() == value["name"]:
                return value
        return None

    def load_SQL_database(self):
        table_columns = ["Simulation ID", "Simulation Name", "Date Created","Owner"]
        self.set_columns(table_columns)

        session = self.get_database_session()
        simulations = session.getAllSimulations()

        if not simulations:
            self.empty_list_message.Show()
            return

        self.empty_list_message.Hide()
        data = self.simulations_to_table_data(simulations)
        self.set_table_content(data)

    @staticmethod
    def simulations_to_table_data(series):
        """
        Turns the results from the sql database to a format that can be loaded into the ListCtrl
        :param series:
        :return: 2D list to be passed into set_table_content()
        """
        rows = []
        for s in series:
            data = []
            simulation = s.Simulations
            person = s.People
            action = s.Actions

            data.append(str(getattr(simulation, "SimulationID", "N/A")))
            data.append(str(getattr(simulation, "SimulationName", "N/A")))
            data.append(str(getattr(action, "BeginDateTime", "N/A")))
            data.append(str(getattr(person, "PersonLastName", "N/A")))

            rows.append(data)
        return rows

    ###############################
    # EVENTS
    ###############################

    def on_add_connection(self, event):
        AddConnectionCtrl(self)

    def on_connection_combo(self, event):
        self.empty_list_message.Hide()
        self.clear_table()
        self.load_SQL_database()

    def on_double_click(self, event):
        self.on_view_menu(event)

    def on_refresh(self, event):
        """
        Refresh both the connection combo box and the table
        :param event:
        :return:
        """
        self.on_refresh_connection_combo(event)
        self.on_connection_combo(event)

    def on_refresh_connection_combo(self, event):
        """
        Refreshes/updates the connection combo box. This method is fired when the engine has loaded the database
        :param event:
        :return:
        """
        connections = engineAccessors.getDbConnections()
        for key, value in connections.iteritems():
            self.append_to_connection_combo(value["name"])

    def on_right_click(self, event):
        self.PopupMenu(self.popup_menu)

    def on_view_menu(self, event):
        row_data = self.get_selected_row()
        results = self.get_row_data(row_data[0])

        if not results:
            print "Results is None"
            return

        controller = SimulationPlotCtrl(parentClass=self)
        controller.SetTitle("Results for Simulation: " + row_data[1])

        plot_data = {}
        variable_list_entries = {}

        for variable, value in results.iteritems():
            sub_variables = value
            for sub in sub_variables:
                variable_list_entries[sub[2].ResultID] = [sub[2].VariableObj.VariableCode,
                                                      sub[2].UnitsObj.UnitsAbbreviation,
                                                      sub[2].FeatureActionObj.ActionObj.BeginDateTime,
                                                      sub[2].FeatureActionObj.ActionObj.EndDateTime,
                                                      sub[2].VariableObj.VariableNameCV,
                                                      sub[2].FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName]

            # Get the data belonging to the model
            plot_data[sub[2].ResultID] = [sub[0], sub[1]]

        # controller.set_timeseries_variables(variable_list_entries)
        controller.populate_variable_list(variable_list_entries)
        controller.plot_data = plot_data
