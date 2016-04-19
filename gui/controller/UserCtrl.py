import wx
from gui.views.UserView import UserView, OrganizationView
import datetime
import os
import coordinator.users as users
import json
import uuid
import environment


class OrganizationCtrl(OrganizationView):
    def __init__(self, parent, data=None):
        OrganizationView.__init__(self,parent)
        self.parent = parent
        self.SetTitle("Organization")

        # https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_organizations.md for a list of types
        self.choices = ["Federal Agency", "State Agency", "Academic Research Group", "Academic Department", "University", "Non-Profit", "Other"]

        self.type_combo.SetItems(self.choices)
        self.load_data(data=data)
        self.accept_button.Bind(wx.EVT_BUTTON, self.on_accept)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

    def get_values(self):
        data = {
            "name": self.name_textbox.GetValue(),
            "description": self.description_textbox.GetValue(),
            "type": self.type_combo.GetValue(),
            "url": self.url_textbox.GetValue(),
            "start_date": self.start_date_picker.GetValue(),
            "phone": self.phone_textbox.GetValue(),
            "email": self.email_textbox.GetValue(),
        }
        return data

    def load_data(self, data):
        if data:
            self.name_textbox.SetValue(data["name"])
            self.description_textbox.SetValue(data["description"])
            self.type_combo.SetValue(data["type"])
            self.url_textbox.SetValue(data["url"])
            self.start_date_picker.SetValue(data["start_date"])
            self.phone_textbox.SetValue(data["phone"])
            self.email_textbox.SetValue(data["email"])
        return

    def on_accept(self, event):
        data = self.get_values()
        self.parent.organization_data[data["name"]] = data
        self.parent.refresh_organization_box()
        self.on_cancel(None)

    def on_cancel(self, event):
        self.Close()

class UserCtrl(UserView):
    def __init__(self, parent, OnStartUp = False):

        UserView.__init__(self, parent)
        self.OnStartUp = OnStartUp

        self.organization_data = {}

        # initialize bindings
        self.firstnameTextBox.Bind(wx.EVT_TEXT, self.on_text_enter)
        self.lastnameTextBox.Bind(wx.EVT_TEXT, self.on_text_enter)
        # self.organizationTextBox.Bind(wx.EVT_TEXT, self.on_text_enter)
        self.phoneTextBox.Bind(wx.EVT_TEXT, self.on_text_enter)
        self.emailTextBox.Bind(wx.EVT_TEXT, self.on_text_enter)
        self.addressTextBox.Bind(wx.EVT_TEXT, self.on_text_enter)
        self.startDatePicker.Bind(wx.EVT_TEXT, self.on_text_enter)
        self.okbutton.Bind(wx.EVT_BUTTON, self.on_ok)
        self.addOrganization.Bind(wx.EVT_BUTTON, self.add_organization_clicked)
        self.removeOrganization.Bind(wx.EVT_BUTTON, self.remove_organization_clicked)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.editOrganization.Bind(wx.EVT_BUTTON, self.on_edit)

    def add_organization_clicked(self, event):
        OrganizationCtrl(self)

    @staticmethod
    def create_user_json():
        # If path path exist do nothing else create it
        path = environment.getDefaultUsersJsonPath()
        if os.path.isfile(path):
            return
        open(path, "w")

    def datetimeToString(self, date):
        date = datetime.datetime.strptime(date.FormatISOCombined(), "%Y-%m-%dT%H:%M:%S")
        date = self.json_serial(date)
        return date

    def get_text_box_values(self):
        data = {"person": {
            "first_name": self.firstnameTextBox.GetValue(),
            "last_name": self.lastnameTextBox.GetValue(),
        }}

        organizations = []
        for key, value in self.organization_data.iteritems():
            organizations.append(value)
        data["organizations"] = organizations

        return data
        
    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime.datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

    @staticmethod
    def is_user_json_empty():
        path = environment.getDefaultUsersJsonPath()
        if os.stat(path).st_size == 0:
            return True
        return False

    def on_cancel(self, event):
        try:
            self.parent.check_users_json()
        except KeyError:
            # Parent does not have check_users_json()
        self.Close()

    def on_edit(self, event):
        index = self.organizationListBox.GetSelection()
        if index == -1:
            return
        selected = self.organizationListBox.GetString(index)
        data = self.organization_data[selected]
        OrganizationCtrl(self, data=data)

    def on_ok(self, event):
        new_data = self.get_text_box_values()
        person = users.Person(firstname=new_data["person"]["first_name"], lastname=new_data["person"]["last_name"])
        organizations = []
        affilations = []
        for i in new_data["organizations"]:
            organ = users.Organization(typeCV=i["name"], name=i["name"], code=i["name"])
            start_date = datetime.datetime.strptime(i["start_date"].FormatISOCombined(), "%Y-%m-%dT%H:%M:%S")
            affil = users.Affiliation(email=i["email"], startDate=start_date, organization=organ, person=person, phone=i["phone"])
            organizations.append(organ)
            affilations.append(affil)

        user_json_filepath = os.environ['APP_USER_PATH']  # get the file path of the user.json

        with open(user_json_filepath, 'r') as f:
            try:
                previous_users = json.load(f)
            except ValueError:
                previous_users = {}

        with open(user_json_filepath, 'w') as f:
            for i in range(len(affilations)):
                new_data["organizations"][i] = affilations[i]._affilationToDict()

            data = {str(uuid.uuid4()): new_data}
            data.update(previous_users)
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ':'))
            f.close()

        self.parent.refreshUserAccount()
        self.is_alive = False
        self.Close()

    def on_text_enter(self, event):
        if self.firstnameTextBox.GetValue() \
                and self.lastnameTextBox.GetValue():
            self.okbutton.Enable()
        else:
            self.okbutton.Disable()

    def parse_organization_date(self, data):
        for i in range(len(data)):
            data["organizations"][i]["start_date"] = self.datetimeToString(data["organizations"][i]["start_date"])
        return data

    def refresh_organization_box(self):
        choices = []
        for key, value in self.organization_data.iteritems():
            choices.append(key)

        self.organizationListBox.SetItems(choices)

    def remove_organization_clicked(self, event):
        index = self.organizationListBox.GetSelection()
        if index == -1:
            return
        selected = self.organizationListBox.GetString(index)
        del self.organization_data[selected]
        self.organizationListBox.Delete(index)

    def setvalues(self, first, last, org, phone, email, address, date):
        self.firstnameTextBox = first
        self.lastnameTextBox = last
        # self.organizationTextBox = org
        self.phoneTextBox = phone
        self.emailTextBox = email
        self.addressTextBox = address
        self.startDatePicker = date
