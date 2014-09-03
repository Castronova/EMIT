__author__ = 'Mario'
import wx
import wx.gizmos as gizmos
from images import icons
import ConfigParser
import os
from os.path import *
import fnmatch


class TestPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.Bind(wx.EVT_SIZE, self.OnSize)

        self.tree = gizmos.TreeListCtrl(self, -1, style =
                                        wx.TR_DEFAULT_STYLE
                                        #| wx.TR_HAS_BUTTONS
                                        #| wx.TR_TWIST_BUTTONS
                                        #| wx.TR_ROW_LINES
                                        #| wx.TR_COLUMN_LINES
                                        #| wx.TR_NO_LINES
                                        | wx.TR_FULL_ROW_HIGHLIGHT
                                   )

        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        fldridx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        fileidx     = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        # smileidx    = il.Add(images.Smiles.GetBitmap())

        self.tree.SetImageList(il)
        self.il = il

        ini = join(dirname(abspath(__file__)), 'Resources/ToolboxPaths')
        config_params = {}
        cparser = ConfigParser.ConfigParser(None, multidict)
        cparser.read(ini)
        sections = cparser.sections()
        modelpaths = {}

        for s in sections:
            # get the section key (minus the random number)
            section = s.split('^')[0]

            # get the section options
            options = cparser.options(s)

            # save ini options as dictionary
            d = {}
            for option in options:
                d[option] = cparser.get(s,option)
            # d['type'] = section


            if section not in modelpaths:
                modelpaths[section] = [d]
            else:
                modelpaths[section].append(d)

        self.tree.AddColumn("Main column")
        self.tree.SetMainColumn(0) # the one with the tree in it...
        self.tree.SetColumnWidth(0, 175)
        self.root = self.tree.AddRoot("Models")
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
                for root, dirnames, filenames in os.walk(apath):
                    for filename in fnmatch.filter(filenames, '*.mdl'):
                        matches.append(os.path.join(root, filename))
                        fullpath = join(root, filename)

                        txt =  filename.split('.mdl')[0]
                        child = self.tree.AppendItem(cat, txt)
                        self.tree.SetItemImage(child, fldropenidx, which = wx.TreeItemIcon_Expanded)
                        self.tree.SetItemImage(child, fldropenidx, which = wx.TreeItemIcon_Normal)

            # create some columns
        # self.tree.AddColumn("Main column")
        # self.tree.AddColumn("Column 1")
        # self.tree.AddColumn("Column 2")
        # self.tree.SetMainColumn(0) # the one with the tree in it...
        # self.tree.SetColumnWidth(0, 175)
        #
        #
        # self.root = self.tree.AddRoot("The Root Item")
        # self.tree.SetItemText(self.root, "col 1 root", 1)
        # self.tree.SetItemText(self.root, "col 2 root", 2)
        # self.tree.SetItemImage(self.root, fldridx, which = wx.TreeItemIcon_Normal)
        # self.tree.SetItemImage(self.root, fldropenidx, which = wx.TreeItemIcon_Expanded)
        #
        #
        # for x in range(15):
        #     txt = "Item %d" % x
        #     child = self.tree.AppendItem(self.root, txt)
        #     self.tree.SetItemText(child, txt + "(c1)", 1)
        #     self.tree.SetItemText(child, txt + "(c2)", 2)
        #     self.tree.SetItemImage(child, fldridx, which = wx.TreeItemIcon_Normal)
        #     self.tree.SetItemImage(child, fldropenidx, which = wx.TreeItemIcon_Expanded)
        #
        #     for y in range(5):
        #         txt = "item %d-%s" % (x, chr(ord("a")+y))
        #         last = self.tree.AppendItem(child, txt)
        #         self.tree.SetItemText(last, txt + "(c1)", 1)
        #         self.tree.SetItemText(last, txt + "(c2)", 2)
        #         self.tree.SetItemImage(last, fldridx, which = wx.TreeItemIcon_Normal)
        #         self.tree.SetItemImage(last, fldropenidx, which = wx.TreeItemIcon_Expanded)
        #
        #         for z in range(5):
        #             txt = "item %d-%s-%d" % (x, chr(ord("a")+y), z)
        #             item = self.tree.AppendItem(last,  txt)
        #             self.tree.SetItemText(item, txt + "(c1)", 1)
        #             self.tree.SetItemText(item, txt + "(c2)", 2)
        #             self.tree.SetItemImage(item, fileidx, which = wx.TreeItemIcon_Normal)
        #             # self.tree.SetItemImage(item, smileidx, which = wx.TreeItemIcon_Selected)


        self.tree.Expand(self.root)

        self.tree.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate)


    def OnActivate(self, evt):
        # self.log.write('OnActivate: %s' % self.tree.GetItemText(evt.GetItem()))
        pass

    def OnRightUp(self, evt):
        pos = evt.GetPosition()
        item, flags, col = self.tree.HitTest(pos)
        # if item:
        #     self.log.write('Flags: %s, Col:%s, Text: %s' %
        #                    (flags, col, self.tree.GetItemText(item, col)))

    def OnSize(self, evt):
        self.tree.SetSize(self.GetSize())

def runTest(frame, nb):
    win = TestPanel(nb)
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