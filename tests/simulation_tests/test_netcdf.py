

import os
import time
import unittest
import datetime
import wrappers
from coordinator.engine import Coordinator

class testNetcdfSimulation(unittest.TestCase):


    def setUp(self):
        self.engine = Coordinator()

    def tearDown(self):
        pass


    def test_netcdf_feedforward(self):

        args = dict(ncpath = '../data/prcp.nc',
                    tdim = 'time',
                    xdim = 'x',
                    ydim = 'y',
                    tunit = 'hours',
                    starttime = '10-26-2015 00:00:00',
                    type = wrappers.Types.NETCDF)

        self.assertTrue(os.path.exists(args['ncpath']))

        # add the wof component to the engine
        self.engine.add_model(id=1234, attrib=args)

        # load a test component
        multiplier_mdl = os.path.abspath('./data/multiplier/multiplier.mdl')
        self.assertTrue(os.path.exists(multiplier_mdl), 'Path does not exist: %s'%multiplier_mdl)
        args = dict(mdl=multiplier_mdl)
        self.engine.add_model(id=1235, attrib=args)

        # assert that the models have been added correctly
        models = self.engine.get_all_models()
        self.assertTrue(len(models) == 2)

        # add a link from wof to multiplier
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
        time.sleep(5)  # give the simulation a chance to run

        # check that output data was generated
        m = self.engine.get_model_by_id(id = 1235)

        values = m.instance().outputs()['multipliedValue'].getValues2()
        self.assertTrue(len(values) > 0)
        self.assertTrue(values[0] != 0)

