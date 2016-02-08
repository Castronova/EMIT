import datetime
import os
import time

import wx

import coordinator.users as users
from coordinator import engineAccessors
from coordinator.emitLogging import elog
from gui.views.PreRunView import viewPreRun
from utilities.gui import loadAccounts


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

        # populate the database_combo control with known databases
        dbs = self.getDatabases()
        db_names = [db['name'] for db in dbs.itervalues()]
        self.database_combo.AppendItems(db_names)
        self.database_combo.SetSelection(0)

        # populate the account droplist with known users
        self.refreshUserAccount()

    def refreshUserAccount(self):
        self.account_combo.Clear()
        self.accounts = loadAccounts()
        account_names = [' '.join([affil.person.lastname, '[' + affil.organization.code + ']']) for affil in
                         self.accounts]
        if len(account_names) > 0:
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
            elog.debug("PreRunCtrl.insert_data must be a dictionary")
        return

    def sort_output_model(self, models):
        output_name_list = {}
        for model_id, model_name in sorted(models.items(), key=lambda x: x[1]):
            oei = engineAccessors.getOutputExchangeItems(model_id, returnGeoms=False)
            output_name_list[model_name] = [ei['name'] for ei in oei]
        return output_name_list

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
        dlg = AddNewUserDialog(self, title="Add New User")
        dlg.CenterOnScreen()
        dlg.ShowModal()

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


class AddNewUserDialog(wx.Dialog):
    def __init__(self, parent, id=wx.ID_ANY, title="", size=wx.DefaultSize,
                 pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP):

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, id, title, pos, size, style)

        self.PostCreate(pre)
        self.parent = parent

        self.sizer = wx.GridBagSizer(5, 5)
        today = wx.DateTime_Now()

        #  Static Text
        self.firstname = wx.StaticText(self, label="First Name: ")
        self.lastname = wx.StaticText(self, label="Last Name: ")
        self.organization = wx.StaticText(self, label="Organization: ")
        self.phone = wx.StaticText(self, label=" Phone: ")
        self.email = wx.StaticText(self, label=" Email: ")
        self.address = wx.StaticText(self, label=" Address: ")
        self.startdate = wx.StaticText(self, label=" Start Date: ")
        self.whitespace = wx.StaticText(self, label="")

        #  Text Boxes
        self.firstnameTextBox = wx.TextCtrl(self)
        self.lastnameTextBox = wx.TextCtrl(self)
        self.organizationTextBox = wx.TextCtrl(self)
        self.phoneTextBox = wx.TextCtrl(self)
        self.emailTextBox = wx.TextCtrl(self)
        self.addressTextBox = wx.TextCtrl(self)
        # self.startdateTextBox = wx.TextCtrl(self)
        self.startDatePicker = wx.DatePickerCtrl(self, id=wx.ID_ANY, dt=today)

        #  Static Text
        self.sizer.Add(self.firstname, pos=(1, 0), flag=wx.LEFT, border=15)
        self.sizer.Add(self.lastname, pos=(2, 0), flag=wx.LEFT, border=15)
        self.sizer.Add(self.organization, pos=(3, 0), flag=wx.LEFT, border=15)
        self.sizer.Add(self.phone, pos=(4, 0), flag=wx.LEFT, border=10)
        self.sizer.Add(self.email, pos=(5, 0), flag=wx.LEFT, border=10)
        self.sizer.Add(self.address, pos=(6, 0), flag=wx.LEFT, border=10)
        self.sizer.Add(self.startdate, pos=(7, 0), flag=wx.LEFT, border = 10)
        self.sizer.Add(self.whitespace, pos=(0, 3), flag=wx.LEFT, border=5)

        #  Textbox
        self.sizer.Add(self.firstnameTextBox, pos=(1, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.lastnameTextBox, pos=(2, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.organizationTextBox, pos=(3, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.phoneTextBox, pos=(4, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.emailTextBox, pos=(5, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.addressTextBox, pos=(6, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.startDatePicker, pos=(7, 1), span=(1, 1), flag=wx.TOP | wx.EXPAND)

        #  Line Break After all the textboxes
        self.lineBreak = wx.StaticLine(self)
        self.sizer.Add(self.lineBreak, pos=(8, 0), span=(1, 4), flag=wx.EXPAND | wx.TOP, border=10)

        #  Buttons
        buttonsizer = wx.StdDialogButtonSizer()
        self.okbutton = wx.Button(self, wx.ID_OK)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL)

        self.okbutton.SetDefault()
        self.okbutton.Disable()

        buttonsizer.AddButton(self.okbutton)
        buttonsizer.AddButton(self.cancelButton)
        buttonsizer.Realize()

        self.sizer.Add(buttonsizer, pos=(9, 1), span=(0, 2), flag=wx.ALIGN_RIGHT | wx.ALL, border=5)

        self.sizer.AddGrowableCol(2)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.initBinding()


    def initBinding(self):
        self.firstnameTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.lastnameTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.organizationTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.phoneTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.emailTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.addressTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.startDatePicker.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.okbutton.Bind(wx.EVT_BUTTON, self.onOkBtn)

    def setvalues(self, first, last, org, phone, email, address, date):
        self.firstnameTextBox = first
        self.lastnameTextBox = last
        self.organizationTextBox = org
        self.phoneTextBox = phone
        self.emailTextBox = email
        self.addressTextBox = address
        self.startDatePicker = date

    def onOkBtn(self, event):
        # This works by reading the user file and getting all the users.
        # Then it writes to the user file with the old users + the new one added.

        new_user = self.GetTextBoxValues()
        firstname = new_user[0]
        lastname = new_user[1]
        organization = new_user[2]
        phone = new_user[3]
        email = new_user[4]
        address = new_user[5]
        start_date = new_user[6]
        #  The date needs to be converted to a datetime.datetime object
        start_date = datetime.datetime.strptime(start_date.FormatISOCombined(), "%Y-%m-%dT%H:%M:%S")

        # These are only samples for testing
        user_json_filepath = os.environ['APP_USER_PATH']  # get the file path of the user.json
        person = users.Person(firstname=firstname, lastname=lastname)

        organ = users.Organization(typeCV=organization, name=organization, code=organization)

        affilations = [users.Affiliation(email=email, startDate=start_date,
                                         organization=organ, person=person,
                                         phone=phone, address=address)]

        import json
        with open(user_json_filepath, 'r') as f:
            previous_user = f.read()

        with open(user_json_filepath, 'w') as f:
            new_user = {}
            for a in affilations:
                affil = a._affilationToDict()
                new_user.update(affil)
            new_user = json.dumps(new_user, sort_keys=True, indent=4, separators=(',', ': '))


            if not previous_user.isspace() and len(previous_user) > 0:
                # Removes the last } of previous_user and first { of new_user
                previous_user = previous_user.lstrip().rstrip().rstrip('}').rstrip()
                new_user = new_user.lstrip().rstrip().lstrip('{').lstrip()
                f.write(previous_user + ',' + new_user)
            else:
                # No previous users were found so only adding the new one.
                f.write(new_user)
            f.close()

        self.parent.refreshUserAccount()

        self.Close()

    def OnTextEnter(self, event):
        if not self.firstnameTextBox.GetValue or \
                not self.lastnameTextBox.GetValue or \
                        self.organizationTextBox.GetValue() == '' or \
                        self.phoneTextBox.GetValue() == '' or \
                        self.emailTextBox.GetValue() == '' or \
                        self.addressTextBox.GetValue() == '' or \
                        self.startDatePicker.GetValue == '':
            self.okbutton.Disable()
        else:
            self.okbutton.Enable()

    def GetTextBoxValues(self):
        accountinfo = [self.firstnameTextBox.GetValue(), self.lastnameTextBox.GetValue(),
                       self.organizationTextBox.GetValue(), self.phoneTextBox.GetValue(),
                       self.emailTextBox.GetValue(), self.addressTextBox.GetValue(),
                       self.startDatePicker.GetValue()]
        return accountinfo
