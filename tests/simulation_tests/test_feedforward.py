

import sys
import time
import sprint
import unittest
import environment
from coordinator.engine import Coordinator

class testFeedForwardSimulation(unittest.TestCase):


    def setUp(self):
        # initialize environment variables
        environment.getEnvironmentVars()

        if sys.gettrace():
            print 'Detected Debug Mode'
            # initialize debug listener (reroute messages to console)
            self.d = sprint.DebugListener()

        self.engine = Coordinator()
        sprint.PrintTarget.CONSOLE = 1134

    def tearDown(self):
        pass

    def test_feedforward_simulation(self):

        sprint.sPrint('test', sprint.MessageType.DEBUG)

        randomizer_path = '../../app_data/models/randomizer/randomizer.mdl'
        multiplier_mdl = '../../app_data/models/multiplier/multiplier.mdl'


        self.engine.add_model(id=1234,  attrib={'mdl':randomizer_path})
        self.engine.add_model(id=1235,  attrib={'mdl':multiplier_mdl})


        # assert that the models have been added correctly
        models = self.engine.get_all_models()
        self.assertTrue(len(models) == 2)


        # add a link from randomizer to multiplier
        rand_oei = self.engine.get_output_exchange_items_summary(id=1234)
        mult_iei = self.engine.get_input_exchange_items_summary(id=1235)
        self.engine.add_link(from_id=1234, from_item_id=rand_oei[0]['name'],
                             to_id=1235, to_item_id=mult_iei[0]['name'],
                             spatial_interp=None,
                             temporal_interp=None,
                             uid=None)

        # assert that the link has been established correctly
        links = self.engine.get_all_links()
        self.assertTrue(len(links) == 1)

        # run the simulation
        self.engine.run_simulation()
        time.sleep(5)  # give the simulation a chance to run

        # check that output data was generated
        m = self.engine.get_model_by_id(id = 1235)

        values = m.instance().outputs()['multipliedValue'].getValues2()
        self.assertTrue(len(values) > 0)
        self.assertTrue(values[0] != 0)

