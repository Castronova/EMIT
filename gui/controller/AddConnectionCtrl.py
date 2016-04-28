import ConfigParser
import os

import wx
from wx.lib.pubsub import pub as Publisher

from emitLogging import elog
from environment import ConnectionVars
from gui.views.AddConnectionView import AddConnectionView
from webservice import wateroneflow


class AddConnectionCtrl(AddConnectionView):
    def __init__(self, parent):
        AddConnectionView.__init__(self, parent)
        self.con = ConnectionVars()

        self.address_txtctrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.database_txtctrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.user_txtctrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.title_txtctrl.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.ok_btn.Bind(wx.EVT_BUTTON, self.onOktBtn)
        self.engine_combo.Bind(wx.EVT_COMBOBOX, self.DropBoxChange)
        self.wofRadio.Bind(wx.EVT_RADIOBUTTON, self.ComboboxChange)
        self.odmRadio.Bind(wx.EVT_RADIOBUTTON, self.ComboboxChange)

    def ComboboxChange(self, event):
        if self.odmRadio.GetValue():
            print "ODM2 selected"
            self.engine.Enable()
            self.engine_combo.Enable()
            self.password.Enable()
            self.password_txtctrl.Enable()
            self.user.Enable()
            self.user_txtctrl.Enable()
            self.address.LabelText = "*Database Address"
            self.database.LabelText = "*Database Name"
        else:
            print "WOF selected"
            self.engine.Disable()
            self.engine_combo.Disable()
            self.user.Disable()
            self.user_txtctrl.Disable()
            self.password.Disable()
            self.password_txtctrl.Disable()
            self.address.LabelText = "*WOF WSDL"
            self.database.LabelText = "*Network Code"

    def DropBoxChange(self, event):
        if self.engine_combo.GetValue() == "MySQL" or self.engine_combo.GetValue() == "PostgreSQL":
            self.address.Enable()
            self.address_txtctrl.Enable()
            self.database.Enable()
            self.database_txtctrl.Enable()
            self.database.LabelText = "*Database:"
            self.user.Enable()
            self.user.LabelText = "*User:"
            self.password.Enable()
        elif self.engine_combo.GetValue() == "SQLite":
            self.user.Disable()
            self.user_txtctrl.Disable()
            self.password.Disable()
            self.password_txtctrl.Disable()
            self.database.Disable()
            self.database_txtctrl.Disable()

    def getConnectionParams(self):
        title = self.title_txtctrl.GetValue()
        desc = self.description_txtctrl.GetValue()
        engine = self.engine_combo.GetValue().lower()
        address = self.address_txtctrl.GetValue()
        db = self.database_txtctrl.GetValue()
        user = self.user_txtctrl.GetValue()
        pwd = self.password_txtctrl.GetValue()

        return dict(name = title,
                description = desc,
                engine=engine,
                address=address,
                database=db,
                username = user,
                password=pwd)

    def OnTextEnter(self, event):
        if self.odmRadio.GetValue():
            if self.engine_combo.GetValue() == "MySQL" or self.engine_combo.GetValue() == "PostgreSQL":
                if self.address_txtctrl.GetValue() == '' or  \
                        self.database_txtctrl.GetValue() == '' or  \
                        self.user_txtctrl.GetValue() == '' or \
                        self.title_txtctrl.GetValue() == '':
                    self.ok_btn.Disable()
                else:
                    self.ok_btn.Enable()
            if self.engine_combo.GetValue() == "SQLite":
                if self.address_txtctrl.GetValue() == '' or self.title_txtctrl.GetValue() == '':
                    self.ok_btn.Disable()
                else:
                    self.ok_btn.Enable()
        else:
            if self.address_txtctrl.GetValue() == '' or \
                    self.database_txtctrl.GetValue() == '' or \
                    self.title_txtctrl.GetValue() == '':
                self.ok_btn.Disable()
            else:
                self.ok_btn.Enable()

    def onOktBtn(self, event):

        # Add ODM2 Connection
        if self.odmRadio.GetValue():
            params = self.getConnectionParams()
            if self.con.saveConnection(params):
                print Publisher.sendMessage('DatabaseConnection',
                                              title=params[0],
                                              desc=params[1],
                                              dbengine=params[2],
                                              address=params[3],
                                              name=params[4],
                                              user=params[5],
                                              pwd=params[6])


                Publisher.sendMessage('getDatabases')
                self.Close()
                return
            else:
                wx.MessageBox('\aUnable to connect to the database. \nPlease review the information that was provided and try again.', 'Failed to Establish Connection', wx.OK | wx.ICON_ERROR)

        # Add WOF Connection
        else:
            params = self.getConnectionParams()
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
