__author__ = 'Mario'

import os
import wx
from gui.views.viewEMIT import ViewEMIT
import coordinator.engineAccessors as engine
import sqlite3 as lite
# from gui.controller.logicFileDrop import LogicFileDrop
# import pyspatialite.dbapi2 as sqlite3
from environment import env_vars
# from ODM2PythonAPI.src.api.ODMconnection import dbconnection

class LogicEMIT(ViewEMIT):
    def __init__(self, parent):
        import threading
        print "before", threading.activeCount()
        # print threading.enumerate()
        ViewEMIT.__init__(self, parent)
        self.FloatCanvas = self.Canvas.FloatCanvas

        # todo: the connections file should be a binary object (pickle)
        # connect to known databases
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/connections'))
        engine.connectToDbFromFile(dbtextfile=connections_txt)

        # todo: Delete this
        # engine.createSQLiteInMemory()
        # Create or connect to local database, create local folder in db
        db_path = os.path.abspath(os.path.join(currentdir, '../../db/local.db'))
        env_vars.set_environment_variable('LOCAL_DB', 'PATH', db_path)

        # if os.path.exists(env_vars.LOCAL_DB_PATH):
        #     odm2_db = sqlite3.connect(db_path)
        #
        # elif os.path.exists(env_vars.LOCAL_DB_PATH+"/local.db"):
        #     odm2_db = sqlite3.connect(db_path)
        # else:
        #     # Create local.db
        #     odm2_db = sqlite3.connect(env_vars.LOCAL_DB_PATH+"/local.db")
        #     empty_dump_script = open(env_vars.LOCAL_DB_PATH+".dbload",'r').read()
        #     odm2_db.executescript(empty_dump_script)

        # todo: this path should come from the app settings file, not hardcoded
        filepath = os.getcwd() + "/app_data/db/local.db" # The path of where the database is created

        if not os.path.exists(filepath):

        # # fixme: will this always recreate the database, because that is not what we want
        # removedb(filepath)  # Its going to delete the file, than recreate it to avoid errors

            # todo: only do this if the database doesn't exist
            conn = lite.connect(filepath)
            script = open(os.getcwd() + "/app_data/db/.dbload")
            with conn:
                cur = conn.cursor()
                cur.executescript(script.read())
            script.close()

        # load the local database into the engine
        engine.connectToDb(title='ODM2 SQLite (local)',desc='Local SQLite database',engine='sqlite',address=filepath, name=None, user=None, pwd=None)


def removedb(file):
    try:
        os.remove(file)
    except OSError:
        pass
