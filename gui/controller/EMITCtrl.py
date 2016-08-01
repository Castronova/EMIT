from gui.views.EMITView import EMITView
from sprint import *
from utilities import gui
import wx
from gui import events
from coordinator.engineManager import Engine
import coordinator.engineAccessors as engine
from emitLogging import elog
import threading
from gui.controller.NetcdfCtrl import NetcdfCtrl
from gui.controller.UserCtrl import UserCtrl
from ..controller.NetcdfDetailsCtrl import NetcdfDetailsCtrl
from gui.controller.ModelInputPromptCtrl import ModelInputPromptCtrl
from gui.controller.SettingsCtrl import SettingsCtrl


class EMITCtrl(EMITView):
    def __init__(self, parent):

        EMITView.__init__(self, parent)
        self.FloatCanvas = self.Canvas.FloatCanvas
        connections_txt = os.environ['APP_CONNECTIONS_PATH']
        self.local_db_path = os.environ['APP_LOCAL_DB_PATH']
        self.loading_path = None

        if "APP_DEFAULT_SAVE_PATH" in os.environ:
            self.defaultLoadDirectory = os.environ["APP_DEFAULT_SAVE_PATH"]
        else:
            self.defaultLoadDirectory = os.getcwd() + "/models/MyConfigurations/"
            environment.setEnvironmentVar("APP", "default_save_path", self.defaultLoadDirectory)

        # load databases threaded
        t = threading.Thread(target=self.connect_to_databases, name='Connect_To_Databases', args=(connections_txt,))
        t.setDaemon(True)
        t.start()

        self.check_users_json()

        # File Option Bindings
        self.Bind(wx.EVT_MENU, self.on_load_configuration, self._load)
        self.Bind(wx.EVT_MENU, self.on_add_user, self._add_user_menu)
        self.Bind(wx.EVT_MENU, self.on_save_configuration, self._save_menu)
        self.Bind(wx.EVT_MENU, self.on_save_configuration_as, self.save_as_menu)
        self.Bind(wx.EVT_MENU, self.on_settings, self._settings_menu)
        self.Bind(wx.EVT_MENU, self.on_close, self._exit)

        # View Option Bindings
        self.Bind(wx.EVT_MENU, self.on_toggle_console, self._toggle_console_menu)
        self.Bind(wx.EVT_MENU, self.on_toggle_toolbar, self._toggle_toolbar_menu)
        self.Bind(wx.EVT_MENU, self.on_default_view, self._default_view_menu)

        # Data Menu Bindings
        self.Bind(wx.EVT_MENU, self.on_add_csv_file, self._add_file)
        self.Bind(wx.EVT_MENU, self.on_add_net_cdf_file, self._add_netcdf)
        self.Bind(wx.EVT_MENU, self.on_open_dap_viewer, self._open_dap_viewer_menu)
        # All other bindings
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.on_switch_lower_panel_tab)
        self.Bind(wx.EVT_CLOSE, self.on_close)
        events.onSaveFromCanvas += self.on_save_configuration_as

    def on_toggle_toolbar(self, event):
        pane = self.m_mgr.GetPane(self.Toolbox)
        if event.Selection == 0:
            pane.Show(show=True)
        if event.Selection == 1:
            pane.Hide()
        self.m_mgr.Update()

    def model_input_prompt(self, path):
        ModelInputPromptCtrl(self, path)

    def check_users_json(self):
        UserCtrl.create_user_json()
        if UserCtrl.is_user_json_empty():
            controller = UserCtrl(self)
            controller.CenterOnScreen()
            controller.Show()

    def connect_to_databases(self, connections_txt):
        # connect to databases defined in the connections file
        dbs = gui.read_database_connection_from_file(connections_txt)
        for db in dbs:
            usr, pwd = self.decrypt_db_username_password(db['username'], db['password'])
            if usr is not None:
                engine.connectToDb(db['name'],db['description'],db['engine'],db['address'],db['database'],usr,pwd)
            else:
                msg = 'Could not resolve database username for %s/%s.  Make sure secret.py is created correcly.' % (db['address'], db['database'])
                sPrint(msg, MessageType.ERROR)

        # load the local database into the engine
        engine.connectToDb(title='ODM2 SQLite (local)', desc='Local SQLite database',
                           engine='sqlite', address=self.local_db_path,
                           dbname=None, user=None,
                           pwd=None, default=True)

    def decrypt_db_username_password(self, uhash, phash):
        """
        decrypts database username and password that is stored in connections.txt using secret key (secret.py) and AES encryption
        Args:
            uhash: encrypted username hash
            phash: encrypted password hash

        Returns: decrypted username (or None), decrypted password

        """

        import secret
        import encrypt
        cipher = encrypt.AESCipher(secret.key)
        usr = cipher.decrypt(uhash) or None
        pwd = cipher.decrypt(phash)
        return usr, pwd

    ##################################
    # EVENTS
    ##################################

    def on_add_csv_file(self, event):
        file_dialog = wx.FileDialog(self.Parent,
                                    message="Add *.csv file",
                                    defaultDir=os.getcwd(),
                                    defaultFile="",
                                    wildcard=" CSV File (*.csv)|*.csv", style=wx.FD_OPEN)

        if file_dialog.ShowModal() == wx.ID_OK:
            path = file_dialog.GetPath()

    def on_add_net_cdf_file(self, event):
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

    def on_add_user(self, event):
        controller = UserCtrl(self)
        controller.CenterOnScreen()
        controller.Show()

    def on_close(self, event):
        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        dial.SetYesNoLabels(yes="Quit", no="Cancel")
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

    def on_default_view(self, event):
        """
        Restore previously saved perspective
        """
        self.m_mgr.LoadPerspective(self._default_perspective)

    def on_open_dap_viewer(self, event):
        NetcdfCtrl(self.Canvas.GetTopLevelParent())

    def on_toggle_console(self, event):
        ConsolePane = self.m_mgr.GetPane(self.bnb)
        if event.Selection == 0:
            ConsolePane.Show(show=True)
        if event.Selection == 1:
            ConsolePane.Hide()
        self.m_mgr.Update()

    def on_load_configuration(self, event):
        file_dialog = wx.FileDialog(self, message="Load New File",
                                       defaultDir=self.defaultLoadDirectory,
                                       defaultFile="",
                                       wildcard="Simulation Files (*.sim)|*.sim|MDL Files (*.mdl)|*.mdl",
                                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if file_dialog.ShowModal() == wx.ID_OK:
            self.defaultLoadDirectory = os.path.dirname(file_dialog.GetPath())
            self.model_input_prompt(file_dialog.GetPath())
        file_dialog.Destroy()

    def on_save_configuration_as(self, event):

        print os.environ.get("APP_DEFAULT_SAVE_PATH")
        # Executes from File ->Save As
        save = wx.FileDialog(self.Canvas.GetTopLevelParent(), message="Save Configuration",
                             defaultDir=self.defaultLoadDirectory, defaultFile="",
                             wildcard="Simulation Files (*.sim)|*.sim", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if save.ShowModal() == wx.ID_OK:
            self.save_path = save.GetPath()
            if self.save_path[-4] != '.':  # check if extension was added
                self.save_path += '.sim'
            self.loading_path = self.save_path
            self.defaultLoadDirectory = os.path.dirname(self.loading_path)
            self.Canvas.save_simulation(self.save_path)
            txt = save.Filename.split('.sim')[0]
            e = dict(cat=self.Toolbox.cat, txt=txt, fullpath=save.Path)
            self.Toolbox.loadSIMFile(e)
            self.Toolbox.refresh_toolbox()
        save.Destroy()

    def on_save_configuration(self, event):
        if not self.loading_path:
            self.on_save_configuration_as(event)
            return
        self.Canvas.save_simulation(self.save_path)
        self.Toolbox.refresh_toolbox()

    def on_switch_lower_panel_tab(self, event):
        try:
            # update databases in a generic way
            selected_page = self.bnb.GetPage(event.GetSelection())
            if len(selected_page.connection_combobox.GetItems()) == 0:
                 selected_page.refreshConnectionsListBox()

        except: pass

    def on_settings(self, event):
        SettingsCtrl(self)


