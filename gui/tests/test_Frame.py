__author__ = 'Mario'

from ..Frame import SimpleFrame
import wx
class TestFrame():

    def setup(self):
        app = wx.App(False)
        self.frame = SimpleFrame(None)
        assert self.frame
        self.frame.Show(True)
        assert self.frame.IsShown()

    def test_initSystem(self):
        assert self.frame
        assert self.frame.canvasLogic
        self.frame.Destroy()

    def test_initAUIManager(self):
        assert self.frame.pnlDocking
        assert self.frame.m_mgr
        assert self.frame.m_directoryCtrl
        assert self.frame.canvas
        self.frame.Destroy()

    def test_initMenu(self):
        assert self.frame
        assert self.frame.m_statusBar2
        assert self.frame.m_menubar
        assert self.frame.m_fileMenu
        assert self.frame.m_toolMenu
        assert self.frame.m_viewMenu

    def teardown(self):
        assert self.frame
        self.frame.Destroy()
        self.frame.onClose(event=None)




