import wx
import wx.aui
import wx.xrc

import environment
from coordinator import engineManager
from gui.controller.EMITCtrl import EMITCtrl
import os

class EMITApp(wx.App):
    def OnInit(self):

        # load environment variables
        environment.getEnvironmentVars()

        # Don't delete this line, instantiating the Borg Engine main thread here
        engine = engineManager.Engine()

        # We are terminating dependency logging errors, We may want this in the future but it
        # tends to add clutter to our console.
        wx.Log.SetLogLevel(0)

        self.logicEmit = EMITCtrl(None)
        return True

if __name__ == '__main__':

    userPath = os.getcwd() + '/app_data/config/user.json'
    if os.environ.has_key('APP_USER_PATH') == False:
        os.environ['APP_USER_PATH'] = userPath
    app = EMITApp()
    app.MainLoop()

