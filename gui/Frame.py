__author__ = 'Mario'

import wx
import wx.xrc
import wx.aui

from CanvasView import Canvas
from CanvasLogic import CanvasLogic
from DirectoryView import DirectoryCtrlView



# ##########################################################################
# # Class MainFrame
# ##########################################################################

class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        print "filename: {2} x: {0} y: {1}".format(x,y, filenames)

        #Canvas = NC.NavCanvas(self, -1, size=wx.DefaultSize).Canvas
        #Canvas.AddRectangle((110, 10), (100, 100), FillColor='Red')
        print x,y
        originx, originy = self.window.Canvas.PixelToWorld((0,0))
        #ar = self.window.Canvas.ScreenPosition
        #x-= ar[0]
        x = x +originx
        y = originy - y
        #x, y = self.window.Canvas.WorldToPixel((nx,ny))
        #print x,y
        #x = y = 0
        self.window.createBox(filepath=filenames.pop(), xCoord=x, yCoord=y)
        self.window.Canvas.Draw()


class MainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                          size=wx.Size(1500, 600), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.initAUIManager()
        self.initSystem()
        self.initMenu()
        self.Bind(wx.EVT_CLOSE, self.onClose)


    def initSystem(self):
        self.canvasLogic = CanvasLogic(Canvas=self.canvas)

    def initAUIManager(self):
        self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(605, 458),
                                   style=wx.TAB_TRAVERSAL)

        self.m_mgr = wx.aui.AuiManager()
        self.m_mgr.SetManagedWindow(self.pnlDocking)
        self.m_mgr.SetFlags(wx.aui.AUI_MGR_DEFAULT)

        self.m_directoryCtrl = DirectoryCtrlView(self.pnlDocking)
        self.m_mgr.AddPane(self.m_directoryCtrl,
                           wx.aui.AuiPaneInfo().Left().CloseButton(False).MaximizeButton(True).MinimizeButton(
                               True).PinButton(True).Resizable().MinSize(wx.Size(375,500)).Floatable())

        self.canvas = Canvas(parent=self.pnlDocking, ProjectionFun=None, Debug=0, BackgroundColor="White", )
        self.m_mgr.AddPane(self.canvas,
                           wx.aui.AuiPaneInfo().Center().Name("Canvas").Position(0).CloseButton(False).MaximizeButton(
                               True).MinimizeButton(True).PinButton(True).Resizable().Floatable().Movable().MinSize(
                               wx.Size(1000, 400)))

        self.m_mgr.Update()

        ## Drag and drop
        dt = FileDrop(self.canvas)
        self.canvas.SetDropTarget(dt)



    def initMenu(self):
        ## Menu stuff
        self.m_statusBar2 = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)

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
        self.canvas.ZoomToFit(Event=None)

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


class SimpleFrame(MainFrame):
    def __init__(self, parent):
        MainFrame.__init__(self, parent)

if __name__ == '__main__':
    app = wx.App(False)
    frame = SimpleFrame(None)
    frame.Show(True)

    app.MainLoop()
