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

        wx.Frame.__init__(self, parent=parent, title="Add User",
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)
        self.parent = parent

        # Create panel
        panel = wx.Panel(self)

        # Create sizers
        fgs = wx.FlexGridSizer(rows=5, cols=2, vgap=9, hgap=5)
        organization_button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)


        #  Static Text
        self.first_name_label = wx.StaticText(panel, label="First Name: ")
        self.last_name_label = wx.StaticText(panel, label="Last Name: ")
        self.organization_label = wx.StaticText(panel, label="Organization: ")
        white_space_label = wx.StaticText(panel, label="")  # Created so the organization list box will be on the left
        white_space_label2 = wx.StaticText(panel, label="")  # Created so the ok and cancel buttons will be on the left

        #  Text Boxes
        self.first_name_text_box = wx.TextCtrl(panel)
        self.last_name_text_box = wx.TextCtrl(panel)
        self.add_organization_btn = wx.Button(panel, label="Add", style=wx.BU_EXACTFIT)
        self.edit_organization_btn = wx.Button(panel, label="Edit", style=wx.BU_EXACTFIT)
        self.remove_organization_btn = wx.Button(panel, label="Remove", style=wx.BU_EXACTFIT)
        self.organization_list_box = wx.ListBox(panel)

        # Buttons
        self.cancel_button = wx.Button(panel, wx.ID_CANCEL)
        self.ok_button = wx.Button(panel, wx.ID_OK)

        self.ok_button.SetDefault()
        self.ok_button.Disable()

        organization_button_sizer.Add(self.add_organization_btn, 1, wx.EXPAND | wx.ALL, 0)
        organization_button_sizer.Add(self.edit_organization_btn, 1, wx.EXPAND | wx.ALL, 0)
        organization_button_sizer.Add(self.remove_organization_btn, 1, wx.EXPAND | wx.ALL, 0)

        button_sizer.Add(self.ok_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        button_sizer.Add(self.cancel_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        fgs.AddMany([self.first_name_label, (self.first_name_text_box, 1, wx.EXPAND),
                     self.last_name_label, (self.last_name_text_box, 1, wx.EXPAND),
                     self.organization_label, (organization_button_sizer, 1, wx.EXPAND),
                     white_space_label, (self.organization_list_box, 1, wx.EXPAND),
                     white_space_label2, (button_sizer, 1, wx.ALL | wx.ALIGN_RIGHT, 0)])

        hbox.Add(fgs, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)

        # Allows the organization list box to expand vertically
        fgs.AddGrowableRow(3, 1)
        # Allows the second column to expand when resizing
        fgs.AddGrowableCol(1, 1)

        panel.SetSizerAndFit(hbox)
        hbox.Fit(self)  # Sizes the window automatically so the components fit inside the window
