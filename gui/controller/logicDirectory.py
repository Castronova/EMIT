__author__ = 'tonycastronova'


import os
from gui.views.viewDirectory import ViewDirectory, HomeID, PreviousID, UpID, RefreshID
from gui.views.viewContext import DirectoryContextMenu
from gui.views.viewModel import ViewModel
from gui.controller.logicModel import LogicModel
from wx.lib.pubsub import pub as Publisher
import wx
from coordinator.emitLogging import elog


class LogicDirectory(ViewDirectory):
    def __init__(self, parent):

        # Initialize the View
        ViewDirectory.__init__(self, parent)

        self.initBindings()


    def initBindings(self):

        # List control events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDClick)

        # Toolbar events
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
        # Check if clicked Item is a directory
        dirpath = os.path.join(os.getcwd(), event.GetText())
        if os.path.isdir(dirpath):

            try:
                self.directoryStack.append(os.getcwd())
                os.chdir(dirpath)

            except Exception, e:
                self.directoryStack.append(os.getcwd())
                os.chdir('..')
                elog.error("ERROR|", e)

        elif os.path.isfile(dirpath):

            fileName, fileExtension = os.path.splitext(dirpath)
            if fileExtension == ".mdl" or fileExtension == ".sim":

                # hack:  Should I be calling Logic instead of View???
                model_details = LogicModel(self)
                model_details.Show()
                # ShowModel = ViewModel(self)
                # ShowModel.Show()

                Publisher.sendMessage('textsavepath', fileExtension=dirpath)

        self.dirCtrl.clearItems()


    ## Tool bar events
    def OnHomeClick(self, event):
        dirpath = self.dirCtrl.gethomepath()

        try:
            self.directoryStack.append(dirpath)
            os.chdir(dirpath)
            # print "You have returned home: ", dirpath
            self.dirCtrl.clearItems()
        except:
            elog.error('ERROR | Home Not Defined')

    def OnUpClick(self, event):
        parent = os.path.abspath(os.path.join(self.dirCtrl.getcurrentdirectory(), os.pardir))

        self.directoryStack.append(parent)

        os.chdir(parent)
        self.dirCtrl.clearItems()

    def OnBackClick(self, event):
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
        fullpath = str(os.path.join(dirname, filename))

        data.AddFile(fullpath)

        dropSource = wx.DropSource(obj)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop()

    def OnRightClick(self, event):
        self.dirCtrl.PopupMenu(DirectoryContextMenu(self, event), event.GetPosition())

    def OnRefresh(self, event):
        self.dirCtrl.Refresh()