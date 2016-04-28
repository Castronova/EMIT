import os
import threading

import wx
import wx.html2
import wx.lib.agw.aui as aui
from wx.lib.newevent import NewEvent
from wx.lib.pubsub import pub as Publisher

import environment
from LowerPanelView import ViewLowerPanel
from coordinator.engineManager import Engine
from emitLogging import elog
from gui import events
from gui.controller.CanvasCtrl import CanvasCtrl
from gui.controller.NetcdfCtrl import NetcdfCtrl
from gui.controller.ToolboxCtrl import LogicToolbox
from gui.controller.UserCtrl import UserCtrl
from gui.controller.settingsCtrl import settingsCtrl
from ..controller.NetcdfDetailsCtrl import NetcdfDetailsCtrl

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

        self.initMenu()

        # creating components
        self.Toolbox = LogicToolbox(self.pnlDocking)
        self.Canvas = CanvasCtrl(self.pnlDocking)

        self.Toolbox.Hide()
        self.initAUIManager()
        self._init_sizers()

        self.filename = None
        self.loadingpath = None

        self.Center()

        self.Show()

        self.defaultLoadDirectory = os.getcwd() + "/models/MyConfigurations/"


    def refreshUserAccount(self):
        # This method is here because AddNewUserDialog.on_ok looks for this method at the end of the function
        # The refresh was implemented so the pre-run dialog user account box would refresh after adding new user
        return

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

        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnSelect)
        self.Bind(wx.EVT_CLOSE, self.onClose)

        self.m_mgr.Update()

        self._default_perspective = self.m_mgr.SavePerspective()

    def OnSelect(self, event):

        try:
            # update databases in a generic way
            selected_page = self.bnb.GetPage(event.GetSelection())
            if len(selected_page.connection_combobox.GetItems()) == 0:
                 selected_page.refreshConnectionsListBox()

        except: pass

    def initMenu(self):
        # Menu stuff

        self._menubar = wx.MenuBar()

        self.file_menu = wx.Menu()
        Load = self.file_menu.Append(wx.NewId(), '&Load\tCtrl+O', 'Load Configuration')
        Save = self.file_menu.Append(wx.NewId(), '&Save Configuration\tCtrl+S', 'Save Configuration')
        AddUser = self.file_menu.Append(wx.NewId(), 'Add User', 'Add New User')
        SaveAs = self.file_menu.Append(wx.NewId(), '&Save Configuration As', 'Save Configuration')
        Settings = self.file_menu.Append(wx.NewId(), "Settings...")
        exit = self.file_menu.Append(wx.NewId(), '&Quit\tCtrl+Q', 'Quit application')


        self._menubar.Append(self.file_menu, "&File")

        self.m_toolMenu = wx.Menu()


        self.view_menu = wx.Menu()
        self.view_menu.Append(wx.NewId(), '&Toolbox\tCtrl+A', 'Show all associated files', wx.ITEM_RADIO)
        self.view_menu.Append(wx.NewId(), 'separate', 'separate', wx.ITEM_SEPARATOR)
        MinimizeConsole = self.view_menu.Append(wx.NewId(), '&Console Off', 'Minimizes the Console', wx.ITEM_CHECK)

        defaultview = self.view_menu.Append(wx.NewId(), '&Restore Default View', 'Returns the view to the default (initial) state', wx.ITEM_NORMAL)

        self._menubar.Append(self.view_menu, "&View")

        self.data_menu = wx.Menu()
        self._menubar.Append(self.data_menu, "Data")
        add_file = self.data_menu.Append(wx.NewId(), "&Add CSV File")
        # todo: implement and enable the CSV menu option below
        add_file.Enable(False)
        add_netcdf = self.data_menu.Append(wx.NewId(), '&Add NetCDF')

        open_dap_viewer = self.data_menu.Append(wx.NewId(), "&OpenDap Explorer")

        self.SetMenuBar(self._menubar)

        wx.CallAfter(self._postStart)

        # Events
        # View Option Bindings
        self.Bind(wx.EVT_MENU, self.SaveConfiguration, Save)
        self.Bind(wx.EVT_MENU, self.SaveConfigurationAs, SaveAs)
        self.Bind(wx.EVT_MENU, self.LoadConfiguration, Load)
        self.Bind(wx.EVT_MENU, self.Settings, Settings)
        self.Bind(wx.EVT_MENU, self.onClose, exit)
        self.Bind(wx.EVT_MENU, self.onAddUser, AddUser)
        events.onSaveFromCanvas += self.SaveConfigurationAs

        # View Option Bindings
        self.Bind(wx.EVT_MENU, self.onConsole, MinimizeConsole)
        self.Bind(wx.EVT_MENU, self.defaultview, defaultview)

        # Data Menu Bindings
        self.Bind(wx.EVT_MENU, self.onAddCsvFile, add_file)
        self.Bind(wx.EVT_MENU, self.onAddNetcdfFile, add_netcdf)
        self.Bind(wx.EVT_MENU, self.onOpenDapViewer, open_dap_viewer)

    def onAddCsvFile(self, event):
        file_dialog = wx.FileDialog(self.Parent,
                                    message="Add *.csv file",
                                    defaultDir=os.getcwd(),
                                    defaultFile="",
                                    wildcard=" CSV File (*.csv)|*.csv", style=wx.FD_OPEN)

        if file_dialog.ShowModal() == wx.ID_OK:
            path = file_dialog.GetPath()

    def onAddUser(self, event):
        controller = UserCtrl(self)
        controller.CenterOnScreen()
        controller.Show()

    def onAddNetcdfFile(self, event):
        file_dialog = wx.FileDialog(self.Parent,
                                    message="Add *.nc file",
                                    defaultDir=os.getcwd(),
                                    defaultFile="",
                                    wildcard="NetCDF File(*.nc)|*.nc", style=wx.FD_OPEN)

        # if a file is selected
        if file_dialog.ShowModal() == wx.ID_OK:
            path = file_dialog.GetPath()
            filename = file_dialog.GetFilename()
            NetcdfDetailsCtrl(self.Parent, path, filename)

    def onClose(self, event):
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if event == None or dial.ShowModal() == wx.ID_YES:

            # kill multiprocessing
            e = Engine()
            msg = e.close()
            elog.debug('Closing Engine Processes: %s' % msg)


            # kill all threads

            threads = {t.name:t for t in threading.enumerate()}
            mainthread = threads.pop('MainThread')

            elog.debug('Closing EMIT Threads: %s' % msg)

            non_daemon = []
            for t in threads.itervalues():

                # check if the thread is a daemon, if so, it should not cause any problems
                if t.isDaemon():
                    elog.debug('%s daemon=%s' %(t.name, t.isDaemon()))
                else:
                    # add this thread to the non-daemon list
                    non_daemon.append(t)

            for t in non_daemon:
                elog.warning('%s is not a daemon thread and may cause problems while shutting down' % t.name)
                t.join(1)

            # determine if there are any non-daemon threads that are still alive
            non_daemon_and_alive = []
            for t in threads.itervalues():
                if not t.isDaemon() and t.isAlive():
                    non_daemon_and_alive.append(t)

            # attempt to stop non-daemon threads
            try:
                for t in non_daemon_and_alive:
                    t._Thread__stop()
            except Exception, e:
                elog.error('Error encountered closing thread %s: %s' % (t.name, e))

            # close the main thread
            self.Destroy()
            wx.App.ExitMainLoop
            wx.WakeUpMainThread

    def onOpenDapViewer(self, event):
        NetcdfCtrl(self.Canvas.GetTopLevelParent())

    def defaultview(self, event):
        """
        Restore previously saved perspective
        """
        self.m_mgr.LoadPerspective(self._default_perspective)


    def _postStart(self):
        # Starts stuff after program has initiated
        self.Canvas.ZoomToFit(event=None)

    def LoadConfiguration(self,event):

        openFileDialog = wx.FileDialog(self, message="Load New File", defaultDir=self.defaultLoadDirectory, defaultFile="",
                                       wildcard="Simulation Files (*.sim)|*.sim|MDL Files (*.mdl)|*.mdl", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:
            filename = openFileDialog.GetFilename()
            elog.info("Filename is: " + filename)
            # proceed loading the file chosen by the user
            # this can be done with e.g. wxPython input streams:
            filepath = (openFileDialog.GetPath())
            try:
                Publisher.sendMessage('SetLoadPath',file=filepath)  # send message to canvascontroller
            except:
                elog.error("Could not load file")

            self.filename = openFileDialog.GetFilename()
            self.loadingpath = filepath
            self.defaultLoadDirectory = os.path.dirname(filepath)

    def Settings(self, event):
        settingsCtrl(self.Canvas.GetTopLevelParent())

    def SaveConfiguration(self,event):
        if self.loadingpath == None:
            save = wx.FileDialog(self.Canvas.GetTopLevelParent(), "Save Configuration","","",
                                 "Simulation Files (*.sim)|*.sim", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

            if save.ShowModal() == wx.ID_OK:
                self.save_path = save.GetPath() + ".sim"
            else:
                save.Destroy()

            Publisher.sendMessage('SetSavePath',path=save.GetPath()) #send message to canvascontroller.SaveSimulation

            self.loadingpath = save.GetPath()
        else:
            Publisher.sendMessage('SetSavePath', path=self.loadingpath)

    def SaveConfigurationAs(self,event):
        # Executes from File ->Save As
        save = wx.FileDialog(self.Canvas.GetTopLevelParent(), message="Save Configuration",
                             defaultDir=self.defaultLoadDirectory, defaultFile="",
                             wildcard="Simulation Files (*.sim)|*.sim", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if save.ShowModal() == wx.ID_OK:
            self.save_path = save.GetPath()
            if self.save_path[-4] != '.':  # check if extension was added
                self.save_path += '.sim'
            self.loadingpath = self.save_path
            self.defaultLoadDirectory = os.path.dirname(self.loadingpath)
            Publisher.sendMessage('SetSavePath',path=self.save_path) #send message to canvascontroller.SaveSimulation
            txt = save.Filename.split('.sim')[0]
            e = dict(cat=self.Toolbox.cat, txt=txt, fullpath=save.Path)
            events.onSimulationSaved.fire(**e)  # calls loadSIMFile from logicToolBox
            self.Toolbox.RefreshToolbox()
        else:
            save.Destroy()

    def onConsole(self, event):
        ConsolePane = self.m_mgr.GetPane(self.bnb)
        if event.Selection == 0:
            ConsolePane.Show(show=True)
        if event.Selection == 1:
            ConsolePane.Hide()
        self.m_mgr.Update()
