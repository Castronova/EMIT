import wx
import wx.xrc
from gui.Models.CustomGrid import CustomGrid


class ModelView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.notebook = wx.Notebook(self)

        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)


class ModelDetailsView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Create components
        self.grid = CustomGrid(self)

        # Create sizer and add components
        sizer = wx.BoxSizer()
        sizer.Add(self.grid, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def reset_grid(self):
        del self.grid
        self.grid = CustomGrid(self)


class ModelEditView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Components
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_WORDWRAP)
        self.save_button = wx.Button(self, label="Save")

        # Sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, 1, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.save_button, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        self.SetSizer(sizer)







