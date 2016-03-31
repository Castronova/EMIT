import wx
from gui.views.UserView import UserView
import datetime
import os
import coordinator.users as users

class UserCtrl(UserView):
    def __init__(self, parent):

        UserView.__init__(self, parent, id=wx.ID_ANY, title="Create New User", size=wx.DefaultSize,
                          pos=wx.DefaultPosition, style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)

        # initialize bindings
        self.firstnameTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.lastnameTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.organizationTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.phoneTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.emailTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.addressTextBox.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.startDatePicker.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.okbutton.Bind(wx.EVT_BUTTON, self.onOkBtn)
        self.addOrganization.Bind(wx.EVT_BUTTON, self.add_organization_clicked)
        self.removeOrganization.Bind(wx.EVT_BUTTON, self.remove_organization_clicked)

    def add_organization_clicked(self, event):
        entry = self.organizationTextBox.GetValue()
        if entry == "" or entry.isspace():
            return  # Empty string

        self.organizationListBox.Append(entry.strip())  # Strip/remove white space

    def GetTextBoxValues(self):
        accountinfo = [self.firstnameTextBox.GetValue(), self.lastnameTextBox.GetValue(),
                       self.organizationTextBox.GetValue(), self.phoneTextBox.GetValue(),
                       self.emailTextBox.GetValue(), self.addressTextBox.GetValue(),
                       self.startDatePicker.GetValue()]
        return accountinfo

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

    def remove_organization_clicked(self, event):
        index = self.organizationListBox.GetSelection()
        if index == -1:
            return

        self.organizationListBox.Delete(index)

    def setvalues(self, first, last, org, phone, email, address, date):
        self.firstnameTextBox = first
        self.lastnameTextBox = last
        self.organizationTextBox = org
        self.phoneTextBox = phone
        self.emailTextBox = email
        self.addressTextBox = address
        self.startDatePicker = date
