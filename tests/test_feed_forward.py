__author__ = 'tonycastronova'

import unittest

# from stdlib import *
# from coordinator import engine

# from utilities import gui
from coordinator import engineAccessors as engine
from coordinator import events
class test_feed_forward(unittest.TestCase):

    def setUp(self):

        # add bindings to model accessor events
        events.onModelAdded += self.generic_listener
        events.onLinkAdded += self.generic_listener
        events.onSimulationFinished += self.generic_listener

    def test_run(self):
        # # load databases from file
        # # db = self.sim.connect_to_db(['/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/connections'])
        #
        # # set default database
        # # self.sim.set_default_database('ODM2 Simulation database')
        #

        # add models
        mdl1 = '../models/test_models/randomizer/randomizer.mdl'
        mdl2 = '../models/test_models/multiplier/multiplier.mdl'

        # add both models.  ids can be anything
        id1 = 'id:randomizer'
        id2 = 'id:multiplier'
        engine.addModel(id=id1, attrib={'mdl':mdl1})
        engine.addModel(id=id2, attrib={'mdl':mdl2})

        # test that the models were created
        m1 = engine.getModelById(id1)
        m2 = engine.getModelById(id2)
        self.assertTrue(m1 is not None)
        self.assertTrue(m2 is not None)


        # create link
        linkid = engine.addLink(id1,'random 1-10',id2,'some_value')

        # test that the link was created
        l1 =  engine.getLinkById(linkid)
        self.assertTrue(l1 is not None)


        is_successful =  engine.runSimulation()
        self.assertTrue(is_successful)


    def generic_listener(self, e):
        # this is a listener function for all modeladded, linkadded, etc.
        # if we don't have this pycharm will complain (e.g. Exception: ('No handlers for event: ', 'onModelAdded'))
        print '\n',17*'-','\n| Event Caught! |', '\n', 17*'-'
        for k,v in e.__dict__.iteritems():
            print k,' =   ',v