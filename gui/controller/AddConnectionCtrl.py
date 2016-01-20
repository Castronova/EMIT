import wx
from wx.lib.pubsub import pub as Publisher

from environment import ConnectionVars
from gui.views.AddConnectionView import AddConnectionView


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

        return title, desc, engine, address, db, user, pwd, title, desc
    def OnTextEnter(self, event):
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

    def onOktBtn(self, event):
        params = self.getConnectionParams()
        if self.con.Write_New_Connection(params):
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
            wx.MessageBox('\aI was unable to connect to the database with the information provided\nPlease review the information and try again.', 'Info', wx.OK | wx.ICON_ERROR)