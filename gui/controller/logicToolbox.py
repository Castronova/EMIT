import os
import random

__author__ = 'tonycastronova'

from gui.views.viewToolbox import ViewToolbox
from gui.views.viewContext import ToolboxContextMenu
from gui.controller.logicModel import LogicModel

import wx
from wx.lib.pubsub import pub as Publisher
from os.path import join,dirname, abspath
import ConfigParser
import fnmatch

# todo: refactor
from gui.views.viewModel import ViewModel

class LogicToolbox(ViewToolbox):

    modelpaths = ""

    def initBinding(self):
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnItemContextMenu)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.onDrag)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onDoubleClick)

    def loadToolbox(self, modelpaths):
        count = 0
        for category, data in modelpaths.iteritems():
            txt = category
            self.cat = self.tree.AppendItem(self.root, txt)
            if count == 0:
                self.simCategory = self.tree.AppendItem(self.root, 'Sim Files')
                self.tree.SetItemImage(self.simCategory, self.folderConfigIcon, which=wx.TreeItemIcon_Expanded)
                self.tree.SetItemImage(self.simCategory, self.folderConfigIcon, which=wx.TreeItemIcon_Normal)
                count += 1
            self.tree.SetItemImage(self.cat, self.fldropenidx, which=wx.TreeItemIcon_Expanded)
            self.tree.SetItemImage(self.cat, self.fldropenidx, which=wx.TreeItemIcon_Normal)
            for d in data:
                path = d['path']
                apath = join(dirname(abspath(__file__)), '../' + path)
                matches = []
                self.dirlist = []
                for root, dirnames, filenames in os.walk(apath):
                    for filename in fnmatch.filter(filenames, '*.mdl'):
                        matches.append(os.path.join(root, filename))
                        fullpath = join(root, filename)

                        txt = filename.split('.mdl')[0]
                        self.loadMDLFile(txt, fullpath)

                    for filename in fnmatch.filter(filenames, '*.sim'):
                        matches.append(os.path.join(root, filename))
                        fullpath = join(root, filename)
                        txt = filename.split('.sim')[0]
                        self.loadSIMFile(txt, fullpath)

    def getModelPath(self):
        return self.modelpaths

    def sectionKey(self):
        ini = join(dirname(abspath(__file__)), '../Resources/ToolboxPaths')
        cparser = ConfigParser.ConfigParser(None, multidict)
        cparser.read(ini)
        sections = cparser.sections()
        for s in sections:
            # get the section key (minus the random number)
            section = s.split('^')[0]

            # get the section options
            options = cparser.options(s)

            # save ini options as dictionary
            d = {}
            for option in options:
                d[option] = cparser.get(s, option)

            if section not in self.modelpaths:
                self.modelpaths[section] = [d]
            else:
                self.modelpaths[section].append(d)

    def __init__(self, parent):



        # Initialize the View
        ViewToolbox.__init__(self, parent)

        self.p = parent
        # config_params = {}

        self.modelpaths = {}
        self.items = {}
        self.filepath = {}

        self.sectionKey()

        self.loadToolbox(self.getModelPath())

        self.tree.SetItemImage(self.root, self.fldropenidx, which = wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(self.root, self.fldropenidx, which = wx.TreeItemIcon_Normal)

        self.tree.Expand(self.root)
        self.tree.ExpandAll()

        self.initBinding()

    def loadMDLFile(self, txt, fullpath):
        mdl_parser = ConfigParser.ConfigParser(None, multidict)
        mdl_parser.read(fullpath)
        mdls = mdl_parser.sections()
        for s in mdls:
            section = s.split('^')[0]
            if section == 'general':
                # options = cparser.options(s)
                txt = mdl_parser.get(s,'name')


        child = self.tree.AppendItem(self.cat, txt)
        self.filepath[txt] = fullpath

        self.items[child] = fullpath

        child.__setattr__('path', fullpath)
        self.tree.SetItemImage(child, self.modelicon, which = wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(child, self.modelicon, which = wx.TreeItemIcon_Normal)

    def loadSIMFile(self, txt, fullpath):

        child = self.tree.AppendItem(self.simCategory, txt)
        self.filepath[txt] = fullpath
        self.items[child] = fullpath

        child.__setattr__('path', fullpath)
        self.tree.SetItemImage(child, self.simicon, which = wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(child, self.simicon, which = wx.TreeItemIcon_Normal)
        pass

    def SetCurrentlySelected(self,evt):
        item = self.tree.GetSelection()

        for i in self.items.keys():
            if i == item:
                self.__currently_selected_item_path = os.path.abspath(self.items[i])
                break

    # def OnActivate(self, evt):
    #     item = self.tree.GetSelection()

    def onDoubleClick(self, event):
        id = event.GetItem()
        filename = id.GetText()
        fullpath = self.filepath[filename]
        filenames = []
        filenames.append(fullpath)

        originx, originy = self.p.FloatCanvas.WorldToPixel(self.p.Canvas.GetPosition())

        # Generate random coordinates about the center of the canvas
        x = random.randint(-200, 200)
        y = random.randint(-200, 200)
        nx = (originx + x)
        ny = (originy + y)




        # Send the filepath to the FileDrop class in CanvasController
        Publisher.sendMessage('toolboxclick', x = nx, y = ny, filenames = filenames)

    def OnItemContextMenu(self, evt):

        self.tree.GetSelection()
        item = self.tree.GetSelection()
        key = self.tree.GetItemText(item)
        filepath = self.filepath.get(key)
        #ext = ""
        #if filepath is not None:
        name, ext = os.path.splitext(filepath)

        if ext == '.sim':
            flag = True
        else:
            flag = False

        self.tree.PopupMenu(ToolboxContextMenu(self, evt, flag))

    def onDrag(self, event):
        data = wx.FileDataObject()
        obj = event.GetEventObject()
        id = event.GetItem()
        filename = id.GetText()
        fullpath = self.filepath[filename]

        data.AddFile(fullpath)
        dropSource = wx.DropSource(obj)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop()
    #
    # def OnRightUp(self, evt):
    #     pos = evt.GetPosition()

    def OnSize(self, evt):
        self.tree.SetSize(self.GetSize())

    def OnExpandAll(self):
        self.tree.Expand(self.root)

    def OnCollapseAll(self):
        self.tree.Collapse(self.root)


    def ShowDetails(self):

        item = self.tree.GetSelection()
        key = self.tree.GetItemText(item)

        filepath = self.filepath.get(key)

        kwargs = {'spatial':False}
        model_details = LogicModel(self,**kwargs)
        model_details.PopulateDetails(filepath)
        model_details.PopulateEdit(filepath)
        model_details.PopulateSummary(filepath)
        model_details.Show()

    def Remove(self, e):
        dlg = wx.MessageDialog(None, 'Are you sure you would like to delete?', 'Question', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() ==wx.ID_YES:
            item = self.tree.GetSelection()
            key = self.tree.GetItemText(item)
            filepath = self.filepath.get(key)
            os.remove(filepath)
            self.tree.Delete(item)




class multidict(dict):
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^'+str(self._unique)
        dict.__setitem__(self, key, val)