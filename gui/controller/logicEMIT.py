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
        ViewEMIT.__init__(self, parent)

        self.FloatCanvas = self.Canvas.FloatCanvas

        # connect to known databases
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/connections'))
        engine.connectToDbFromFile(dbtextfile=connections_txt)

        # engine.createSQLiteInMemory()
        # Create or connect to local database, create local folder in db
        # env_vars.set_environment_variable('LOCAL_DB_BASE', 'test')
        # db_path = os.path.abspath(os.path.join(currentdir, '../../db/local.db'))
        # if os.path.exists(env_vars.LOCAL_DB_PATH):
        #     odm2_db = sqlite3.connect(db_path)
        #
        # elif os.path.exists(env_vars.LOCAL_DB_BASE+"/local.db"):
        #     odm2_db = sqlite3.connect(db_path)
        # else:
        #     # Create local.db
        #     odm2_db = sqlite3.connect(env_vars.LOCAL_DB_BASE+"/local.db")
        #     empty_dump_script = open(env_vars.LOCAL_DB_BASE+".dbload",'r').read()
        #     odm2_db.executescript(empty_dump_script)

        filepath = os.getcwd() + "/db/local.db"
        removedb(filepath)  # Its going to delete the file, than recreate it to avoid errors
        con = lite.connect(filepath)
        script = open(os.getcwd() + "/app_data/db/.dbload")

        with con:
            cur = con.cursor()
            cur.executescript(script.read())

def removedb(file):
    try:
        os.remove(file)
    except OSError:
        pass
