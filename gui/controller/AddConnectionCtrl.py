import wx
from wx.lib.pubsub import pub as Publisher
import environment
from emitLogging import elog
from gui.views.AddConnectionView import AddConnectionView
import os
from webservice import wateroneflow
import ConfigParser


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

        return dict(name = title,
                description = desc,
                engine=engine,
                address=address,
                database=db,
                username = user,
                password=pwd)

    ####################################
    # EVENTS
    ####################################

    def on_combo_box_change(self, event):
        if self.odm_radio.GetValue():
            print "ODM2 selected"
            self.engine_label.Enable()
            self.engine_combo.Enable()
            self.password_label.Enable()
            self.password_txt_ctrl.Enable()
            self.user_label.Enable()
            self.username_txt_ctrl.Enable()
            self.database_address_label.LabelText = "*Database Address"
            self.database_name_label.LabelText = "*Database Name"
        else:
            print "WOF selected"
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

        # Add ODM2 Connection
        if self.odm_radio.GetValue():
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
                self.Close()
                return
            else:
                wx.MessageBox('\aUnable to connect to the database. \nPlease review the information that was provided and try again.', 'Failed to Establish Connection', wx.OK | wx.ICON_ERROR)

        # Add WOF Connection
        else:
            params = self.get_connection_params()
            currentdir = os.path.dirname(os.path.abspath(__file__))
            wof_txt = os.path.abspath(os.path.join(currentdir, '../../data/wofsites'))
            valid = True
            try:
                print params[3]
                print params[4]
                self.api = wateroneflow.WaterOneFlow(params[3], params[4])
            except Exception:
                valid = False
                elog.debug("Wof web service took to long or failed.")
                elog.info("Web service took to long. Wof may be down.")
            if valid:
                cparser = ConfigParser.ConfigParser(None)
                cparser.add_section('wofconnection')
                cparser.set('wofconnection', 'name', params[0])
                cparser.set('wofconnection', 'desc', params[1])
                cparser.set('wofconnection', 'wsdl', params[3])
                cparser.set('wofconnection', 'network', params[4])
                with open(wof_txt, 'a') as configfile:
                    cparser.write(configfile)

                self.Close()
            else:
                wx.MessageBox('\aI was unable to verify the connection with the information provided\nPlease verify you have inputed the right information')

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
