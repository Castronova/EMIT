from gui.views.TimeSeriesView import TimeSeriesView
import wx
import coordinator.events as engineEvents
import coordinator.engineAccessors as engineAccessors
from odm2api.ODMconnection import dbconnection as dbconnection2
import db.dbapi_v2 as db2
from utilities import db as dbUtilities


class NewSimulationsTabCtrl(TimeSeriesView):
    def __init__(self, parent):
        TimeSeriesView.__init__(self, parent)

        table_columns = ["Simulation ID", "Simulation Name", "Date Created","Owner"]
        self.set_columns(table_columns)
        self.alternate_row_color()

        # Bind Events
        self.connection_combo.Bind(wx.EVT_CHOICE, self.on_connection_combo)
        self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh)
        engineEvents.onDatabaseConnected += self.on_refresh_connection_combo

    def get_selected_database(self):
        for key, value in engineAccessors.getDbConnections().iteritems():
            if self.connection_combo.GetStringSelection() == value["name"]:
                return value
        return None

    def load_SQL_database(self):
        table_columns = ["Simulation ID", "Simulation Name", "Model Name", "Simulation Start", "Simulation End", "Date Created","Owner"]
        self.set_columns(table_columns)
        db = self.get_selected_database()
        if db["args"]["engine"] == "sqlite":
            session = dbconnection2.createConnection(engine=db["args"]["engine"], address=db["args"]["address"],
                                                     db=db["args"]["db"], user=db["args"]["user"],
                                                     password=db["args"]["pwd"])
            conn = db2.connect(session)
            simulations = conn.getAllSimulations()
        elif db["args"]["engine"] == "postgresql":
            session_factory = dbUtilities.build_session_from_connection_string(db["connection_string"])
            session = db2.connect(session_factory)
            simulations = session.getAllSimulations()
        else:
            raise Exception("Failed to load simulations database")

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

    def on_connection_combo(self, event):
        self.empty_list_message.Hide()
        self.clear_table()
        self.load_SQL_database()

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
