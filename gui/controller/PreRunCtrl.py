__author__ = 'Francisco'

import wx
from gui.views.PreRunView import viewPreRun
import os
import time
from coordinator import engineAccessors
from environment import env_vars

class logicPreRun(viewPreRun):
    def __init__(self):
        viewPreRun.__init__(self)
        self.dlg = self.summary_page.onAddUser()
        self.logfilename = "prerunlog.txt"
        self.initBinding()

        # load data
        dbs = self.getDatabases()
        db_names = [db['name'] for db in dbs.itervalues()]
        self.summary_page.databaseCombo.AppendItems(db_names)
        self.summary_page.databaseCombo.SetSelection(0)

        # Load account drop down
        self.accounts = self.summary_page.loadAccounts()
        account_names = [' '.join([affil.person.lastname,'['+affil.organization.code+']']) for affil in self.accounts]
        self.summary_page.accountCombo.AppendItems(account_names)
        self.summary_page.accountCombo.SetSelection(0)

        # change the selection to the index of the first local db that is found
        for i in range(0,len(db_names)):
            if '(local)' in db_names[i]:
                self.summary_page.databaseCombo.SetSelection(i)

    def initBinding(self):
        self.summary_page.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.summary_page.runButton.Bind(wx.EVT_BUTTON, self.OnRun)
        self.summary_page.addAccountButton.Bind(wx.EVT_BUTTON, self.OnAddNew)
        self.dlg.okbutton.Bind(wx.EVT_BUTTON, self.OnOkButton)

    def OnCancel(self, e):
        self.Close(True)

    def OnRun(self, e):

        # fixme: this doesn't look like it is setting anything in the engine.
        # send database info into the engine
        name = self.summary_page.simulationNameTextBox.GetValue()
        db = self.summary_page.databaseCombo.GetValue()
        user_name = self.summary_page.accountCombo.GetValue()


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

    def GetDataToSave(self):

        if len(self.data_page.cb_list) < 1:
            return
        else:
            eitems = {}
            model_item_tuples = [(c.GetName().split('_')) for c in self.data_page.cb_list if c.GetValue()]
            for model, item in model_item_tuples:
                if model not in eitems.keys():
                    eitems[model] = [item]
                else:
                    eitems[model].append(item)
            return eitems

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