import wx
import wx.propgrid as wxpg

import environment
from emitLogging import elog
from gui.views.settingsView import settingsView
from sprint import *


class settingsCtrl(settingsView):

    def __init__(self, parent):

        # initialize the view objects
        settingsView.__init__(self, parent)

        # populate console settings property grid
        self.settings.Append(wxpg.PropertyCategory('Console'))

        loggingvars = [v for v in os.environ.keys() if v[:7] == 'LOGGING']
        for var in loggingvars:
            messageType = var.split('SHOW')[-1]
            label = 'Display %s messages' % messageType.lower()
            value = int(os.environ[var])
            self.settings.Append(wxpg.BoolProperty(label=label, name=var, value=value))
            self.settings.SetPropertyAttribute(var, 'UseCheckbox', True)

        # add bindings
        self.Bind(wx.EVT_BUTTON, self.OnSave, id=1)

    def OnSave(self, event):

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