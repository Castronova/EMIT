__author__ = 'tonycastronova'

from os.path import *
import unittest
from datetime import datetime
import utilities


from examples.swmm.src import swmm_wrapper


class test_swmm(unittest.TestCase):

    def test_init(self):

        # get the configuration file
        mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))

        # parse the configuration parameters
        params = utilities.parse_config_without_validation(mdl)

        # initialize swmm
        swmm = swmm_wrapper.swmm(params)

        # verify that the model has initialized properly
        self.assertTrue(swmm.simulation_start() == datetime(2013,2,4,0,0,0))
        self.assertTrue(swmm.simulation_end() == datetime(2013,2,5,0,0,0))
        self.assertTrue(swmm.time_step() == (5,'minute'))
        self.assertTrue(swmm.name() == 'SWMM')


    def test_execute_no_inputs(self):

        # initialize swmm
        mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
        params = utilities.parse_config_without_validation(mdl)
        swmm = swmm_wrapper.swmm(params)

        # run the simulation
        inputs = []
        self.assertTrue(swmm.run(inputs))

        # parse outputs

