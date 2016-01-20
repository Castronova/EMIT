import glob
import os
import time

import wx

from gui.views.DirectoryListControlView import ViewDirectoryListControl


class LogicDirectoryListControl(ViewDirectoryListControl):
    def __init__(self, parent, size, style):
        ViewDirectoryListControl.__init__(self, parent, wx.ID_ANY, wx.DefaultPosition, size, style)

    def getcurrentdirectory(self, value=None):

        if value is not None:
            self.currentdirectory = value
        return self.currentdirectory

    def gethomepath(self, value=None):
        return self.home

    def refreshList(self, cwd):

        self.getcurrentdirectory(cwd)
        self.InsertStringItem(0, '..')

        types = (cwd + '/*.mdl', cwd + '/*.sim')
        filtered_files = []
        for files in types:
            filtered_files.extend(glob.glob(files))

        # get directories
        directories = [name for name in os.listdir(cwd) if os.path.isdir(os.path.join(cwd, name))]
        j = 1
        for directory in sorted(directories):
            self.InsertStringItem(j, os.path.basename(directory))
            self.SetItemImage(j, 1)

        for i in filtered_files:
            (name, ext) = os.path.splitext(i)
            size = os.path.getsize(i)
            sec = os.path.getmtime(i)
            self.InsertStringItem(j, os.path.basename(i))
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