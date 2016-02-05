
__author__ = 'tonycastronova'

import sys
sys.path.append('../')

import unittest
from stdlib import *
import datetime
from utilities import spatial, mdl, geometry
from shapely.geometry import Point
from advanced_geometry import *
from datetime import timedelta
from datetime import datetime as dt
import environment
import random


class testNewDataOrg(unittest.TestCase):

    def setUp(self):

        # -- Create Unit --#
        unit = mdl.create_unit('cubic meters per second')

        # -- Create Variable --#
        variable = mdl.create_variable('streamflow')

        # create exchange item
        self.item = ExchangeItem(name='Test', desc='Test Exchange Item', unit=unit, variable=variable)

        coords = [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10)]
        x,y = zip(*coords)
        geoms = geometry.build_point_geometries(x, y)

        self.item.addGeometries2(geoms)


    def test_get_geoms2(self):

        # get all geoms
        g = self.item.getGeometries2()
        self.assertTrue(len(g) == 9)

        # get one geom
        g = self.item.getGeometries2(4)
        self.assertTrue(isinstance(g, Geometry2))
        self.assertTrue(g.geom().x == 5)
        self.assertTrue(g.geom().y == 6)

    def test_add_geoms2(self):

        # add a single geom
        pt = geometry.build_point_geometry(10, 11)
        x,y,z = pt.GetPoint()
        self.assertTrue(isinstance(pt, Geometry2))

        ret = self.item.addGeometry(pt)
        self.assertTrue(ret)

        g = self.item.getGeometries2(-1)
        self.assertTrue(isinstance(g, Geometry2))
        x,y,z = g.GetPoint()
        self.assertTrue(x == 10)
        self.assertTrue(y == 11)
        self.assertTrue(z == 0)

        # add an invalid geometry
        ret = self.item.addGeometry((0,1,1))
        self.assertFalse(ret)

        # add many of geometries
        xs = range(100,110)
        ys = range(110,120)
        pts = geometry.build_point_geometries(xs, ys)
        geoms = []
        for pt in pts:
            geoms.append(pt)
        ret = self.item.addGeometries2(geoms)
        self.assertTrue(ret)
        g = self.item.getGeometries2(-1)
        self.assertTrue(isinstance(g, Geometry2))
        x,y,z = g.GetPoint()
        self.assertTrue(x == 109)
        self.assertTrue(y == 119)
        self.assertTrue(z == 0)

        # add a mix of valid and invalid geometries
        geoms = []
        for i in range(100,110):
            if i % 2 == 0:
                pt = geometry.build_point_geometry(i, i + 1)
                geoms.append(pt)
            else:
                geoms.append((i,i+1))

        ret = self.item.addGeometries2(geoms)
        self.assertFalse(ret)
        g = self.item.getGeometries2(-1)
        self.assertTrue(isinstance(g, Geometry2))
        x,y,z = g.GetPoint()
        self.assertTrue(x == 108)
        self.assertTrue(y == 109)
        self.assertTrue(z == 0)

    def test_values(self):

        # add values
        time = dt.now()
        geoms = self.item.getGeometries2()
        values = [random.random() for g in geoms]
        ret = self.item.setValues2(values, time)
        self.assertTrue(ret)
        values = self.item.getValues2()
        self.assertTrue(len(values[0]) == len(geoms))


        # add many dates and values
        times = [time + timedelta(days=i) for i in range(5, 15)]
        values = [[random.random() for g in geoms] for i in range(5,15)]
        v1 = self.item.getValues2()
        ret = self.item.setValues2(values, times)
        self.assertTrue(ret)
        v2 = self.item.getValues2()
        self.assertTrue(len(v2) - len(v1) == 10)

        # add dates and values that do not match geometries
        times = [time + timedelta(days=i) for i in range(5, 15)]
        values = [[random.random() for g in geoms] for i in range(5,10)]
        ret = self.item.setValues2(values, times)
        self.assertFalse(ret)

        # replace data single geometry, for a single time
        new_values = [i**2 for i in range(0, len(geoms))]
        time = times[0]
        idx, date_value = self.item.getDates2(time)
        values_old = self.item.getValues2(time_idx=idx)
        ret = self.item.setValues2(new_values, time)
        values = self.item.getValues2(time_idx=idx)
        self.assertFalse(values == values_old)

        # add invalid time
        time = dt.now().strftime('%Y-%m-%d')
        ret = self.item.setValues2(values, time)
        self.assertFalse(ret)

        # get datetime range
        st = times[0] + timedelta(days=1) + timedelta(hours=5)
        et = st + timedelta(days=4)
        values = self.item.getValues2(start_time=st, end_time=et)
        dates = self.item.getDates2(start=st, end=et)
        self.assertTrue(len(dates) == len(values))

        # try getting one date
        all_dates = self.item.getDates2()
        date_value = self.item.getDates2(all_dates[0][1])
        self.assertTrue(all_dates[0] == date_value)

        # test invalid date object
        invalid = self.item.getDates2(start='2014-07-01', end='2014-08-01')
        self.assertTrue(invalid == (0, None))

        # test getting datavalue geometry subsets
        values = self.item.getValues2(idx_start=3, idx_end=5, start_time=st, end_time=et)
        self.assertTrue(len(values) == 5)
        self.assertTrue(len(values[0]) == 3)