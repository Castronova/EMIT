__author__ = 'Jacob'

import os
import time

import wx

from images import icons

import glob


ID_BUTTON = 100
ID_EXIT = 200
ID_SPLITTER = 300


class DirectoryListCtrl(wx.ListCtrl):
    def __init__(self, parent, id, pos, size, style):
        wx.ListCtrl.__init__(self, parent=parent, id=id, size=size, pos=pos, style=style)

        currentdir = os.path.dirname(os.path.realpath(__file__))
        home = os.path.join(currentdir,'../tests/data')
        dirpath = os.path.abspath(home)
        self.home = dirpath
        self.currentdirectory = dirpath
        files = os.listdir(dirpath)
        # types = (dirpath+'/*.mdl',dirpath+'/*.sim')
        # files = []
        # for f in types:
        #     files.extend(glob.glob(f))

        images = [icons.folder_documents.GetBitmap(),
                  icons.folder.GetBitmap(),
                  icons.earth.GetBitmap(),
                  icons.GearSim.GetBitmap()]
        # # , 'images/source_py.png', 'images/image.png', 'images/pdf.png', 'images/up16.png'

        self.InsertColumn(0, 'Name')
        #self.InsertColumn(1, 'Ext', wx.LIST_FORMAT_LEFT)
        self.InsertColumn(1, 'Size', wx.LIST_FORMAT_LEFT)
        self.InsertColumn(2, 'Modified', wx.LIST_FORMAT_LEFT)

        self.SetColumnWidth(0, 150)
        #self.SetColumnWidth(1, 40)
        self.SetColumnWidth(1, 70)
        self.SetColumnWidth(2, 150)

        self.il = wx.ImageList(22, 22)
        #self.il = wx.ImageList(256, 256)
        for i in images:
            if i.GetSize()[0] > 22 or i.GetSize()[1] < 22:
                # need to resize
                image = wx.ImageFromBitmap(i)
                rescaled = image.Rescale(22,22)
                i = wx.BitmapFromImage(image)

            self.il.Add(i)
        self.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        self.refreshList(self.home)

    def getcurrentdirectory(self, value=None):

        if value is not None:
            self.currentdirectory=value
        return self.currentdirectory

    def gethomepath(self, value=None):

        return self.home


    def refreshList(self,cwd):

        self.getcurrentdirectory(cwd)
        print 'Current Working Directory - ', cwd

        j = 1
        self.InsertStringItem(0, '..')
        #self.SetItemImage(0, 5)

        types = (cwd+'/*.mdl',cwd+'/*.sim')
        filtered_files = []
        for files in types:
            filtered_files.extend(glob.glob(files))


        # get directories
        #directories = [x[0] for x in os.walk(cwd)]
        directories = [ name for name in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, name)) ]

        for directory in sorted(directories):
            size = ''
            sec = ''
            self.InsertStringItem(j, os.path.basename(directory))
            #self.SetStringItem(j, 1, str(size) + ' B')
            #self.SetStringItem(j, 2, time.strftime('%Y-%m-%d %H:%M', time.localtime(sec)))
            self.SetItemImage(j, 1)

        for i in filtered_files:
            (name, ext) = os.path.splitext(i)
            #ex = ext[1:]
            size = os.path.getsize(i)
            sec = os.path.getmtime(i)
            self.InsertStringItem(j, os.path.basename(i))
            #self.SetStringItem(j, 1, ex)
            self.SetStringItem(j, 1, str(size) + ' B')
            self.SetStringItem(j, 2, time.strftime('%Y-%m-%d %H:%M', time.localtime(sec)))

            if os.path.isdir(i):
                self.SetItemImage(j, 1)

            elif ext == '.mdl':
                self.SetItemImage(j, 2)

            elif ext == '.sim':
                self.SetItemImage(j, 3)

            elif ext == '.py':
                self.SetItemImage(j, 3)

            else:
                self.SetItemImage(j, 0)

            if (j % 2) == 0:
                self.SetItemBackgroundColour(j, '#e6f1f5')
            j = j + 1

    def clearItems(self):
        self.DeleteAllItems()
        self.refreshList(os.getcwd())
        self.selectedFiles = os.listdir(os.getcwd())