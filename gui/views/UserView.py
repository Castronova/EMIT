import wx


class OrganizationView(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize,
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        panel = wx.Panel(self)
        today = wx.DateTime_Now()

        # Labels
        name_label = wx.StaticText(panel, label="Name: ")
        description_label = wx.StaticText(panel, label="Description: ")
        type_label = wx.StaticText(panel, label="Type: ")
        url_label = wx.StaticText(panel, label="URL: ")
        start_date_label = wx.StaticText(panel, label="Start Date: ")
        phone_label = wx.StaticText(panel, label="Phone: ")
        email_label = wx.StaticText(panel, label="Email: ")

        # Textboxes/Dropdown/etc
        self.name_textbox = wx.TextCtrl(panel)
        self.description_textbox = wx.TextCtrl(panel)
        self.type_combo = wx.ComboBox(panel, style=wx.CB_READONLY)
        self.url_textbox = wx.TextCtrl(panel)
        self.start_date_picker = wx.DatePickerCtrl(panel, id=wx.ID_ANY, dt=today)
        self.phone_textbox = wx.TextCtrl(panel)
        self.email_textbox = wx.TextCtrl(panel)
        self.accept_button = wx.Button(panel, label="Accept")
        self.cancel_button = wx.Button(panel, label="Cancel")

        # Sizer
        sizer = wx.GridBagSizer(5, 5)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(name_label, pos=(1, 0), flag=wx.LEFT, border=15)
        sizer.Add(description_label, pos=(2, 0), flag=wx.LEFT, border=15)
        sizer.Add(type_label, pos=(3, 0), flag=wx.LEFT, border=15)
        sizer.Add(url_label, pos=(4, 0), flag=wx.LEFT, border=15)
        sizer.Add(start_date_label, pos=(5, 0), flag=wx.LEFT, border=15)
        sizer.Add(phone_label, pos=(6, 0), flag=wx.LEFT, border=15)
        sizer.Add(email_label, pos=(7, 0), flag=wx.LEFT, border=15)

        sizer.Add(self.name_textbox, pos=(1, 1), span=(1, 1), flag=wx.EXPAND | wx.RIGHT, border=10)
        sizer.Add(self.description_textbox, pos=(2, 1), span=(1, 1), flag=wx.EXPAND | wx.RIGHT, border=10)
        sizer.Add(self.type_combo, pos=(3, 1), span=(1, 1), flag=wx.EXPAND | wx.RIGHT, border=10)
        sizer.Add(self.url_textbox, pos=(4, 1), span=(1, 1), flag=wx.EXPAND | wx.RIGHT, border=10)
        sizer.Add(self.start_date_picker, pos=(5, 1), span=(1, 1), flag=wx.EXPAND | wx.RIGHT, border=10)
        sizer.Add(self.phone_textbox, pos=(6, 1), span=(1, 1), flag=wx.EXPAND | wx.RIGHT, border=10)
        sizer.Add(self.email_textbox, pos=(7, 1), span=(1, 1), flag=wx.EXPAND | wx.RIGHT, border=10)
        sizer.Add(button_sizer, pos=(8, 1), span=(1, 1), flag=wx.ALL | wx.EXPAND | wx.RIGHT, border=10)
        button_sizer.Add(self.accept_button, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        button_sizer.Add(self.cancel_button, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        panel.SetSizer(sizer)
        sizer.Fit(self)

        self.Show()


class UserView(wx.Frame):

    def __init__(self, parent):

        wx.Frame.__init__(self, parent=parent, title="Add User", style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^
                           wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.parent = parent

        psizer = wx.GridBagSizer(5, 5)
        fsizer = wx.BoxSizer(wx.VERTICAL)

        today = wx.DateTime_Now()

        panel = wx.Panel(self, -1, style=wx.TAB_TRAVERSAL)

        #  Static Text
        self.firstname_label = wx.StaticText(panel, label="First Name: ")
        self.lastname_label = wx.StaticText(panel, label="Last Name: ")
        self.organization_label = wx.StaticText(panel, label="Organization: ")
        self.phone_label = wx.StaticText(panel, label=" Phone: ")
        self.email_label = wx.StaticText(panel, label=" Email: ")
        self.address_label = wx.StaticText(panel, label=" Address: ")
        self.startdate_label = wx.StaticText(panel, label=" Start Date: ")
        self.whitespace_label = wx.StaticText(panel, label="")

        #  Text Boxes
        self.firstnameTextBox = wx.TextCtrl(panel)
        self.lastnameTextBox = wx.TextCtrl(panel)
        self.addOrganization = wx.Button(panel, label="Add", style=wx.BU_EXACTFIT)
        self.editOrganization = wx.Button(panel, label="Edit", style=wx.BU_EXACTFIT)
        self.removeOrganization = wx.Button(panel, label="Remove", style=wx.BU_EXACTFIT)
        self.organizationListBox = wx.ListBox(panel)
        self.phoneTextBox = wx.TextCtrl(panel)
        self.emailTextBox = wx.TextCtrl(panel)
        self.addressTextBox = wx.TextCtrl(panel)
        self.startDatePicker = wx.DatePickerCtrl(panel, id=wx.ID_ANY, dt=today)


        #  Static Text
        psizer.Add(self.firstname_label, pos=(1, 0), flag=wx.LEFT, border=15)
        psizer.Add(self.lastname_label, pos=(2, 0), flag=wx.LEFT, border=15)
        psizer.Add(self.organization_label, pos=(3, 0), flag=wx.LEFT, border=15)
        psizer.Add(self.phone_label, pos=(5, 0), flag=wx.LEFT, border=10)
        psizer.Add(self.email_label, pos=(6, 0), flag=wx.LEFT, border=10)
        psizer.Add(self.address_label, pos=(7, 0), flag=wx.LEFT, border=10)
        psizer.Add(self.startdate_label, pos=(8, 0), flag=wx.LEFT, border=10)
        psizer.Add(self.whitespace_label, pos=(0, 4), flag=wx.LEFT, border=5)

        #  Textbox
        psizer.Add(self.firstnameTextBox, pos=(1, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        psizer.Add(self.lastnameTextBox, pos=(2, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        psizer.Add(self.addOrganization, pos=(3, 1), span=(1, 1), flag=wx.TOP)
        psizer.Add(self.editOrganization, pos=(3, 2), span=(1, 1), flag=wx.TOP)
        psizer.Add(self.removeOrganization, pos=(3, 3), span=(1, 1), flag=wx.TOP)
        psizer.Add(self.organizationListBox, pos=(4, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        psizer.Add(self.phoneTextBox, pos=(5, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        psizer.Add(self.emailTextBox, pos=(6, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        psizer.Add(self.addressTextBox, pos=(7, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)
        psizer.Add(self.startDatePicker, pos=(8, 1), span=(1, 3), flag=wx.TOP | wx.EXPAND)

        #  Line Break After all the textboxes
        self.lineBreak = wx.StaticLine(self)
        psizer.Add(self.lineBreak, pos=(9, 0), span=(1, 5), flag=wx.EXPAND | wx.TOP, border=10)

        #  Buttons
        buttonsizer = wx.StdDialogButtonSizer()
        self.okbutton = wx.Button(panel, wx.ID_OK)
        self.cancelButton = wx.Button(panel, wx.ID_CANCEL)

        self.okbutton.SetDefault()
        self.okbutton.Disable()

        buttonsizer.AddButton(self.okbutton)
        buttonsizer.AddButton(self.cancelButton)
        buttonsizer.Realize()

        psizer.Add(buttonsizer, pos=(10, 1), span=(0, 3), flag=wx.ALIGN_RIGHT | wx.LEFT, border=10)

        # set the sizer for the panel
        panel.SetSizer(psizer)

        # add the panel to the fsizer
        fsizer.Add(panel)

        # set the sizer for the frame
        self.SetSizer(fsizer)
        self.Fit()

