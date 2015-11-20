__author__ = 'tonycastronova'

# import sys
# sys.path.append('../')
import unittest
# from stdlib import *
# from utilities import gui

import time
from coordinator import engineAccessors as engine
import sys


class test_build_composition(unittest.TestCase):

    def setUp(self):
        # add models
        self.mdl1 = '../models/test_models/randomizer/randomizer.mdl'
        self.mdl2 = '../models/test_models/multiplier/multiplier.mdl'
        self.engine = engine

    def tearDown(self):
        links = self.engine.getAllLinks()
        for link in links:
            self.engine.removeLinkById(link['id'])

        models = self.engine.getAllModels()
        for model in models:
            self.engine.removeModelById(model['id'])

        # self.engine.Close()
        # del self.engine


    def test_addModel(self):

        # load a model
        id = 'id:randomizer'
        self.engine.addModel(id=id, attrib={'mdl':self.mdl1})
        time.sleep(1)

        # check that the model exists
        m = self.engine.getModelById(id)
        self.assertIsNotNone(m)

    def test_get_model_by_id(self):

        # load a model
        id = 'id:randomizer'
        self.engine.addModel(id=id, attrib={'mdl':self.mdl1})

        # test getting an id that doesnt exist
        self.assertIsNone(self.engine.getModelById(10))

        # test getting an id that exists
        self.assertIsNotNone(self.engine.getModelById(id))

    def test_remove_model(self):

        # load a model
        id = 'id:randomizer'
        self.engine.addModel(id=id, attrib={'mdl':self.mdl1})

        # check that the model exists
        self.assertTrue(self.engine.getModelById(id) is not None)

        # test removing id that doesnt exist
        self.assertIsNone(self.engine.removeModelById(10))

        # test removing id that exists
        self.assertIsNotNone(self.engine.removeModelById(id))

    def test_remove_link(self):

        # add both models.  ids can be anything
        id1 = 'id:randomizer'
        id2 = 'id:multiplier'
        self.engine.addModel(id=id1, attrib={'mdl':self.mdl1})
        self.engine.addModel(id=id2, attrib={'mdl':self.mdl2})
        time.sleep(1)

        # create link
        linkid = self.engine.addLink(id1,'random 1-10',id2,'some_value')
        time.sleep(1)

        # verify that the link has been created
        links = self.engine.getAllLinks()
        self.assertTrue(len(links) > 0)

        # remove the link
        self.engine.removeLinkById(linkid)

        # verify that the link has been removed
        links = self.engine.getAllLinks()
        self.assertTrue(len(links) == 0)



    def test_get_link_by_id(self):
        print 'here'
        # add both models.  ids can be anything
        id1 = 'id:randomizer'
        id2 = 'id:multiplier'
        self.engine.addModel(id=id1, attrib={'mdl':self.mdl1})
        self.engine.addModel(id=id2, attrib={'mdl':self.mdl2})
        time.sleep(1)
        print 'model added'

        # create link
        linkid = self.engine.addLink(id1,'random 1-10',id2,'some_value')
        time.sleep(1)
        print 'link added'

        # test getting an id that doesnt exist
        self.assertIsNone(self.engine.getLinkById(10))

        # test getting an id that exists
        self.assertIsNotNone(self.engine.getLinkById(linkid))



    def test_addLink(self):

        # add both models.  ids can be anything
        id1 = 'id:randomizer'
        id2 = 'id:multiplier'
        self.engine.addModel(id=id1, attrib={'mdl':self.mdl1})
        self.engine.addModel(id=id2, attrib={'mdl':self.mdl2})

        # test that the models were created
        m1 = self.engine.getModelById(id1)
        m2 = self.engine.getModelById(id2)
        time.sleep(1)
        self.assertTrue(m1 is not None)
        self.assertTrue(m2 is not None)

        # create link
        linkid = self.engine.addLink(id1,'random 1-10',id2,'some_value')
        time.sleep(1)

        # test that the link was created
        l1 =  self.engine.getLinkById(linkid)
        self.assertTrue(l1 is not None)


    def test_remove_model_with_links(self):

        # add both models.  ids can be anything
        id1 = 'id:randomizer'
        id2 = 'id:multiplier'
        self.engine.addModel(id=id1, attrib={'mdl':self.mdl1})
        self.engine.addModel(id=id2, attrib={'mdl':self.mdl2})

        # test that the models were created
        m1 = self.engine.getModelById(id1)
        m2 = self.engine.getModelById(id2)
        time.sleep(1)
        self.assertTrue(m1 is not None)
        self.assertTrue(m2 is not None)

        # create link
        linkid = self.engine.addLink(id1,'random 1-10',id2,'some_value')
        time.sleep(1)

        # remove model
        self.assertTrue(self.engine.removeModelById(id1))

    def test_get_links_by_model(self):

        # add both models.  ids can be anything
        id1 = 'id:randomizer'
        id2 = 'id:multiplier'
        self.engine.addModel(id=id1, attrib={'mdl':self.mdl1})
        self.engine.addModel(id=id2, attrib={'mdl':self.mdl2})

        # test that now links are returned
        self.assertIsNone(self.engine.getLinkById(id1))

        # create link
        linkid = self.engine.addLink(id1,'random 1-10',id2,'some_value')
        time.sleep(1)

        # test that links are returned
        links = self.engine.getLinksBtwnModels(id1, id2)
        self.assertTrue(len(links) == 1)

#     def test_get_data(self):
#         # add models
#         id1 = engine.addModel(self.mdl1)
#         id2 = engine.addModel(self.mdl2)
#
#
#         # create link
#         linkid = engine.addLink(id2,'OUTPUT1',id1,'INPUT1')
#
#
#         # load databases from file
#         db = engine.connectToDbFromFile(['/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/connections'])
#
#         # set default database
#         engine.set_default_database('ODM2 Simulation database')
#
#         # get timeseries
# #        gui.get_ts_from_database_link(engine.get_default_db(), engine.get_links_by_model(id1),engine.get_model_by_id(id1))
#
#
#     def test_run(self):
#         # load databases from file
#         db = engine.connectToDbFromFile(['/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/connections'])
#
#         # set default database
#         engine.set_default_database('ODM2 Simulation database')
#
#         # add models
#         id1 = engine.addModel(self.mdl1)
#         id2 = engine.addModel(self.mdl2)
#
#         # create link
#         linkid = engine.addLink(id2,'OUTPUT1',id1,'INPUT1')
#
#         # get data required for simulation
#         finished = engine.runSimulation()
#
#
#         #links = engine.get_links_by_model(id1)
#         # test that links are returned
#         #self.assertTrue(len(links) == 1)
#
