__author__ = 'tonycastronova'

import unittest

from stdlib import *
from coordinator import main
import utilities

class test_build_composition(unittest.TestCase):

    def setUp(self):
        self.sim = main.Coordinator()

    def test_add_model(self):

        # model file
        mdl = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'

        # load a model
        id = self.sim.add_model(mdl)

        # check that the model exists
        self.assertTrue(self.sim.get_model_by_id(id))

        # remove the model
        self.sim.remove_model_by_id(id)

    def test_get_model_by_id(self):
        # model file
        mdl = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'

        # load a model
        id = self.sim.add_model(mdl)

        # test getting an id that doesnt exist
        self.assertFalse(self.sim.get_model_by_id(10))

        # test getting an id that exists
        self.assertTrue(self.sim.get_model_by_id(id))

        # check that the correct model was retrieved
        self.assertTrue(self.sim.get_model_by_id(id) == self.sim._Coordinator__models.items()[0][1])


    def test_remove_model(self):
        # model file
        mdl = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'

        # load a model
        id = self.sim.add_model(mdl)

        # check that the model exists
        self.assertTrue(self.sim.get_model_by_id(id))

        # test removing id that doesnt exist
        self.assertFalse(self.sim.remove_model_by_id(10))

        # test removing id that exists
        self.assertTrue(self.sim.remove_model_by_id(id))

        # check that no models exist in sim._models {}
        self.assertTrue(len(self.sim._Coordinator__models.keys())== 0)


    def test_remove_link(self):
         # add models
        mdl1 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'
        id1 = self.sim.add_model(mdl1)
        mdl2 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/random.mdl'
        id2 = self.sim.add_model(mdl2)

        # create link
        linkid = self.sim.add_link(id2,'OUTPUT1',id1,'INPUT1')

        # verify that the link has been created
        self.assertTrue(len(self.sim._Coordinator__links.keys()) == 1)

        # remove the link
        self.sim.remove_link_by_id(linkid)

        # verify that the link has been removed
        self.assertTrue(len(self.sim._Coordinator__links.keys()) == 0)



    def test_get_link_by_id(self):
         # add models
        mdl1 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'
        id1 = self.sim.add_model(mdl1)
        mdl2 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/random.mdl'
        id2 = self.sim.add_model(mdl2)

        # create link
        linkid = self.sim.add_link(id2,'OUTPUT1',id1,'INPUT1')

        # test getting an id that doesnt exist
        self.assertFalse(self.sim.get_link_by_id(10))

        # test getting an id that exists
        self.assertTrue(self.sim.get_link_by_id(linkid))

        # check that the correct model was retrieved
        self.assertTrue(self.sim.get_link_by_id(linkid) == self.sim._Coordinator__links.items()[0][1])

        # remove the link
        self.sim.remove_link_by_id(linkid)


    def test_add_link(self):
        # add models
        mdl1 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'
        id1 = self.sim.add_model(mdl1)
        mdl2 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/random.mdl'
        id2 = self.sim.add_model(mdl2)

        # create link
        linkid = self.sim.add_link(id2,'OUTPUT1',id1,'INPUT1')

        self.assertTrue(len(self.sim._Coordinator__links.keys()) == 1)

        # remove the link
        self.sim.remove_link_by_id(linkid)

    def test_remove_model_with_links(self):
        # add models
        mdl1 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'
        id1 = self.sim.add_model(mdl1)
        mdl2 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/random.mdl'
        id2 = self.sim.add_model(mdl2)

        # create link
        linkid = self.sim.add_link(id2,'OUTPUT1',id1,'INPUT1')

        # remove model
        self.assertTrue(self.sim.remove_model_by_id(id1))

        # make sure that the link was removed too
        self.assertFalse(self.sim.get_link_by_id(linkid))

    def test_get_links_by_model(self):
        # add models
        mdl1 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'
        id1 = self.sim.add_model(mdl1)
        mdl2 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/random.mdl'
        id2 = self.sim.add_model(mdl2)

        # test that now links are returned
        self.assertFalse(self.sim.get_links_by_model(id1))

        # create link
        linkid = self.sim.add_link(id2,'OUTPUT1',id1,'INPUT1')

        links = self.sim.get_links_by_model(id1)
        # test that links are returned
        self.assertTrue(len(links) == 1)

    def test_get_data(self):
        # add models
        mdl1 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'
        id1 = self.sim.add_model(mdl1)
        mdl2 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/random.mdl'
        id2 = self.sim.add_model(mdl2)


        # create link
        linkid = self.sim.add_link(id2,'OUTPUT1',id1,'INPUT1')


        # load databases from file
        db = self.sim.connect_to_db(['/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/connections'])

        # set default database
        self.sim.set_default_database('ODM2 Simulation database')

        # get timeseries
        utilities.get_ts_from_link(self.sim.get_default_db(), self.sim.get_links_by_model(id1),self.sim.get_model_by_id(id1))


    def test_run(self):
        # load databases from file
        db = self.sim.connect_to_db(['/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/connections'])

        # set default database
        self.sim.set_default_database('ODM2 Simulation database')

        # add models
        mdl1 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'
        id1 = self.sim.add_model(mdl1)
        mdl2 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/random.mdl'
        id2 = self.sim.add_model(mdl2)

        # create link
        linkid = self.sim.add_link(id2,'OUTPUT1',id1,'INPUT1')

        # get data required for simulation
        finished = self.sim.run_simulation()


        #links = self.sim.get_links_by_model(id1)
        # test that links are returned
        #self.assertTrue(len(links) == 1)

