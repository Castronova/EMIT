import wx
import wx.lib.customtreectrl as CT
from gui.Resources import icons
from gui.Models.AppImages import AppImages


class ToolboxView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        app_images = AppImages()

        self.tree = CT.CustomTreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE)
        self.tree.SetBackgroundColour((255, 255, 255))
        image_list = wx.ImageList(width=16, height=16)

        self.fldropenidx = image_list.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16)))
        self.modelicon = image_list.Add(app_images.get_model_as_bitmap())

        self.folderConfigIcon = image_list.Add(icons.folderConfigIcon.GetBitmap())
        self.folderComponents = image_list.Add(icons.folder_desktop.GetBitmap())

        self.tree.SetImageList(image_list)
        self.root_mdl = self.tree.AddRoot("Toolbox")


class multidict(dict):
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^' + str(self._unique)
        dict.__setitem__(self, key, val)