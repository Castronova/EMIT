__author__ = 'tonycastronova'

import unittest
from models.test_models.weather import weather
from utilities.gui import parse_config

class test_weather(unittest.TestCase):

    def setUp(self):

        # load the model
        mdl = '../weatherReader.mdl'
        config_params = parse_config(mdl)
        self.model = weather.weatherReader(config_params)

    def test_initialize(self):

        # check output exchange items
        out_items = self.model.outputs()
        self.assertTrue(len(out_items.keys()) == 1)
        self.assertTrue('Precipitation' in out_items.keys())

        # check that output geoms exist
        p = out_items['Precipitation']
        p_geoms = p.getGeometries2()
        self.assertTrue(len(p_geoms) == 1)

        # check output geometry type
        geom_type = p_geoms[0].geom().geometryType()
        self.assertTrue(geom_type == 'Polygon')

    def test_run(self):

        # call 'run'
        self.model.run([])

        # validate output data
        precip = self.model.outputs()['Precipitation']
        self.assertTrue(len(precip.getGeometries2()) == 1)
        self.assertTrue(len(precip.getDates2()) == 145 )
        self.assertTrue(len(precip.getValues2()) == 145)

