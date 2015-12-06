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
    def __init__(self):
        viewPreRun.__init__(self)

        # Defining the table columns
        table_columns = ["Name", "Component"]
        for i in range(len(table_columns)):
            self.variableList.InsertColumn(i, str(table_columns[i]))

        self._data = None

        self.populateVariableList()

        self.cancel_button.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.run_button.Bind(wx.EVT_BUTTON, self.OnRun)
        self.add_account_button.Bind(wx.EVT_BUTTON, self.OnAddNew)

        self.dlg = self.onAddUser()

        self.accounts = self.loadAccounts()

        # Old code
        # self.dlg = self.summary_page.onAddUser()
        # self.logfilename = "prerunlog.txt"
        # self.initBinding()
        #
        # # load data
        # dbs = self.getDatabases()
        # db_names = [db['name'] for db in dbs.itervalues()]
        # self.summary_page.databaseCombo.AppendItems(db_names)
        # self.summary_page.databaseCombo.SetSelection(0)
        #
        # # Load account drop down
        # self.accounts = self.summary_page.loadAccounts()
        # account_names = [' '.join([affil.person.lastname,'['+affil.organization.code+']']) for affil in self.accounts]
        # self.summary_page.accountCombo.AppendItems(account_names)
        # self.summary_page.accountCombo.SetSelection(0)
        #
        # # change the selection to the index of the first local db that is found
        # for i in range(0,len(db_names)):
        #     if '(local)' in db_names[i]:
        #         self.summary_page.databaseCombo.SetSelection(i)

    def loadAccounts(self):
        # todo: get path from environment variables
        currentdir = os.path.dirname(os.path.abspath(__file__))  # Get the directory
        known_users = []
        # with open(os.path.abspath(os.path.join(currentdir, '../../app_data/configuration/users.pkl')),'rb') as f:
        #     users.extend(dill.load(f))

        # todo: get from environments
        # build affiliation/person/org objects from the users.yaml file
        # with open(os.path.abspath(os.path.join(currentdir, '../../app_data/configuration/users.json')),'r') as f:

        userjson = env_vars.USER_JSON
        elog.debug('userjson ' + userjson)
        with open(userjson,'r') as f:
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


        #     # build checkbox elements for each output exchange item found above
        #     y_pos = 30
        #     for key, value in self.output_name_list.iteritems():
        #         wx.StaticText(scrollWin, id=wx.ID_ANY, label=key, pos=(30, y_pos))
        #         y_pos += 20
        #
        #         for i in value:
        #             # todo: cb_id should be modelID_itemID to provide easy lookup in engine.
        #             cb_id = key + '_' + i
        #             cb = wx.CheckBox(scrollWin, id=wx.ID_ANY, label=i, pos=(50, y_pos), name=cb_id)
        #             cb.SetValue(True)
        #             y_pos += 20
        #             self.cb_list.append(cb)

    # def initBinding(self):
    #     self.summary_page.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
    #     self.summary_page.runButton.Bind(wx.EVT_BUTTON, self.OnRun)
    #     self.summary_page.addAccountButton.Bind(wx.EVT_BUTTON, self.OnAddNew)
    #     self.dlg.okbutton.Bind(wx.EVT_BUTTON, self.OnOkButton)

    def OnCancel(self, e):
        self.Close(True)

    def OnRun(self, e):

        # fixme: this doesn't look like it is setting anything in the engine.
        # send database info into the engine
        name = self.simulation_name_textbox.GetValue()
        db = self.database_combo.GetValue()
        user_name = self.account_combo.GetValue()

        # todo: pass simulation name, database id, and user info into the engine
        datasets = self.GetDataToSave()

        # get the user account from selected user_name
        user_info = None
        for affil in self.accounts:
            if affil.ID() == user_name:
                user_info_json = affil.toJSON()

        # todo: check all constraints before executing a simulation
        # raise exceptions before executing the simulation
        if user_info_json is None:
            raise Exception('Cannot execute simulation if no user account is provided')
        if name.strip() == '':
            name = "Simulation_run_" + time.strftime('%m-%d-%Y')
            # raise Exception('Cannot execute simulation if no simulation name is provided')

        # build kwargs to pass to engineAccessors
        kwargs = dict(simulationName=name, dbName=db, user_json=user_info_json, datasets=datasets)

        # initiate simulation
        engineAccessors.runSimulation(**kwargs)

        self.Close()

    def getSelectedItems(self):
        selected = []
        num = self.variableList.GetItemCount()
        print "num: " + str(num)
        for i in range(num):
            if self.variableList.IsChecked(i):
                selected.append(self.variableList.GetItemText(i))

        return selected


    def GetDataToSave(self):

        # if len(self.data_page.cb_list) < 1:
        #     return
        selected = self.getSelectedItems()
        print "self._data: " + str(self._data)
        print "selected: " + str(selected)
        if len(selected) < 1:
            elog.info("Nothing was selected")
            return
        else:
            # eitems = {}
            return selected
            # model_item_tuples = [(c.GetName().split('_')) for c in self.data_page.cb_list if c.GetValue()]

            # for model, item in model_item_tuples:
            #     if model not in eitems.keys():
            #         eitems[model] = [item]
            #     else:
            #         eitems[model].append(item)
            # return eitems

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

    def OnOkButton(self, event):

        # currentdir = os.path.dirname(os.path.abspath(__file__))
        # connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/preferences'))
        # file = open(connections_txt, 'a')

        usersjson = env_vars.USERS_JSON
        with open(usersjson, 'a') as f:
            self.accountinfo = self.dlg.GetTextBoxValues()
            accounttxt = "[person]\n" \
                         "firstname = " + self.accountinfo[0] + "\n" \
                         + "lastname = " + self.accountinfo[1] + "\n" \
                         + "organizationcode = " + self.accountinfo[2] + "\n" \
                         + "phone = " + self.accountinfo[3] + "\n" \
                         + "email = " + self.accountinfo[4] + "\n" \
                         + "address = " + self.accountinfo[5] + "\n" \
                         + "start_date = " + self.accountinfo[6] + "\n" \
                         + "\n"
        self.RefreshCombo()

        file.write(accounttxt)
        file.close()
        self.dlg.Close(True)

    def RefreshCombo(self):
        # Simply appends the item to the combobox
        self.summary_page.accountCombo.AppendItems([self.accountinfo[1]])

    def LogSimulation(self):
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../log/' + self.logfilename))
        file = open(connections_txt, 'a')
        loginfo = self.summary_page.GetLogValues()
        logtxt = "[Simulation]\n" + \
                 "Simulation Name = " + loginfo[0] + "\n" + \
                 "Database = " + loginfo[1] + "\n" + \
                 "User = " + loginfo[2] + "\n" +\
                 "Date = " + time.strftime("%m/%d/%Y") + "\n" + \
                 "\n\n"
        file.write(logtxt)
        file.close()

    def CheckSimulationName(self, simname):
        filepath = self.CreatePreRunLogFile()
        file = open(filepath, 'r')
        if simname in file.read():
            file.close()
            return True
        else:
            file.close()
            return False

    def CreatePreRunLogFile(self):
        currentdir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.abspath(os.path.join(currentdir, '../../log/' + self.logfilename))
        if os.path.exists(filepath):
            return filepath
        else:
            file = open(filepath, 'w')
            file.close()
            return filepath
