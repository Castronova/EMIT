import os
import sqlite3 as lite
import sys

import coordinator.engineAccessors as engine
from gui.views.EMITView import ViewEMIT
from sprint import *

# todo: the connections file should be a binary object (pickle)

class EMITCtrl(ViewEMIT):
    def __init__(self, parent):


        ViewEMIT.__init__(self, parent)
        self.FloatCanvas = self.Canvas.FloatCanvas

        # connect to known databases
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/connections'))
        script_path = os.path.abspath(os.path.join(currentdir, "../../app_data/db/.dbload"))
        filepath = os.path.abspath(os.path.join(currentdir, "../../app_data/db/local.db"))

        # change file paths if app is running as installed package
        if getattr(sys, 'frozen', False):
            connections_txt = os.path.join(sys._MEIPASS, 'data/connections')
            filepath = os.path.join(sys._MEIPASS, 'app_data/db/local.db')
            script_path = os.path.join(sys._MEIPASS, "app_data/db/.dbload")

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
        engine.connectToDb(title='ODM2 SQLite (local)',desc='Local SQLite database',engine='sqlite',address=filepath, name=None, user=None, pwd=None)

        self.checkUsers()

    def refreshUserAccount(self):
        self.accounts = self.loadAccounts()

def removedb(file):
    try:
        os.remove(file)
    except OSError:
        pass
