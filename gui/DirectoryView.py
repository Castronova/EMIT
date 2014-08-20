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
from wx.lib.pubsub import pub as Publisher

from DirectoryLstCtrl import DirectoryListCtrl
from images import icons
from txtctrlModel import ModelTxtCtrl, MyTree

from ContextMenu import DirectoryContextMenu, ModelContextMenu
import utilities
from shapely import wkt

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
        border = 3
        panelSizer = wx.BoxSizer(wx.VERTICAL)
        self.toolbar = self.iconToolBar()
        panelSizer.Add(self.toolbar, 0, wx.EXPAND, border)

        listCtrlSizer = wx.BoxSizer(wx.VERTICAL)
        listCtrlSizer.SetMinSize(wx.Size(1000, 600))
        #bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.sb = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(600, -1),
                                       wx.TE_READONLY|wx.TE_CHARWRAP)
        listCtrlSizer.Add(self.sb, 0, wx.ALL | wx.EXPAND, border)
       # bSizer4.Add(self.sb, 0, wx.ALL | wx.EXPAND, border)

        #listCtrlSizer.Add(bSizer4, 1, wx.EXPAND, border)

        self.dirCtrl = DirectoryListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(1000, 400), wx.LC_REPORT)
        listCtrlSizer.Add(self.dirCtrl, 1, wx.ALL, border)

        self.directoryStack.append(self.dirCtrl.gethomepath())
        panelSizer.Add(listCtrlSizer, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, border)

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

        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.OnRightClick)

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
        dirpath = self.dirCtrl.getcurrentdirectory()
        path = os.path.join(dirpath, event.GetText())
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
            except Exception, e:
                self.directoryStack.append(os.getcwd())
                os.chdir('..')
                print "WindowsError! ", e
        elif os.path.isfile(dirpath):
            fileName, fileExtension = os.path.splitext(dirpath)
            print "Execute me", fileExtension
            if fileExtension == ".mdl" or fileExtension == ".sim":

                ShowModel = ModelTxtCtrl(self)
                ShowModel.Show()
                Publisher.sendMessage('texteditpath', fileExtension=dirpath)
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
            print "You have returned home: ", dirpath
            self.dirCtrl.clearItems()
        except:
            print 'Crap happened on the way home'

    def OnUpClick(self, event):
        parent = os.path.abspath(os.path.join(self.dirCtrl.getcurrentdirectory(), os.pardir))

        self.directoryStack.append(parent)

        os.chdir(parent)
        self.dirCtrl.clearItems()

    def OnBackClick(self, event):
        print 10*'-'
        for d in self.directoryStack:
            print d
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
        self.dirCtrl.PopupMenu(DirectoryContextMenu(self,event), event.GetPosition())


    def ShowDetails(self):

        # create the details view
        view = ModelTxtCtrl(self)


        # load the file contents
        view.PopulateEdit(self.sb.GetValue())


        # load the geometry data
        view.PopulateSpatial(self.read_geoms(self.sb.GetValue(),'input'),'input')
        view.PopulateSpatial(self.read_geoms(self.sb.GetValue(),'output'),'output')

        # show the details view
        #listview = MyTree(self)
        view.PopulateEdit(self.sb.GetValue())
        view.PopulateDetails(self.sb.GetValue())

        #listview.PopulateDetails(self.sb.GetValue())
        view.Show()


    def read_geoms(self, filepath, type):

        coords = []

        # if this is a mdl file
        if filepath.split('.')[-1] == 'mdl':

            # parse the mdl file
            dic = utilities.parse_config_without_validation(self.sb.GetValue())

            geom = []
            if type in dic:
                for input in dic[type]:

                    # return empty coord array if no elementset is defined
                    if 'elementset' not in input:
                        return []

                    eset = input['elementset']

                    # check if the value is a path
                    if os.path.dirname(eset ) != '':
                        if not os.path.isfile(eset):
                            raise Exception('Could not find file: %s'%eset)

                        geom,srs = utilities.read_shapefile(eset)

                    # otherwise it must be a wkt
                    else:
                        value = ''
                        try:
                            value = eset.strip('\'').strip('"')
                            geoms = wkt.loads(value)

                            if 'Multi' in geoms.geometryType():
                                    geom  = [g for g in geoms]
                            else:
                                geom = [geoms]

                        except:
                            raise Exception('Could not load WKT string: %s.'%value)



                # build coord list
                for g in geom:
                    if g.type == 'Polygon':
                        coords.append(list(g.boundary.coords))
                    elif g.type == 'Point':
                        coords.append(list(g.coords))
                    elif g.type == 'LineString':
                        coords.append(list(g.coords))

        return coords

        #ShowModel.Show()

