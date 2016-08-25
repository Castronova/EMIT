import wx
from gui.views.AboutView import AboutView
import os
import sys


class AboutCtrl(AboutView):
    def __init__(self):
        AboutView.__init__(self)

        app_path = os.getcwd() + "/app_data"
        if getattr(sys, 'frozen', False):
            app_path = os.path.join(sys._MEIPASS, 'app_data')

        icon_path = app_path + "/img/Water-Droplet-121.png"

        name = "EMIT (1.0)"
        description = """
            Sample Text. Technology for building coupled models within the water resource domain has been advancing at a rapid pace. Many modeling framworks have been developed (e.g. OpenMI, CSDMS, OMS, etc) that control the flow of data between model components during a simulation. These efforts have largely focused on establishing software interfaces for componentizing scientific calculations such that they can receive input data and supply output data during a simulation. However, there has been a lack of emphasis on closing the gap between observed and simulated data, and component simulations. One objective of this project is to investigate how observed and simulation data can be integrated seamlessly into component-based model simulations.
        """

        license_text = "Sample License. All rights reserved"
        contributors = ["Tony Castronova", "Steve Jobs", "Green Lantern", "Fantastic Mr. Fox", "Superman", "Homer Simpson"]
        site = "https://www.github.com/Castronova/EMIT"
        self.set_icon(icon_path)
        self.set_name(name)
        self.set_description(description)
        self.set_license(license_text)
        self.set_contributors(contributors)
        self.set_website(site)

        self.SetTitle("About %s" % name)
        self.SetSize((700, 500))

    def set_website(self, site):
        if not isinstance(site, str):
            return

        self.website_hyperlink.SetLabel(site)
        self.website_hyperlink.SetURL(site)

    def set_contributors(self, list_of_strings):
        if not isinstance(list_of_strings, list):
            return

        text = ""
        for item in list_of_strings:
            text += item + ", "

        text = text.rstrip(', ')  # Remove last comma from list
        self.contributors_static_text.SetLabel("Developers: " + text)

    def set_icon(self, icon_path):
        if not os.path.exists(icon_path):
            return

        bitmap = wx.Bitmap(icon_path, type=wx.BITMAP_TYPE_ANY)
        self.png.SetBitmap(bitmap)

    def set_name(self, name):
        if not isinstance(name, str):
            return

        font = wx.Font(pointSize=18, family=wx.DEFAULT, style=wx.NORMAL, weight=wx.NORMAL)
        font.MakeBold()
        self.name_static_text.SetLabel(name)
        self.name_static_text.SetFont(font)

    def set_license(self, text):
        if not isinstance(text, str):
            return

        self.license_static_text.SetLabel(text)

    def set_description(self, description):
        if not isinstance(description, str):
            return

        self.description_text.SetLabel(description)


