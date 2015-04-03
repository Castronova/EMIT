__author__ = 'Mario'
import wx
import os
import ConfigParser
from os.path import *
import fnmatch
import wx.lib.customtreectrl as CT
import utilities
from wx.lib.pubsub import pub as Publisher
import random

# todo: refactor
from ..txtctrlModel import ModelTxtCtrl
from ..ContextMenu import TreeItemContextMenu
from ..images import icons

class ViewToolbox(wx.Panel):
    def __init__(self, parent):

        # todo: this need to be fixed/removed
        # self.__cmd = parent.__getattribute__('cmd')

        # create object to store the currently selected item's path
        self.__currently_selected_item_path = None

        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour((0,0,0))

        self.tree = CT.CustomTreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE )
        self.tree.SetBackgroundColour((255,255,255))
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])

        self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        self.mdlidx    = il.Add(icons.Earth_icon.GetBitmap())

        self.tree.SetImageList(il)
        self.il = il

        self.root = self.tree.AddRoot("Model Toolbox")






class multidict(dict):
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^'+str(self._unique)
        dict.__setitem__(self, key, val)