import wx
import os


class AppImages(object):

    def __init__(self):

        self.image_directory = os.getcwd() + "/app_data/img"

        if not os.path.exists(self.image_directory):
            raise Exception("AppImages.image_directory path does not exist")

    def get_model_as_bitmap(self, width=16, height=16):
        """
        width, and height are used for scaling the image. Returns a bitmap
        :param width: type(Int)
        :param height: type(Int)
        :return: type(Bitmap)
        """

        path = self.image_directory + "/Water-96.png"
        if not os.path.exists(path):
            return None

        image = wx.Image(path, wx.BITMAP_TYPE_ANY).Scale(width, height)
        image.SetMask()

        bitmap = image.ConvertToBitmap()

        return bitmap
