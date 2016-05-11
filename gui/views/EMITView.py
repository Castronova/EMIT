import os
import wx
import wx.html2
import wx.lib.agw.aui as aui
from wx.lib.newevent import NewEvent
from LowerPanelView import ViewLowerPanel
from gui.controller.CanvasCtrl import CanvasCtrl
from gui.controller.ToolboxCtrl import ToolboxViewCtrl

# create custom events
wxCreateBox, EVT_CREATE_BOX = NewEvent()
wxStdOut, EVT_STDDOUT= NewEvent()
wxDbChanged, EVT_DBCHANGED= NewEvent()


class EMITView(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Environmental Model Integration Project", pos=wx.DefaultPosition,
                          size=wx.Size(1200, 750), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(1200, 750),
                                   style=wx.TAB_TRAVERSAL)
        self.bnb = wx.Notebook(self.pnlDocking)
        ViewLowerPanel(self.bnb)

        ##################################
        # MENU BAR
        ##################################
        self._menu_bar = wx.MenuBar()
        self.view_menu = wx.Menu()
        self.data_menu = wx.Menu()

        # File Menu Option
        self._file_menu = wx.Menu()
        self._load = self._file_menu.Append(wx.NewId(), '&Load\tCtrl+O', 'Load Configuration')
        self._save_menu = self._file_menu.Append(wx.NewId(), '&Save Configuration\tCtrl+S', 'Save Configuration')
        self._add_user_menu = self._file_menu.Append(wx.NewId(), 'Add User', 'Add New User')
        self.save_as_menu = self._file_menu.Append(wx.NewId(), '&Save Configuration As', 'Save Configuration')
        self._settings_menu = self._file_menu.Append(wx.NewId(), "Settings...")
        self._exit = self._file_menu.Append(wx.NewId(), '&Quit\tCtrl+Q', 'Quit application')

        # View Menu Option
        self._toggle_console_menu = self.view_menu.Append(wx.NewId(), '&Toggle Console', 'Toggle the Console', wx.ITEM_CHECK)
        self._default_view_menu = self.view_menu.Append(wx.NewId(), '&Restore Default View', 'Returns the view to the default (initial) state', wx.ITEM_NORMAL)

        # Data Menu Option
        self._add_file = self.data_menu.Append(wx.NewId(), "&Add CSV File")
        self._add_netcdf = self.data_menu.Append(wx.NewId(), '&Add NetCDF')
        self._open_dap_viewer_menu = self.data_menu.Append(wx.NewId(), "&OpenDap Explorer")

        # Add menu items
        self._menu_bar.Append(self._file_menu, "&File")
        self._menu_bar.Append(self.view_menu, "&View")
        self._menu_bar.Append(self.data_menu, "Data")

        # todo: implement and enable the CSV menu option below
        self._add_file.Enable(False)

        self.SetMenuBar(self._menu_bar)

        wx.CallAfter(self._postStart)

        # creating components
        self.Toolbox = ToolboxViewCtrl(self.pnlDocking)
        self.Canvas = CanvasCtrl(self.pnlDocking)

        self.Toolbox.Hide()
        self.initAUIManager()
        self._init_sizers()

        self.filename = None
        self.loading_path = None

        self.Center()

        self.Show()

        self.defaultLoadDirectory = os.getcwd() + "/models/MyConfigurations/"

    def _init_sizers(self):
        self.s = wx.BoxSizer(wx.VERTICAL)
        self.s.AddWindow(self.pnlDocking, 85, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.s)

    def initAUIManager(self):

        self.m_mgr = aui.AuiManager()
        self.m_mgr.SetManagedWindow(self.pnlDocking)

        self.m_mgr.AddPane(self.Canvas,
                           aui.AuiPaneInfo().
                           Center().
                           Name("Canvas").
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           Floatable(False).
                           BestSize(wx.Size(1000, 400)).CaptionVisible(False)
        )

        self.m_mgr.AddPane(self.Toolbox,
                           aui.AuiPaneInfo().
                           Left().
                           Dock().
                           Name("Toolbox").
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           BestSize(wx.Size(275, 400)).
                           Floatable(False).
                           Movable(False).
                           Show(show=True).CaptionVisible(False)
                           )

        self.m_mgr.AddPane(self.bnb,
                           aui.AuiPaneInfo().
                           Bottom().
                           Name("Console").
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           Movable(False).
                           Floatable(False).
                           BestSize(wx.Size(1200, 225)).CaptionVisible(False)
                           )


        self.m_mgr.Update()

        self._default_perspective = self.m_mgr.SavePerspective()

    def _postStart(self):
        # Starts stuff after program has initiated
        self.Canvas.ZoomToFit(event=None)
