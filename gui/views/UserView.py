
import wx

class UserView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, title="Create a User", style=wx.FRAME_FLOAT_ON_PARENT|wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        gbs = wx.GridBagSizer(vgap=5, hgap=5)

        self.firstName = wx.StaticText(panel, label="*First Name:")
        self.firstName_txtctrl = wx.TextCtrl(panel, size=(200, -1))

        self.middleName = wx.StaticText(panel, label="Middle Name:")
        self.middleName_txtctrl = wx.TextCtrl(panel, size=(200, -1))


        self.lastName = wx.StaticText(panel, label="*Last Name:")
        self.lastName_txtctrl = wx.TextCtrl(panel, size=(200, -1))

        self.Organization = wx.StaticText(panel, label="Organization")

        break_line = wx.StaticLine(panel)
        break_line_Person = wx.StaticLine(panel)
        self.ok_btn = wx.Button(panel, label="OK")
        self.ok_btn.SetDefault()
        self.ok_btn.Disable()

        #  Required fields are set to bold
        self.firstName.SetFont(self.firstName.GetFont().MakeBold())
        self.lastName.SetFont(self.lastName.GetFont().MakeBold())

        gbs.Add(self.firstName, pos=(0, 0), border=2), gbs.Add(self.firstName_txtctrl, pos=(0, 1), border=2)
        gbs.Add(self.middleName, pos=(1, 0), border=2), gbs.Add(self.middleName_txtctrl, pos=(1, 1), border=2)
        gbs.Add(self.lastName, pos=(2, 0), border=2), gbs.Add(self.lastName_txtctrl, pos=(2, 1), border=2)
        gbs.Add(break_line_Person, pos=(3, 0), span=(1, 2), flag=wx.EXPAND| wx.TOP, border=10)
        gbs.Add(break_line, pos=(7, 0), span=(1, 2), flag=wx.EXPAND | wx.TOP, border=10)
        gbs.Add(self.ok_btn, pos=(8, 1), flag=wx.ALIGN_RIGHT, border=2)

        vbox.Add(gbs, 1, wx.EXPAND | wx.ALL, 20)

        panel.SetSizer(vbox)

        vbox.Fit(self)  # Makes the frame/panel a nice size so everything is compact

        self.Show()
