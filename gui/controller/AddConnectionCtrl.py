__author__ = "ryan"
import wx
from gui.views.AddConnectionView import AddConnectionView
from environment import ConnectionVars
from wx.lib.pubsub import pub as Publisher

class AddConnectionCtrl(AddConnectionView):
    def __init__(self,parent):
        AddConnectionView.__init__(self, parent)
        print "starting"
        engine = self.engine.GetStringSelection().lower()
        self.con = ConnectionVars();

        self.address.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.name.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.user.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.title.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.btnok.Bind(wx.EVT_BUTTON, self.AddButtonHit)
        self.btn.Bind(wx.EVT_BUTTON, self.CloseHit)
        self.engine.Bind(wx.EVT_COMBOBOX, self.DropBoxChange)

    def DropBoxChange(self, event):
        print "fire away!"
        if self.engine.GetValue() is "MySQL" or self.engine.GetValue() is "PostgreSQL":
            self.address.Enable()
            #use labelTExt
            self.name.Enable()
            self.user.Enable()
        else:
            self.user.Disable()

    def CloseHit(self, event):
        self.Close()

    def getConnectionParams(self):

        #engine = self.engine.GetStringSelection().lower()

        engine = self.engine.GetValue()
        address = self.address.GetValue()
        name = self.name.GetValue()
        user = self.user.GetValue()
        pwd = self.password.GetValue()
        title = self.title.GetValue()
        desc = self.description.GetValue()

        return title,desc, engine,address,name,user,pwd,title,desc
    def OnTextEnter(self, event):

        if self.engine.GetValue() is "MySQL" or self.engine.GetValue() is "PostgreSQL":
            if self.address.GetValue() == '' or  \
                    self.name.GetValue() == '' or  \
                    self.user.GetValue() == '' or \
                    self.title.GetValue() == '':
                self.btnok.Disable()
            else:
                self.btnok.Enable()

    def AddButtonHit(self, event):
        params = self.getConnectionParams()
        if self.con.Write_New_Connection(params) :
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
            wx.MessageBox('I was unable to connect to the database with the information provided :(', 'Info', wx.OK | wx.ICON_ERROR)