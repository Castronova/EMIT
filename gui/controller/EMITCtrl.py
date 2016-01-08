__author__ = 'Mario'

import os
from gui.views.EMITView import ViewEMIT
import coordinator.engineAccessors as engine
import sqlite3 as lite


class LogicEMIT(ViewEMIT):
    def __init__(self, parent):


        ViewEMIT.__init__(self, parent)
        self.FloatCanvas = self.Canvas.FloatCanvas

        # todo: the connections file should be a binary object (pickle)
        # connect to known databases
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/connections'))
        engine.connectToDbFromFile(dbtextfile=connections_txt)

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
