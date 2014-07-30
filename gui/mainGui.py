__author__ = 'Mario'
import wx
import wx.grid as grid
#import wx.html
import wx.html2
from DirectoryView import DirectoryCtrlView
import sys
from CanvasView import Canvas
from wx.lib.pubsub import pub as Publisher
import wx.lib.agw.ultimatelistctrl as ULC
from ObjectListView.ObjectListView import FastObjectListView

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

        #redir= RedirectText(self.output)
        #sys.stdout=redir

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
                               True).MinimizeButton(True).MinimizeButton( True ).PinButton(True).Resizable().Floatable(True).MinSize(
                               wx.Size(1000, 400)))

        self.m_mgr.AddPane(self.output,
                          wx.aui.AuiPaneInfo().Caption('Python Console').Center().Name("Console").CloseButton(False).MaximizeButton(
                               True).Movable().MinimizeButton(True).PinButton(True).Resizable().Floatable().MinSize(
                               wx.Size(1000, 200)))

        self.m_mgr.AddPane(self.nb,
                   wx.aui.AuiPaneInfo().Left().CloseButton(False).MaximizeButton(True).MinimizeButton(
                    True ).PinButton(True).Resizable().MinSize(wx.Size(375,500)).Floatable().FloatingSize(size=(600, 800)).CloseButton(
                    True))

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
        bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        bSizer1.SetMinSize( wx.Size( 400, 300))
        bSizer2.SetMinSize( wx.Size( -1, 40))
        bSizer3.SetMinSize( wx.Size( -1, 350))

        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )
        bSizer1.Add( bSizer3, 1, wx.EXPAND, 5 )

        self.m_choice2Choices = []

        self.m_choice2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.m_choice2Choices, 0 )
        self.m_choice2.SetSelection( 0 )
        bSizer2.Add( self.m_choice2, 0, wx.ALL, 5 )

        self.m_button1 = wx.Button( self, wx.ID_ANY, u"Add Connection", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )
        self.m_button1.Bind(wx.EVT_LEFT_DOWN, self.AddConnection)

        # self.list = ULC.UltimateListCtrl(self, wx.ID_ANY, agwStyle=wx.LC_REPORT | wx.LC_VRULES | wx.LC_HRULES | wx.LC_SINGLE_SEL)
        #
        # self.list.InsertColumn(0, "Column 1")
        # self.list.InsertColumn(1, "Column 2")
        #
        # index = self.list.InsertStringItem(sys.maxint, "Item 1")
        # self.list.SetStringItem(index, 1, "Sub-item 1")
        #
        # index = self.list.InsertStringItem(sys.maxint, "Item 2")
        # self.list.SetStringItem(index, 1, "Sub-item 2")
        #
        # choice = wx.Choice(self.list, -1, choices=["one", "two"])
        # index = self.list.InsertStringItem(sys.maxint, "A widget")
        #
        # self.list.SetItemWindow(index, 1, choice, expand=True)
        #
        # bSizer3.Add(self.list, 1, wx.EXPAND)

        

        self.SetSizer( bSizer1 )
        self.Layout()



    def AddConnection(self, event):

        dlg = AddConnectionDialog(self, -1, "Sample Dialog", size=(350, 200),
                         style=wx.DEFAULT_DIALOG_STYLE,
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        params = dlg.getConnectionParams()

        dlg.Destroy()
        Publisher.sendMessage('DatabaseConnection', params)


        # dlg = wx.TextEntryDialog(
        #         self, 'Please enter connection information below: ',
        #         'Database Connection', 'Python')
        #
        # dlg.SetValue("")
        #
        # connectionstring = dlg.GetValue()



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

class AddConnectionDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition,
            style=wx.DEFAULT_DIALOG_STYLE,
            ):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)

        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Database Connection")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Engine :")
        label.SetHelpText("Database Parsing Engine (e.g. mysql, psycopg2, etc)")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.engine = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.engine, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        #d['engine'],d['address'],d['db'],d['user'],d['pwd']


        label = wx.StaticText(self, -1, "Address :")
        label.SetHelpText("Database Address")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.address = wx.TextCtrl(self, -1, "", size=(80,-1))
        box.Add(self.address, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        #d['engine'],d['address'],d['db'],d['user'],d['pwd']


        label = wx.StaticText(self, -1, "Name :")
        label.SetHelpText("Database Name")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.name = wx.TextCtrl(self, -1, "", size=(80,-1))

        box.Add(self.name, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        #d['engine'],d['address'],d['db'],d['user'],d['pwd']


        label = wx.StaticText(self, -1, "User :")
        label.SetHelpText("Database Username")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.user = wx.TextCtrl(self, -1, "", size=(80,-1))

        box.Add(self.user, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)
        #d['engine'],d['address'],d['db'],d['user'],d['pwd']


        label = wx.StaticText(self, -1, "Password :")
        label.SetHelpText("Database Password")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.password = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.password.SetHelpText("Here's some help text for field #2")
        box.Add(self.password, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)



        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()

        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)

        self.btnok = wx.Button(self, wx.ID_OK)
        self.btnok.SetDefault()
        btnsizer.AddButton(self.btnok)
        self.btnok.Disable()

        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)


        self.engine.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.address.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.name.Bind(wx.EVT_TEXT, self.OnTextEnter)
        self.user.Bind(wx.EVT_TEXT, self.OnTextEnter)


    def getConnectionParams(self):
        return self.engine.GetValue(), self.address.GetValue(), self.name.GetValue(), self.user.GetValue(), self.password.GetValue()

    def OnTextEnter(self, event):
        if self.engine.GetValue() == '' or \
                self.address.GetValue() == '' or  \
                self.name.GetValue() == '' or  \
                self.user.GetValue() == '':
            self.btnok.Disable()
        else:
            self.btnok.Enable()
