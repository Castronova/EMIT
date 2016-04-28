import sqlite3 as lite
from gui.controller.UserCtrl import UserCtrl
import environment
import coordinator.engineAccessors as engine
from gui.views.EMITView import EMITView
from sprint import *


class EMITViewCtrl(EMITView):
    def __init__(self, parent):

        EMITView.__init__(self, parent)
        self.FloatCanvas = self.Canvas.FloatCanvas

        connections_txt = environment.getDefaultConnectionsTextPath()
        script_path = environment.getDefaultScriptPath()
        filepath = environment.getDefaultLocalDBPath()

        # connect to known databases
        # if the database is not found in the dir (dev mode) or app (install mode), create it
        if not os.path.exists(filepath):
            conn = lite.connect(filepath)
            script = open(script_path)
            with conn:
                cur = conn.cursor()
                cur.executescript(script.read())
            script.close()

        # connect to databases defined in the connections file
        engine.connectToDbFromFile(dbtextfile=connections_txt)

        # load the local database into the engine
        engine.connectToDb(title='ODM2 SQLite (local)',desc='Local SQLite database',engine='sqlite',address=filepath, name=None, user=None, pwd=None, default=True)
        self.check_users_json()

    def check_users_json(self):
        UserCtrl.create_user_json()
        if UserCtrl.is_user_json_empty():
            controller = UserCtrl(self)
            controller.CenterOnScreen()
            controller.Show()
