from utilities.threading import wxUpdateConsole

__author__ = 'jmeline'

import wx

from utilities.threading.baseThread import BaseThread

class CommunicatorThread(BaseThread):
    def __init__(self, dispatcher):
        BaseThread.__init__(self)
        self.dispatcher = dispatcher

    def run(self):
        while self.signal:
            output = self.dispatcher.getOutput()
            evt = wxUpdateConsole()
            evt.message = output
            wx.PostEvent(wx.GetApp().frame, evt)
            self.dispatcher.getOutputQueue().task_done()

    def stop(self):
        self.onStop()

        if self.isAlive():
            self.join(.5)





