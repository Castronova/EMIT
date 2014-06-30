# -*- coding: utf-8 -*- 

# ##########################################################################
# # Python code generated with wxFormBuilder (version Jun  5 2014)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import os

import wx
import wx.xrc

from DirectoryLstCtrl import DirectoryListCtrl
from images import icons
from wx.lib.pubsub import pub as Publisher


###########################################################################
## Class directoryCtrlPanel
###########################################################################
[PreviousID, UpID, HomeID, SaveID, RefreshID, TerminalID, HelpID] = [wx.NewId() for _init_ctrls in range(7)]


class DirectoryCtrlView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300),
                          style=wx.TAB_TRAVERSAL)
        self.directoryStack = []
        self.initInterface()
        self.initBindings()

    def initInterface(self):
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = self.iconToolBar()
        panelSizer.Add(self.toolbar, 0, wx.EXPAND, 5)

        listCtrlSizer = wx.BoxSizer(wx.VERTICAL)

        listCtrlSizer.SetMinSize(wx.Size(800, 600))
        self.dirCtrl = DirectoryListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(1000, 400), wx.LC_REPORT)
        listCtrlSizer.Add(self.dirCtrl, 0, wx.ALL, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.sb = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(600, -1),
                                       wx.TE_READONLY)
        bSizer4.Add(self.sb, 0, wx.ALL, 5)

        listCtrlSizer.Add(bSizer4, 1, wx.EXPAND, 5)

        panelSizer.Add(listCtrlSizer, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.SetSizer(panelSizer)
        self.Layout()

        self.sb.SetValue(os.getcwd())

    def initBindings(self):
        # # List control events
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnClick)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnDClick)

        # # Toolbar events
        self.Bind(wx.EVT_TOOL, self.OnHomeClick, id=HomeID)
        self.Bind(wx.EVT_TOOL, self.OnBackClick, id=PreviousID)
        self.Bind(wx.EVT_TOOL, self.OnUpClick, id=UpID)

        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)

    def iconToolBar(self):
        toolbar = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        toolbar.AddSeparator()

        tool = toolbar.AddLabelTool(PreviousID, label='Previous', bitmap=icons.go_previous.GetBitmap())
        tool = toolbar.AddLabelTool(UpID, label='Up one directory', bitmap=icons.go_up.GetBitmap())
        tool = toolbar.AddLabelTool(HomeID, label='Go Home', bitmap=icons.go_home.GetBitmap())
        tool = toolbar.AddLabelTool(RefreshID, label='Refresh', bitmap=icons.view_refresh.GetBitmap())
        tool = toolbar.AddLabelTool(SaveID, label='Save', bitmap=icons.document_save.GetBitmap())
        tool = toolbar.AddLabelTool(TerminalID, label='Terminal', bitmap=icons.draw_star.GetBitmap())
        tool = toolbar.AddLabelTool(HelpID, label='Help', bitmap=icons.help_info.GetBitmap())

        toolbar.AddSeparator()
        toolbar.Realize()
        return toolbar

    def OnExit(self, e):
        self.Close(True)

    def OnClick(self, event):
        path = os.path.join(os.getcwd(), event.GetText())
        print path
        self.sb.SetValue(path)


    def OnDClick(self, event):
        ## Check if clicked Item is a directory
        dirpath = os.path.join(os.getcwd(), event.GetText())
        print "Dirpath is a file?: ", os.path.isfile(dirpath)
        if os.path.isdir(dirpath):
            print "Changing path to: ", dirpath
            try:
                self.directoryStack.append(os.getcwd())
                os.chdir(dirpath)
            except WindowsError as e:
                self.directoryStack.append(os.getcwd())
                os.chdir('..')
                print "WindowsError! ", e
        elif os.path.isfile(dirpath):
            fileName, fileExtension = os.path.splitext(dirpath)
            print "Execute me", fileExtension
            if fileExtension == ".txt" or fileExtension == ".py":
                Publisher.sendMessage('createBox', filepath=dirpath)

        self.dirCtrl.clearItems()


    ## Tool bar events
    def OnHomeClick(self, event):
        dirpath = os.path.abspath("C:\\")
        try:
            self.directoryStack.append(os.getcwd())
            os.chdir(dirpath)
            print "You have returned home: ", dirpath
            self.dirCtrl.clearItems()
        except:
            print 'Crap happened on the way home'

    def OnUpClick(self, event):
        self.directoryStack.append(os.getcwd())
        os.chdir(os.pardir)
        self.dirCtrl.clearItems()

    def OnBackClick(self, event):
        print "directory Stack: ", self.directoryStack
        if len(self.directoryStack) > 0:
            os.chdir(self.directoryStack.pop())
            self.dirCtrl.clearItems()

    def onDrag(self, event):
        data = wx.FileDataObject()
        obj = event.GetEventObject()
        id = event.GetIndex()
        filename = obj.GetItem(id).GetText()
        dirname = os.path.dirname(os.path.abspath(os.listdir(".")[0]))
        fullpath = str(os.path.join(dirname, filename))

        data.AddFile(fullpath)

        dropSource = wx.DropSource(obj)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop()
       #print fullpath
