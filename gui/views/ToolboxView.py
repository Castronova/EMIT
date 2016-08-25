import wx.lib.customtreectrl as CT
from gui.Models.AppImages import *


class ToolboxView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        app_images = AppImages()

        self.tree = CT.CustomTreeCtrl(self, -1, style=wx.TR_DEFAULT_STYLE)
        self.tree.SetBackgroundColour((255, 255, 255))
        image_list = wx.ImageList(width=16, height=16)

        self.model_icon = image_list.Add(app_images.get_icon(icon_type=IconType.MODEL))
        self.closed_folder_icon = image_list.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, (16, 16)))
        self.open_folder_icon = image_list.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN, wx.ART_OTHER, (16, 16)))

        self.tree.SetImageList(image_list)
        self.root_mdl = self.tree.AddRoot("Toolbox")


class multidict(dict):
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^' + str(self._unique)
        dict.__setitem__(self, key, val)