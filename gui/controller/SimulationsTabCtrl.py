from gui.views.TimeSeriesView import TimeSeriesView
import wx
import coordinator.events as engineEvents
import coordinator.engineAccessors as engineAccessors
import db.dbapi_v2 as db2
from utilities import db as dbUtilities
from gui.controller.SimulationPlotCtrl import SimulationsPlotCtrl
from odm2api.ODMconnection import dbconnection
from gui.controller.AddConnectionCtrl import AddConnectionCtrl


class SimulationsTabCtrl(TimeSeriesView):
    def __init__(self, parent):
        TimeSeriesView.__init__(self, parent)

        table_columns = ["Simulation ID", "Simulation Name", "Date Created","Owner"]
        self.table.set_columns(table_columns)
        self.table.alternate_row_color()

        # Pop up menu
        self.popup_menu = wx.Menu()
        view_menu = self.popup_menu.Append(1, "View")

        # Bind Events
        self.Bind(wx.EVT_MENU, self.on_view_menu, view_menu)
        self.table.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_right_click)
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
            self.table.empty_list_message.Show()  # No results were returned
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
        self.table.set_columns(table_columns)

        session = self.get_database_session()
        simulations = session.getAllSimulations()

        if not simulations:
            self.table.empty_list_message.Show()
            return

        self.table.empty_list_message.Hide()
        data = self.simulations_to_table_data(simulations)
        self.table.set_table_content(data)

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
        self.table.empty_list_message.Hide()
        selection = self.connection_combo.GetStringSelection()
        if selection == "---":
            self.table.clear_content()
            return

        self.table.clear_table()
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
        row_data = self.table.get_selected_row()
        if not row_data:
            return  # No rows in the table

        results = self.get_row_data(row_data[0])

        if not results:
            self.table.empty_list_message.Hide()
            return

        table_data = []
        table_columns = ["ID", "Variable", "Units", "Begin Date", "End Date", "Description", "Organization"]

        controller = SimulationsPlotCtrl(self, columns=table_columns)
        controller.SetTitle("Results for Simulation: " + row_data[1])

        for key, value in results.iteritems():
            row = []
            wkt = []
            wkt_data = []
            row.append(value[0][2].ResultID)
            row.append(value[0][2].VariableObj.VariableCode)
            row.append(value[0][2].UnitsObj.UnitsAbbreviation)
            row.append(value[0][2].FeatureActionObj.ActionObj.BeginDateTime)
            row.append(value[0][2].FeatureActionObj.ActionObj.EndDateTime)
            row.append(value[0][2].VariableObj.VariableNameCV)
            row.append(value[0][2].FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName)
            for item in value:
                wkt.append(item[2].FeatureActionObj.SamplingFeatureObj.FeatureGeometryWKT)
                wkt_data.append([item[0], item[1]])

            if len(row) != len(table_columns):  # If these do not match, the app will crash
                raise Exception("Number of columns must match the number of items in the row")

            table_data.append(row)
            controller.data[row[0]] = wkt_data
            controller.geometries[row[0]] = wkt

        controller.table.set_table_content(table_data)
