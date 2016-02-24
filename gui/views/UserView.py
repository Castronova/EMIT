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


    #     self.initBinding()
    #
    #
    # def initBinding(self):
    #     self.firstnameTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
    #     self.lastnameTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
    #     self.organizationTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
    #     self.phoneTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
    #     self.emailTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
    #     self.addressTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
    #     self.startDatePicker.Bind(wx.EVT_TEXT, self.OnTextEnter)
    #     self.okbutton.Bind(wx.EVT_BUTTON, self.onOkBtn)

    # def setvalues(self, first, last, org, phone, email, address, date):
    #     self.firstnameTextBox = first
    #     self.lastnameTextBox = last
    #     self.organizationTextBox = org
    #     self.phoneTextBox = phone
    #     self.emailTextBox = email
    #     self.addressTextBox = address
    #     self.startDatePicker = date
    #
    # def onOkBtn(self, event):
    #     # This works by reading the user file and getting all the users.
    #     # Then it writes to the user file with the old users + the new one added.
    #
    #     new_user = self.GetTextBoxValues()
    #     firstname = new_user[0]
    #     lastname = new_user[1]
    #     organization = new_user[2]
    #     phone = new_user[3]
    #     email = new_user[4]
    #     address = new_user[5]
    #     start_date = new_user[6]
    #     #  The date needs to be converted to a datetime.datetime object
    #     start_date = datetime.datetime.strptime(start_date.FormatISOCombined(), "%Y-%m-%dT%H:%M:%S")
    #
    #     # These are only samples for testing
    #     user_json_filepath = os.environ['APP_USER_PATH']  # get the file path of the user.json
    #     person = users.Person(firstname=firstname, lastname=lastname)
    #
    #     organ = users.Organization(typeCV=organization, name=organization, code=organization)
    #
    #     affilations = [users.Affiliation(email=email, startDate=start_date,
    #                                      organization=organ, person=person,
    #                                      phone=phone, address=address)]
    #
    #     import json
    #     with open(user_json_filepath, 'r') as f:
    #         previous_user = f.read()
    #
    #     with open(user_json_filepath, 'w') as f:
    #         new_user = {}
    #         for a in affilations:
    #             affil = a._affilationToDict()
    #             new_user.update(affil)
    #         new_user = json.dumps(new_user, sort_keys=True, indent=4, separators=(',', ': '))
    #
    #
    #         if not previous_user.isspace() and len(previous_user) > 0:
    #             # Removes the last } of previous_user and first { of new_user
    #             previous_user = previous_user.lstrip().rstrip().rstrip('}').rstrip()
    #             new_user = new_user.lstrip().rstrip().lstrip('{').lstrip()
    #             f.write(previous_user + ',' + new_user)
    #         else:
    #             # No previous users were found so only adding the new one.
    #             f.write(new_user)
    #         f.close()
    #
    #     self.parent.refreshUserAccount()
    #
    #     self.Close()
    #
    # def OnTextEnter(self, event):
    #     if not self.firstnameTextBox.GetValue or \
    #             not self.lastnameTextBox.GetValue or \
    #                     self.organizationTextBox.GetValue() == '' or \
    #                     self.phoneTextBox.GetValue() == '' or \
    #                     self.emailTextBox.GetValue() == '' or \
    #                     self.addressTextBox.GetValue() == '' or \
    #                     self.startDatePicker.GetValue == '':
    #         self.okbutton.Disable()
    #     else:
    #         self.okbutton.Enable()
    #
    # def GetTextBoxValues(self):
    #     accountinfo = [self.firstnameTextBox.GetValue(), self.lastnameTextBox.GetValue(),
    #                    self.organizationTextBox.GetValue(), self.phoneTextBox.GetValue(),
    #                    self.emailTextBox.GetValue(), self.addressTextBox.GetValue(),
    #                    self.startDatePicker.GetValue()]
    #     return accountinfo
