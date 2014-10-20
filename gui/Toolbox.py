__author__ = 'Mario'
import wx
import wx.gizmos as gizmos
from images import icons
from ContextMenu import TreeContextMenu, TreeItemContextMenu
import ConfigParser
import os
from os.path import *
import fnmatch
import wx.lib.customtreectrl as CT
import utilities

from PropertyGrid import pnlProperty

class ToolboxPanel(wx.Panel):
    def __init__(self, parent):

        self.cmd = parent.__getattribute__('cmd')

        # create object to store the currently selected item's path
        self.__currently_selected_item_path = None

        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour((0,0,0))
        self.Bind(wx.EVT_SIZE, self.OnSize)
        #
        # self.tree = gizmos.TreeListCtrl(self, -1, style =
        #                                 wx.TR_DEFAULT_STYLE
        #                                 #| wx.TR_HAS_BUTTONS
        #                                 #| wx.TR_TWIST_BUTTONS
        #                                 #| wx.TR_ROW_LINES
        #                                 #| wx.TR_COLUMN_LINES
        #                                 #| wx.TR_NO_LINES
        #                                 | wx.TR_FULL_ROW_HIGHLIGHT
        #                            )


        ini = join(dirname(abspath(__file__)), 'Resources/ToolboxPaths')
        config_params = {}
        cparser = ConfigParser.ConfigParser(None, multidict)
        cparser.read(ini)
        sections = cparser.sections()
        modelpaths = {}

        self.tree = CT.CustomTreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE )
        self.tree.SetBackgroundColour((255,255,255))
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        mdlidx    = il.Add(icons.Earth_icon.GetBitmap())

        self.tree.SetImageList(il)
        self.il = il
        self.items = {}
        self.filepath = {}

        for s in sections:
            # get the section key (minus the random number)
            section = s.split('^')[0]

            # get the section options
            options = cparser.options(s)

            # save ini options as dictionary
            d = {}
            for option in options:
                d[option] = cparser.get(s,option)

            if section not in modelpaths:
                modelpaths[section] = [d]
            else:
                modelpaths[section].append(d)

        # self.tree.AddColumn("File Categories")
        # self.tree.SetMainColumn(0) # the one with the tree in it...
        # self.tree.SetColumnWidth(0, 175)
        self.root = self.tree.AddRoot("Model Toolbox")
        self.tree.SetItemImage(self.root, fldropenidx, which = wx.TreeItemIcon_Expanded)
        self.tree.SetItemImage(self.root, fldropenidx, which = wx.TreeItemIcon_Normal)

        for category, data in modelpaths.iteritems():
            txt =  category
            cat = self.tree.AppendItem(self.root, txt)
            self.tree.SetItemImage(cat, fldropenidx, which = wx.TreeItemIcon_Expanded)
            self.tree.SetItemImage(cat, fldropenidx, which = wx.TreeItemIcon_Normal)
            for d in data:
                path = d['path']
                apath = join(dirname(abspath(__file__)), path)
                matches = []
                self.dirlist = []
                for root, dirnames, filenames in os.walk(apath):
                    for filename in fnmatch.filter(filenames, '*.mdl'):
                        matches.append(os.path.join(root, filename))
                        fullpath = join(root, filename)

                        txt =  filename.split('.mdl')[0]

                        mdl_parser = ConfigParser.ConfigParser(None, multidict)
                        mdl_parser.read(fullpath)
                        mdls = mdl_parser.sections()
                        for s in mdls:
                            section = s.split('^')[0]
                            if section == 'general':
                                # options = cparser.options(s)
                                txt = mdl_parser.get(s,'name')


                        child = self.tree.AppendItem(cat, txt)
                        self.filepath[txt] = fullpath

                        self.items[child] = fullpath

                        child.__setattr__('path', fullpath)
                        self.tree.SetItemImage(child, mdlidx, which = wx.TreeItemIcon_Expanded)
                        self.tree.SetItemImage(child, mdlidx, which = wx.TreeItemIcon_Normal)


        self.tree.Expand(self.root)
        self.tree.ExpandAll()

        # self.tree.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnContextMenu)
        self.tree.Bind(wx.EVT_RIGHT_UP, self.OnContextMenu)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)
        self.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnItemContextMenu)
        # self.Bind(wx.EVT_TREE_ITEM_MENU, self.OnItemContextMenu)
        self.Bind(wx.EVT_TREE_BEGIN_DRAG, self.onDrag)

    def OnContextMenu(self, evt):

        # save the currently selected item
        self.SetCurrentlySelected(evt)

        # launch the context menu
        self.tree.PopupMenu(TreeContextMenu(self,evt))

    def OnItemContextMenu(self, evt):

        self.tree.GetSelection()
        self.tree.PopupMenu(TreeItemContextMenu(self,evt))

    def SetCurrentlySelected(self,evt):
        item = self.tree.GetSelection()

        for i in self.items.keys():
            if i == item:
                self.__currently_selected_item_path = os.path.abspath(self.items[i])
                break

    def OnActivate(self, evt):

        # item = self.tree.GetItemText(evt.GetItem())
        item = self.tree.GetSelection()

        for i in self.items.keys():
            if i == item:
                print self.items[i]
                break
        pass

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

    def OnRightUp(self, evt):
        pos = evt.GetPosition()
        item, flags, col = self.tree.HitTest(pos)
        # if item:
        #     self.log.write('Flags: %s, Col:%s, Text: %s' %
        #                    (flags, col, self.tree.GetItemText(item, col)))

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
        print filepath
        # create the details view
        view = pnlProperty(self)

        view.PopulateEdit(filepath)


        # load the geometry data
        # view.PopulateSpatial(self.read_geoms(self.sb.GetValue(),'input'),'input')
        # view.PopulateSpatial(self.read_geoms(self.sb.GetValue(),'output'),'output')

        # show the details view
        #listview = MyTree(self)
        view.PopulateEdit(filepath)
        view.PopulateDetails(filepath)

        #listview.PopulateDetails(self.sb.GetValue())
        view.Show()


def runTest(frame, nb):
    win = ToolboxPanel(nb)
    return win

#----------------------------------------------------------------------



overview = """<html><body>
<h2><center>TreeListCtrl</center></h2>

The TreeListCtrl is essentially a wx.TreeCtrl with extra columns,
such that the look is similar to a wx.ListCtrl.

</body></html>
"""


if __name__ == '__main__':
    #raw_input("Press enter...")
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

class multidict(dict):
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^'+str(self._unique)
        dict.__setitem__(self, key, val)