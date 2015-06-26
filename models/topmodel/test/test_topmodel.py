__author__ = 'tonycastronova'

import unittest
import time
from models.topmodel import topmodel
from utilities.gui import parse_config

class test_topmodel(unittest.TestCase):

    def setUp(self):
        # add models
        self.mdl = '../topmodel.mdl'

    def test_initialize(self):

        config_params = parse_config(self.mdl)
        # load topmodel
        top = topmodel.topmodel(config_params)


        # check input geometries
        in_items = top.inputs()#['some_value'].getGeometries2()
        self.assertTrue(len(in_items.keys()) == 1)
        self.assertTrue('precipitation' in in_items.keys())
        precip = in_items['precipitation']

        precip_geoms = precip.getGeometries2()
        self.assertTrue(len(precip_geoms) > 0)




        # check output geometries


        print 'done'