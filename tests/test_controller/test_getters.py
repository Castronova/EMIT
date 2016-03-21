__author__ = 'tonycastronova'

import unittest
import os, sys
from stdlib import *
from coordinator import engineAccessors
from coordinator.engine import Coordinator
import wrappers
from utilities import mdl
import sprint
import environment

class test_getters(unittest.TestCase):

    def setUp(self):

        # initialize environment variables
        environment.getEnvironmentVars()

        if sys.gettrace():
            print 'Detected Debug Mode'
            # initialize debug listener (reroute messages to console)
            self.d = sprint.DebugListener()

        sprint.PrintTarget.CONSOLE = 1134

        self._engine = Coordinator()
        self.basepath = os.path.dirname(__file__)


    def tearDown(self):
        pass



    def test_get_oei(self):

        multiplier_mdl = os.path.join(self.basepath, '../../app_data/models/multiplier/multiplier.mdl')

        # add a model to the engine
        m1 = self._engine.add_model(id=1234,  attrib={'mdl':multiplier_mdl})
        self.assertTrue(m1)


        # query the oei
        oei = self._engine.get_exchange_item_info(1234, 'OUTPUT')

        self.assertTrue(len(oei) == 1)
        self.assertTrue(oei[0]['geometry'].has_key('type'))
        self.assertTrue(oei[0]['geometry'].has_key('srs'))
        self.assertTrue(oei[0]['geometry'].has_key('count'))
        self.assertTrue(oei[0]['geometry'].has_key('extent'))
        self.assertTrue(oei[0]['geometry'].has_key('wkb'))
        self.assertTrue(oei[0]['geometry'].has_key('hash'))



    def test_get_iei(self):

        multiplier_mdl = os.path.join(self.basepath, '../../app_data/models/multiplier/multiplier.mdl')

        # add a model to the engine
        m1 = self._engine.add_model(id=1234,  attrib={'mdl':multiplier_mdl})
        self.assertTrue(m1)

        # query the oei
        oei = self._engine.get_exchange_item_info(1234, 'INPUT')

        self.assertTrue(len(oei) == 1)
        self.assertTrue(oei[0]['geometry'].has_key('type'))
        self.assertTrue(oei[0]['geometry'].has_key('srs'))
        self.assertTrue(oei[0]['geometry'].has_key('count'))
        self.assertTrue(oei[0]['geometry'].has_key('extent'))
        self.assertTrue(oei[0]['geometry'].has_key('wkb'))
        self.assertTrue(oei[0]['geometry'].has_key('hash'))


