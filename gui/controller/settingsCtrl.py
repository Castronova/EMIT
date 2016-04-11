
import wx
from coordinator.emitLogging import elog
from sprint import *
import environment
from gui.views.settingsView import settingsView

class settingsCtrl(settingsView):

    def __init__(self):

        settingsView.__init__(self)

        self.Bind(wx.EVT_BUTTON, self.OnSave, id=1)

    def OnSave(self, event):
        chkvalues = self.getCheckboxValue()
        infchk = int(chkvalues['info'])
        wrnchk = int(chkvalues['warn'])
        crtchk = int(chkvalues['critical'])
        debchk = int(chkvalues['debug'])
        errchk = int(chkvalues['error'])


        environment.setEnvironmentVar('LOGGING', 'showinfo', infchk)
        environment.setEnvironmentVar('LOGGING', 'showwarning', wrnchk)
        environment.setEnvironmentVar('LOGGING', 'showcritical', crtchk)
        environment.setEnvironmentVar('LOGGING', 'showdebug', debchk)
        environment.setEnvironmentVar('LOGGING', 'showerror', errchk)

        msg = 'Verbosity Settings Saved'
        elog.info(msg)
        sPrint(msg, MessageType.INFO)

        self.Close()

    def getCheckboxValue(self):
        '''
        Get the checked status for each verbosity checkbox
        :return: dictionary of Booleans, e.g {'info':True, }
        '''

        info = self.c1.GetValue()
        warn = self.c2.GetValue()
        critical = self.c3.GetValue()
        error = self.c4.GetValue()
        debug = self.c5.GetValue()
        cb = {'info': info, 'warn': warn, 'critical': critical, 'error': error, 'debug': debug}
        return cb