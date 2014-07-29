__author__ = 'Mario'
import wx
import wx.grid as grid
#import wx.html
import wx.html2
from DirectoryView import DirectoryCtrlView
import sys
from CanvasView import Canvas

class MainGui(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                          size=wx.Size(1500, 650), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(1500, 650),
                                   style=wx.TAB_TRAVERSAL)
        #self.Bind(wx.EVT_CLOSE, self.onClose)
        self.initMenu()
        self.initAUIManager()


    def initAUIManager(self):

        self.m_mgr = wx.aui.AuiManager()
        self.m_mgr.SetManagedWindow(self.pnlDocking)
        self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)

        self.Canvas = Canvas(self.pnlDocking)
        self.nb = wx.Notebook(self.pnlDocking)

        self.output = wx.TextCtrl(self, -1, size=(100,100), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        # redir= RedirectText(self.output)
        # sys.stdout=redir

        page1 = DirectoryCtrlView(self.nb)
        page2 = ModelView(self.nb)
        page3 = LinkView(self.nb)
        page4 = TimeSeries(self.nb)

        self.nb.AddPage(page1, "Directory")
        self.nb.AddPage(page2, "Model View")
        self.nb.AddPage(page3, "Link View")
        self.nb.AddPage(page4, "Series Selector")


        self.m_mgr.AddPane(self.Canvas,
                           wx.aui.AuiPaneInfo().Center().Name("Canvas").Position(0).CloseButton(False).MaximizeButton(
                               True).MinimizeButton(True).PinButton(True).Resizable().Floatable(True).MinSize(
                               wx.Size(1000, 400)))

        self.m_mgr.AddPane(self.output,
                          wx.aui.AuiPaneInfo().Center().Name("Output").Position(1).CloseButton(False).MaximizeButton(
                               True).MinimizeButton(True).PinButton(True).Resizable().Floatable().MinSize(
                               wx.Size(1000, 200)))

        self.m_mgr.AddPane(self.nb,
                   wx.aui.AuiPaneInfo().Left().CloseButton(False).MaximizeButton(True).MinimizeButton(
                       True).PinButton(True).Resizable().MinSize(wx.Size(375,500)).Floatable())

        self.m_mgr.Update()


    def initMenu(self):
        ## Menu stuff
        #self.m_statusBar2 = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)

        self.m_menubar = wx.MenuBar()

        self.m_fileMenu = wx.Menu()
        #exit = wx.MenuItem(self.m_fileMenu, wx.ID_EXIT, '&Quit\tCtrl+Q')
        exit = self.m_fileMenu.Append(wx.NewId(), '&Quit\tCtrl+Q', 'Quit application')

        self.m_menubar.Append(self.m_fileMenu, "&File")

        self.m_toolMenu = wx.Menu()
        self.m_menubar.Append(self.m_toolMenu, "&Tools")

        self.m_viewMenu = wx.Menu()
        self.m_menubar.Append(self.m_viewMenu, "&View")

        self.SetMenuBar(self.m_menubar)

        wx.CallAfter(self._postStart)

        ## Events
        self.Bind(wx.EVT_MENU, self.onClose, exit)

    def _postStart(self):
        ## Starts stuff after program has initiated
        self.Canvas.ZoomToFit(Event=None)

    def __del__(self):
        self.m_mgr.UnInit()

    def onClose(self, event):
        windowsRemaining = len(wx.GetTopLevelWindows())
        if windowsRemaining > 0:
            import wx.lib.agw.aui.framemanager as aui
            # logger.debug("Windows left to close: %d" % windowsRemaining)
            for item in wx.GetTopLevelWindows():
                #logger.debug("Windows %s" % item)
                if not isinstance(item, self.__class__):
                    if isinstance(item, aui.AuiFloatingFrame):
                        item.Destroy()
                    elif isinstance(item, aui.AuiSingleDockingGuide):
                        item.Destroy()
                    elif isinstance(item, aui.AuiDockingHintWindow):
                        item.Destroy()
                    elif isinstance(item, wx.Dialog):
                        item.Destroy()
                    item.Close()
        self.Destroy()


class ModelView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        #Canvas.ObjectHit()
        t = wx.StaticText(self, -1, "This view shows relevant model information.", (60,60))



        self.contents = wx.html2.WebView.New(self)



        #self.contents = wx.html.HtmlWindow (self, style=wx.TE_MULTILINE | wx.HSCROLL | wx.TE_READONLY)
        #self.contents.SetPage("New Text")



        sizer = wx.BoxSizer()
        sizer.Add(self.contents, 1, wx.ALL|wx.EXPAND, 5)
        parent.SetSizer(sizer)
        self.SetSizerAndFit(sizer)

    def setText(self, value=None):
        self.contents.SetPage(value,"")

class LinkView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        t = wx.StaticText(self, -1, "This view shows relations between models.", (60,60))

class TimeSeries(wx.Panel):

    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        m_choice2Choices = ['From Database 1', 'From Database 2']
        self.m_choice2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choice2Choices, 0 )
        self.m_choice2.SetSelection( 0 )
        bSizer1.Add( self.m_choice2, 0, wx.ALL, 5 )

        self.Database = wx.grid.Grid( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        # Grid
        self.Database.CreateGrid( 5, 5 )
        self.Database.EnableEditing( True )
        self.Database.EnableGridLines( True )
        self.Database.SetGridLineColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )
        self.Database.EnableDragGridSize( False )
        self.Database.SetMargins( 0, 0 )

        # Columns
        self.Database.EnableDragColMove( False )
        self.Database.EnableDragColSize( True )
        self.Database.SetColLabelSize( 30 )
        self.Database.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )

        # Rows
        self.Database.EnableDragRowSize( True )
        self.Database.SetRowLabelSize( 80 )
        self.Database.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )

        # Label Appearance

        # Cell Defaults
        self.Database.SetDefaultCellAlignment( wx.ALIGN_LEFT, wx.ALIGN_TOP )
        bSizer1.Add( self.Database, 0, wx.ALL, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

    def __del__( self ):
        pass


class consoleOutput(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        log = wx.TextCtrl(self, -1, size=(100,100),
                          style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)

        # # Add widgets to a sizer
        sizer = wx.BoxSizer()
        sizer.Add(log, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)

        # redirect text here
        redir= RedirectText(log)
        sys.stdout=redir

        self.SetSizerAndFit(sizer)

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out=aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)