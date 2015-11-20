__author__ = 'tonycastronova'



import unittest

from stdlib import *
from coordinator import main

class test_build_composition(unittest.TestCase):

    def setUp(self):
        self.sim = main.Coordinator()

         # add models
        mdl1 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'
        id1 = self.sim.add_model(mdl1)
        mdl2 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/random.mdl'
        id2 = self.sim.add_model(mdl2)

        # create link
        linkid = self.sim.add_link(id2,'OUTPUT1',id1,'INPUT1')


    def test_config_summary(self):
        self.sim.get_configuration_details('summary')

    def test_config_models(self):
        self.sim.get_configuration_details('models')

    def test_config_links(self):
        self.sim.get_configuration_details('links')