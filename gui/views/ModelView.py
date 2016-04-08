import wx
import wx.xrc
import wx.propgrid as wxpg

class ModelView(wx.Frame):
    def __init__(self, parent, edit=True, spatial=False, temporal=False, properties=True, configuration=False):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='Model Properties', pos=wx.DefaultPosition,
                          size=wx.Size(650, 700),
                          style=wx.FRAME_FLOAT_ON_PARENT | wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)

        self.edit = edit
        self.spatial = spatial
        self.temporal = temporal
        self.properties = properties
        self.configuration = configuration

        self.current_file = None

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        # create the sizers
        sizer_notebook = wx.BoxSizer(wx.VERTICAL)
        txtctrlSizer = wx.BoxSizer(wx.VERTICAL)
        treectrlSizer = wx.BoxSizer(wx.VERTICAL)


        # intialize the notebook

        self.notebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        if properties:
            # make the detail view
            self.treectrlView = wx.Panel(self.notebook, wx.ID_ANY, wx.DefaultPosition,
                                         wx.DefaultSize, wx.TAB_TRAVERSAL)

            self.treectrlView.SetSizer(treectrlSizer)
            self.PropertyGrid = MyPropertyGrid(self.notebook, id=wx.ID_ANY,
                                               pos=wx.Point(0, 0),
                                               # size=wx.Size(700,500))
                                               size=wx.Size(423, 319))
            self.notebook.AddPage(self.PropertyGrid, u"General", True)

        # make the spatial view
        if spatial:

            self.spatial_page = SpatialPage(self.notebook)
            self.notebook.AddPage(self.spatial_page, "Spatial")

        # make edit view
        if edit:
            self.txtctrlView = wx.Panel(self.notebook, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.notebook.AddPage(self.txtctrlView, u"Edit", False)
            self.SaveButton = wx.Button(self.txtctrlView, wx.ID_ANY, u"Save Changes",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
            self.txtctrlView.SetSizer(txtctrlSizer)
            self.TextDisplay = wx.TextCtrl(self.txtctrlView, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(450, 500),
                                           wx.TE_MULTILINE | wx.TE_WORDWRAP)

            txtctrlSizer.Add(self.TextDisplay, 0, wx.ALL | wx.EXPAND, 5)
            txtctrlSizer.Add(self.SaveButton, 0, wx.ALL, 5)

        if configuration:
            xmlPanel = wx.Panel(self.notebook, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.notebook.AddPage(xmlPanel, u"File Configurations (Read-Only)", False)
            txtSizer = wx.BoxSizer(wx.VERTICAL)
            self.xmlTextCtrl = wx.TextCtrl(xmlPanel, -1,
                                           wx.EmptyString,
                                           size=(640, 550),
                                           style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_READONLY)
            txtSizer.Add(self.xmlTextCtrl, 0, wx.ALL, 5)
            xmlPanel.SetSizer(txtSizer)

        sizer_notebook.Add(self.notebook, 1, wx.EXPAND | wx.ALL, 5)

        if properties:
            self.treectrlView.Layout()
            treectrlSizer.Fit(self.treectrlView)

        self.SetSizer(sizer_notebook)
        self.Layout()

        self.Centre(wx.BOTH)


    def InitMenu(self):

        menubar = wx.MenuBar()
        viewMenu = wx.Menu()

        self.shst = viewMenu.Append(wx.ID_ANY, 'Show Edit',
                                    'Show Edit', kind=wx.ITEM_CHECK)

        viewMenu.Check(self.shst.GetId(), False)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)

        menubar.Append(viewMenu, '&Edit')
        self.SetMenuBar(menubar)

        self.SetSize((500, 500))
        self.SetTitle('Check menu item')
        self.Centre()
        self.Show(True)


class SpatialPage(wx.Panel):

    def __init__(self, parent):

        wx.Panel.__init__(self, parent)
        from gui.controller.SpatialCtrl import SpatialCtrl

        self.controller = SpatialCtrl(self)

class MyPropertyGrid(wx.propgrid.PropertyGrid):
    def __init__(self, *args, **kwargs):
        wxpg.PropertyGrid.__init__(self, *args, **kwargs)

