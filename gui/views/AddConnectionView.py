__author__ = 'ryan'

import wx

class AddConnectionView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, title="Add New Connection",
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        gbs = wx.GridBagSizer(vgap=5, hgap=5)

        self.title = wx.StaticText(panel, label="*Title:")
        self.title_txtctrl = wx.TextCtrl(panel, size=(150, -1))

        self.description  = wx.StaticText(panel, label="Description:")
        self.description_txtctrl = wx.TextCtrl(panel, size=(150, -1))

        self.engine = wx.StaticText(panel, label="*Engine:")
        self.engine_combo = wx.ComboBox(panel, value="---", choices=['PostgreSQL', 'MySQL', 'SQLite'], size=(150, -1))

        self.address = wx.StaticText(panel, label="*Address:")
        self.address_txtctrl = wx.TextCtrl(panel, size=(150, -1))

        self.database = wx.StaticText(panel, label="*Database:")
        self.database_txtctrl = wx.TextCtrl(panel, size=(150, -1))

        self.user = wx.StaticText(panel, -1, "*User:")
        self.user_txtctrl = wx.TextCtrl(panel, size=(150, -1))

        self.password = wx.StaticText(panel, -1, "Password:")
        self.password_txtctrl = wx.TextCtrl(panel, size=(150, -1))

        break_line = wx.StaticLine(panel)
        self.ok_btn = wx.Button(panel, label="OK")
        self.ok_btn.SetDefault()
        self.ok_btn.Disable()

        #  Required fields are set to bold
        self.title.SetFont(self.title.GetFont().MakeBold())
        self.engine.SetFont(self.engine.GetFont().MakeBold())
        self.address.SetFont(self.address.GetFont().MakeBold())
        self.database.SetFont(self.database.GetFont().MakeBold())
        self.user.SetFont(self.user.GetFont().MakeBold())

        gbs.Add(self.title, pos=(0, 0), border=2), gbs.Add(self.title_txtctrl, pos=(0, 1), border=2)
        gbs.Add(self.description, pos=(1, 0), border=2), gbs.Add(self.description_txtctrl, pos=(1, 1), border=2)
        gbs.Add(self.engine, pos=(2, 0), border=2), gbs.Add(self.engine_combo, pos=(2, 1), border=2)
        gbs.Add(self.address, pos=(3, 0), border=2), gbs.Add(self.address_txtctrl, pos=(3, 1), border=2)
        gbs.Add(self.database, pos=(4, 0), border=2), gbs.Add(self.database_txtctrl, pos=(4, 1), border=2)
        gbs.Add(self.user, pos=(5, 0), border=2), gbs.Add(self.user_txtctrl, pos=(5, 1), border=2)
        gbs.Add(self.password, pos=(6, 0), border=2), gbs.Add(self.password_txtctrl, pos=(6, 1), border=2)
        gbs.Add(break_line, pos=(7, 0), span=(1, 2), flag=wx.EXPAND | wx.TOP, border=10)
        gbs.Add(self.ok_btn, pos=(8, 1), flag=wx.ALIGN_RIGHT, border=2)

        vbox.Add(gbs, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(vbox)

        vbox.Fit(self)  # Makes the frame/panel a nice size so everything is compact

        self.Show()
