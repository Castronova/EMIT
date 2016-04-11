import os
import wx
import wx.propgrid as wxpg



class settingsView(wx.Frame):

    def __init__(self):
        self.window_width = 350
        self.window_height=400
        wx.Frame.__init__(self, parent=None, id=-1, title="Settings...", pos=wx.DefaultPosition, size=wx.Size(self.window_width, self.window_height), style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        console_title = wx.StaticText(self.panel, id=wx.ID_ANY, label="Configure Console Verbosity",pos=(20, 100))
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        console_title.SetFont(font)


        # self.PropertyGrid = MyPropertyGrid(self.panel, id=wx.ID_ANY,
        #                                        pos=wx.Point(0, 0),
        #                                        size=wx.Size(self.window_width-25,  # slightly less than the window width
        #                                                     self.window_height-75) # make room for buttons at bottom
        #                                    )


        self.c1 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Info Messages")
        self.c2 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Warning Messages")
        self.c3 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Critical Messages")
        self.c4 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Error Messages")
        self.c5 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Debug Messages")

        self.c1.SetValue(int(os.environ['LOGGING_SHOWINFO']))
        self.c2.SetValue(int(os.environ['LOGGING_SHOWWARNING']))
        self.c3.SetValue(int(os.environ['LOGGING_SHOWCRITICAL']))
        self.c4.SetValue(int(os.environ['LOGGING_SHOWERROR']))
        self.c5.SetValue(int(os.environ['LOGGING_SHOWDEBUG']))

        self.saveButton = wx.Button(self.panel, 1, 'Save')

        sizer.Add(console_title, .1, flag=wx.ALL | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c1, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c2, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c3, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c4, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c5, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.saveButton, 1, flag=wx.RIGHT | wx.ALIGN_RIGHT, border=20)


        self.panel.SetSizer(sizer)
        self.Layout()
        self.Refresh()
        self.Show()


class MyPropertyGrid(wx.propgrid.PropertyGrid):
    def __init__(self, *args, **kwargs):
        wxpg.PropertyGrid.__init__(self, *args, **kwargs)

        self.Bind(wx.EVT_LEFT_DOWN, self.onClick)
        self.Bind(wx.EVT_LEFT_DCLICK, self.onClick)

    def onClick(self, event):
        """
        event handler for property grid click.  This function makes the property grid fields uneditable
        Returns: None

        """
        pass