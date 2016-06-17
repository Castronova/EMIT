import ConfigParser
import fnmatch
import random
import wx
from wx.lib.pubsub import pub as Publisher
from emitLogging import elog
from gui import events
from gui.controller.ModelCtrl import ModelCtrl
from gui.views.ToolboxView import ToolboxView
from sprint import *
from utilities import models


class ToolboxCtrl(ToolboxView):
    modelpaths = ""

    def __init__(self, parent):

        # Initialize the View
        ToolboxView.__init__(self, parent)

        self.p = parent

        self.cat = ""
        self.items = {}
        self.filepath = {}
        self.modelpaths = self.parseModelPaths()

        # initialize event bindings
        self.initBinding()

        self.loadToolbox(self.modelpaths)

        self.tree.SetItemImage(self.root_mdl, self.fldropenidx, which=wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(self.root_mdl, self.fldropenidx, which=wx.TreeItemIcon_Normal)

        # Expand "Toolbox", "Configurations", and "Components" trees in the toolbox
        self.root_mdl.Expand()
        self.componentBranch.Expand()
        self.simConfigurations.Expand()

        # Context Menu
        self.popup_menu = wx.Menu()
        view_details_menu = self.popup_menu.Append(1, "View Details")
        remove_menu = self.popup_menu.Append(2, "Remove")

        # Context menu bindings
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.on_right_click)
        self.Bind(wx.EVT_MENU, self.on_view_details, view_details_menu)
        self.Bind(wx.EVT_MENU, self.on_remove, remove_menu)

    def on_view_details(self, event):
        self.ShowDetails()

    def on_remove(self, event):
        self.Remove(event)

    def on_right_click(self, event):
        self.PopupMenu(self.popup_menu)

    def initBinding(self):
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onDoubleClick)

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
                                self.load_json_file(cat, fullpath)

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
                                # events.onSimulationSaved.fire(**e)
                                self.loadSIMFile(e)

    def RefreshToolbox(self):
        self.tree.DeleteChildren(self.tree.GetRootItem())
        self.loadToolbox(self.modelpaths)

        self.root_mdl.Expand()
        self.componentBranch.Expand()
        self.simConfigurations.Expand()

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

    def load_json_file(self, cat, fullpath):
        data = models.parse_json(fullpath)
        txt = data["general"][0]["name"]

        child = self.tree.AppendItem(cat, txt)
        self.filepath[txt] = fullpath
        self.items[child] = fullpath

        child.__setattr__("path", fullpath)
        self.tree.SetItemImage(child, self.modelicon, which=wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(child, self.modelicon, which=wx.TreeItemIcon_Normal)

    def loadSIMFile(self, e):
        child = self.tree.AppendItem(e["cat"], e["txt"])
        self.filepath[e["txt"]] = e["fullpath"]
        self.items[child] = e["fullpath"]
        child.__setattr__('path', e["fullpath"])
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
            # get selected filename
            filename = self.filepath[filename]
            self.GetTopLevelParent().model_input_prompt(filename)

        except Exception, e:
            # Clicked on a folder
            elog.error(e)
            pass

    def OnSize(self, evt):
        self.tree.SetSize(self.GetSize())

    def OnExpandAll(self):
        self.tree.Expand(self.root_mdl)

    def OnCollapseAll(self):
        self.tree.Collapse(self.root_mdl)

    def ShowDetails(self):
        name = self.tree.GetItemText(self.tree.GetSelection())
        path = self.filepath.get(name)

        filename, ext = os.path.splitext(path)
        if ext == '.mdl':
            model_details = ModelCtrl(self)

            data = models.parse_json(path)
            model_details.properties_page_controller.add_data(data)
            model_details.PopulateEdit(path)
            model_details.Show()

        if ext == '.sim':

            kwargs = {'configuration': True, 'edit': False, 'properties': False, 'spatial': False}
            model_details = ModelCtrl(self, **kwargs)
            try:
                model_details.ConfigurationDisplay(path)
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
