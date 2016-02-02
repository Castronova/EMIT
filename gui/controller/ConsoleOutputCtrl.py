import os
import json
import threading
import time
from socket import AF_INET, SOCK_DGRAM, socket
from sprint import *
import wx
import wx.lib.newevent

import coordinator.emitLogging as l
from gui.views.ConsoleView import ConsoleView


class consoleCtrl(ConsoleView):

    def __init__(self, parent):
        ConsoleView.__init__(self, parent=parent)

        # todo: get the port number from the environment variables so that the user can change as necessary
        self.buf = 1024
        self.port = PrintTarget.CONSOLE  # random port number
        self.host = ''
        self.addr = (self.host, self.port)

        # start the message server
        self.thread = threading.Thread(target=self.messageServer, name='MessageServer')
        self.thread.daemon = True
        self.thread.start()

    def Print(self, text, type):

        wx.CallAfter(self.log.SetInsertionPoint, 0)
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
        wx.CallAfter(self.log.WriteText, text + '\n')
        wx.CallAfter(self.log.EndTextColour, )
        wx.CallAfter(self.log.Refresh, )

    def messageServer(self):

        udpsocket = socket(AF_INET, SOCK_DGRAM)
        udpsocket.bind(self.addr)

        while True:

            # receive the message from the socket
            (data, addr) = udpsocket.recvfrom(self.buf)
            type, text = data.split('|')

            # print the message in the console if the environment variable is set to True
            key = 'LOGGING_SHOW'+type.upper()
            if int(os.environ[key]):
                self.Print(text, type)