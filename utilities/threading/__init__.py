__author__ = 'jmeline'

from wx.lib.newevent import NewEvent

wxCreateBox, EVT_CREATE_BOX = NewEvent()

wxUpdateConsole, EVT_UPDATE_CONSOLE = NewEvent()

from threadManager import ThreadManager

