__author__ = 'tonycastronova'

import unittest

# from stdlib import *
# from coordinator import engine

# from utilities import gui
from coordinator import engineManager

class test_feed_forward(unittest.TestCase):

    def setUp(self):
        self.engine = engineManager.Engine()

    def test_run(self):
        print "in here"
        # # load databases from file
        # # db = self.sim.connect_to_db(['/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/connections'])
        #
        # # set default database
        # # self.sim.set_default_database('ODM2 Simulation database')
        #
        # # add models
        # mdl1 = '/home/mike/Projects/EMIT/models/test_models/randomizer/randomizer.mdl'
        # id1 = self.sim.add_model(mdl1)
        # mdl2 = '/home/mike/Projects/EMIT/models/test_models/randomizer/randomizer.mdl'
        # id2 = self.sim.add_model(mdl2)
        #
        # # create link
        # linkid = self.sim.add_link(id2,'random 1-10',id1,'some_value')
        #
        # # get data required for simulation
        # finished = self.sim.run_simulation()
        #
        #
        # #links = self.sim.get_links_by_model(id1)
        # # test that links are returned
        # #self.assertTrue(len(links) == 1)

