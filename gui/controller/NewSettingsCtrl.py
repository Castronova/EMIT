from gui.views.NewSettingsView import NewSettingsView
import wx


class NewSettingsCtrl(NewSettingsView):
    def __init__(self, parent):
        NewSettingsView.__init__(self, parent)

        self.console_button.Bind(wx.EVT_BUTTON, self.on_console)
        self.another_button.Bind(wx.EVT_BUTTON, self.on_another)
        self.Bind(wx.EVT_SIZE, self._on_resize)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_close)

        self.console_panel.SetSize(self.GetClientSizeTuple())
        self.another_panel.SetSize(self.GetClientSizeTuple())

    ############################
    # EVENTS
    ############################

    def on_another(self, event):
        self.another_button.SetForegroundColour(wx.WHITE)
        self.console_button.SetForegroundColour(wx.LIGHT_GREY)
        self.console_panel.Hide()
        self.another_panel.Show()
        self.main_sizer.Layout()
        self.another_button.SetFocus()

    def on_close(self, event):
        self.Destroy()

    def on_console(self, event):
        self.console_button.SetForegroundColour(wx.WHITE)
        self.another_button.SetForegroundColour(wx.LIGHT_GREY)
        self.console_panel.Show()
        self.another_panel.Hide()
        self.main_sizer.Layout()

    def _on_resize(self, event):
        event.Skip()
        self.console_panel.SetSize(self.GetClientSizeTuple())
        self.another_panel.SetSize(self.GetClientSizeTuple())
