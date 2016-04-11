import os
import threading

import wx
import wx.html2
import time
import wx.lib.agw.aui as aui
from wx.lib.newevent import NewEvent
from wx.lib.pubsub import pub as Publisher

import environment
from LowerPanelView import viewLowerPanel
from coordinator.emitLogging import elog
from coordinator.engineManager import Engine
from gui import events
from gui.controller.CanvasCtrl import CanvasCtrl
from gui.controller.DirectoryCtrl import LogicDirectory
from gui.controller.NetcdfCtrl import NetcdfCtrl
from gui.controller.UserCtrl import UserCtrl
from gui.controller.ToolboxCtrl import LogicToolbox
from gui.controller.settingsCtrl import settingsCtrl
from ..controller.NetcdfDetailsCtrl import NetcdfDetailsCtrl
from utilities.gui import loadAccounts

import coordinator.users as users
# create custom events
wxCreateBox, EVT_CREATE_BOX = NewEvent()
wxStdOut, EVT_STDDOUT= NewEvent()
wxDbChanged, EVT_DBCHANGED= NewEvent()


class ViewEMIT(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title="Environmental Model Integration Project", pos=wx.DefaultPosition,
                          size=wx.Size(1200, 750), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.pnlDocking = wx.Panel(id=wx.ID_ANY, name='pnlDocking', parent=self, size=wx.Size(1200, 750),
                                   style=wx.TAB_TRAVERSAL)
        self.bnb = wx.Notebook(self.pnlDocking)
        lowerpanel = viewLowerPanel(self.bnb)

        self.parent = parent

        self.initMenu()

        # creating components
        self.Directory = LogicDirectory(self.pnlDocking)
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
                           BestSize(wx.Size(1000, 400))
        )

        self.m_mgr.AddPane(self.Directory,
                           aui.AuiPaneInfo().
                           Left().
                           Dock().
                           CloseButton(False).
                           MaximizeButton(False).
                           MinimizeButton(False).
                           PinButton(False).
                           BestSize(wx.Size(275, 400)).
                           Floatable(False).
                           Movable(False).
                           Show(show=False).Hide()
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
                           Show(show=True)
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
        ShowAll = self.view_menu.Append(wx.NewId(), '&Toolbox\tCtrl+A', 'Show all associated files', wx.ITEM_RADIO)
        ShowDir = self.view_menu.Append(wx.NewId(), '&Directory\tCtrl+D', 'Shows file directory', wx.ITEM_RADIO)
        separator = self.view_menu.Append(wx.NewId(), 'separate', 'separate', wx.ITEM_SEPARATOR)
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
        self.Bind(wx.EVT_MENU, self.onDirectory, ShowDir)
        self.Bind(wx.EVT_MENU, self.onAllFiles, ShowAll)
        self.Bind(wx.EVT_MENU, self.onConsole, MinimizeConsole)
        self.Bind(wx.EVT_MENU, self.defaultview, defaultview)

        # Data Menu Bindings
        self.Bind(wx.EVT_MENU, self.onAddCsvFile, add_file)
        self.Bind(wx.EVT_MENU, self.onAddNetcdfFile, add_netcdf)
        self.Bind(wx.EVT_MENU, self.onOpenDapViewer, open_dap_viewer)


    def checkUsers(self):
        return
        # user_path = os.environ['APP_USER_PATH']
        # print user_path
        # if os.path.isfile(user_path):
        #     print loadAccounts()
        # else:
        #     # File does not exist so create
        #     open(user_path, "w")
        #     controller = UserCtrl(self)
        #     controller.Show()


        # if os.path.isfile(userPath) == False:
        #     file = open(userPath, 'w+')
        #     controller = UserCtrl(self)
        #     controller.CenterOnScreen()
        #     controller.Show()
        # else:
        #     # users = self.loadAccounts()
        #     users = loadAccounts()
        #     if len(users) < 1:
        #         controller = UserCtrl(self)
        #         controller.CenterOnScreen()
        #         controller.Show()
        #
        # # users = self.loadAccounts()
        # users = loadAccounts()
        # userAdded = False
        # no = False
        # if len(users) > 0:
        #     userAdded = True
        # while userAdded == False:# and no == False:
        #
        #     # users = self.loadAccounts()
        #     users = loadAccounts()
        #     if len(users) == 0 and no == False:
        #         dial = wx.MessageDialog(None, 'You must add a user to continue', 'Question',
        #             wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        #         if dial.ShowModal() == wx.ID_NO:
        #             pid = os.getpid()
        #             #os.system("kill -9 " + pid)
        #             no = True
        #         else:
        #             controller = UserCtrl(self)
        #             controller.CenterOnScreen()
        #             controller.Show()
        #     else:
        #         userAdded = True
        #         self.onClose(None)

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
        netcdf = NetcdfCtrl(self)

    def defaultview(self, event):
        """
        Restore previously saved perspective
        """
        self.m_mgr.LoadPerspective(self._default_perspective)


    def _postStart(self):
        # Starts stuff after program has initiated
        self.Canvas.ZoomToFit(event=None)

    def __del__(self):
        self.m_mgr.UnInit()

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

        settings = settingsCtrl()
        # settings.show()

        # settings = viewMenuBar()
        # settings.Show()

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

    def onDirectory(self, event):
        ToolboxPane = self.m_mgr.GetPane(self.Toolbox)
        ToolboxPane.Hide()
        DirectoryPane = self.m_mgr.GetPane(self.Directory)
        DirectoryPane.Show(show=True)
        self.m_mgr.Update()
        pass

    def onAllFiles(self, event):
        DirectoryPane = self.m_mgr.GetPane(self.Directory)
        DirectoryPane.Hide()
        ToolboxPane = self.m_mgr.GetPane(self.Toolbox)
        ToolboxPane.Show(show=True)
        self.m_mgr.Update()
        pass

    def onConsole(self, event):
        ConsolePane = self.m_mgr.GetPane(self.bnb)
        if event.Selection == 0:
            ConsolePane.Show(show=True)
        if event.Selection == 1:
            ConsolePane.Hide()
        self.m_mgr.Update()
        pass

class ModelView(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.contents = wx.html2.WebView.New(self)
        sizer = wx.BoxSizer()
        sizer.Add(self.contents, 1, wx.ALL|wx.EXPAND, 5)
        parent.SetSizer(sizer)
        self.SetSizerAndFit(sizer)

    def setText(self, value=None):
        self.contents.SetPage(value, "")


class viewMenuBar(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=-1, title="Settings...", pos=wx.DefaultPosition, size=wx.Size(350, 250))

        self.panel = wx.Panel(self)

        sizer = wx.BoxSizer(wx.VERTICAL)

        console_title = wx.StaticText(self.panel, id=wx.ID_ANY, label="Configure Console Verbosity",pos=(20, 100))
        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        console_title.SetFont(font)

        self.c1 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Info Messages")
        self.c2 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Warning Messages")
        self.c3 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Critical Messages")
        self.c4 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Error Messages")
        self.c5 = wx.CheckBox(self.panel, id=wx.ID_ANY, label="Show Debug Messages")

        self.c1.SetValue(int(os.environ['LOGGING_SHOWINFO']))
        self.c2.SetValue(int(os.environ['LOGGING_SHOWWARNING']))
        self.c3.SetValue(int(os.environ['LOGGING_SHOWCRITICAL']))
        self.c4.SetValue(int(os.environ['LOGGING_SHOWERROR']))
        self.c5.SetValue(int(os.environ['LOGGING_SHOWDEBUG']))

        self.saveButton = wx.Button(self.panel, 1, 'Save')

        sizer.Add(console_title, .1, flag=wx.ALL | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c1, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c2, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c3, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c4, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.c5, 0, flag=wx.LEFT | wx.ALIGN_LEFT, border=20)
        sizer.Add(self.saveButton, 1, flag=wx.RIGHT | wx.ALIGN_RIGHT, border=20)

        self.Bind(wx.EVT_BUTTON, self.OnSave, id=1)

        self.panel.SetSizer(sizer)
        self.Layout()
        self.Refresh()
        self.Show()

    def OnSave(self, event):
        chkvalues = self.getCheckboxValue()
        infchk = int(chkvalues['info'])
        wrnchk = int(chkvalues['warn'])
        crtchk = int(chkvalues['critical'])
        debchk = int(chkvalues['debug'])
        errchk = int(chkvalues['error'])


        environment.setEnvironmentVar('LOGGING', 'showinfo', infchk)
        environment.setEnvironmentVar('LOGGING', 'showwarning', wrnchk)
        environment.setEnvironmentVar('LOGGING', 'showcritical', crtchk)
        environment.setEnvironmentVar('LOGGING', 'showdebug', debchk)
        environment.setEnvironmentVar('LOGGING', 'showerror', errchk)

        elog.info('Verbosity Settings Saved')

        self.Close()

    def getCheckboxValue(self):
        '''
        Get the checked status for each verbosity checkbox
        :return: dictionary of Booleans, e.g {'info':True, }
        '''

        info = self.c1.GetValue()
        warn = self.c2.GetValue()
        critical = self.c3.GetValue()
        error = self.c4.GetValue()
        debug = self.c5.GetValue()
        cb = {'info': info, 'warn': warn, 'critical': critical, 'error': error, 'debug': debug}
        return cb
