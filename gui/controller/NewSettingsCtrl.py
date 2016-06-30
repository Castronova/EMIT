from gui.views.NewSettingsView import NewSettingsView
import wx
from sprint import *  # Contains os.environ


class NewSettingsCtrl(NewSettingsView):
    def __init__(self, parent):
        NewSettingsView.__init__(self, parent)

        self._set_console_message_checkboxes()

        self.console_button.Bind(wx.EVT_BUTTON, self.on_console)
        self.another_button.Bind(wx.EVT_BUTTON, self.on_another)
        self.environment_button.Bind(wx.EVT_BUTTON, self.on_environment)
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)
        self.Bind(wx.EVT_SIZE, self._on_resize)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_close)

        self.SetSize((-1, 400))

        self.console_panel.SetSize(self.GetClientSizeTuple())
        self.another_panel.SetSize(self.GetClientSizeTuple())
        self.environment_panel.SetSize(self.GetClientSizeTuple())

    def get_logging_variables(self):
        items = []
        for v in os.environ.keys():
            if v[:7] == "LOGGING":
                items.append(v)
        return items

    def save_logging_variables(self):
        environment.setEnvironmentVar("LOGGING", "showinfo", str(int(self.info_text.GetValue())))
        environment.setEnvironmentVar("LOGGING", "showwarning", str(int(self.warning_text.GetValue())))
        environment.setEnvironmentVar("LOGGING", "showcritical", str(int(self.critical_text.GetValue())))
        environment.setEnvironmentVar("LOGGING", "showdebug", str(int(self.debug_text.GetValue())))
        environment.setEnvironmentVar("LOGGING", "showerror", str(int(self.error_checkbox.GetValue())))

    def _set_console_message_checkboxes(self):
        logging_vars = self.get_logging_variables()
        for var in logging_vars:
            message_type = var.split('SHOW')[-1]
            value = int(os.environ[var])

            if message_type == "CRITICAL":
                self.critical_text.SetValue(value)
                continue
            if message_type == "WARNING":
                self.warning_text.SetValue(value)
                continue
            if message_type == "INFO":
                self.info_text.SetValue(value)
                continue
            if message_type == "DEBUG":
                self.debug_text.SetValue(value)
                continue
            if message_type == "ERROR":
                self.error_checkbox.SetValue(value)
                continue

    ############################
    # EVENTS
    ############################

    def on_another(self, event):
        # Color selected
        self.another_button.SetForegroundColour(wx.WHITE)
        self.console_button.SetForegroundColour(wx.LIGHT_GREY)
        self.environment_button.SetForegroundColour(wx.LIGHT_GREY)

        # Display correct panel
        self.console_panel.Hide()
        self.another_panel.Show()
        self.environment_panel.Hide()
        self.main_sizer.Layout()

    def on_close(self, event):
        self.Destroy()

    def on_console(self, event):
        # Color selected
        self.console_button.SetForegroundColour(wx.WHITE)
        self.another_button.SetForegroundColour(wx.LIGHT_GREY)
        self.environment_button.SetForegroundColour(wx.LIGHT_GREY)

        # Display correct panel
        self.console_panel.Show()
        self.another_panel.Hide()
        self.environment_panel.Hide()
        self.main_sizer.Layout()

    def on_environment(self, event):
        # Color selected
        self.console_button.SetForegroundColour(wx.LIGHT_GREY)
        self.another_button.SetForegroundColour(wx.LIGHT_GREY)
        self.environment_button.SetForegroundColour(wx.WHITE)

        # Display correct panel
        self.console_panel.Hide()
        self.another_panel.Hide()
        self.environment_panel.Show()
        self.main_sizer.Layout()

    def _on_resize(self, event):
        event.Skip()
        self.console_panel.SetSize(self.GetClientSizeTuple())
        self.another_panel.SetSize(self.GetClientSizeTuple())
        self.environment_panel.SetSize(self.GetClientSizeTuple())

    def on_save(self, event):
        """
        Save all settings in all panels
        :param event:
        :return:
        """

        self.save_logging_variables()

        sPrint("Settings saved", MessageType.INFO)
        self.on_close(event)