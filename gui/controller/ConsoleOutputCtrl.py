import threading

import wx
import wx.lib.newevent

from gui.views.ConsoleView import ConsoleView
from sprint import *


class consoleCtrl(ConsoleView):

    def __init__(self, parent):
        ConsoleView.__init__(self, parent=parent)

        # todo: get the port number from the environment variables so that the user can change as necessary
        self.buf = 1024
        self.port = PrintTarget.CONSOLE  # random port number
        self.host = 'localhost'
        self.addr = (self.host, self.port)
        self.linenum = 1

        # Pop up menu
        self.popup_menu = wx.Menu()
        clear_menu = self.popup_menu.Append(1, "Clear")

        # Bindings
        self.log.Bind(wx.EVT_CONTEXT_MENU, self.on_right_click)
        self.log.Bind(wx.EVT_MENU, self.on_clear, clear_menu)

        # start the message server
        self.thread = threading.Thread(target=self.messageServer, name='MessageServer')
        self.thread.daemon = True
        self.thread.start()

        self.log.Bind(wx.EVT_TEXT, self.onMessagePrint)

    def onMessagePrint(self, event):
        """
        scrolls to the bottom of the text control everytime a message is printed
        Args:
            event: EVT_TEXT

        Returns:None

        """
        # scroll to the end of the textctrl
        lastpos = self.log.GetLastPosition()-2
        wx.CallAfter(self.log.ShowPosition, lastpos)


    def resetLineNumbers(self):
        self.linenum = 1

    def Print(self, text, type):

        #wx.CallAfter(self.log.SetInsertionPoint, 0)
        if type == 'INFO':
                wx.CallAfter(self.log.BeginTextColour, (42, 78, 110))
        elif type == 'WARNING':
            wx.CallAfter(self.log.BeginTextColour, (255, 140, 0))
        elif type =='ERROR':
            wx.CallAfter(self.log.BeginTextColour, (255, 0, 0))
        elif type == 'DEBUG':
            wx.CallAfter(self.log.BeginTextColour, (0, 0, 0))
        elif type == 'CRITICAL':
            wx.CallAfter(self.log.BeginTextColour, (170, 57, 57))

        # format the message text
        msg = '%d:  %s\n' % (self.linenum, text)

        # print the message to the console
        wx.CallAfter(self.log.WriteText, msg)
        wx.CallAfter(self.log.EndTextColour, )
        wx.CallAfter(self.log.Refresh, )

        # increment line numbers after each print
        self.linenum += 1

    def messageServer(self):

        udpsocket = socket(AF_INET, SOCK_DGRAM)
        udpsocket.bind(self.addr)

        while True:

            # receive the message from the socket
            (data, addr) = udpsocket.recvfrom(self.buf)
            type, text = data.split('|')

            # print the message in the console if the environment variable is set to True
            key = 'LOGGING_SHOW' + type.upper()
            if os.environ.has_key(key):
                if int(os.environ[key]):
                    self.Print(text, type)

    ###########################
    # EVENTS
    ###########################

    def on_clear(self, event):
        self.log.Clear()
        self.resetLineNumbers()

    def on_right_click(self, event):
        self.log.PopupMenu(self.popup_menu)