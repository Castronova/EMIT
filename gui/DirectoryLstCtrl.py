__author__ = 'Jacob'

import os
import time

import wx

from images import icons


ID_BUTTON = 100
ID_EXIT = 200
ID_SPLITTER = 300


class DirectoryListCtrl(wx.ListCtrl):
    def __init__(self, parent, id, pos, size, style):
        wx.ListCtrl.__init__(self, parent=parent, id=id, size=size, pos=pos, style=style)

        files = os.listdir('.')
        self.home = os.path.abspath("C:\\")


        #e = icons.earth

        '''
        wxImage image = bmp.ConvertToImage();
        bmp = wxBitmap(image.Scale(32, 32));
        // another possibility:
        image.Rescale(32, 32);
        bmp = image;
        '''

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
        self.refreshList(files)

    def refreshList(self, files):
        j = 1
        self.InsertStringItem(0, '..')
        #self.SetItemImage(0, 5)

        for i in files:
            (name, ext) = os.path.splitext(i)
            #ex = ext[1:]
            size = os.path.getsize(i)
            sec = os.path.getmtime(i)
            self.InsertStringItem(j, i)
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
        self.refreshList(os.listdir('.'))
        self.selectedFiles = os.listdir('.')