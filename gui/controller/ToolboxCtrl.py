import ConfigParser
import fnmatch
import random

import wx
from wx.lib.pubsub import pub as Publisher

from emitLogging import elog
from gui import events
from gui.controller.ModelCtrl import ModelCtrl
from gui.views.ContextView import ToolboxContextMenu
from gui.views.ToolboxView import ToolboxView
from sprint import *
from utilities import gui


# todo: refactor


class ToolboxViewCtrl(ToolboxView):
    modelpaths = ""

    def __init__(self, parent):

        # Initialize the View
        ToolboxView.__init__(self, parent)

        self.p = parent
        # config_params = {}

        self.cat = ""
        self.items = {}
        self.filepath = {}
        self.modelpaths = self.parseModelPaths()

        # initialize event bindings
        self.initBinding()

        self.loadToolbox(self.getModelPath())

        self.tree.SetItemImage(self.root_mdl, self.fldropenidx, which=wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(self.root_mdl, self.fldropenidx, which=wx.TreeItemIcon_Normal)

        # Expand "Toolbox", "Configurations", and "Components" trees in the toolbox
        self.root_mdl.Expand()
        self.componentBranch.Expand()
        self.simConfigurations.Expand()

    def initBinding(self):
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnItemContextMenu)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onDoubleClick)
        events.onSimulationSaved += self.loadSIMFile

    def loadToolbox(self, modelpaths):
        # add base-level folders
        self.simConfigurations = self.tree.AppendItem(self.root_mdl, "Configurations")
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
            self.cat = cat

            # save the folder instance so that child elements can be added during future iterations
            folders[folder_path + '/' + folder_name] = cat

            # set folder images
            self.tree.SetItemImage(cat, self.folderComponents, which=wx.TreeItemIcon_Expanded)
            self.tree.SetItemImage(cat, self.folderComponents, which=wx.TreeItemIcon_Normal)

            # get the PATH
            if 'path' in pathinfo:
                path = pathinfo['path']

                # populate models
                if 'Components' in folder_path:
                    for p in path.split(';'):
                        apath = os.path.realpath(__file__ + "../../../../" + p)
                        matches = []
                        self.dirlist = []

                        for root, dirnames, filenames in os.walk(apath):
                            for filename in fnmatch.filter(filenames, '*.mdl'):
                                matches.append(os.path.join(root, filename))
                                fullpath = join(root, filename)
                                txt = filename.split('.mdl')[0]
                                self.loadMDLFile(cat, txt, fullpath)

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
                                e = dict(cat=self.cat, txt=txt, fullpath=fullpath)

                                # fixme: this should not call onSimulationSaved
                                events.onSimulationSaved.fire(**e)

    def RefreshToolbox(self):
        self.tree.DeleteChildren(self.tree.GetRootItem())
        self.loadToolbox(self.getModelPath())

        self.root_mdl.Expand()
        self.componentBranch.Expand()
        self.simConfigurations.Expand()

    def getModelPath(self):
        return self.modelpaths

    def getCat(self):
        return self.cat

    def parseModelPaths(self):
        """
        reads the APP_TOOLBOX_PATH and parses the model/config paths
        Returns: modelpaths lists

        """

        ini = os.environ['APP_TOOLBOX_PATH']
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

        return d

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

    def loadSIMFile(self, e):
        child = self.tree.AppendItem(e.cat, e.txt)
        self.filepath[e.txt] = e.fullpath
        self.items[child] = e.fullpath
        child.__setattr__('path', e.fullpath)
        self.tree.SetItemImage(child, self.modelicon, which=wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(child, self.modelicon, which=wx.TreeItemIcon_Normal)

    def SetCurrentlySelected(self, evt):
        item = self.tree.GetSelection()

        for i in self.items.keys():
            if i == item:
                self.__currently_selected_item_path = os.path.abspath(self.items[i])
                break

    def onDoubleClick(self, event):
        id = event.GetItem()
        filename = id.GetText()
        try:
            filename = self.filepath[filename]

            # Send the message to logicCanvas
            # todo: replace with custom event
            Publisher.sendMessage('AddModel', filepath=filename)

        except Exception, e:
            # Clicked on a folder
            elog.error(e)
            pass

    def OnItemContextMenu(self, evt):

        self.tree.GetSelection()
        item = self.tree.GetSelection()
        key = self.tree.GetItemText(item)
        filepath = self.filepath.get(key)

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
            model_details = ModelCtrl(self, **kwargs)

            # Use .json instead of .mdl
            path = filepath[:-4] + ".json"
            data = gui.parse_json(path)
            model_details.properties_page_controller.add_data(data)
            model_details.PopulateEdit(filepath)
            model_details.Show()

        if ext == '.sim':

            kwargs = {'configuration': True, 'edit': False, 'properties': False, 'spatial': False}
            model_details = ModelCtrl(self, **kwargs)
            try:
                model_details.ConfigurationDisplay(filepath)
                model_details.Show()
            except:
                dlg = wx.MessageDialog(None, 'Error trying to view details', 'Error', wx.OK)
                dlg.ShowModal()

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
        self.itemlist = super(multidict, self).keys()
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
