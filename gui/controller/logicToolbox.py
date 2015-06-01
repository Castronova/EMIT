from collections import OrderedDict
import os
import random

__author__ = 'tonycastronova'

from gui.views.viewToolbox import ViewToolbox
from gui.views.viewContext import ToolboxContextMenu
from gui.controller.logicModel import LogicModel

import wx
from wx.lib.pubsub import pub as Publisher
from os.path import join, dirname, abspath
import ConfigParser
import fnmatch
from logicFileDrop import filepath


# todo: refactor
from gui.views.viewModel import ViewModel


class LogicToolbox(ViewToolbox):
    modelpaths = ""

    def __init__(self, parent):


        # Initialize the View
        ViewToolbox.__init__(self, parent)

        self.p = parent
        # config_params = {}

        self.modelpaths = []
        self.cat = ""
        self.items = {}
        self.filepath = {}

        self.sectionKey()

        self.loadToolbox(self.getModelPath())

        self.tree.SetItemImage(self.root_mdl, self.fldropenidx, which=wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(self.root_mdl, self.fldropenidx, which=wx.TreeItemIcon_Normal)

        self.tree.Expand(self.root_mdl)
        self.tree.ExpandAll()

        self.initBinding()
        self.simConfigurations.Collapse()

    def initBinding(self):
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnItemContextMenu)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.onDrag)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onDoubleClick)

    def loadToolbox(self, modelpaths):

        # add base-level folders
        self.simConfigurations = self.tree.AppendItem(self.root_mdl, 'Configurations')
        self.tree.SetItemImage(self.simConfigurations, self.folderConfigIcon, which=wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(self.simConfigurations, self.folderConfigIcon, which=wx.TreeItemIcon_Normal)
        self.componentBranch = self.tree.AppendItem(self.root_mdl, "Components")
        self.tree.SetItemImage(self.componentBranch, self.folderConfigIcon, which=wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(self.componentBranch, self.folderConfigIcon, which=wx.TreeItemIcon_Normal)

        folders = dict(Configurations=self.simConfigurations, Components=self.componentBranch)

        for pathinfo in modelpaths:

            # get the folder name and path
            folder_path = pathinfo['folder_path']
            folder_name = pathinfo['folder']

            # create the folder
            parent = folders[pathinfo['folder_path']]
            cat = self.tree.AppendItem(parent, folder_name)

            # save the folder instance so that child elements can be added during future iterations
            folders[folder_path+'/'+folder_name] = cat

            # set folder images
            self.tree.SetItemImage(cat, self.folderComponents, which=wx.TreeItemIcon_Expanded)
            self.tree.SetItemImage(cat, self.folderComponents, which=wx.TreeItemIcon_Normal)


            # get the PATH
            if 'path' in pathinfo:
                path = pathinfo['path']

                # populate models
                if 'Components' in folder_path:
                    for p in path.split(';'):
                        apath = join(dirname(abspath(__file__)), '../../' + p)
                        matches = []
                        self.dirlist = []
                        for root, dirnames, filenames in os.walk(apath):
                            for filename in fnmatch.filter(filenames, '*.mdl'):
                                matches.append(os.path.join(root, filename))
                                fullpath = join(root, filename)
                                txt = filename.split('.mdl')[0]
                                self.loadMDLFile(cat, txt, fullpath)

                            for filename in fnmatch.filter(filenames, '*.sim'):
                                matches.append(os.path.join(root, filename))
                                fullpath = join(root, filename)
                                txt = filename.split('.sim')[0]
                                self.cat = cat
                                self.loadSIMFile(cat, txt, fullpath)

                # populate simulations
                if 'Configurations' in folder_path:
                    for p in path.split(';'):
                        apath = join(dirname(abspath(__file__)), '../../' + p)
                        matches = []
                        self.dirlist = []
                        for root, dirnames, filenames in os.walk(apath):
                            for filename in fnmatch.filter(filenames, '*.sim'):
                                matches.append(os.path.join(root, filename))
                                fullpath = join(root, filename)
                                txt = filename.split('.sim')[0]
                                self.loadSIMFile(cat, txt, fullpath)

    def getModelPath(self):
        return self.modelpaths

    def getCat(self):
        return self.cat

    def sectionKey(self):
        ini = join(dirname(abspath(__file__)), '../Resources/ToolboxPaths')
        cparser = ConfigParser.ConfigParser(None, multidict)
        cparser.read(ini)
        sections = cparser.sections()
        d = []
        for s in sections:
            # get the section key (minus the random number)
            section = s.split('^')[0]

            # get the section options
            options = cparser.options(s)

            # save ini options as dictionary

            kvp = dict(folder=section)
            for option in options:
                kvp[option] = cparser.get(s, option)
            d.append(kvp)

            #if section not in self.modelpaths:
        self.modelpaths = d
            # else:
            #     self.modelpaths[section].append(d)


    def loadMDLFile(self, cat, txt, fullpath):
        mdl_parser = ConfigParser.ConfigParser(None, multidict)
        mdl_parser.read(fullpath)
        mdls = mdl_parser.sections()
        for s in mdls:
            section = s.split('^')[0]
            if section == 'general':
                # options = cparser.options(s)
                txt = mdl_parser.get(s, 'name')

        child = self.tree.AppendItem(cat, txt)
        self.filepath[txt] = fullpath
        self.items[child] = fullpath

        child.__setattr__('path', fullpath)
        self.tree.SetItemImage(child, self.modelicon, which=wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(child, self.modelicon, which=wx.TreeItemIcon_Normal)

    def loadSIMFile(self, cat, txt, fullpath):
        child = self.tree.AppendItem(cat, txt)
        self.filepath[txt] = fullpath
        self.items[child] = fullpath

        child.__setattr__('path', fullpath)
        self.tree.SetItemImage(child, self.simicon, which=wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(child, self.simicon, which=wx.TreeItemIcon_Normal)


    def SetCurrentlySelected(self, evt):
        item = self.tree.GetSelection()

        for i in self.items.keys():
            if i == item:
                self.__currently_selected_item_path = os.path.abspath(self.items[i])
                break

    # def OnActivate(self, evt):
    # item = self.tree.GetSelection()

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
        Publisher.sendMessage('toolboxclick', x=nx, y=ny, filenames=filenames)

    def OnItemContextMenu(self, evt):

        self.tree.GetSelection()
        item = self.tree.GetSelection()
        key = self.tree.GetItemText(item)
        filepath = self.filepath.get(key)

        ext = ""
        folder = False
        removable = False
        if filepath is not None:
            name, ext = os.path.splitext(filepath)

            if ext == '.sim':
                removable = True
            else:
                removable = False
        else:
            folder = True

        if not folder:
            self.tree.PopupMenu(ToolboxContextMenu(self, evt, removable, folder))

    def onDrag(self, event):

        data = wx.FileDataObject()
        obj = event.GetEventObject()
        id = event.GetItem()
        filename = id.GetText()
        fullpath = self.filepath[filename]

        # filepathclass = filepath()
        # filepathclass.filepath = fullpath
        Publisher.sendMessage('dragpathsent', path=fullpath)
        dragCursor = wx.StockCursor(wx.CURSOR_LEFT_BUTTON)
        self.SetCursor(dragCursor)


        # data.AddFile(fullpath)
        # dropSource = wx.DropSource(obj)
        # dropSource.SetData(data)
        # dropSource.DoDragDrop()

    def OnSize(self, evt):
        self.tree.SetSize(self.GetSize())

    def OnExpandAll(self):
        self.tree.Expand(self.root_mdl)

    def OnCollapseAll(self):
        self.tree.Collapse(self.root_mdl)


    def ShowDetails(self):

        item = self.tree.GetSelection()
        key = self.tree.GetItemText(item)

        filepath = self.filepath.get(key)


        filename, ext = os.path.splitext(filepath)
        if ext == '.mdl':
            kwargs = {'spatial': False}
            model_details = LogicModel(self, **kwargs)
            try:
                model_details.PopulateDetails(filepath)
                model_details.PopulateEdit(filepath)
                model_details.PopulateSummary(filepath)
                model_details.Show()
            except:
                dlg = wx.MessageDialog(None, 'Error trying to view details', 'Error', wx.OK)
                dlg.ShowModal()
                pass
        if ext == '.sim':

            kwargs = {'configuration': True, 'edit': False, 'properties': False, 'spatial': False}
            model_details = LogicModel(self, **kwargs)
            try:
                model_details.ConfigurationDisplay(filepath)
                model_details.Show()
            except:
                dlg = wx.MessageDialog(None, 'Error trying to view details', 'Error', wx.OK)
                dlg.ShowModal()
                pass

    def Remove(self, e):
        dlg = wx.MessageDialog(None, 'Are you sure you would like to delete?', 'Question',
                               wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() == wx.ID_YES:
            item = self.tree.GetSelection()
            key = self.tree.GetItemText(item)
            filepath = self.filepath.get(key)
            os.remove(filepath)
            self.tree.Delete(item)



class multidict(dict):
    """
    Dictionary class that has been extended for Ordering and Duplicate Keys
    """

    def __init__(self, *args, **kw):
        self.itemlist = super(multidict,self).keys()
        self._unique = 0

    def __setitem__(self, key, val):

        if isinstance(val, dict):
            self._unique += 1
            key += '^' + str(self._unique)
        self.itemlist.append(key)
        dict.__setitem__(self, key, val)

    def __iter__(self):
        return iter(self.itemlist)
    def keys(self):
       return self.itemlist
    def values(self):
        return [self[key] for key in self]
    def itervalues(self):
        return (self[key] for key in self)