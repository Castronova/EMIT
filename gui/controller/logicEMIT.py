__author__ = 'Mario'

import os
import wx
from gui.views.viewEMIT import ViewEMIT
import coordinator.engineAccessors as engine
from gui.controller.logicFileDrop import LogicFileDrop


class LogicEMIT(ViewEMIT):
    def __init__(self, parent):
        ViewEMIT.__init__(self, parent)

        self.FloatCanvas = self.Canvas.FloatCanvas

        # connect to known databases
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/connections'))
        engine.connectToDbFromFile(dbtextfile=connections_txt)

        engine.createSQLiteInMemory()

        dropTarget = LogicFileDrop(self.Canvas, self.FloatCanvas)
        self.SetDropTarget(dropTarget)

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


