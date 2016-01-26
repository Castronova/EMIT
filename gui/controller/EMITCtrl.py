import os
import sqlite3 as lite
import sys

import coordinator.engineAccessors as engine
from gui.views.EMITView import ViewEMIT


class EMITCtrl(ViewEMIT):
    def __init__(self, parent):


        ViewEMIT.__init__(self, parent)
        self.FloatCanvas = self.Canvas.FloatCanvas
        # todo: the connections file should be a binary object (pickle)
        # connect to known databases
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/connections'))
        script_path = os.path.join(os.path.abspath(__file__), "app_data/db/.dbload")
        
        # todo: this path should come from the app settings file, not hardcoded
        filepath = os.getcwd() + "/app_data/db/local.db" # The path of where the database is create
        if getattr(sys, 'frozen', False):
            connections_txt = os.path.join(sys._MEIPASS, 'data/connections')
            filepath = os.path.join(sys._MEIPASS, 'app_data/db/local.db')
            script_path = os.path.join(sys._MEIPASS, "app_data/db/.dbload")

        # create db directory if it doesn't exist
#        db_dirpath = os.path.dirname(filepath)
#        if not os.path.exists(db_dirpath):
#            os.mkdir(db_dirpath)

        engine.connectToDbFromFile(dbtextfile=connections_txt)
        
        # if the database is not found in the dir (dev mode) or app (install mode), create it
        if not os.path.exists(filepath):

        # # fixme: will this always recreate the database, because that is not what we want
        # removedb(filepath)  # Its going to delete the file, than recreate it to avoid errors

            # todo: only do this if the database doesn't exist
            conn = lite.connect(filepath)
            script = open(script_path) 
            with conn:
                cur = conn.cursor()
                cur.executescript(script.read())
            script.close()

        # load the local database into the engine
        engine.connectToDb(title='ODM2 SQLite (local)',desc='Local SQLite database',engine='sqlite',address=filepath, name=None, user=None, pwd=None)

        self.checkUsers()

    def refreshUserAccount(self):
        #self.account_combo.Clear()
        self.accounts = self.loadAccounts()

def removedb(file):
    try:
        os.remove(file)
    except OSError:
        pass
