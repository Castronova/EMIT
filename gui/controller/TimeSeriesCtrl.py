from gui.views.TimeSeriesView import TimeSeriesView
from webservice import wateroneflow
import wx
import os
import json
import coordinator.engineAccessors as engineAccessors
from gui.controller.WofSitesCtrl import WofSitesCtrl
from odm2api.ODMconnection import dbconnection as dbconnection2
from gui.controller.AddConnectionCtrl import AddConnectionCtrl
import db.dbapi_v2 as db2
from utilities import db as dbUtilities


class TimeSeriesCtrl(TimeSeriesView):
    def __init__(self, parent):
        TimeSeriesView.__init__(self, parent)
        self.api = None

        self.sites_metadata = []

        self.databases = {}

        table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.table.set_columns(table_columns)

        # Pop up menu
        self.popup_menu = wx.Menu()
        view_menu = self.popup_menu.Append(1, "View")

        self.load_connection_combo()

        self.table.alternate_row_color()
        self.connection_combo.Bind(wx.EVT_CHOICE, self.on_connection_combo)
        self.add_connection_button.Bind(wx.EVT_BUTTON, self.on_add_connection)
        self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh_table)
        self.Bind(wx.EVT_MENU, self.on_view_menu, view_menu)
        # Must be bound to table so the pop up menu does not get passed to child view
        self.table.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_right_click)
        self.table.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_double_click)

    def convert_selected_row_into_object(self):

        # get the index of the selected table row
        idx = self.table.GetFirstSelected()

        # grab the data associated with this site and build dictionary
        row_data = self.sites_metadata[idx]
        keys = ['site_name', 'network', 'site_code', 'county', 'state', 'site_type', 'latitude', 'longitude']
        data = dict(zip(keys, row_data))

        # cast dictionary into an object
        record_object = type("WOFRecord", (object,), data)

        return record_object

    def get_selected_database(self):
        """
        Returns an empty string when a wof site or --- is selected
        :return:
        """
        db = {}
        for key, value in engineAccessors.getDbConnections().iteritems():
            if self.connection_combo.GetStringSelection() == value["name"]:
                db = value
                break
        return db

    @staticmethod
    def get_wof_connection_names():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        wof_json = os.path.abspath(os.path.join(current_directory, '../../app_data/dat/wofsites.json'))

        if not os.path.exists(wof_json):
            print("Path %s does not exist" % wof_json)
            return

        with open(wof_json, "r") as f:
            try:
                data = json.load(f)
            except ValueError:
                print "Failed to parse WOF json"
                data = {}
        return data

    def load_connection_combo(self):
        # Add the wof sites to the connection combo option
        self.wof_names = self.get_wof_connection_names()
        for key, value in self.wof_names.iteritems():
            self.append_to_connection_combo(key)

        connections = engineAccessors.getDbConnections()
        for key, value in connections.iteritems():
            self.append_to_connection_combo(connections[key]["name"])

    def load_SQL_database(self):
        table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.table.set_columns(table_columns)
        db = self.get_selected_database()

        if db["args"]["engine"] == "sqlite":
            session_factory = dbconnection2.createConnection(engine=db["args"]["engine"], address=db["args"]["address"])
            session = db2.connect(session_factory)
            series = session.getAllSeries()
        elif db["args"]["engine"] == "postgresql":  # db is postresql
            session_factory = dbUtilities.build_session_from_connection_string(db["connection_string"])
            session = db2.connect(session_factory)
            series = session.getAllSeries()
        else:
            # Fails if db is not sqlite or postresql
            raise Exception("Failed to load database")

        if not series:
            self.table.empty_list_message.Show()
            return

        self.table.empty_list_message.Hide()
        data = self.series_to_table_data(series)

        self.table.set_table_content(data)

    @staticmethod
    def series_to_table_data(series):
        """
        Turns the results from the sql database to a format that can be loaded into the ListCtrl
        :param series:
        :return: rows: 2D list to be loaded into set_table_content()
        """
        rows = []
        for s in series:
            data = []
            variable = s.VariableObj
            unit = s.UnitsObj
            action = s.FeatureActionObj.ActionObj
            samplingfeature = s.FeatureActionObj.SamplingFeatureObj
            organization = s.FeatureActionObj.ActionObj.MethodObj.OrganizationObj

            data.append(str(getattr(s, "ResultID", "N/A")))
            data.append(str(getattr(variable, 'VariableCode', 'N/A')))
            data.append(str(getattr(unit, 'UnitsName', 'N/A')))
            data.append(str(getattr(action, 'BeginDateTime', 'N/A')))
            data.append(str(getattr(action, 'ActionTypeCV', 'N/A')))
            data.append(str(getattr(samplingfeature, 'SamplingFeatureCode', 'N/A')))
            data.append(str(getattr(organization, 'OrganizationName', 'N/A')))
            rows.append(data)

        return rows

    def _load_wof(self, name):
        """
        Loads everything necessary to show Logan River
        :return:
        """
        columns = ['Site Name', 'Network', 'Site Code', 'County', 'State', 'Site Type']
        self.table.set_columns(columns)
        value = self.wof_names[name]
        self.api = wateroneflow.WaterOneFlow(value['wsdl'], value['network'])

        if not self.api.conn:  # Check if connection failed
            self.table.set_empty_message_text("Connection Failed")
            self.table.empty_list_message.Show()
            return

        data = self.api.parse_sites_waterml()

        # save the site data
        self.sites_metadata = data

        data = [d[:-2] for d in data]  # omit the last items  (latitude and longitude)
        self.table.set_table_content(data)

    ###############################
    # EVENTS
    ###############################

    def on_add_connection(self, event):
        AddConnectionCtrl(self)

    def on_connection_combo(self, event):
        self.table.set_empty_message_text("This list is empty")
        self.table.empty_list_message.Hide()
        selection = event.GetEventObject().GetStringSelection()
        if selection == "---":
            self.table.clear_content()
            return

        self.table.clear_table()
        if selection in self.wof_names:
            self._load_wof(selection)
            return

        self.load_SQL_database()

    def on_double_click(self, event):
        """
        Open the WofSiteCtrl
        :param event:
        :return:
        """
        if self.connection_combo.GetStringSelection() in self.wof_names:
            # WofSiteCtrl takes an object so need to convert row into object
            site_object = self.convert_selected_row_into_object()
            WofSitesCtrl(self, site_object, self.api)

    def on_right_click(self, event):
        self.PopupMenu(self.popup_menu)

    def on_refresh_table(self, event):
        """
        Refreshes both the table and the connection combo
        :param event:
        :return:
        """
        self.load_connection_combo()
        selection = self.connection_combo.GetStringSelection()
        if selection != "---" and selection != "":
            if selection in self.wof_names:
                self._load_wof(selection)
                return

            self.load_SQL_database()

    def on_view_menu(self, event):
        self.on_double_click(event)
