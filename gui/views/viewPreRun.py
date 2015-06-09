__author__ = 'Francisco'

import wx
import os


class viewPreRun(wx.Frame):
    def __init__(self):                                                         # this style makes the window non-resizable
        wx.Frame.__init__(self, None, title="Pre Run", size=(450, 425), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

        #  Variables
        self.panel = ""
        self.page1 = ""
        self.page2 = ""
        self.page3 = ""
        self.notebook = ""
        self.sizer = ""

        # Here we create a panel and a notebook on the panel
        self.panel = wx.Panel(self)
        self.notebook = wx.Notebook(self.panel)

        # create the page windows as children of the notebook
        self.page1 = PageOne(self.notebook)
        self.page2 = PageTwo(self.notebook)
        self.page3 = PageThree(self.notebook)

        # add the pages to the notebook with the label to show on the tab
        self.notebook.AddPage(self.page1, "Summary")
        self.notebook.AddPage(self.page2, "Details")
        self.notebook.AddPage(self.page3, "Page 3")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.notebook, 1, wx.EXPAND)
        self.panel.SetSizer(self.sizer)

class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)

        #  Variables
        self.parent = ""
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
        self.databaseComboChoices = self.loadDatabase()
        self.accountComboChoices = self.loadAccounts()


        self.parent = parent
        self.sizer = wx.GridBagSizer(5, 5)

        self.simulationName = wx.StaticText(self, label="Simulation Name: ")
        self.sizer.Add(self.simulationName, pos=(1, 0), flag=wx.LEFT, border=10)

        self.simulationNameTextBox = wx.TextCtrl(self)
        self.sizer.Add(self.simulationNameTextBox, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)

        self.databaseName = wx.StaticText(self, label="Database: ")
        self.sizer.Add(self.databaseName, pos=(2, 0), flag=wx.LEFT|wx.TOP, border=10)

        self.databaseCombo = wx.ComboBox(self, choices=self.databaseComboChoices, style=wx.CB_READONLY)
        self.sizer.Add(self.databaseCombo, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND, border=5)

        # browseDataBaseButton = wx.Button(self, label="Browse...")
        # sizer.Add(browseDataBaseButton, pos=(2, 4), flag=wx.TOP|wx.RIGHT, border=5)

        self.accountName = wx.StaticText(self, label="User Account: ")
        self.sizer.Add(self.accountName, pos=(3, 0), flag=wx.TOP|wx.LEFT, border=10)

        self.accountCombo = wx.ComboBox(self, choices=self.accountComboChoices, style=wx.CB_READONLY)
        self.sizer.Add(self.accountCombo, pos=(3, 1), span=(1, 2), flag=wx.TOP|wx.EXPAND, border=5)

        self.addAccountButton = wx.Button(self, label="Add New")
        self.sizer.Add(self.addAccountButton, pos=(3, 3), flag=wx.TOP|wx.RIGHT, border=5)

        self.lineBreak = wx.StaticLine(self)
        self.sizer.Add(self.lineBreak, pos=(4, 0), span=(1, 4), flag=wx.EXPAND|wx.BOTTOM, border=10)

        self.sizerStaticBox = wx.StaticBox(self, label="Optional Features")

        self.boxsizer = wx.StaticBoxSizer(self.sizerStaticBox, wx.VERTICAL)
        self.boxsizer.Add(wx.CheckBox(self, label="Display Simulation Message"), flag=wx.LEFT|wx.TOP, border=5)
        self.boxsizer.Add(wx.CheckBox(self, label="Log Simulation Message"), flag=wx.LEFT, border=5)
        self.boxsizer.Add(wx.CheckBox(self, label="Checkbox 3"), flag=wx.LEFT|wx.BOTTOM, border=5)
        self.sizer.Add(self.boxsizer, pos=(5, 0), span=(1, 4), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

        self.helpButton = wx.Button(self, label='Help')
        self.sizer.Add(self.helpButton, pos=(7, 0), flag=wx.LEFT, border=10)

        self.runButton = wx.Button(self, label="Run")
        self.sizer.Add(self.runButton, pos=(7, 3), flag=wx.BOTTOM | wx.RIGHT, border=5)

        self.cancelButton = wx.Button(self, label="Cancel")
        self.sizer.Add(self.cancelButton, pos=(7, 2), flag=wx.BOTTOM | wx.RIGHT, border=5)

        self.sizer.AddGrowableCol(2)

        self.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def onAddUser(self):
        dlg = AddNewUserDialog(self, id=-1, title="Add New User", style=wx.DEFAULT_DIALOG_STYLE)
        return dlg

    def loadDatabase(self):
        currentdir = os.path.dirname(os.path.abspath(__file__))  # Get the directory
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/connections'))  # finds the file
        file = open(connections_txt, 'r')
        data = file.readlines()
        file.close()
        return self.getFromFile(data, "name")

    def loadAccounts(self):
        currentdir = os.path.dirname(os.path.abspath(__file__))  # Get the directory
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/preferences'))  # finds the file
        file = open(connections_txt, 'r')
        data = file.readlines()
        file.close()
        return self.getFromFile(data, "lastname")

    def getFromFile(self, data, search):
        combobox = []
        for line in data:
            words = line.split(' = ')
            if words[0] == search:
                combobox.append(words[1].split('\n')[0])
        combobox.sort()
        return combobox


class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a Page Two", (40, 40))

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a Page Three\nThis is here in case we want to add another tab. ", (60, 60))

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
        if self.firstnameTextBox.GetValue == '' or \
                        self.lastnameTextBox.GetValue == '' or \
                        self.organizationTextBox.GetValue() == '' or \
                        self.phoneTextBox.GetValue() == '' or \
                        self.emailTextBox.GetValue() == '' or \
                        self.addressTextBox.GetValue() == '' or \
                        self.startdateTextBox.GetValue == '':
            self.okbutton.Disable()
        else:
            self.okbutton.Enable()

    def GetTextBoxValues(self):
        accountInfo = [self.firstnameTextBox, self.lastnameTextBox, self.organizationTextBox,
                       self.phoneTextBox, self.emailTextBox,
                       self.addressTextBox, self.startdateTextBox]
        return accountInfo

