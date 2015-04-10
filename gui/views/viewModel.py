__author__ = 'Mario'

import wx
import wx.xrc
from ..pnlSpatial import pnlSpatial
import wx.propgrid as wxpg


class ViewModel(wx.Frame):
    def __init__(self, parent, edit=True, spatial=False, temporal=False, properties=False):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(500, 500), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.edit = edit
        self.spatial = spatial
        self.temporal = temporal
        self.properties = properties

        self.current_file = None

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        # create the sizers
        NBSizer = wx.BoxSizer(wx.VERTICAL)
        txtctrlSizer = wx.BoxSizer(wx.VERTICAL)
        treectrlSizer = wx.BoxSizer(wx.VERTICAL)


        # intialize the notebook

        self.txtNotebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # make the detail view
        self.treectrlView = wx.Panel(self.txtNotebook, wx.ID_ANY, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TAB_TRAVERSAL)
        self.DetailTree = MyTree(self.treectrlView, id=wx.ID_ANY,
                                 pos=wx.Point(0, 0),
                                 size=wx.Size(423, 319), style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)

        self.treectrlView.SetSizer(treectrlSizer)

        self.PropertyGrid = MyPropertyGrid(self.txtNotebook, id=wx.ID_ANY,
                                           pos=wx.Point(0, 0),
                                           size=wx.Size(423, 319))
        self.txtNotebook.AddPage(self.PropertyGrid, u"Properties", True)


        # treectrlSizer.Add( self.propertyGrid, 0, wx.ALL, 5 )
        # make the spatial view
        if spatial:
            self.matplotView = pnlSpatial(self.txtNotebook)
            self.txtNotebook.AddPage(self.matplotView, u"Spatial Definition", False)
        # if not spatial:
        #     page = self.txtNotebook.GetPage(1)
        #     self.txtNotebook.GetPage(1).Disable()


        # make edit view
        if edit:
            self.txtctrlView = wx.Panel(self.txtNotebook, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.txtNotebook.AddPage(self.txtctrlView, u"Edit", False)

            self.SaveButton = wx.Button(self.txtctrlView, wx.ID_ANY, u"Save Changes",
                                        wx.DefaultPosition, wx.DefaultSize, 0)

            self.txtctrlView.SetSizer(txtctrlSizer)

            self.TextDisplay = wx.TextCtrl(self.txtctrlView, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(450, 350), wx.TE_MULTILINE | wx.TE_WORDWRAP)

            txtctrlSizer.Add(self.TextDisplay, 0, wx.ALL | wx.EXPAND, 5)
            txtctrlSizer.Add(self.SaveButton, 0, wx.ALL, 5)

        # if not edit:
        #     self.txtNotebook.GetPage(2).Disable()

        NBSizer.Add(self.txtNotebook, 1, wx.EXPAND | wx.ALL, 5)



        # Bindings
        #self.SaveButton.Bind( wx.EVT_BUTTON, self.OnSave )

        self.treectrlView.Layout()
        treectrlSizer.Fit(self.treectrlView)

        self.SetSizer(NBSizer)
        self.Layout()

        self.Centre(wx.BOTH)
        # self.InitMenu()


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


class MyTree(wx.TreeCtrl):
    def __init__(self, *args, **kwargs):
        wx.TreeCtrl.__init__(self, *args, **kwargs)

        self.ExpandAll()

        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

    def OnLeftUp(self, event):
        item, location = self.HitTest(event.GetPositionTuple())

        data = self.GetPyData(item)
        # if data is not None: print data


class MyPropertyGrid(wx.propgrid.PropertyGrid):
    def __init__(self, *args, **kwargs):
        wxpg.PropertyGrid.__init__(self, *args, **kwargs)
