from coordinator import engine

__author__ = 'Mario'

import wx
import wx.xrc
import wx.propgrid as wxpg
from gui.views import PlotView
from gui.controller.logicSpatialPlot import LogicSpatialPlot
# from gui.views.viewPanel import SpatialPanel

class ViewModel(wx.Frame):
    def __init__(self, parent, edit=True, spatial=False, temporal=False, properties=True, configuration=False):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(665, 640), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.edit = edit
        self.spatial = spatial
        self.temporal = temporal
        self.properties = properties
        self.configuration = configuration

        self.current_file = None

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        # create the sizers
        NBSizer = wx.BoxSizer(wx.VERTICAL)
        txtctrlSizer = wx.BoxSizer(wx.VERTICAL)
        treectrlSizer = wx.BoxSizer(wx.VERTICAL)


        # intialize the notebook

        self.txtNotebook = wx.Notebook(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        if properties:
            # make the detail view
            self.treectrlView = wx.Panel(self.txtNotebook, wx.ID_ANY, wx.DefaultPosition,
                                         wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.DetailTree = MyTree(self.treectrlView, id=wx.ID_ANY,
                                     pos=wx.Point(0, 0),
                                     # size=wx.Size(700,500),
                                     size=wx.Size(423, 319),
                                     style=wx.TR_HAS_BUTTONS | wx.TR_HIDE_ROOT)

            self.treectrlView.SetSizer(treectrlSizer)
            self.PropertyGrid = MyPropertyGrid(self.txtNotebook, id=wx.ID_ANY,
                                               pos=wx.Point(0, 0),
                                               # size=wx.Size(700,500))
                                               size=wx.Size(423, 319))
            self.txtNotebook.AddPage(self.PropertyGrid, u"Properties", True)


        # make the spatial view
        if spatial:
            # self.plotPanel = LogicSpatialPlot(self.txtNotebook)
            # inputSelection = wx.CheckBox(self.plotPanel, 998,label='Input Exchange Item: ')
            # self.txtNotebook.AddPage(self.plotPanel, u"Spatial Definition", False)

            panel = wx.Panel(self.txtNotebook, size=wx.Size(500, 300))

            self.plotPanel = LogicSpatialPlot(panel)
            # self.inputSelection = wx.CheckBox(panel, 998,label='Input Exchange Item: ')

            # self.inputSelections = wx.Choice( panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0, choices=None )
            # self.inputSelections.SetSelection( 0 )

            self.inputLabel = wx.StaticText(panel, wx.ID_ANY, u"Input", wx.DefaultPosition, wx.DefaultSize, 0)
            self.inputSelections = wx.ComboBox(panel, wx.ID_ANY, "-", wx.DefaultPosition, wx.DefaultSize, [],
                                               wx.CB_DROPDOWN | wx.CB_READONLY)
            self.outputLabel = wx.StaticText(panel, wx.ID_ANY, u"Output", wx.DefaultPosition, wx.DefaultSize, 0)
            self.outputSelections = wx.ComboBox(panel, wx.ID_ANY, "-", wx.DefaultPosition, wx.DefaultSize, [],
                                                wx.CB_DROPDOWN | wx.CB_READONLY | wx.ALIGN_RIGHT)

            mainSizer = wx.BoxSizer(wx.VERTICAL)
            plotSizer = wx.BoxSizer(wx.VERTICAL)
            inOutSelectionSizer = wx.BoxSizer(wx.HORIZONTAL)

            plotSizer.Add(self.plotPanel, 1, wx.ALL, 5)

            inOutSelectionSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
            inOutSelectionSizer.Add( self.inputLabel, 0, wx.ALL, 5)
            inOutSelectionSizer.Add(self.inputSelections, 0, wx.ALL, 5)
            inOutSelectionSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
            inOutSelectionSizer.Add( self.outputLabel, 0, wx.ALL, 5)
            inOutSelectionSizer.Add(self.outputSelections, 0, wx.ALL, 5)
            inOutSelectionSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

            mainSizer.Add(plotSizer, 1, wx.EXPAND, 5)
            mainSizer.Add(inOutSelectionSizer, 1, wx.EXPAND, 5)

            panel.SetSizer(mainSizer)
            panel.Layout()
            self.txtNotebook.AddPage(panel, u"Spatial Definition", False)

            # m_bitmap1 = wx.StaticBitmap( self, wx.ID_ANY, wx.NullBitmap, wx.DefaultPosition, wx.DefaultSize, 0 )
            # s = wx.BoxSizer(wx.VERTICAL)
            # s.Add(m_bitmap1, 0, wx.ALL, 5)
            # s.Add(inputSelection, 0, wx.ALL, 5)
            # P.SetSizer(s)
            # P.Layout()
            # self.txtNotebook.AddPage(P, u"Spatial Definition", False)

        # make edit view
        if edit:
            self.txtctrlView = wx.Panel(self.txtNotebook, wx.ID_ANY, wx.DefaultPosition,
                                        wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.txtNotebook.AddPage(self.txtctrlView, u"Edit", False)
            self.SaveButton = wx.Button(self.txtctrlView, wx.ID_ANY, u"Save Changes",
                                        wx.DefaultPosition, wx.DefaultSize, 0)
            self.txtctrlView.SetSizer(txtctrlSizer)
            self.TextDisplay = wx.TextCtrl(self.txtctrlView, wx.ID_ANY, wx.EmptyString,
                                           wx.DefaultPosition, wx.Size(450, 500),
                                           wx.TE_MULTILINE | wx.TE_WORDWRAP)

            txtctrlSizer.Add(self.TextDisplay, 0, wx.ALL | wx.EXPAND, 5)
            txtctrlSizer.Add(self.SaveButton, 0, wx.ALL, 5)

        if configuration:
            xmlPanel = wx.Panel(self.txtNotebook, wx.ID_ANY, wx.DefaultPosition,
                                wx.DefaultSize, wx.TAB_TRAVERSAL)
            self.txtNotebook.AddPage(xmlPanel, u"File Configurations (Read-Only)", False)
            txtSizer = wx.BoxSizer(wx.VERTICAL)
            self.xmlTextCtrl = wx.TextCtrl(xmlPanel, -1,
                                           wx.EmptyString,
                                           size=(640, 550),
                                           style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER | wx.TE_READONLY)
            txtSizer.Add(self.xmlTextCtrl, 0, wx.ALL, 5)
            xmlPanel.SetSizer(txtSizer)

        NBSizer.Add(self.txtNotebook, 1, wx.EXPAND | wx.ALL, 5)

        if properties:
            self.treectrlView.Layout()
            treectrlSizer.Fit(self.treectrlView)

        self.SetSizer(NBSizer)
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


class MyTree(wx.TreeCtrl):
    def __init__(self, *args, **kwargs):
        wx.TreeCtrl.__init__(self, *args, **kwargs)

        self.ExpandAll()

        self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)

    def OnLeftUp(self, event):
        item, location = self.HitTest(event.GetPositionTuple())

        data = self.GetPyData(item)


class MyPropertyGrid(wx.propgrid.PropertyGrid):
    def __init__(self, *args, **kwargs):
        wxpg.PropertyGrid.__init__(self, *args, **kwargs)

