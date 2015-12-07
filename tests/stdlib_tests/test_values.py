

import unittest
from stdlib import ExchangeItem
import datetime
import random
from utilities import geometry


class testValues(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSetValuesBySlice(self):
        pass

    def testSetValuesByTime(self):

        item = ExchangeItem('e1', 'Test', 'Test Exchange Item')


        # set start and end dates
        st = datetime.datetime(2014, 1, 1, 12, 0, 0)
        et = datetime.datetime(2014, 2, 1, 12, 0, 0)
        timestep_in_seconds = 3600

        # build geometries
        x = [random.random() for i in range(0,150)]
        y = [random.random() for i in range(0,150)]
        geoms = geometry.build_point_geometries(x,y)
        item.addGeometries2(geoms)

        values = range(30)

        # set values for geometry=0, beginning at the start time
        success = item.setValuesBySlice(values, time_index_slice=(0,30,1), geometry_index_slice=(0, 1, 1))
        self.assertFalse(success)

        # initialize the dates and values containers
        item.initializeDatesValues(st, et, timestep_in_seconds)
        success = item.setValuesBySlice(values, time_index_slice=(0,30,1), geometry_index_slice=(0, 1, 1))
        self.assertTrue(success)

        # get the data
        geoms = item.getGeometries2()
        times = item.getDates2()
        vals = item.getValues2()

        # assert that data is set properly
        self.assertTrue(len(geoms) == 150)
        self.assertTrue(times[0][1] == st)
        self.assertTrue(times[-1][1] == et)
        self.assertTrue((times[-1][1] - times[-2][1]).total_seconds() == float(timestep_in_seconds))
        self.assertTrue(vals.shape[0] == len(times))
        self.assertTrue(vals.shape[1] == len(geoms))



