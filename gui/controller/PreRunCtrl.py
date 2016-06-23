import os
import time
import wx
from coordinator import engineAccessors, users
from emitLogging import elog
from gui.controller.UserCtrl import UserCtrl
from gui.views.PreRunView import PreRunView


class PreRunCtrl(PreRunView):
    def __init__(self, parent=None):
        PreRunView.__init__(self, parent=parent)

        # Defining the table columns
        table_columns = ["Name", "Component"]
        for i in range(len(table_columns)):
            self.variableList.InsertColumn(i, str(table_columns[i]))

        self._data = None
        self.user_data = None

        # populate outputs table
        self.populate_variable_list()

        # initialize bindings for Run, Add, and Cancel
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run)
        self.add_account_button.Bind(wx.EVT_BUTTON, self.on_add_new)

        # populate the database_combo control with known databases
        self.set_database_combo_default()

        # populate the account drop list with known users
        self.refresh_user_account()

    def get_account_id(self, person, organization):
        return '%s [%s]' % (person.last_name, organization.name)

    def get_databases(self):
        '''
        Queries the engine for the known databases
        :return: a list of databases that are loaded into the engine
        '''

        # query the engine to get all available database connections
        available_connections = engineAccessors.getDbConnections()
        return available_connections

    def get_selected_items(self):
        '''
        builds a dictionary containing lists of all output variables that have been selected for saving,
         by component name
        :return: dictionary of datasets to save
        '''
        datasets = {}
        num = self.variableList.GetItemCount()
        for i in range(num):
            # get the component name and add it to the datasets dictionary
            component_name = self.variableList.GetItemText(i, 1)
            if component_name not in datasets:
                datasets[component_name] = []

            # add variable if selected
            if self.variableList.IsChecked(i):
                variable_name = self.variableList.GetItemText(i, 0)
                datasets[component_name].append(variable_name)

        return datasets

    def get_user_info(self):
        account = self.account_combo.GetValue()

        # get the user account from selected user_name
        for affiliation_id in self.user_data.iterkeys():
            if affiliation_id == account:
                return self.user_data[affiliation_id]

    def insert_data(self, data):
        if isinstance(data, dict):
            col_number = 0
            for key, values in data.iteritems():
                for value in values:
                    pos = self.variableList.InsertStringItem(col_number, str(value))
                    col_number += 1
                    self.variableList.SetStringItem(pos, col_number, str(key))
                    col_number = 0
        else:
            elog.debug("PreRunCtrl.insert_data must be a dictionary")
        return

    def populate_variable_list(self):
        if len(engineAccessors.getAllLinks()) < 1:
            elog.info("No links have been added")
            return
        else:
            models = {}
            # compile a list of model ids and names that exist in the configuration
            links = engineAccessors.getAllLinks()
            for link in links:
                s_id = link['source_component_id']
                t_id = link['target_component_id']
                if s_id not in models.keys():
                    models[s_id] = link['source_component_name']
                if t_id not in models.keys():
                    models[t_id] = link['target_component_name']

            # sort models
            self._data = self.sort_output_model(models)
            self.insert_data(self._data)
            self.autoSizeColumns()
            self.alternateRowColor()

    def refresh_user_account(self):
        self.account_combo.Clear()

        # Get users
        path = os.environ['APP_USER_PATH']
        self.user_data = users.json_to_dict(path)
        account_names = []
        for affiliation in self.user_data.itervalues():
            account_names.append(affiliation.ID())

        self.account_combo.AppendItems(account_names)
        self.account_combo.SetSelection(0)

    def set_database_combo_default(self):
        dbs = self.get_databases()
        db_names = [db['name'] for db in dbs.itervalues()]
        self.database_combo.AppendItems(db_names)
        for i in range(0, self.database_combo.GetCount()):
            if "local" in self.database_combo.GetString(i):
                self.database_combo.SetSelection(i)
                return

        # If local is not found set it to the first value
        self.database_combo.SetSelection(0)

    def sort_output_model(self, models):
        output_name_list = {}
        for model_id, model_name in sorted(models.items(), key=lambda x: x[1]):
            oei = engineAccessors.getExchangeItems(model_id, type='OUTPUT')
            output_name_list[model_name] = [ei['name'] for ei in oei]
        return output_name_list

    #################################
    # EVENTS
    #################################

    def on_add_new(self, e):
        controller = UserCtrl(self)
        controller.CenterOnScreen()
        controller.Show()
        controller.Bind(wx.EVT_CLOSE, self.on_user_ctrl_closed)

    def on_cancel(self, e):
        self.Close(True)

    def on_run(self, e):
        # get data to send to the engine
        name = self.simulation_name_textbox.GetValue()
        db = self.database_combo.GetValue()
        # user_name = self.account_combo.GetValue()
        datasets = self.get_selected_items()

        user_info = self.get_user_info()

        # todo: check all constraints before executing a simulation
        # raise exceptions before executing the simulation
        if user_info is None:
            elog.critical('Cannot execute simulation if no user account is provided')
            return

        # set a default simulation name if none is provided
        if name.strip() == '':
            name = "Simulation_run_" + time.strftime('%m-%d-%Y')

        # build kwargs to pass to engineAccessors
        kwargs = dict(simulationName=name, dbName=db, user_info=user_info, datasets=datasets)

        # initiate simulation
        engineAccessors.runSimulation(**kwargs)

        self.Close()

    def on_user_ctrl_closed(self, event):
        """
        Detects when the user ctrl has been closed
        Allows this class to refresh the user account and not the UserCtrl class
        :param event:
        :return:
        """
        event.GetEventObject().Destroy()
        self.refresh_user_account()