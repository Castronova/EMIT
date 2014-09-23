__author__ = 'tonycastronova'

import os
import unittest
from stdlib import *
import utilities as utils
from utilities import mdl, spatial, gui
import datetime
from shapely.wkt import loads

class testExchangeItem(unittest.TestCase):

    def setUp(self):

        self.srscode = 2921

        self.item = ExchangeItem('e1','Test','Test Exchange Item')

    def tearDown(self):
        del self.item


    def test_create_exchange_item(self):

        item = self.item

        # -- Create Unit --#
        unit = mdl.create_unit('cubic meters per second')

        # -- Create Variable --#
        variable = mdl.create_variable('streamflow')

        # create dataset 1
        vals1 = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        geometry1 = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        dv1 = DataValues(vals1)
        geom = Geometry()
        geom.set_geom_from_wkt(geometry1)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues(dv1)
        item.add_geometry(geom)

        # create dataset 2
        vals2 = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        geometry2 = 'POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))'
        dv2 = DataValues(vals2)
        geom = Geometry()
        geom.set_geom_from_wkt(geometry2)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues(dv2)
        item.add_geometry(geom)

        self.assertTrue(item.name() == 'Test')
        self.assertTrue(item.description() == 'Test Exchange Item')
        self.assertTrue(item.StartTime == datetime.datetime(2014,1,1,12,0,0))
        self.assertTrue(item.EndTime == datetime.datetime(2014,4,10,12,0,0))

    def test_add_dataset_seq(self):
        item = self.item

        # create dataset 1
        vals1 = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        geometry1 = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        dv1 = DataValues(vals1)
        geom = Geometry()
        geom.set_geom_from_wkt(geometry1)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues(dv1)
        item.add_geometry(geom)

        # create dataset 2
        vals2 = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        geometry2 = 'POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))'
        dv2 = DataValues(vals2)
        geom = Geometry()
        geom.set_geom_from_wkt(geometry2)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues(dv2)
        item.add_geometry(geom)

        datasets = item.get_all_datasets()
        self.assertTrue(len(datasets.keys()) == 2)
        for g,ts in datasets.iteritems():
            if g.geom().almost_equals(loads(geometry1),5):
                self.assertTrue(g.datavalues() == dv1)
            elif g.geom().almost_equals(loads(geometry2),5):
                self.assertTrue(g.datavalues() == dv2)


    def test_add_datasets_as_list(self):
        item = self.item
        geoms = []

        # create dataset 1 & 2 together
        vals1 = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        dv1 = DataValues(vals1)
        geometry1 = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        geom = Geometry()
        geom.set_geom_from_wkt(geometry1)
        geom.type(ElementType.Polygon)
        geom.srs(utils.get_srs_from_epsg(self.srscode))
        geom.spatial(dv1)
        geoms.append(geom)

        vals2 = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        dv2 = DataValues(vals2)
        geometry2 = 'POLYGON ((40 20, 50 50, 30 50, 20 30, 40 20))'
        geom = Geometry()
        geom.set_geom_from_wkt(geometry2)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues(dv2)
        geoms.append(geom)

        # add both datasets
        item.add_geometry(geoms)

        datasets = item.get_all_datasets()
        self.assertTrue(len(datasets.keys()) == 2)
        for g,ts in datasets.iteritems():
            if g.geom().almost_equals(loads(geometry1),5):
                self.assertTrue(g.datavalues() == dv1)
            elif g.geom().almost_equals(loads(geometry2),5):
                self.assertTrue(g.datavalues() == dv2)

    def test_clear_datasets(self):
        item = self.item

        # create dataset 1
        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        dv = DataValues(self.vals)

        geometry = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        geom = Geometry()
        geom.set_geom_from_wkt(geometry)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues(dv)
        item.add_geometry(geom)


        item.clear()
        ds = item.get_all_datasets()
        self.assertTrue(len(ds.keys()) == 0)


    def test_utilites_build_exchange_items(self):

        config = os.path.realpath('./configuration.ini')

        params = gui.parse_config(config)
        eitems = mdl.build_exchange_items(params)

        print 'done'