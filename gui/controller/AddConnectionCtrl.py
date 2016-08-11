import wx
from wx.lib.pubsub import pub as Publisher
from gui.views.AddConnectionView import AddConnectionView
from webservice import wateroneflow
import json
from sprint import *
import time


class AddConnectionCtrl(AddConnectionView):
    def __init__(self, parent):
        AddConnectionView.__init__(self, parent)

        self.database_address_txt_ctrl.Bind(wx.EVT_TEXT, self.on_text_entered)
        self.database_name_txt_ctrl.Bind(wx.EVT_TEXT, self.on_text_entered)
        self.username_txt_ctrl.Bind(wx.EVT_TEXT, self.on_text_entered)
        self.connection_name_txt_ctrl.Bind(wx.EVT_TEXT, self.on_text_entered)
        self.ok_btn.Bind(wx.EVT_BUTTON, self.on_ok_btn)
        self.engine_combo.Bind(wx.EVT_COMBOBOX, self.on_drop_box_change)
        self.wof_radio.Bind(wx.EVT_RADIOBUTTON, self.on_combo_box_change)
        self.odm_radio.Bind(wx.EVT_RADIOBUTTON, self.on_combo_box_change)

    def get_connection_params(self):
        title = self.connection_name_txt_ctrl.GetValue()
        desc = self.description_txt_ctrl.GetValue()
        engine = self.engine_combo.GetValue().lower()
        address = self.database_address_txt_ctrl.GetValue()
        db = self.database_name_txt_ctrl.GetValue()
        user = self.username_txt_ctrl.GetValue()
        pwd = self.password_txt_ctrl.GetValue()

        return dict(name=title,
                    description=desc,
                    engine=engine,
                    address=address,
                    database=db,
                    username=user,
                    password=pwd)

    ####################################
    # EVENTS
    ####################################

    def on_combo_box_change(self, event):
        if self.odm_radio.GetValue():
            self.engine_label.Enable()
            self.engine_combo.Enable()
            self.password_label.Enable()
            self.password_txt_ctrl.Enable()
            self.user_label.Enable()
            self.username_txt_ctrl.Enable()
            self.database_address_label.LabelText = "*Database Address"
            self.database_name_label.LabelText = "*Database Name"
        else:
            self.engine_label.Disable()
            self.engine_combo.Disable()
            self.user_label.Disable()
            self.username_txt_ctrl.Disable()
            self.password_label.Disable()
            self.password_txt_ctrl.Disable()
            self.database_address_label.LabelText = "*WOF WSDL"
            self.database_name_label.LabelText = "*Network Code"

    def on_drop_box_change(self, event):
        if self.engine_combo.GetValue() == "MySQL" or self.engine_combo.GetValue() == "PostgreSQL":
            self.database_address_label.Enable()
            self.database_address_txt_ctrl.Enable()
            self.database_name_label.Enable()
            self.database_name_txt_ctrl.Enable()
            self.database_name_label.LabelText = "*Database:"
            self.user_label.Enable()
            self.user_label.LabelText = "*User:"
            self.password_label.Enable()
        elif self.engine_combo.GetValue() == "SQLite":
            self.user_label.Disable()
            self.username_txt_ctrl.Disable()
            self.password_label.Disable()
            self.password_txt_ctrl.Disable()
            self.database_name_label.Disable()
            self.database_name_txt_ctrl.Disable()

    def on_ok_btn(self, event):
        if self.odm_radio.GetValue():
            completed = self._handle_adding_odm2_connection()
        else:
            completed = self._handle_adding_wof_connection()

        if completed:
            self.Close()
        else:
            self.shake_frame()

    def shake_frame(self):
        position = self.GetPosition()
        for i in range(0, 5):
            time.sleep(0.1)
            if i % 2 == 0:
                self.SetPosition((position[0] + 8, position[1]))
            else:
                self.SetPosition((position[0] - 8, position[1]))

    def _handle_adding_odm2_connection(self):
        """
        Return True if the connection was successful, false otherwise
        :return:
        """
        params = self.get_connection_params()
        if environment.saveConnection(params):
            Publisher.sendMessage('DatabaseConnection',
                                  title=params['name'],
                                  desc=params['description'],
                                  dbengine=params['engine'],
                                  address=params['address'],
                                  name=params['name'],
                                  user=params['username'],
                                  pwd=params['password'])

            Publisher.sendMessage('getDatabases')
            return True
        else:
            wx.MessageBox(
                '\aUnable to connect to the database. \nPlease review the information that was provided and try again.',
                'Failed to Establish Connection', wx.OK | wx.ICON_ERROR)
            return False

    def _handle_adding_wof_connection(self):
        """
        Return True if the connection was successful, false otherwise
        :return:
        """
        params = self.get_connection_params()
        current_directory = os.path.dirname(os.path.abspath(__file__))  # rename to current_directory
        wof_path = os.path.abspath(os.path.join(current_directory, '../../app_data/dat/wofsites.json'))

        # Validate the information provided creates a connection
        api = wateroneflow.WaterOneFlow(params["address"], params["database"])
        if not api.conn:
            sPrint("Failed to establish connection. Review provided information")
            return False

        with open(wof_path, "r") as f:
            try:
                data = json.load(f)
            except ValueError:
                sPrint("_handle_adding_wof_connection() failed to parse wof_path")
                return False

        wof_site = {
            params["name"]: {
                "wsdl": params["address"],
                "network": params["database"]
            }
        }
        data.update(wof_site)

        with open(wof_path, "w") as f:
            try:
                wof_json = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
                f.write(wof_json)
            except ValueError:
                sPrint("Failed to write to file")
                return False

        return True

    def on_text_entered(self, event):
        if self.odm_radio.GetValue():
            if self.engine_combo.GetValue() == "MySQL" or self.engine_combo.GetValue() == "PostgreSQL":
                if self.database_address_txt_ctrl.GetValue() == '' or  \
                        self.database_name_txt_ctrl.GetValue() == '' or  \
                        self.username_txt_ctrl.GetValue() == '' or \
                        self.connection_name_txt_ctrl.GetValue() == '':
                    self.ok_btn.Disable()
                else:
                    self.ok_btn.Enable()
            if self.engine_combo.GetValue() == "SQLite":
                if self.database_address_txt_ctrl.GetValue() == '' or self.connection_name_txt_ctrl.GetValue() == '':
                    self.ok_btn.Disable()
                else:
                    self.ok_btn.Enable()
        else:
            if self.database_address_txt_ctrl.GetValue() == '' or \
                    self.database_name_txt_ctrl.GetValue() == '' or \
                    self.connection_name_txt_ctrl.GetValue() == '':
                self.ok_btn.Disable()
            else:
                self.ok_btn.Enable()
