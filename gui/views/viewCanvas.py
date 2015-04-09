__author__ = 'Mario'

import wx
import sys
from gui.controller.logicNavigationToolbar import LogicNavigationToolbar

# todo: refactor

# sys.path.append("..")
class ViewCanvas(LogicNavigationToolbar):

    def __init__(self, *args, **kwargs):

        LogicNavigationToolbar.__init__(self, *args, **kwargs)


