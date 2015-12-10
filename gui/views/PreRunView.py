__author__ = 'Francisco'

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, CheckListCtrlMixin


class CheckListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, CheckListCtrlMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, size=(350, 400), style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)
        CheckListCtrlMixin.__init__(self)

class viewPreRun(wx.Frame):
    def __init__(self, parent=None):                             # this style makes the window non-resizable
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





