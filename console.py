__author__ = 'tonycastronova'


import logging
import logging.config
import wx
import threading
from threading import Thread
import time

class CustomConsoleHandler(logging.StreamHandler):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, textctrl):
        """"""
        logging.StreamHandler.__init__(self)
        self.textctrl = textctrl


    #----------------------------------------------------------------------
    def emit(self, record):
        """Constructor"""
        msg = self.format(record)
        self.textctrl.WriteText(msg + "\n")
        self.flush()


class console(Thread):
    def __init__(self):
        Thread.__init__(self)




    def run(self):
        self.app = wx.App()

        f = wx.Frame(None)





        # Add a panel so it looks the correct on all platforms
        self.log = wx.TextCtrl(f, -1, size=(1000,1000),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)


        # # Add widgets to a sizer
        # sizer = wx.BoxSizer()
        # sizer.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
        # self.SetSizer(sizer)
        # self.SetSizerAndFit(sizer)



        # thread = threading.Thread(target=self.run,args=())
        # thread.daemon = True
        # thread.start()

        f.Show()
        self.run2()

        self.app.MainLoop()



    def run2(self):

        while 1:
            time.sleep(.5)
            wx.CallAfter(self.log.WriteText, str(time.clock())+'\n')


class consoleOutput(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # self.logger = logging.getLogger('wxApp')


        # Add a panel so it looks the correct on all platforms
        self.log = wx.TextCtrl(self, -1, size=(100,100),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        # txtHandler = console.CustomConsoleHandler(log)
        # self.logger.addHandler(txtHandler)

        # redir= RedirectText(log)
        # sys.stdout=redir


        # # Add widgets to a sizer
        sizer = wx.BoxSizer()
        sizer.Add(self.log, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(sizer)


        self.SetSizerAndFit(sizer)


        thread = threading.Thread(target=self.run,args=())
        thread.daemon = True
        thread.start()

    def run(self):

        while 1:
            time.sleep(.5)
            wx.CallAfter(self.log.WriteText, str(time.clock())+'\n')