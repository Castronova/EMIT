import wx
import wx.lib.customtreectrl as CT
from gui.Resources import icons


class ToolboxView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.tree = CT.CustomTreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE)
        self.tree.SetBackgroundColour((255, 255, 255))
        isz = (16, 16)
        il = wx.ImageList(isz[0], isz[1])

        self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, isz))
        self.simicon = il.Add(icons.blueBall_simFiles.GetBitmap())
        self.modelicon = il.Add(icons.modelicon.GetBitmap())
        self.componentFolder = il.Add(icons.componentFolder.GetBitmap())
        self.hydrologyFolder = il.Add(icons.hydrologyFolder.GetBitmap())

        self.folderConfigIcon = il.Add(icons.folderConfigIcon.GetBitmap())
        self.folderComponents = il.Add(icons.folder_desktop.GetBitmap())

        self.tree.SetImageList(il)
        self.il = il

        self.root_mdl = self.tree.AddRoot("Toolbox")


class multidict(dict):
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^' + str(self._unique)
        dict.__setitem__(self, key, val)