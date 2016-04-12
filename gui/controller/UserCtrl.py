import wx
from gui.views.UserView import UserView, OrganizationView
import datetime
import os
import coordinator.users as users
import json



class OrganizationCtrl(OrganizationView):
    def __init__(self, parent, data=None):
        OrganizationView.__init__(self)
        self.parent = parent
        self.SetTitle("Organization")

        # https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_organizations.md for a list of types
        self.choices = ["Federal Agency", "State Agency", "Academic Research Group", "Academic Department", "University", "Non-Profit", "Other"]

        self.type_combo.SetItems(self.choices)
        self.load_data(data=data)
        self.accept_button.Bind(wx.EVT_BUTTON, self.on_accept)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

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

    def on_accept(self, event):
        data = self.get_values()
        self.parent.organization_data[data["name"]] = data
        self.parent.refresh_organization_box()
        self.on_cancel(None)

    def on_cancel(self, event):
        self.Close()

class UserCtrl(UserView):
    def __init__(self, parent):

        UserView.__init__(self, parent)

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

    def GetTextBoxValues(self):
        data = {"person": {
            "firstname": self.firstnameTextBox.GetValue(),
            "lastname": self.lastnameTextBox.GetValue(),
            "phone": self.phoneTextBox.GetValue(),
            "email": self.emailTextBox.GetValue(),
            "address": self.addressTextBox.GetValue(),
            "start_date": self.startDatePicker.GetValue()
        }}

        for key, value in self.organization_data.iteritems():
            data[key] = value

        return data

    def on_cancel(self, event):
        self.Close()

    def on_edit(self, event):
        index = self.organizationListBox.GetSelection()
        if index == -1:
            return
        selected = self.organizationListBox.GetString(index)
        data = self.organization_data[selected]
        OrganizationCtrl(self, data=data)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime.datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError ("Type not serializable")


    def on_ok(self, event):
        new_user = self.GetTextBoxValues()
        firstname = new_user["person"]["firstname"]
        lastname = new_user["person"]["lastname"]
        organization = new_user[self.organization_data.keys()[0]]["name"]
        phone = new_user["person"]["phone"]
        email = new_user["person"]["email"]
        address = new_user["person"]["address"]
        start_date = new_user["person"]["start_date"]
        #  The date needs to be converted to a datetime.datetime object
        start_date = datetime.datetime.strptime(start_date.FormatISOCombined(), "%Y-%m-%dT%H:%M:%S")

        user_json_filepath = os.environ['APP_USER_PATH']  # get the file path of the user.json
        person = users.Person(firstname=firstname, lastname=lastname)

        organ = users.Organization(typeCV=organization, name=organization, code=organization)

        affilations = [users.Affiliation(email=email, startDate=start_date,
                                         organization=organ, person=person,
                                         phone=phone, address=address)]

        new_user["person"]["start_date"] = self.parse_date(new_user["person"]["start_date"])
        new_user = self.parse_organization_date(new_user)

        with open(user_json_filepath, 'r') as f:
            try:
                previous_users = json.load(f)
            except ValueError:
                previous_users = {}

        with open(user_json_filepath, 'w') as f:
            data = {}
            data[affilations[0]._affilationToDict().keys()[0]] = new_user
            data.update(previous_users)
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ':'))
            f.close()
        self.parent.refreshUserAccount()
        self.Close()

    def on_text_enter(self, event):
        if self.firstnameTextBox.GetValue() \
                and self.lastnameTextBox.GetValue() \
                and self.phoneTextBox.GetValue()\
                and self.emailTextBox.GetValue()\
                and self.addressTextBox.GetValue()\
                and self.startDatePicker.GetValue():
            self.okbutton.Enable()
        else:
            self.okbutton.Disable()

    def parse_date(self, date):
        date = datetime.datetime.strptime(date.FormatISOCombined(), "%Y-%m-%dT%H:%M:%S")
        date = self.json_serial(date)
        return date

    def parse_organization_date(self, data):
        for key, value in self.organization_data.iteritems():
            data[key]["start_date"] = self.parse_date(data[key]["start_date"])
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
