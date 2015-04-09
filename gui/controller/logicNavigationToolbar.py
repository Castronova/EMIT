__author__ = 'tonycastronova'

import wx
from gui.views.viewNavigationToolbar import ViewNavigationToolbar


class LogicNavigationToolbar(ViewNavigationToolbar):

    def __init__(self, parent, **kwargs):

        ViewNavigationToolbar.__init__(self, parent, id = wx.ID_ANY, **kwargs)
