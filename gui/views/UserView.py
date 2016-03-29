import wx



class UserView(wx.Dialog):
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
        self.firstname_label = wx.StaticText(self, label="First Name: ")
        self.lastname_label = wx.StaticText(self, label="Last Name: ")
        self.organization_label = wx.StaticText(self, label="Organization: ")
        self.phone_label = wx.StaticText(self, label=" Phone: ")
        self.email_label = wx.StaticText(self, label=" Email: ")
        self.address_label = wx.StaticText(self, label=" Address: ")
        self.startdate_label = wx.StaticText(self, label=" Start Date: ")
        self.whitespace_label = wx.StaticText(self, label="")

        #  Text Boxes
        self.firstnameTextBox = wx.TextCtrl(self)
        self.lastnameTextBox = wx.TextCtrl(self)
        self.organizationTextBox = wx.TextCtrl(self, size=(150, -1))
        self.addOrganization = wx.Button(self, label="+", style=wx.BU_EXACTFIT)
        self.removeOrganization = wx.Button(self, label="X", style=wx.BU_EXACTFIT)
        self.organizationListBox = wx.ListBox(self)
        self.phoneTextBox = wx.TextCtrl(self)
        self.emailTextBox = wx.TextCtrl(self)
        self.addressTextBox = wx.TextCtrl(self)
        self.startDatePicker = wx.DatePickerCtrl(self, id=wx.ID_ANY, dt=today)

        #  Static Text
        self.sizer.Add(self.firstname_label, pos=(1, 0), flag=wx.LEFT, border=15)
        self.sizer.Add(self.lastname_label, pos=(2, 0), flag=wx.LEFT, border=15)
        self.sizer.Add(self.organization_label, pos=(3, 0), flag=wx.LEFT, border=15)
        self.sizer.Add(self.phone_label, pos=(5, 0), flag=wx.LEFT, border=10)
        self.sizer.Add(self.email_label, pos=(6, 0), flag=wx.LEFT, border=10)
        self.sizer.Add(self.address_label, pos=(7, 0), flag=wx.LEFT, border=10)
        self.sizer.Add(self.startdate_label, pos=(8, 0), flag=wx.LEFT, border=10)
        self.sizer.Add(self.whitespace_label, pos=(0, 4), flag=wx.LEFT, border=5)

        #  Textbox
        self.sizer.Add(self.firstnameTextBox, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.lastnameTextBox, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.organizationTextBox, pos=(3, 1), span=(1, 1), flag=wx.TOP)
        self.sizer.Add(self.addOrganization, pos=(3, 2), span=(1, 1), flag=wx.TOP)
        self.sizer.Add(self.removeOrganization, pos=(3, 3), span=(1, 1), flag=wx.TOP)
        self.sizer.Add(self.organizationListBox, pos=(4, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)

        self.sizer.Add(self.phoneTextBox, pos=(5, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.emailTextBox, pos=(6, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.addressTextBox, pos=(7, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        self.sizer.Add(self.startDatePicker, pos=(8, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)

        #  Line Break After all the textboxes
        self.lineBreak = wx.StaticLine(self)
        self.sizer.Add(self.lineBreak, pos=(9, 0), span=(1, 5), flag=wx.EXPAND | wx.TOP, border=10)

        #  Buttons
        buttonsizer = wx.StdDialogButtonSizer()
        self.okbutton = wx.Button(self, wx.ID_OK)
        self.cancelButton = wx.Button(self, wx.ID_CANCEL)

        self.okbutton.SetDefault()
        self.okbutton.Disable()

        buttonsizer.AddButton(self.okbutton)
        buttonsizer.AddButton(self.cancelButton)
        buttonsizer.Realize()

        self.sizer.Add(buttonsizer, pos=(10, 1), span=(0, 4), flag=wx.ALIGN_RIGHT | wx.ALL, border=5)

        self.sizer.AddGrowableCol(2)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
