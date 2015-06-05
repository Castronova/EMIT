__author__ = 'Francisco'

import wx


class viewPreRun(wx.Frame):
    def __init__(self):                                                         # this style makes the window non-resizable
        wx.Frame.__init__(self, None, title="Window Title", size=(450, 425), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)

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
        self.browseAccountButton = ""
        self.lineBreak = ""
        self.sizerStaticBox = ""
        self.boxsizer = ""
        self.cancelButton = ""
        self.runButton = ""

        self.parent = parent
        self.sizer = wx.GridBagSizer(5, 5)

        self.simulationName = wx.StaticText(self, label="Simulation Name: ")
        self.sizer.Add(self.simulationName, pos=(1, 0), flag=wx.LEFT, border=10)

        self.simulationNameTextBox = wx.TextCtrl(self)
        self.sizer.Add(self.simulationNameTextBox, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)

        self.databaseName = wx.StaticText(self, label="Database: ")
        self.sizer.Add(self.databaseName, pos=(2, 0), flag=wx.LEFT|wx.TOP, border=10)

        self.databaseCombo = wx.ComboBox(self)
        self.sizer.Add(self.databaseCombo, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND, border=5)

        # browseDataBaseButton = wx.Button(self, label="Browse...")
        # sizer.Add(browseDataBaseButton, pos=(2, 4), flag=wx.TOP|wx.RIGHT, border=5)

        self.accountName = wx.StaticText(self, label="User Account: ")
        self.sizer.Add(self.accountName, pos=(3, 0), flag=wx.TOP|wx.LEFT, border=10)

        self.accountCombo = wx.ComboBox(self)
        self.sizer.Add(self.accountCombo, pos=(3, 1), span=(1, 3), flag=wx.TOP|wx.EXPAND, border=5)

        self.browseAccountButton = wx.Button(self, label="Add New")
        self.sizer.Add(self.browseAccountButton, pos=(3, 4), flag=wx.TOP|wx.RIGHT, border=5)

        self.lineBreak = wx.StaticLine(self)
        self.sizer.Add(self.lineBreak, pos=(4, 0), span=(1, 5), flag=wx.EXPAND|wx.BOTTOM, border=10)

        self.sizerStaticBox = wx.StaticBox(self, label="Optional Features")

        self.boxsizer = wx.StaticBoxSizer(self.sizerStaticBox, wx.VERTICAL)
        self.boxsizer.Add(wx.CheckBox(self, label="Display Simulation Message"), flag=wx.LEFT|wx.TOP, border=5)
        self.boxsizer.Add(wx.CheckBox(self, label="Log Simulation Message"), flag=wx.LEFT, border=5)
        self.boxsizer.Add(wx.CheckBox(self, label="Checkbox 3"), flag=wx.LEFT|wx.BOTTOM, border=5)
        self.sizer.Add(self.boxsizer, pos=(5, 0), span=(1, 5), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, border=10)

        self.helpButton = wx.Button(self, label='Help')
        self.sizer.Add(self.helpButton, pos=(7, 0), flag=wx.LEFT, border=10)

        self.runButton = wx.Button(self, label="Run")
        self.sizer.Add(self.runButton, pos=(7, 4))

        self.cancelButton = wx.Button(self, label="Cancel")
        self.sizer.Add(self.cancelButton, pos=(7, 3), span=(1, 1), flag=wx.BOTTOM | wx.RIGHT, border=5)

        self.sizer.AddGrowableCol(2)

        self.SetSizer(self.sizer)


class PageTwo(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a Page Two", (40, 40))

class PageThree(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This is a Page Three\nThis is here in case we want to add another tab. ", (60, 60))

