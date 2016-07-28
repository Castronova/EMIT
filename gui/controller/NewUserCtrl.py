from gui.views.NewUserView import NewUserView
from gui.views.NewUserView import RegisterUserView
import wx
from gui.views.NewUserView import OrganizationView
import datetime
import os
import json
import coordinator.users as users


class NewUserCtrl(NewUserView):
    def __init__(self, parent):
        NewUserView.__init__(self, parent)
        self.parent = parent
        self.SetSize((500, 500))

        # Create pages
        self.page1 = RegisterUserCtrl(self.notebook)

        # Add pages to notebook
        self.notebook.AddPage(self.page1, "Register")


class RegisterUserCtrl(RegisterUserView):

    def __init__(self, parent):
        RegisterUserView.__init__(self, parent)
        self.parent = parent
        self.organization_data = {}

        # enable and disable buttons
        self.edit_organization_btn.Disable()
        self.remove_organization_btn.Disable()

        # initialize bindings
        self.first_name_text_box.Bind(wx.EVT_TEXT, self.check_save)
        self.last_name_text_box.Bind(wx.EVT_TEXT, self.check_save)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)
        self.add_organization_btn.Bind(wx.EVT_BUTTON, self.on_add_organization_button)
        self.remove_organization_btn.Bind(wx.EVT_BUTTON, self.on_remove_organization)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.edit_organization_btn.Bind(wx.EVT_BUTTON, self.on_edit)
        self.organization_list_box.Bind(wx.EVT_LISTBOX, self.on_organization_selected)

    def check_save(self, event):
        """
        Checks that the required entries are filled
        :param event:
        :return:
        """
        if self.first_name_text_box.GetValue() \
                and self.last_name_text_box.GetValue() \
                and self.organization_list_box.GetCount() > 0:
            self.ok_button.Enable()
        else:
            self.ok_button.Disable()

    def get_text_box_values(self):
        data = {"person": {
            "first_name": self.first_name_text_box.GetValue(),
            "last_name": self.last_name_text_box.GetValue(),
        }}

        organizations = []
        for key, value in self.organization_data.iteritems():
            organizations.append(value)
        data["organizations"] = organizations

        return data

    def refresh_organization_box(self):
        choices = []
        for key, value in self.organization_data.iteritems():
            choices.append(key)

        self.organization_list_box.SetItems(choices)

    def set_organization_data(self, value=None):
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
    def wxdate_to_string(date):
        date = datetime.datetime.strptime(date.FormatISOCombined(), "%Y-%m-%dT%H:%M:%S")
        date = RegisterUserCtrl.json_serial(date)
        return date

    @staticmethod
    def string_to_wxdate(datestr):
        dt = datetime.datetime.strptime(datestr, '%Y-%m-%dT%H:%M:%S')
        tt = dt.timetuple()
        dmy = (tt[2], tt[1] - 1, tt[0])
        wxDate = wx.DateTimeFromDMY(*dmy)
        return wxDate

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

    @staticmethod
    def get_existing_users():
        # Returns the content inside users.json
        # Returns {} if the file is empty or fails to load
        path = os.environ['APP_USER_PATH']
        with open(path, "r") as f:
            try:
                data = json.load(f)
            except ValueError:
                data = {}
        return data

    ###############################
    # EVENTS
    ###############################

    def on_add_organization_button(self, event):
        OrganizationCtrl(self)

    def on_cancel(self, event):
        # If no users exist it wil prompt them to add one. Clicking No will close the application
        try:
            if self.is_user_json_empty():
                message = wx.MessageDialog(None, "No users have been registered. Would you like to register a user?",
                                           "Question", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)

                message.SetYesNoLabels(yes="Register", no="Close")
                if message.ShowModal() == wx.ID_NO:
                    self.GetTopLevelParent().parent.on_close(None)
                self.GetTopLevelParent().parent.check_users_json()

        except KeyError:
            # Parent does not have check_users_json()
            pass
        self.GetTopLevelParent().Destroy()

    def on_edit(self, event):
        index = self.organization_list_box.GetSelection()
        if index == -1:
            return
        selected = self.organization_list_box.GetString(index)
        data = self.organization_data[selected]
        OrganizationCtrl(self, data=data)

    def on_organization_selected(self, event):
        # get the selection
        selection = self.organization_list_box.GetSelection()

        # enable/disable the edit and remove buttons
        if selection > -1:
            self.remove_organization_btn.Enable()
            self.edit_organization_btn.Enable()
        else:
            self.remove_organization_btn.Disable()
            self.edit_organization_btn.Disable()

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
                                            startDate=datetime.datetime.strptime(d['start_date'], '%Y-%m-%dT%H:%M:%S'),
                                            organization=organization,
                                            person=person,
                                            phone=d['phone'],
                                            address=None,
                                            isPrimaryOrganizationContact=False,
                                            affiliationEnd=None,
                                            personLink=None)

            organizations.append([organization, affiliation])

        path = os.environ['APP_USER_PATH']
        previous_users = RegisterUserCtrl.get_existing_users()

        # save the user info in a simplified way
        with open(path, 'w') as f:
            data = {}
            combined = {}
            for org in organizations:
                combined[org[0].name] = users.combine_organization_affiliation(org[0], org[1])

            data[person.get_random_id()] = {
                "person": person.__dict__,
                "organizations": combined
            }

            data.update(previous_users)
            json.dump(data, f, sort_keys=True, indent=4, separators=(',', ': '))
            f.close()

        self.GetTopLevelParent().Destroy()

    def on_remove_organization(self, event):
        index = self.organization_list_box.GetSelection()
        if index == -1:
            return
        selected = self.organization_list_box.GetString(index)
        del self.organization_data[selected]
        self.organization_list_box.Delete(index)
        self.check_save(None)


class OrganizationCtrl(OrganizationView):
    def __init__(self, parent, data=None):
        OrganizationView.__init__(self, parent)
        self.parent = parent
        self.SetTitle("Organization")

        # https://github.com/ODM2/ODM2/blob/master/doc/ODM2Docs/core_organizations.md for a list of types
        self.choices = ["Federal Agency", "State Agency", "Academic Research Group", "Academic Department", "University", "Non-Profit", "Other"]

        self.type_combo.SetItems(self.choices)
        self.load_data(data=data)
        self.accept_button.Bind(wx.EVT_BUTTON, self.on_accept)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)

    def get_values(self):
        """
        :return: the text box values
        """
        data = {
            "name": self.name_textbox.GetValue(),
            "description": self.description_textbox.GetValue(),
            "type_cv": self.type_combo.GetValue(),
            "link": self.url_textbox.GetValue(),
            "start_date": RegisterUserCtrl.wxdate_to_string(self.start_date_picker.GetValue()),
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

            wxdt = RegisterUserCtrl.string_to_wxdate(data['start_date'])
            self.start_date_picker.SetValue(wxdt)

            self.phone_textbox.SetValue(data["phone"])
            self.email_textbox.SetValue(data["email"])
        return

    ###############################
    # EVENTS
    ###############################

    def on_accept(self, event):
        data = self.get_values()
        self.parent.set_organization_data(data)
        self.parent.refresh_organization_box()
        self.parent.check_save(None)
        self.Close()

    def on_cancel(self, event):
        self.parent.check_save(None)
        self.Close()