import wx
import os
import sys


class IconType(object):
    """
    Enum
    """
    MODEL = 0


class AppImages(object):
    def __init__(self):

        # 3B83DB is the hex color of the water droplet, and 41, 152, 228 for RGB
        app_path = os.getcwd() + "/app_data"
        if getattr(sys, 'frozen', False):
            app_path = os.path.join(sys._MEIPASS, 'app_data')
        self.image_directory = app_path + "/img"

        if not os.path.exists(self.image_directory):
            raise Exception(self.image_directory, "AppImages.image_directory path does not exist")

    def __get_path_for_icon_type(self, icon_type=IconType.MODEL):
        if icon_type == IconType.MODEL:
            return self.image_directory + "/water-droplet-32.png"

        return None

    def get_icon(self, icon_type, width=16, height=16):
        path = self.__get_path_for_icon_type(icon_type)
        if not os.path.exists(path):
            return None

        image = wx.Image(path, wx.BITMAP_TYPE_ANY).Scale(width, height)
        bitmap = image.ConvertToBitmap()

        return bitmap
