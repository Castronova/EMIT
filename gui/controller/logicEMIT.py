__author__ = 'Mario'

import os

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

        dropTarget = LogicFileDrop(self.Canvas, self.FloatCanvas)
        self.SetDropTarget(dropTarget)



