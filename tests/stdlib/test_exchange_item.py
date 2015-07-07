__author__ = 'tonycastronova'

import unittest

from os.path import *
from stdlib import *
from utilities import mdl, spatial, gui
import datetime
from shapely.wkt import loads


class testExchangeItem(unittest.TestCase):
    def setUp(self):

        self.srscode = 2921

    def tearDown(self):
        self.item = None

    def test_create_exchange_item(self):

        item = ExchangeItem('e1', 'Test', 'Test Exchange Item')

        # -- Create Unit --#
        unit = mdl.create_unit('cubic meters per second')

        # -- Create Variable --#
        variable = mdl.create_variable('streamflow')

        # create dataset 1
        vals1 = [(datetime.datetime(2014, 1, 1, 12, 0, 0) + datetime.timedelta(days=i), i) for i in range(0, 100)]
        geometry1 = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        dv1 = DataValues(vals1)
        geom = Geometry()
        geom.set_geom_from_wkt(geometry1)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues(dv1)
        item.add_geometry(geom)

        # create dataset 2
        vals2 = [(datetime.datetime(2014, 1, 1, 12, 0, 0) + datetime.timedelta(days=i), i) for i in range(0, 100)]
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
        self.assertTrue(item.getStartTime() == datetime.datetime(2014, 1, 1, 12, 0, 0))
        self.assertTrue(item.getEndTime() == datetime.datetime(2014, 4, 10, 12, 0, 0))

    def test_add_dataset_seq(self):

        item = ExchangeItem('e1', 'Test', 'Test Exchange Item',[])

        # create dataset 1
        vals1 = [(datetime.datetime(2014, 1, 1, 12, 0, 0) + datetime.timedelta(days=i), i) for i in range(0, 100)]
        geometry1 = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        dv1 = DataValues(vals1)
        geom = Geometry()
        geom.set_geom_from_wkt(geometry1)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues(dv1)
        item.add_geometry(geom)

        # create dataset 2
        vals2 = [(datetime.datetime(2014, 1, 1, 12, 0, 0) + datetime.timedelta(days=i), i) for i in range(0, 100)]
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
        for g, ts in datasets.iteritems():
            if g.geom().almost_equals(loads(geometry1), 5):
                self.assertTrue(g.datavalues() == dv1)
            elif g.geom().almost_equals(loads(geometry2), 5):
                self.assertTrue(g.datavalues() == dv2)

    def test_add_datasets_as_list(self):

        # todo: this fails if [] is not set for 'geometry', b/c it will have geometries in it for some reason!
        item = ExchangeItem('e1', 'Test', 'Test Exchange Item', [])
        geoms = []

        # create dataset 1 & 2 together
        vals1 = [(datetime.datetime(2014, 1, 1, 12, 0, 0) + datetime.timedelta(days=i), i) for i in range(0, 100)]
        dv1 = DataValues(vals1)
        geometry1 = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        geom = Geometry()
        geom.set_geom_from_wkt(geometry1)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues(dv1)
        geoms.append(geom)

        vals2 = [(datetime.datetime(2014, 1, 1, 12, 0, 0) + datetime.timedelta(days=i), i) for i in range(0, 100)]
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
        for g, ts in datasets.iteritems():
            if g.geom().almost_equals(loads(geometry1), 5):
                self.assertTrue(g.datavalues() == dv1)
            elif g.geom().almost_equals(loads(geometry2), 5):
                self.assertTrue(g.datavalues() == dv2)

    def test_clear_datasets(self):

        item = ExchangeItem('e1', 'Test', 'Test Exchange Item')

        # create dataset 1
        self.vals = [(datetime.datetime(2014, 1, 1, 12, 0, 0) + datetime.timedelta(days=i), i) for i in range(0, 100)]
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

    def test_get_geoms(self):

        # get a sample configuration path
        current_dir = abspath(dirname(__file__))
        config = abspath(join(current_dir, '../test_data/configuration.ini'))

        # parse the configuration parameters
        params = gui.parse_config(config)

        # populate exchange items
        eitems = mdl.build_exchange_items_from_config(params)
        item = eitems['input'][0]

        # get geoms
        geoms = item.geometries()

        self.assertTrue(len(geoms) == 1)

    def test_add_geoms(self):

        # get a sample configuration path
        current_dir = abspath(dirname(__file__))
        config = abspath(join(current_dir, '../test_data/configuration.ini'))

        # parse the configuration parameters
        params = gui.parse_config(config)

        # populate exchange items
        eitems = mdl.build_exchange_items_from_config(params)

        item = eitems['input'][0]

        # get geoms
        geoms = item.geometries()

        self.assertTrue(len(geoms) == 1)

        # create geom
        geometry = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        geom = Geometry()
        geom.set_geom_from_wkt(geometry)
        geom.type(ElementType.Polygon)
        geom.srs(spatial.get_srs_from_epsg(self.srscode))
        geom.datavalues([])
        item.add_geometry(geom)

        geoms = item.geometries()
        self.assertTrue(len(geoms) == 2)

