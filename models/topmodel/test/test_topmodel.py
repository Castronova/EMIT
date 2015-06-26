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

        # check input exchange items
        in_items = top.inputs()
        self.assertTrue(len(in_items.keys()) == 1)
        self.assertTrue('precipitation' in in_items.keys())
        precip = in_items['precipitation']

        # check that input geometries were created
        precip_geoms = precip.getGeometries2()
        self.assertTrue(len(precip_geoms) > 0)

        # check input geometry type
        geom_type = precip_geoms[0].geom().geometryType()
        self.assertTrue(geom_type == 'Point')

        # check output exchange items
        out_items = top.outputs()
        self.assertTrue(len(out_items.keys()) == 1)
        self.assertTrue('streamflow' in out_items.keys())
        flow = out_items['streamflow']

        # check that output geoms exist
        flow_geoms = flow.getGeometries2()
        self.assertTrue(len(flow_geoms) > 0)

        # check output geometry type
        geom_type = flow_geoms[0].geom().geometryType()
        self.assertTrue(geom_type == 'LineString')