__author__ = 'Francisco'

import os
import wx
import coordinator.users as Users
from coordinator import engineAccessors
from environment import env_vars
from coordinator.emitLogging import elog
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, CheckListCtrlMixin


class CheckListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, CheckListCtrlMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(350, 400), style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        CheckListCtrlMixin.__init__(self)

class viewPreRun(wx.Frame):
    def __init__(self, parent=None):                                                     # this style makes the window non-resizable
        wx.Frame.__init__(self, parent=parent, title="Pre Run", size=(405, 375),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        # define top and bottom panels
        panel = wx.Panel(self)
        top_panel = wx.Panel(panel)
        lower_panel = wx.Panel(panel)

        grid_bag_sizer = wx.GridBagSizer(vgap=5, hgap=5)

        # build top panel
        #  Creating components for the top panel
        self.simulation_name_static_text = wx.StaticText(top_panel, label="Simulation Name:")
        self.simulation_name_textbox = wx.TextCtrl(top_panel)
        self.database_name = wx.StaticText(top_panel, label="Database:")
        self.account_name = wx.StaticText(top_panel, label="User Account:")
        self.database_combo = wx.ComboBox(top_panel, choices=[], style=wx.CB_READONLY)
        self.account_combo = wx.ComboBox(top_panel, choices=[], style=wx.CB_READONLY)
        self.add_account_button = wx.Button(top_panel, label="Add New")
        self.run_button = wx.Button(top_panel, id=wx.ID_OK, label="Run")
        self.cancel_button = wx.Button(top_panel, id=wx.ID_CANCEL, label="Cancel")

        #  Adding components to grid bag sizer
        grid_bag_sizer.Add(self.simulation_name_static_text, pos=(1, 0), flag=wx.LEFT, border=10)
        grid_bag_sizer.Add(self.simulation_name_textbox, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        grid_bag_sizer.Add(self.database_name, pos=(2, 0), flag=wx.LEFT | wx.TOP, border=10)
        grid_bag_sizer.Add(self.database_combo, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND, border=5)
        grid_bag_sizer.Add(self.account_name, pos=(3, 0), flag=wx.TOP | wx.LEFT, border=10)
        grid_bag_sizer.Add(self.account_combo, pos=(3, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND, border=5)
        grid_bag_sizer.Add(self.add_account_button, pos=(3, 3), flag=wx.TOP|wx.RIGHT, border=5)
        grid_bag_sizer.Add(self.run_button, pos=(4, 3), flag=wx.BOTTOM | wx.RIGHT, border=5)
        grid_bag_sizer.Add(self.cancel_button, pos=(4, 2), flag=wx.BOTTOM | wx.RIGHT, border=5)

        self.run_button.SetDefault()
        top_panel.SetSizer(grid_bag_sizer)

        # build lower panel
        self.variableList = CheckListCtrl(lower_panel)
        lower_panel_title = wx.StaticText(lower_panel, label="Select Outputs to Save:")
        hbox_lower_panel = wx.BoxSizer(wx.VERTICAL)
        hbox_lower_panel.Add(lower_panel_title, 0, wx.EXPAND | wx.LEFT, 5)
        hbox_lower_panel.Add(self.variableList, 1, wx.EXPAND | wx.ALL, 2)
        lower_panel.SetSizer(hbox_lower_panel)


        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(top_panel, 1, wx.EXPAND | wx.ALL, 2)
        vbox.Add(lower_panel, 1, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(vbox)
        self.Show()

        #  Old code
        # #  Variables
        # self.panel = ""
        # self.summary_page = ""
        # self.data_page = ""
        # self.page3 = ""
        # self.notebook = ""
        # self.sizer = ""
        #
        # # Here we create a panel and a notebook on the panel
        # self.panel = wx.Panel(self)
        # self.notebook = wx.Notebook(self.panel)
        #
        # # create the page windows as children of the notebook
        # self.summary_page = SummaryPage(self.notebook)
        #
        # #  Uncomment this two bottom lines to show a second or third tab.
        # self.data_page = DataPage(self.notebook)
        # # self.page3 = PageThree(self.notebook)
        #
        # # add the pages to the notebook with the label to show on the tab
        # self.notebook.AddPage(self.summary_page, "Summary")
        # self.notebook.AddPage(self.data_page, "Data")
        # # self.notebook.AddPage(self.page3, "Page 3")
        #
        # # finally, put the notebook in a sizer for the panel to manage
        # # the layout
        # self.sizer = wx.BoxSizer()
        # self.sizer.Add(self.notebook, 1, wx.EXPAND)
        # self.panel.SetSizer(self.sizer)

    def autoSizeColumns(self):
        for i in range(self.variableList.GetColumnCount()):
            self.variableList.SetColumnWidth(i, wx.LIST_AUTOSIZE)

    def alternateRowColor(self, color="#DCEBEE"):
        for i in range(self.variableList.GetItemCount()):
            if i % 2 == 0:
                self.variableList.SetItemBackgroundColour(i, color)

    def onAddUser(self):
        dlg = AddNewUserDialog(self, id=-1, title="Add New User", style=wx.DEFAULT_DIALOG_STYLE)
        return dlg


class SummaryPage(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        #  Variables
        self.parent = parent
        self.sizer = ""
        self.simulationName = ""
        self.simulationNameTextBox = ""
        self.databaseName = ""
        self.accountName = ""
        self.accountCombo = ""
        self.addAccountButton = ""
        self.lineBreak = ""
        self.sizerStaticBox = ""
        self.boxsizer = ""
        self.cancelButton = ""
        self.runButton = ""

        self.sizer = wx.GridBagSizer(vgap=5, hgap=5)

        self.simulationName = wx.StaticText(self, label="Simulation Name: ")
        self.sizer.Add(self.simulationName, pos=(1, 0), flag=wx.LEFT, border=10)

        self.simulationNameTextBox = wx.TextCtrl(self)
        self.sizer.Add(self.simulationNameTextBox, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)

        self.databaseName = wx.StaticText(self, label="Database: ")
        self.sizer.Add(self.databaseName, pos=(2, 0), flag=wx.LEFT | wx.TOP, border=10)

        self.databaseCombo = wx.ComboBox(self, choices=[], style=wx.CB_READONLY)
        self.sizer.Add(self.databaseCombo, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND, border=5)

        self.accountName = wx.StaticText(self, label="User Account: ")
        self.sizer.Add(self.accountName, pos=(3, 0), flag=wx.TOP | wx.LEFT, border=10)

        self.accountCombo = wx.ComboBox(self, choices=[], style=wx.CB_READONLY)
        self.sizer.Add(self.accountCombo, pos=(3, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND, border=5)

        self.addAccountButton = wx.Button(self, label="Add New")
        self.sizer.Add(self.addAccountButton, pos=(3, 3), flag=wx.TOP|wx.RIGHT, border=5)

        self.lineBreak = wx.StaticLine(self)
        self.sizer.Add(self.lineBreak, pos=(4, 0), span=(1, 4), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        self.sizerStaticBox = wx.StaticBox(self, label="Optional Features")

        self.boxsizer = wx.StaticBoxSizer(self.sizerStaticBox, wx.VERTICAL)

        self.displayMessage = wx.CheckBox(self, label="Display Simulation Message")
        self.logMessage = wx.CheckBox(self, label="log Simulation Message")
        # self.checkbox3 = wx.CheckBox(self, label="Checkbox 3")

        self.displayMessage.SetValue(True)  # By default it is checked
        self.logMessage.SetValue(False)

        self.boxsizer.Add(self.displayMessage, flag=wx.LEFT | wx.TOP, border=5)
        self.boxsizer.Add(self.logMessage, flag=wx.LEFT, border=5)
        # self.boxsizer.Add(self.checkbox3, flag=wx.LEFT | wx.BOTTOM, border=5)

        self.sizer.Add(self.boxsizer, pos=(5, 0), span=(1, 4), flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=10)

        # self.helpButton = wx.Button(self, id=wx.ID_HELP, label='Help')
        # self.sizer.Add(self.helpButton, pos=(7, 0), flag=wx.LEFT, border=10)

        self.runButton = wx.Button(self, id=wx.ID_OK, label="Run")
        self.sizer.Add(self.runButton, pos=(7, 3), flag=wx.BOTTOM | wx.RIGHT, border=5)
        self.runButton.SetDefault()

        self.cancelButton = wx.Button(self, id=wx.ID_CANCEL, label="Cancel")
        self.sizer.Add(self.cancelButton, pos=(7, 2), flag=wx.BOTTOM | wx.RIGHT, border=5)

        self.sizer.AddGrowableCol(2)

        self.SetSizer(self.sizer)

    def onAddUser(self):
        dlg = AddNewUserDialog(self, id=-1, title="Add New User", style=wx.DEFAULT_DIALOG_STYLE)
        return dlg


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

    def getFromFile(self, data, search):
        combobox = []
        for line in data:
            words = line.split(' = ')
            if words[0] == search:
                combobox.append(words[1].split('\n')[0])
        combobox.sort()
        return combobox

    def GetLogValues(self):
        loginfo = [self.simulationNameTextBox.GetValue(), self.databaseCombo.GetValue(), self.accountCombo.GetValue()]
        return loginfo


# class DataPage(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
#         scrollWin = wx.ScrolledWindow(self, -1, size=(440, 325))
#         self.cb_list = []
#
#         if len(engineAccessors.getAllLinks()) < 1:
#             wx.StaticText(scrollWin, id=wx.ID_ANY, label="No links have been added", pos=(10, 10))
#         else:
#             wx.StaticText(scrollWin, id=wx.ID_ANY, label="Specify output data sets to be saved", pos=(10, 10))
#             # query the engine for all output exchange items for each model in each link. store these in a dictionary
#             model_name_list = []
#             self.output_name_list = {}
#             temp_list = []
#
#
#             # compile a list of model ids and names that exist in the configuration
#             models = {}
#             links = engineAccessors.getAllLinks()
#             for link in links:
#                 s_id = link['source_component_id']
#                 t_id = link['target_component_id']
#                 if s_id not in models.keys():
#                     models[s_id] = link['source_component_name']
#                 if t_id not in models.keys():
#                     models[t_id] = link['target_component_name']
#
#             # sort models and loop over them to populate checkboxes
#             for model_id, model_name in sorted(models.items(), key=lambda x: x[1]):
#                 oei = engineAccessors.getOutputExchangeItems(model_id, returnGeoms=False)
#                 self.output_name_list[model_name] = [ei['name'] for ei in oei]
#
#             # for i in engineAccessors.getAllLinks():
#             #
#             #
#             #
#             #     # get output exchange items from all source components
#             #     if i['source_component_name'] not in model_name_list:  # Outputs only
#             #         model_name_list.append(i['source_component_name'])
#             #         oei = engineAccessors.getOutputExchangeItems(i['source_component_id'], returnGeoms=False)
#             #         temp_list = [ei['name'] for ei in oei] #temp_list.append(item['name'])
#             #         self.output_name_list[i['source_component_name']] = temp_list
#             #         temp_list = []
#             #
#             #     if i['target_component_name'] not in model_name_list:
#             #         model_name_list.append(i['target_component_name'])
#             #         for item in engineAccessors.getOutputExchangeItems(i['target_component_id'], returnGeoms=False):
#             #             temp_list.append(item['name'])
#             #         self.output_name_list[i['target_component_name']] = temp_list
#             #         temp_list = []
#
#             # build checkbox elements for each output exchange item found above
#             y_pos = 30
#             for key, value in self.output_name_list.iteritems():
#                 wx.StaticText(scrollWin, id=wx.ID_ANY, label=key, pos=(30, y_pos))
#                 y_pos += 20
#
#                 for i in value:
#                     # todo: cb_id should be modelID_itemID to provide easy lookup in engine.
#                     cb_id = key + '_' + i
#                     cb = wx.CheckBox(scrollWin, id=wx.ID_ANY, label=i, pos=(50, y_pos), name=cb_id)
#                     cb.SetValue(True)
#                     y_pos += 20
#                     self.cb_list.append(cb)
#
#             scrollWin.SetScrollbars(0, 30, 0, y_pos/30+1)
#             scrollWin.SetScrollRate(0, 15)  # Scroll speed


# class PageThree(wx.Panel):
#     def __init__(self, parent):
#         wx.Panel.__init__(self, parent)
#         t = wx.StaticText(self, -1, "This is a Page Three\nThis is here in case we want to add another tab. ", (60, 60))

class AddNewUserDialog(wx.Dialog):
    def __init__(self, parent, id=wx.ID_ANY, title="", size=wx.DefaultSize, pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE):

        #  Variables
        self.parent = ""
        self.firstname = ""
        self.firstnameTextBox = ""
        self.lastname = ""
        self.lastnameTextBox = ""
        self.organization = ""
        self.phone = ""
        self.phoneTextBox = ""
        self.email = ""
        self.emailTextBox = ""
        self.address = ""
        self.addressTextBox = ""
        self.startdate = ""
        self.startdateTextBox = ""
        self.whitespace = ""
        self.okbutton = ""
        self.cancelButton = ""
        self.sizer = ""

        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, id, title, pos, size, style)

        self.PostCreate(pre)
        self.parent = parent

        self.sizer = wx.GridBagSizer(5, 5)

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
        self.startdateTextBox = wx.TextCtrl(self)

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
        self.sizer.Add(self.startdateTextBox, pos=(7, 1), span=(1, 2), flag=wx.TOP | wx.EXPAND)

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
        self.startdateTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)

    def setvalues(self, first, last, org, phone, email, address, date):
        self.firstnameTextBox = first
        self.lastnameTextBox = last
        self.organizationTextBox = org
        self.phoneTextBox = phone
        self.emailTextBox = email
        self.addressTextBox = address
        self.startdateTextBox = date

    def OnTextEnter(self, event):
        if not self.firstnameTextBox.GetValue or \
                not self.lastnameTextBox.GetValue or \
                        self.organizationTextBox.GetValue() == '' or \
                        self.phoneTextBox.GetValue() == '' or \
                        self.emailTextBox.GetValue() == '' or \
                        self.addressTextBox.GetValue() == '' or \
                        self.startdateTextBox.GetValue == '':
            self.okbutton.Disable()
        else:
            self.okbutton.Enable()
        self.firstname = ""

    def GetTextBoxValues(self):
        accountinfo = [self.firstnameTextBox.GetValue(), self.lastnameTextBox.GetValue(),
                       self.organizationTextBox.GetValue(), self.phoneTextBox.GetValue(),
                       self.emailTextBox.GetValue(), self.addressTextBox.GetValue(),
                       self.startdateTextBox.GetValue()]
        return accountinfo





