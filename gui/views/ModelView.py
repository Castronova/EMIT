import sys
import wx
import wx.xrc
import wx.propgrid as wxpg


class ModelView(wx.Frame):
    def __init__(self, parent, edit=True, spatial=False, temporal=False, configuration=False):
        if sys.platform == "darwin":
            width, height = (640, 690)
        elif sys.platform == "win32":
            width, height = (660, 690)
        else:
            width, height = (640, 725)

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='Model Properties', pos=wx.DefaultPosition,
                          size=wx.Size(width, height),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE)

        self.edit = edit
        self.spatial = spatial
        self.temporal = temporal
        self.spatial_page = None
        self.configuration = configuration

        self.current_file = None

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        # create the sizers
        sizer_notebook = wx.BoxSizer(wx.VERTICAL)
        txtctrlSizer = wx.BoxSizer(wx.VERTICAL)

        # intialize the notebook
        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # make the spatial view
        if spatial:
            self.spatial_page = SpatialPage(self.notebook)

        # make edit view
        if edit:
            self.txtctrlView = wx.Panel(self.notebook, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.SaveButton = wx.Button(self.txtctrlView, wx.ID_ANY, "Save Changes",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
            self.txtctrlView.SetSizer(txtctrlSizer)
            self.TextDisplay = wx.TextCtrl(self.txtctrlView, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(450, 500),
                                           wx.TE_MULTILINE | wx.TE_WORDWRAP)

            txtctrlSizer.Add(self.TextDisplay, 1, wx.ALL | wx.EXPAND, 5)
            txtctrlSizer.Add(self.SaveButton, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        if configuration:
            xmlPanel = wx.Panel(self.notebook, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.notebook.AddPage(xmlPanel, "Simulation Properties", False)
            txtSizer = wx.BoxSizer(wx.VERTICAL)
            self.xmlTextCtrl = wx.TextCtrl(xmlPanel, -1,
                                           wx.EmptyString,
                                           size=(640, 550),
                                           style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_READONLY)
            txtSizer.Add(self.xmlTextCtrl, 0, wx.ALL, 5)
            xmlPanel.SetSizer(txtSizer)

        sizer_notebook.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(sizer_notebook)
        self.Layout()

        self.Centre(wx.BOTH)


class SpatialPage(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)
        from gui.controller.SpatialCtrl import SpatialCtrl

        self.controller = SpatialCtrl(self)
