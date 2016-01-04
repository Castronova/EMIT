__author__ = 'ryan'

import wx

class AddConnectionView(wx.Frame):
    def __init__(self,parent):
        wx.Frame.__init__(self, parent=parent, id=-1, title="Add New Connection", pos=wx.DefaultPosition, size=(650, 700),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        # I pulled this from the old view
        gridsizer = wx.FlexGridSizer(rows=7,cols=2,hgap=5,vgap=5)

        #titleSizer = wx.BoxSizer(wx.HORIZONTAL)
        #label = wx.StaticText(self, -1, "Database Connection")
        #titleSizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        ######################################################

        self.titlel = wx.StaticText(self, -1, "*Title :")
        self.titlel.SetFont(self.titlel.GetFont().MakeBold())
        self.titlel.SetHelpText("Title of the database connection")
        self.title = wx.TextCtrl(self, wx.ID_ANY, '', size=(200,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.titlel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.title, 0, wx.EXPAND)

        self.descriptionl = wx.StaticText(self, -1, "Description :")
        self.descriptionl.SetHelpText("Description of the database connection")
        self.description = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.descriptionl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.description, 0, wx.EXPAND)

        ######################################################


        self.enginel = wx.StaticText(self, -1, "*Engine :")
        self.enginel.SetFont(self.enginel.GetFont().MakeBold())
        self.enginel.SetHelpText("Database Parsing Engine (e.g. mysql, psycopg2, etc)")
        #self.engine = wx.TextCtrl(self, -1, "", size=(80,-1))
        engine_choices = ['PostgreSQL', 'MySQL', 'SQLite']

        self.engine = wx.ComboBox(self, value="---", size=(150, -1), choices=engine_choices)
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.enginel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.engine, 0, wx.EXPAND)


        self.addressl = wx.StaticText(self, -1, "*Address :")
        self.addressl.SetFont(self.addressl.GetFont().MakeBold())
        self.addressl.SetHelpText("Database Address")
        self.address = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.addressl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.address, 0, wx.EXPAND)

        self.namel = wx.StaticText(self, -1, "*Database :")
        self.namel.SetFont(self.namel.GetFont().MakeBold())
        self.namel.SetHelpText("Database Name")
        self.name = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.namel, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.name, 0, wx.EXPAND)

        self.userl = wx.StaticText(self, -1, "*User :")
        self.userl.SetFont(self.userl.GetFont().MakeBold())
        self.userl.SetHelpText("Database Username")
        self.user = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.userl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.user, 0, wx.EXPAND)

        self.passwordl = wx.StaticText(self, -1, "Password :")
        self.passwordl.SetHelpText("Database Password")
        self.password = wx.TextCtrl(self, -1, "", size=(80,-1))
        box = wx.BoxSizer(wx.HORIZONTAL)
        box.Add(self.passwordl, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridsizer.Add(box,0,wx.ALIGN_LEFT)
        gridsizer.Add(self.password, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.VERTICAL)
        #sizer.Add(titleSizer, 0, wx.CENTER)
        sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(gridsizer, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(wx.StaticLine(self), 0, wx.ALL|wx.EXPAND, 5)
        self.SetSizeHints(250, 300, 500, 400)


        btnsizer = wx.StdDialogButtonSizer()

        self.btnok = wx.Button(self, wx.ID_OK)#, label="Ok")
        self.btnok.Disable()

        self.btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(self.btn)
        btnsizer.AddButton(self.btnok)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

        panel = wx.Panel(self)

        self.Show()