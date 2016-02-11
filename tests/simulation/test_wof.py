

import os, sys
import time
import unittest
import datetime
from coordinator.engine import Coordinator
import wrappers
import environment
from sprint import *

class testWofSimulation(unittest.TestCase):


    def setUp(self):
        self.engine = Coordinator()

        if sys.gettrace():
            print 'Detected Debug Mode'
            # initialize debug listener (reroute messages to console)
            self.d = DebugListener()

        self.engine = Coordinator()
        PrintTarget.CONSOLE = 1134

        self.basepath = os.path.dirname(__file__)

    def tearDown(self):
        pass


    def test_wof_feedforward(self):

        args = dict(network = 'iutah',
                    site = 'LR_WaterLab_AA',
                    variable = 'RH_enc',
                    start = datetime.datetime(2015, 10, 26, 0, 0, 0),
                    end = datetime.datetime(2015, 10, 30, 0, 0, 0),
                    wsdl = 'http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL',
                    type = wrappers.Types.WOF
                    )


        # add the WaterOneFlow component to the engine
        m1 = self.engine.add_model(id=1234, attrib=args)
        self.assertTrue(m1)


        # load a test component
        multiplier_mdl = os.path.join(self.basepath, '../../app_data/models/multiplier/multiplier.mdl')
        args = dict(mdl=multiplier_mdl)
        m2 = self.engine.add_model(id=1235, attrib=args)
        self.assertTrue(m1)

        # assert that the models have been added correctly
        models = self.engine.get_all_models()
        self.assertTrue(len(models) == 2)

        # add a link from WaterOneFlow to multiplier
        wof_oei = self.engine.get_output_exchange_items_summary(id=1234)
        mul_iei = self.engine.get_input_exchange_items_summary(id=1235)
        self.engine.add_link(from_id=1234, from_item_id=wof_oei[0]['name'],
                             to_id=1235, to_item_id=mul_iei[0]['name'],
                             spatial_interp=None,
                             temporal_interp=None,
                             uid=None)

        links = self.engine.get_all_links()
        self.assertTrue(len(links) == 1)


        # run the simulation
        self.engine.run_simulation()
        time.sleep(10)  # give the simulation a chance to run

        # check that output data was generated
        m = self.engine.get_model_by_id(id = 1235)

        values = m.instance().outputs()['multipliedValue'].getValues2()
        self.assertTrue(len(values) > 0)
        self.assertTrue(values[0] != 0)

