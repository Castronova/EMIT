__author__ = 'Francisco'

import wx
from gui.views.PreRunView import viewPreRun
import os
import time
from coordinator import engineAccessors
from environment import env_vars
from coordinator.emitLogging import elog
import coordinator.users as Users

class PreRunCtrl(viewPreRun):
    def __init__(self, parent=None):
        viewPreRun.__init__(self, parent=parent)

        # Defining the table columns
        table_columns = ["Name", "Component"]
        for i in range(len(table_columns)):
            self.variableList.InsertColumn(i, str(table_columns[i]))

        self._data = None

        # populate outputs table
        self.populateVariableList()

        # initialize bindings for Run, Add, and Cancel
        self.cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.run_button.Bind(wx.EVT_BUTTON, self.OnRun)
        self.add_account_button.Bind(wx.EVT_BUTTON, self.OnAddNew)

        # initialize the dialog for adding new users
        self.dlg = self.onAddUser()

        # populate the database_combo control with known databases
        dbs = self.getDatabases()
        db_names = [db['name'] for db in dbs.itervalues()]
        self.database_combo.AppendItems(db_names)
        self.database_combo.SetSelection(0)

        # populate the account droplist with known users
        self.accounts = self.loadAccounts()
        account_names = [' '.join([affil.person.lastname, '['+affil.organization.code+']']) for affil in self.accounts]
        self.account_combo.AppendItems(account_names)
        self.account_combo.SetSelection(0)

    def loadAccounts(self):
        known_users = []
        userjson = env_vars.USER_JSON
        elog.debug('userjson ' + userjson)
        with open(userjson, 'r') as f:
            known_users.extend(Users.BuildAffiliationfromJSON(f.read()))
        return known_users

    def populateVariableList(self):
        if len(engineAccessors.getAllLinks()) < 1:
            elog.info("No links have been added")
        else:
            output_name_list = {}
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
            for model_id, model_name in sorted(models.items(), key=lambda x: x[1]):
                oei = engineAccessors.getOutputExchangeItems(model_id, returnGeoms=False)
                output_name_list[model_name] = [ei['name'] for ei in oei]

            data = output_name_list
            self._data = output_name_list
            col_number = 0
            row_number = 0

            for key, values in data.iteritems():
                for value in values:
                    pos = self.variableList.InsertStringItem(col_number, str(value))
                    col_number += 1
                    self.variableList.SetStringItem(pos, col_number, str(key))
                    row_number += 1
                    col_number = 0

            self.autoSizeColumns()
            self.alternateRowColor()

    def OnCancel(self, e):
        self.Close(True)

    def OnRun(self, e):

        # get data to send to the engine
        name = self.simulation_name_textbox.GetValue()
        db = self.database_combo.GetValue()
        user_name = self.account_combo.GetValue()
        datasets = self.getSelectedItems()

        # get the user account from selected user_name
        user_info_json = None
        for affil in self.accounts:
            if affil.ID() == user_name:
                user_info_json = affil.toJSON()

        # todo: check all constraints before executing a simulation
        # raise exceptions before executing the simulation
        if user_info_json is None:
            elog.critical('Cannot execute simulation if no user account is provided')
            return

        # set a default simulation name if none is provided
        if name.strip() == '':
            name = "Simulation_run_" + time.strftime('%m-%d-%Y')

        # build kwargs to pass to engineAccessors
        kwargs = dict(simulationName=name, dbName=db, user_json=user_info_json, datasets=datasets)

        # initiate simulation
        engineAccessors.runSimulation(**kwargs)

        self.Close()

    def getSelectedItems(self):
        selected = []
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsChecked(i):
                selected.append(self.variableList.GetItemText(i))

        return selected

    def getDatabases(self):
        '''
        Queries the engine for the known databases
        :return: a list of databases that are loaded into the engine
        '''

        # query the engine to get all available database connections
        available_connections = engineAccessors.getDbConnections()
        return available_connections

    def OnAddNew(self, e):
        self.dlg.CenterOnScreen()
        self.dlg.ShowModal()

    # def OnOkButton(self, event):
    #
    #     usersjson = env_vars.USERS_JSON
    #     with open(usersjson, 'a') as f:
    #         self.accountinfo = self.dlg.GetTextBoxValues()
    #         accounttxt = "[person]\n" \
    #                      "firstname = " + self.accountinfo[0] + "\n" \
    #                      + "lastname = " + self.accountinfo[1] + "\n" \
    #                      + "organizationcode = " + self.accountinfo[2] + "\n" \
    #                      + "phone = " + self.accountinfo[3] + "\n" \
    #                      + "email = " + self.accountinfo[4] + "\n" \
    #                      + "address = " + self.accountinfo[5] + "\n" \
    #                      + "start_date = " + self.accountinfo[6] + "\n" \
    #                      + "\n"
    #     self.RefreshCombo()
    #
    #     file.write(accounttxt)
    #     file.close()
    #     self.dlg.Close(True)

    # def RefreshCombo(self):
    #     # Simply appends the item to the combobox
    #     self.summary_page.accountCombo.AppendItems([self.accountinfo[1]])

    # def LogSimulation(self):
    #     currentdir = os.path.dirname(os.path.abspath(__file__))
    #     connections_txt = os.path.abspath(os.path.join(currentdir, '../../log/' + self.logfilename))
    #     file = open(connections_txt, 'a')
    #     loginfo = self.summary_page.GetLogValues()
    #     logtxt = "[Simulation]\n" + \
    #              "Simulation Name = " + loginfo[0] + "\n" + \
    #              "Database = " + loginfo[1] + "\n" + \
    #              "User = " + loginfo[2] + "\n" +\
    #              "Date = " + time.strftime("%m/%d/%Y") + "\n" + \
    #              "\n\n"
    #     file.write(logtxt)
    #     file.close()
    #
    # def CheckSimulationName(self, simname):
    #     filepath = self.CreatePreRunLogFile()
    #     file = open(filepath, 'r')
    #     if simname in file.read():
    #         file.close()
    #         return True
    #     else:
    #         file.close()
    #         return False
    #
    # def CreatePreRunLogFile(self):
    #     currentdir = os.path.dirname(os.path.abspath(__file__))
    #     filepath = os.path.abspath(os.path.join(currentdir, '../../log/' + self.logfilename))
    #     if os.path.exists(filepath):
    #         return filepath
    #     else:
    #         file = open(filepath, 'w')
    #         file.close()
    #         return filepath
