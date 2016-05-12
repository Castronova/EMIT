import wx
from gui.views.UserView import UserView, OrganizationView
import datetime
import os
import coordinator.users as users
import json
import uuid
import environment
from wx.lib.pubsub import pub

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
            "type_cv": self.type_combo.GetValue(),
            "link": self.url_textbox.GetValue(),
            "start_date": UserCtrl.datetime_to_string(self.start_date_picker.GetValue()),
            "phone": self.phone_textbox.GetValue(),
            "email": self.email_textbox.GetValue(),
        }
        return data

    def load_data(self, data):
        if data:
            self.name_textbox.SetValue(data["name"])
            self.description_textbox.SetValue(data["description"])
            self.type_combo.SetValue(data["type_cv"])
            self.url_textbox.SetValue(data["link"])

            wxdt = UserCtrl.string_to_wxdate(data['start_date'])
            self.start_date_picker.SetValue(wxdt)

            self.phone_textbox.SetValue(data["phone"])
            self.email_textbox.SetValue(data["email"])
        return

    def on_accept(self, event):
        data = self.get_values()
        self.parent.organization(data)
        self.parent.refresh_organization_box()
        self.send_and_close()
        self.Close()

    def on_cancel(self, event):
        self.send_and_close()
        self.Close()

    def send_and_close(self):
        pub.sendMessage('OrganizationClose')


class UserCtrl(UserView):
    def __init__(self, parent):
        UserView.__init__(self, parent)

        self.organization_data = {}

        # enable and disable buttons
        self.editOrganization.Disable()
        self.removeOrganization.Disable()

        # initialize bindings
        self.firstnameTextBox.Bind(wx.EVT_TEXT, self.check_save)
        self.lastnameTextBox.Bind(wx.EVT_TEXT, self.check_save)
        # self.phoneTextBox.Bind(wx.EVT_TEXT, self.on_text_enter)
        # self.emailTextBox.Bind(wx.EVT_TEXT, self.on_text_enter)
        # self.addressTextBox.Bind(wx.EVT_TEXT, self.on_text_enter)
        # self.startDatePicker.Bind(wx.EVT_TEXT, self.on_text_enter)
        self.okbutton.Bind(wx.EVT_BUTTON, self.on_ok)
        self.addOrganization.Bind(wx.EVT_BUTTON, self.add_organization_clicked)
        self.removeOrganization.Bind(wx.EVT_BUTTON, self.remove_organization_clicked)
        self.cancelButton.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.editOrganization.Bind(wx.EVT_BUTTON, self.on_edit)
        self.organizationListBox.Bind(wx.EVT_LISTBOX, self.on_organization_selected)
        # listen to OrganizationClose messages from the OrganizationCtrl class
        pub.subscribe(self.on_organization_close, 'OrganizationClose')

    def on_organization_selected(self, event):
        # get the selection
        selection = self.organizationListBox.GetSelection()

        # enable/disable the edit and remove buttons
        if selection > -1:
            self.removeOrganization.Enable()
            self.editOrganization.Enable()
        else:
            self.removeOrganization.Disable()
            self.editOrganization.Disable()

    def on_organization_close(self):
        self.check_save(None)

    def add_organization_clicked(self, event):
        OrganizationCtrl(self)
        # self.check_save(None)

    def organization(self, value=None):
       if value is not None:
           organization_name = value['name']
           self.organization_data[organization_name] = value
       return self.organization_data


    @staticmethod
    def create_user_json():
        # If path path exist do nothing else create it
        path = os.environ['APP_USER_PATH']
        # path = environment.getDefaultUsersJsonPath()
        if os.path.isfile(path):
            return
        open(path, "w")

    @staticmethod
    def datetime_to_string(date):
        date = datetime.datetime.strptime(date.FormatISOCombined(), "%Y-%m-%dT%H:%M:%S")
        date = UserCtrl.json_serial(date)
        return date

    @staticmethod
    def string_to_wxdate(datestr):
        dt = datetime.datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
        tt = dt.timetuple()
        dmy = (tt[2], tt[1]-1, tt[0])
        wxDate = wx.DateTimeFromDMY(*dmy)
        return wxDate

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

    @staticmethod
    def json_serial(obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, datetime.datetime):
            serial = obj.isoformat()
            return serial
        raise TypeError("Type not serializable")

    @staticmethod
    def is_user_json_empty():
        # path = environment.getDefaultUsersJsonPath()
        path = os.environ['APP_USER_PATH']
        if os.stat(path).st_size == 0:
            return True
        return False

    def on_cancel(self, event):
        # If no users exist it wil prompt them to add one. Clicking No will close the application
        try:
            if self.is_user_json_empty():
                message = wx.MessageDialog(None, "No users have been registered. Would you like to register a user?", "Question", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
                if message.ShowModal() == wx.ID_NO:
                    self.parent.on_close(None)
                self.parent.check_users_json()
        except KeyError:
            # Parent does not have check_users_json()
            pass
        self.Close()

    def check_users_json(self):
        UserCtrl.create_user_json()
        if UserCtrl.is_user_json_empty():
            controller = UserCtrl(self)
            controller.CenterOnScreen()
            controller.Show()

    def on_edit(self, event):
        index = self.organizationListBox.GetSelection()
        if index == -1:
            return
        selected = self.organizationListBox.GetString(index)
        data = self.organization_data[selected]
        OrganizationCtrl(self, data=data)


    @staticmethod
    def get_json_from_users_json_file():
        # Returns the content inside users.json
        # Returns empty {} of the file is empty or fails to load
        path = os.environ['APP_USER_PATH']
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except ValueError:
                data = {}
        return data

    def combine_organizaton_affiliation(self, organization, affiliation):
        """
        Joins Organization Objects dictionaries into a single object
        Args:
            organization: Organization Object
            affiliation: Affiliation Object

        Returns: dictionary of all organization and affiliation members

        """

        # get class members for organization and affiliation
        orgmembers = organization.__dict__
        affmembers = affiliation.toSerializableDict()

        temp = orgmembers.copy()
        temp.update(affmembers)
        return temp

    def on_ok(self, event):
        new_data = self.get_text_box_values()
        person = users.Person(first=new_data["person"]["first_name"], last=new_data["person"]["last_name"])

        # build a list of organizations and affiliations
        organizations = []
        for d in new_data["organizations"]:
            organization = users.Organization(typeCV=d['type_cv'],
                                              name=d['name'],
                                              code=d['name'],
                                              description=d['description'],
                                              link=d['link'],
                                              parent=None)

            affiliation = users.Affiliation(email=d['email'],
                                            startDate=datetime.datetime.strptime(d['start_date'],'%Y-%m-%dT%H:%M:%S'),
                                            organization=organization,
                                            person=person,
                                            phone=d['phone'],
                                            address=None,
                                            isPrimaryOrganizationContact=False,
                                            affiliationEnd=None,
                                            personLink=None)

            organizations.append([organization, affiliation])


        path = os.environ['APP_USER_PATH']
        previous_users = UserCtrl.get_json_from_users_json_file()

        # save the userinfo in a simplified way
        with open(path, 'w') as f:
            data  = {}
            combined = {}
            for org in organizations:
                combined[org[0].name] = self.combine_organizaton_affiliation(org[0], org[1])

            data[person.get_random_id()] = {
                    "person": person.__dict__,
                    "organizations": combined,
                }

            data.update(previous_users)
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.close()

        self.parent.refresh_user_account()
        self.Close()

    def check_save(self, event):
        if self.firstnameTextBox.GetValue() \
                and self.lastnameTextBox.GetValue() \
                and self.organizationListBox.GetCount() > 0:
            self.okbutton.Enable()
        else:
            self.okbutton.Disable()

    def parse_organization_date(self, data):
        for i in range(len(data)):
            data["organizations"][i]["start_date"] = self.datetime_to_string(data["organizations"][i]["start_date"])
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

    @staticmethod
    def users_json_file_to_object():



        # Converts the data in users.json to objects
        data = UserCtrl.get_json_from_users_json_file()
        users_dict = {}

        for key, value in data.iteritems():
            organizations_object = []
            organizations = value["organizations"]
            for organ in organizations:
                o = users.Organization(organ["name"])
                o.set_data(organ)
                o.store_date_as_object(o.start_date)
                organizations_object.append(o)

            person = value["person"]
            p = users.Person(person["first_name"], person["last_name"])
            users_dict[p] = organizations_object

        return users_dict

