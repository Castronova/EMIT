import wx
import wx.lib.agw.hyperlink as hyperlink


class AboutView(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        panel = wx.Panel(self)
        content_panel = wx.Panel(panel)
        lower_panel = wx.Panel(panel)

        #############################
        # Content Panel
        #############################

        self.png = wx.StaticBitmap(content_panel)
        self.name_static_text = wx.StaticText(content_panel)
        self.description_text = wx.StaticText(content_panel)
        self.contributors_static_text = wx.StaticText(content_panel)
        self.website_hyperlink = hyperlink.HyperLinkCtrl(content_panel)

        content_sizer = wx.BoxSizer(wx.VERTICAL)
        content_sizer.Add(self.png, 0, wx.ALL | wx.ALIGN_CENTER, border=10)
        content_sizer.Add(self.name_static_text, 0, wx.ALL | wx.ALIGN_CENTER, border=5)
        content_sizer.Add(self.description_text, 1, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, border=24)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.contributors_static_text, 1, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, border=24)
        sizer.Add(self.website_hyperlink, 1, wx.LEFT | wx.RIGHT | wx.ALIGN_CENTER, border=24)
        content_sizer.Add(sizer, 0, wx.ALL | wx.ALIGN_CENTER)

        content_panel.SetSizer(content_sizer)

        #############################
        # Lower Panel
        #############################

        self.license_static_text = wx.StaticText(lower_panel)

        lower_panel_sizer = wx.BoxSizer(wx.VERTICAL)
        lower_panel_sizer.Add(self.license_static_text, 0, wx.ALL | wx.ALIGN_CENTER ^ wx.TOP, border=5)

        lower_panel.SetSizer(lower_panel_sizer)

        #############################
        # Connecting all the panels together
        #############################

        self.frame_sizer = wx.BoxSizer(wx.VERTICAL)
        self.frame_sizer.Add(content_panel, 1, wx.EXPAND)
        self.frame_sizer.Add(lower_panel, 0, wx.EXPAND | wx.ALL)
        panel.SetSizer(self.frame_sizer)



