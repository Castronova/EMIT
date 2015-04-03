__author__ = 'Mario'

import wx
import sys

# todo: refactor
from ..NavToolbar import NavCanvas

sys.path.append("..")
class ViewCanvas(NavCanvas):

    def __init__(self, *args, **kwargs):
        NavCanvas.__init__(self, *args,**kwargs)



