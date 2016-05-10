import wx
import wx.propgrid as wxpg  # Docs http://wxpropgrid.sourceforge.net/docs/pg14/classwxPropertyGrid.htm

import environment
from emitLogging import elog
from gui.views.SettingsView import SettingsView
from sprint import *


class SettingsCtrl(SettingsView):

    def __init__(self, parent):

        # initialize the view objects
        SettingsView.__init__(self, parent)

        # populate console settings property grid
        self.append_category("Console")

        logging_vars = self.get_logging_variables()
        for var in logging_vars:
            messageType = var.split('SHOW')[-1]
            label = 'Display %s messages' % messageType.lower()
            value = int(os.environ[var])
            self.settings.Append(wxpg.BoolProperty(label=label, name=var, value=value))
            self.settings.SetPropertyAttribute(var, 'UseCheckbox', True)

        # add bindings
        self.Bind(wx.EVT_BUTTON, self.on_save, id=1)
        self.settings.FitColumns()  # Reduces column sizes to minimum possible that contents are still visible

    def append_category(self, name):
        self.settings.Append(wxpg.PropertyCategory(str(name)))

    def get_logging_variables(self):
        items = []
        for v in os.environ.keys():
            if v[:7] == "LOGGING":
                items.append(v)
        return items


    def on_save(self, event):

        props = self.settings.GetPropertyValues()

        loggingvars = [v for v in props.keys() if 'LOGGING' in v]
        for var in loggingvars:
            type = var.split('_')[-1].lower()
            value = str(int(props[var]))
            environment.setEnvironmentVar('LOGGING', type, value)

        msg = 'Settings saved'
        elog.info(msg)
        sPrint(msg, MessageType.INFO)

        self.Close()