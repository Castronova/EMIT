__author__ = 'Mario'

import os
import wx
from gui.views.viewEMIT import ViewEMIT
import coordinator.engineAccessors as engine
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


        # dropTarget = LogicFileDrop(self.Canvas, self.FloatCanvas)
        # self.SetDropTarget(dropTarget)

        self.binding()

    def binding(self):
        #Run MenuBar
        self.Bind(wx.EVT_MENU, self.run, self.applicationRun)


    def run(self, e):
        try:
            # self.cmd.run_simulation()
            engine.runSimulation()
        except Exception as e:
            wx.MessageBox(str(e.args[0]), 'Error', wx.OK | wx.ICON_ERROR)


