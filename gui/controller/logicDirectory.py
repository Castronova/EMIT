import os
from gui.ContextMenu import DirectoryContextMenu
from gui.txtctrlModel import ModelTxtCtrl
from wx.lib.pubsub import pub as Publisher
from gui.views.viewDirectory import ViewDirectory, HomeID, PreviousID, UpID, RefreshID

__author__ = 'tonycastronova'

import wx


class LogicDirectory(ViewDirectory):
    def __init__(self, parent):

        # Initialize the View
        ViewDirectory.__init__(self, parent)

        self.initBindings()


    def initBindings(self):

        # # List control events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDClick)

        # # Toolbar events
        self.Bind(wx.EVT_TOOL, self.OnHomeClick, id=HomeID)
        self.Bind(wx.EVT_TOOL, self.OnBackClick, id=PreviousID)
        self.Bind(wx.EVT_TOOL, self.OnUpClick, id=UpID)
        self.Bind(wx.EVT_TOOL, self.OnRefresh, id=RefreshID)

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)

    def OnClick(self, event):
        dirpath = self.dirCtrl.getcurrentdirectory()
        path = os.path.join(dirpath, event.GetText())
        # print '> ', path
        self.sb.SetValue(path)


    def OnDClick(self, event):
        ## Check if clicked Item is a directory
        dirpath = os.path.join(os.getcwd(), event.GetText())
        # print "> Dirpath is a file?: ", os.path.isfile(dirpath)
        if os.path.isdir(dirpath):
            # print "> Changing path to: ", dirpath
            try:
                self.directoryStack.append(os.getcwd())
                os.chdir(dirpath)
            except Exception, e:
                self.directoryStack.append(os.getcwd())
                os.chdir('..')
                print "ERROR|", e
        elif os.path.isfile(dirpath):
            fileName, fileExtension = os.path.splitext(dirpath)
            # print "> Execute me", fileExtension
            if fileExtension == ".mdl" or fileExtension == ".sim":

                ShowModel = ModelTxtCtrl(self)
                ShowModel.Show()
                # Publisher.sendMessage('texteditpath', fileExtension=dirpath)
                Publisher.sendMessage('textsavepath', fileExtension=dirpath)

        self.dirCtrl.clearItems()


    ## Tool bar events
    def OnHomeClick(self, event):
        dirpath = self.dirCtrl.gethomepath()
        #currentdir = os.path.dirname(os.path.realpath(__file__))
        #home = os.path.join(currentdir,'../tests/data')
        #dirpath = os.path.abspath(home)

        try:
            self.directoryStack.append(dirpath)
            os.chdir(dirpath)
            # print "You have returned home: ", dirpath
            self.dirCtrl.clearItems()
        except:
            print 'ERROR | Home Not Defined'

    def OnUpClick(self, event):
        parent = os.path.abspath(os.path.join(self.dirCtrl.getcurrentdirectory(), os.pardir))

        self.directoryStack.append(parent)

        os.chdir(parent)
        self.dirCtrl.clearItems()

    def OnBackClick(self, event):
        # print 10*'-'
        # for d in self.directoryStack:
        #     print d
        if len(self.directoryStack) > 0:
            self.directoryStack.pop()
            os.chdir(self.directoryStack[-1])
            self.dirCtrl.clearItems()

    def onDrag(self, event):
        data = wx.FileDataObject()
        obj = event.GetEventObject()
        id = event.GetIndex()
        filename = obj.GetItem(id).GetText()
        dirname = self.dirCtrl.getcurrentdirectory()
        #dirname = os.path.dirname(os.path.abspath(os.listdir(".")[0]))
        fullpath = str(os.path.join(dirname, filename))

        data.AddFile(fullpath)

        dropSource = wx.DropSource(obj)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop()
       #print fullpath

    def OnRightClick(self, event):
        self.dirCtrl.PopupMenu(DirectoryContextMenu(self, event), event.GetPosition())

    def OnRefresh(self, event):
        self.dirCtrl.Refresh()