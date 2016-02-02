__author__ = 'Jacob'

import os

import wx

from gui.Resources import icons
from os.path import expanduser

ID_BUTTON = 100
ID_EXIT = 200
ID_SPLITTER = 300


class ViewDirectoryListControl(wx.ListCtrl):
    def __init__(self, parent, id, pos, size, style):
        wx.ListCtrl.__init__(self, parent=parent, id=id, size=size, pos=pos, style=style)

        currentdir = os.path.dirname(os.path.realpath(__file__))
        home = expanduser('~')
        #home = os.path.join(currentdir,'../../tests/data')
        dirpath = os.path.abspath(home)
        self.home = dirpath
        self.currentdirectory = dirpath

        images = [icons.folder_documents.GetBitmap(),
                  icons.folder.GetBitmap(),
                  icons.earth.GetBitmap(),
                  icons.GearSim.GetBitmap()]

        self.InsertColumn(0, 'Name')
        self.InsertColumn(1, 'Size', wx.LIST_FORMAT_LEFT)
        self.InsertColumn(2, 'Modified', wx.LIST_FORMAT_LEFT)

        self.SetColumnWidth(0, 150)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 150)

        self.il = wx.ImageList(22, 22)

        # resize images
        for i in images:
            if i.GetSize()[0] > 22 or i.GetSize()[1] < 22:
                image = wx.ImageFromBitmap(i)
                image.Rescale(22,22)
                i = wx.BitmapFromImage(image)

            self.il.Add(i)
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.refreshList(self.home)

