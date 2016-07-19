from gui.views.SettingsView import SettingsView
import wx
from sprint import *  # Contains os.environ


class SettingsCtrl(SettingsView):
    def __init__(self, parent):
        SettingsView.__init__(self, parent)

        self._set_console_message_checkboxes()
        self.environment_panel.load_app_paths()
        self.SetSize((550, 400))

        self.console_button.Bind(wx.EVT_BUTTON, self.on_console)
        self.another_button.Bind(wx.EVT_BUTTON, self.on_another)
        self.environment_button.Bind(wx.EVT_BUTTON, self.on_environment)
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_close)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        self.Bind(wx.EVT_SIZE, self.on_resize)

        # Disables all other windows in the application so that the user can only interact with this window.
        self.MakeModal(True)

    def get_logging_variables(self):
        items = []
        for v in os.environ.keys():
            if v[:7] == "LOGGING":
                items.append(v)
        return items

    def save_logging_variables(self):
        environment.setEnvironmentVar("LOGGING", "showinfo", str(int(self.console_panel.info_checkbox.GetValue())))
        environment.setEnvironmentVar("LOGGING", "showwarning", str(int(self.console_panel.warning_checkbox.GetValue())))
        environment.setEnvironmentVar("LOGGING", "showcritical", str(int(self.console_panel.critical_checkbox.GetValue())))
        environment.setEnvironmentVar("LOGGING", "showdebug", str(int(self.console_panel.debug_checkbox.GetValue())))
        environment.setEnvironmentVar("LOGGING", "showerror", str(int(self.console_panel.error_checkbox.GetValue())))

    def _set_console_message_checkboxes(self):
        logging_vars = self.get_logging_variables()
        for var in logging_vars:
            message_type = var.split('SHOW')[-1]
            value = int(os.environ[var])

            if message_type == "CRITICAL":
                self.console_panel.critical_checkbox.SetValue(value)
                continue
            if message_type == "WARNING":
                self.console_panel.warning_checkbox.SetValue(value)
                continue
            if message_type == "INFO":
                self.console_panel.info_checkbox.SetValue(value)
                continue
            if message_type == "DEBUG":
                self.console_panel.debug_checkbox.SetValue(value)
                continue
            if message_type == "ERROR":
                self.console_panel.error_checkbox.SetValue(value)
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
        self.MakeModal(False)
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

    def on_resize(self, event):
        event.Skip()
        self.console_panel.SetSize(self.details_panel.GetSize())
        self.another_panel.SetSize(self.details_panel.GetSize())
        self.environment_panel.SetSize(self.details_panel.GetSize())

    def on_save(self, event):
        """
        Save all settings in all panels
        :param event:
        :return:
        """
        self.save_logging_variables()
        self.environment_panel.save_app_paths()

        sPrint("Settings saved. Restart application for the settings to take effect", MessageType.INFO)
        self.on_close(event)
