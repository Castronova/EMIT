import time
import wx
from coordinator import engineAccessors, users
from coordinator.emitLogging import elog
from gui.views.PreRunView import PreRunView

from gui.controller.UserCtrl import UserCtrl
from utilities.gui import loadAccounts

import environment

class PreRunViewCtrl(PreRunView):
    def __init__(self, parent=None):
        PreRunView.__init__(self, parent=parent)

        # Defining the table columns
        table_columns = ["Name", "Component"]
        for i in range(len(table_columns)):
            self.variableList.InsertColumn(i, str(table_columns[i]))

        self._data = None

        # populate outputs table
        self.populateVariableList()

        # get all known user accounts
        path = environment.getDefaultUsersJsonPath()
        self.user_data = users.jsonToDict(path)

        # self.accounts = UserCtrl.users_json_file_to_object()

        # initialize bindings for Run, Add, and Cancel
        self.cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.run_button.Bind(wx.EVT_BUTTON, self.OnRun)
        self.add_account_button.Bind(wx.EVT_BUTTON, self.OnAddNew)

        # populate the database_combo control with known databases
        self.setDatabaseComboDefault()

        # populate the account droplist with known users
        self.refreshUserAccount()

    def setDatabaseComboDefault(self):
        dbs = self.getDatabases()
        db_names = [db['name'] for db in dbs.itervalues()]
        self.database_combo.AppendItems(db_names)
        for i in range(0, self.database_combo.GetCount()):
            if "local" in self.database_combo.GetString(i):
                self.database_combo.SetSelection(i)
                return

        # If local is not found set it to the first value
        self.database_combo.SetSelection(0)

    def getAccountID(self, person, organization):
        return '%s [%s]' % (person.last_name, organization.name)

    def refreshUserAccount(self):
        self.account_combo.Clear()
        # self.accounts = UserCtrl.users_json_file_to_object()
        account_names = []
        for affiliation in self.user_data.itervalues():
            account_names.append(affiliation.ID())
            # person = affiliation.person
            # organization = affiliation.organization

        # for person, organizations in self.accounts.iteritems():
        #     for organ in organizations:
        #         user = self.getAccountID(person, organ)
                # user = person.last_name + " [" + organ.name + "]"
                # account_names.append(user)

        self.account_combo.AppendItems(account_names)
        self.account_combo.SetSelection(0)

    def populateVariableList(self):
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

    def insert_data(self, data):
        if isinstance(data, dict):
            col_number = 0
            row_number = 0
            for key, values in data.iteritems():
                for value in values:
                    pos = self.variableList.InsertStringItem(col_number, str(value))
                    col_number += 1
                    self.variableList.SetStringItem(pos, col_number, str(key))
                    row_number += 1
                    col_number = 0
        else:
            elog.debug("PreRunViewCtrl.insert_data must be a dictionary")
        return

    def sort_output_model(self, models):
        output_name_list = {}
        for model_id, model_name in sorted(models.items(), key=lambda x: x[1]):
            oei = engineAccessors.getExchangeItems(model_id, exchange_item_type='OUTPUT', returnGeoms=False)
            output_name_list[model_name] = [ei['name'] for ei in oei]
        return output_name_list

    def OnCancel(self, e):
        self.Close(True)

    def get_user_info(self):
        account = self.account_combo.GetValue()

        # get the user account from selected user_name
        for affiliation_id in self.user_data.iterkeys():
           if  affiliation_id == account:
               return self.user_data[affiliation_id]


    def OnRun(self, e):

        # get data to send to the engine
        name = self.simulation_name_textbox.GetValue()
        db = self.database_combo.GetValue()
        # user_name = self.account_combo.GetValue()
        datasets = self.getSelectedItems()

        user_info = self.get_user_info()

        # for affil in self.accounts:
        #     userID = self.getAccountID()
        #     if affil.ID() == user_name:
        #         user_info_json = affil.toJSON()

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

    def getSelectedItems(self):
        '''
        builds a dictionary containing lists of all output variables that have been selected for saving,
         by component name
        :return: dictionary of datasets to save
        '''
        datasets = {}
        num = self.variableList.GetItemCount()
        for i in range(num):
            # get the component name and add it to the datasets dictionary
            component_name = self.variableList.GetItemText(i,1)
            if component_name not in datasets:
                datasets[component_name] = []

            # add variable if selected
            if self.variableList.IsChecked(i):
                variable_name = self.variableList.GetItemText(i, 0)
                datasets[component_name].append(variable_name)

        return datasets

    def getDatabases(self):
        '''
        Queries the engine for the known databases
        :return: a list of databases that are loaded into the engine
        '''

        # query the engine to get all available database connections
        available_connections = engineAccessors.getDbConnections()
        return available_connections

    def OnAddNew(self, e):
        controller = UserCtrl(self)
        controller.CenterOnScreen()
        controller.Show()
