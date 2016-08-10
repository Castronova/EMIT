from gui.views.SettingsView import SettingsView
import wx
from gui.views.SettingsView import SettingsDatabaseView
from gui.Models.Connection import *


class SettingsCtrl(SettingsView):
    def __init__(self, parent):
        SettingsView.__init__(self, parent)

        self.menu_buttons = [self.console_button, self.database_button, self.environment_button]
        self.selected_font = wx.Font(pointSize=15, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)
        self.non_selected_font = wx.Font(pointSize=12, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)

        # Add panels to the settings overall view
        self.database_panel = SettingsDatabaseCtrl(self.details_panel)
        self.database_panel.Hide()

        self._set_console_message_checkboxes()
        self.environment_panel.load_app_paths()
        self.SetSize((550, 400))

        self._resize_all_panels()
        self._update_menu_button(0)

        self.console_button.Bind(wx.EVT_BUTTON, self.on_console)
        self.database_button.Bind(wx.EVT_BUTTON, self.on_another)
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
        self._update_menu_button(1)

        # Display correct panel
        self.console_panel.Hide()
        self.database_panel.Show()
        self.environment_panel.Hide()
        self.main_sizer.Layout()

    def on_close(self, event):
        self.MakeModal(False)
        self.Destroy()

    def _update_menu_button(self, index):
        if not isinstance(index, int):
            return

        for i in range(len(self.menu_buttons)):
            if i == index:
                self.menu_buttons[i].Font = self.selected_font
                self.menu_buttons[i].SetForegroundColour(wx.WHITE)
            else:
                self.menu_buttons[i].Font = self.non_selected_font
                self.menu_buttons[i].SetForegroundColour(wx.LIGHT_GREY)

    def on_console(self, event):
        self._update_menu_button(0)

        # Display correct panel
        self.console_panel.Show()
        self.database_panel.Hide()
        self.environment_panel.Hide()
        self.main_sizer.Layout()

    def on_environment(self, event):
        self._update_menu_button(2)

        # Display correct panel
        self.console_panel.Hide()
        self.database_panel.Hide()
        self.environment_panel.Show()
        self.main_sizer.Layout()

    def on_resize(self, event):
        event.Skip()
        self._resize_all_panels()

    def _resize_all_panels(self):
        self.console_panel.SetSize(self.details_panel.GetSize())
        self.database_panel.SetSize(self.details_panel.GetSize())
        self.environment_panel.SetSize(self.details_panel.GetSize())

    def on_save(self, event):
        """
        Save all settings in all panels
        :param event:
        :return:
        """
        self.save_logging_variables()
        self.environment_panel.save_app_paths()
        self.database_panel.save_table_content()

        sPrint("Settings saved. Restart application for the settings to take effect", MessageType.INFO)
        self.on_close(event)


class SettingsDatabaseCtrl(SettingsDatabaseView):
    def __init__(self, parent):
        SettingsDatabaseView.__init__(self, parent)
        columns = ["Title", "Network Code", "Url"]
        self.table.set_columns(columns)

        self.wof_sites = get_wof_json_as_list()
        self.table.set_table_content(self.wof_sites)

        self.table.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.on_table_right_click)
        self.Bind(wx.EVT_MENU, self.on_remove_menu, self.remove_menu)

    def save_table_content(self):
        data = {}
        for row in self.wof_sites:
            data[row[0]] = {
                "network": row[1],
                "wsdl": row[2]
            }

        path = get_wof_json_path()
        with open(path, "w") as f:
            try:
                wof_json = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
                f.write(wof_json)
            except ValueError:
                sPrint("Failed to write to file")
                return

    #############################
    # EVENTS
    #############################

    def on_remove_menu(self, event):
        if not self.table.get_selected_row() in self.wof_sites:
            raise Exception("SettingDatabaseCtrl.handle_remove() failed to find selected row")

        self.wof_sites.remove(self.table.get_selected_row())
        self.table.remove_selected_row()

    def on_table_right_click(self, event):
        self.PopupMenu(self.popup_menu)

