from gui.views.NewTimeSeriesView import NewTimeSeriesView
from webservice import wateroneflow
import sys
import wx
import os
import json
from gui.controller.WofSitesCtrl import WofSitesCtrl


class NewTimeSeriesCtrl(NewTimeSeriesView):
    def __init__(self, parent):
        NewTimeSeriesView.__init__(self, parent)
        self.api = None

        table_columns = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        self.set_columns(table_columns)

        # Add the wof sites to the connection combo option
        self.wof_names = self.get_wof_connection_names()
        for key, value in self.wof_names.iteritems():
            self.append_to_connection_combo(key)

        self.alternate_row_color()
        self.connection_combo.Bind(wx.EVT_CHOICE, self.on_connection_combo)
        self.refresh_button.Bind(wx.EVT_BUTTON, self.on_refresh_table)

        self.Bind(wx.EVT_MENU, self.on_view_menu, self.view_menu)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_right_click)

        self.table.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_double_click)

    def alternate_row_color(self, color="#DCEBEE"):
        for i in range(self.table.GetItemCount()):
            if i % 2 == 0:
                self.table.SetItemBackgroundColour(i, color)

    def append_to_connection_combo(self, item):
        self.connection_options.append(item)
        self.connection_combo.SetItems(self.connection_options)

    def auto_size_table(self):
        for i in range(self.table.GetColumnCount()):
            self.table.SetColumnWidth(col=i, width=wx.LIST_AUTOSIZE)
        self.expand_table_to_fill_panel()

    def clear_table(self):
        """
        Clears everything in the table including the header names
        :return:
        """
        self.table.ClearAll()

    def clear_content(self):
        """
        Clears everything in the table except the header names
        :return:
        """
        self.table.DeleteAllItems()

    def convert_selected_row_into_object(self):
        item = self.get_selected_row()
        data = {
            "site_name": item[0],
            "network": item[1],
            "county": item[3],
            "state": item[4],
            "site_type": item[5],
            "site_code": item[2]
        }
        record_object = type("WOFRecord", (object,), data)
        return record_object

    def expand_table_to_fill_panel(self):
        """
        Sets the width of the table to fill up any white space
        :return:
        """
        last_column_index = self.table.GetColumnCount() - 1
        size = self.GetTopLevelParent().GetSize()[1]
        self.table.SetColumnWidth(last_column_index, size)

    def get_selected_row(self):
        row_number = self.table.GetFirstSelected()
        data = []
        for i in range(self.table.GetColumnCount()):
            data.append(self.table.GetItem(row_number, i).GetText())
        return data

    @staticmethod
    def get_wof_connection_names():
        currentdir = os.path.dirname(os.path.abspath(__file__))
        wof_json = os.path.abspath(os.path.join(currentdir, '../../data/wofsites.json'))
        with open(wof_json, "r") as f:
            try:
                data = json.load(f)
            except ValueError:
                print "Failed to parse WOF json"
                data = {}
        return data

    def set_columns(self, columns):
        """
        Sets the name of the columns
        :param columns: a list of strings
        :return:
        """
        self.clear_table()
        for i in range(len(columns)):
            self.table.InsertColumn(i, columns[i])

    def set_table_content(self, data):
        """
        :param data: 2D list
        :return:
        """
        for i in range(len(data)):
            index = self.table.InsertStringItem(sys.maxint, data[i][0])
            for j in range(len(data[i])):
                self.table.SetStringItem(index, j, data[i][j])

        self.auto_size_table()
        self.alternate_row_color()

    def _load_wof(self, name):
        """
        Loads everything necessary to show Logan River
        :return:
        """
        columns = ["Site Name", "Network", "County", "State", "Site Type", "Site Code"]
        self.set_columns(columns)
        value = self.wof_names[name]
        self.api = wateroneflow.WaterOneFlow(value['wsdl'], value['network'])
        data = self.api.get_sites_in_list()
        self.set_table_content(data)

    ###############################
    # EVENTS
    ###############################

    def on_connection_combo(self, event):
        selection = event.GetEventObject().GetStringSelection()
        if selection in self.wof_names:
            self._load_wof(selection)

    def on_double_click(self, event):
        """
        Open the WofSiteCtrl
        :param event:
        :return:
        """
        if self.api:
            # WofSiteCtrl takes an object so need to convert row into object
            site_object = self.convert_selected_row_into_object()
            WofSitesCtrl(self, site_object, self.api)

    def on_right_click(self, event):
        self.PopupMenu(self.popup_menu)

    def on_refresh_table(self, event):
        if self.connection_combo.GetStringSelection() != "---":
            self._load_wof(self.connection_combo.GetStringSelection())

    def on_view_menu(self, event):
        self.on_double_click(event)

