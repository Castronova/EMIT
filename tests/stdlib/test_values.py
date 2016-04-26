

import unittest
from stdlib import ExchangeItem
import datetime
import random
from utilities import geometry
import environment

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



class testDates(unittest.TestCase):

    def setUp(self):

        self.item = ExchangeItem('e1', 'Test', 'Test Exchange Item')

        # set start and end dates
        self.st = datetime.datetime(2014, 1, 1, 12, 0, 0)
        self.et = datetime.datetime(2014, 2, 1, 12, 0, 0)
        self.timestep_in_seconds = 3600

        # build geometries
        x = [random.random() for i in range(0,150)]
        y = [random.random() for i in range(0,150)]
        geoms = geometry.build_point_geometries(x,y)
        self.item.addGeometries2(geoms)
        values = range(30)


        # initialize the dates and values containers
        self.item.initializeDatesValues(self.st, self.et, self.timestep_in_seconds)
        success = self.item.setValuesBySlice(values, time_index_slice=(0,30,1), geometry_index_slice=(0, 1, 1))
        self.assertTrue(success)

    def tearDown(self):
        pass

    def test_getDates(self):

        # get the dates that were created during setup
        dates = self.item.getDates()

        # calculate the number of values that should exist
        dt = (self.et - self.st).total_seconds()
        num = dt / self.timestep_in_seconds + 1

        # assertions
        self.assertTrue(len(dates) == num)
        self.assertTrue(dates[0][1] == self.st)
        self.assertTrue(dates[-1][1] == self.et)


    def test_getNearestDates(self):

        # define a search time
        dt = self.st + datetime.timedelta(seconds=30)

        # test non-list
        nearest = self.item.getNearestDates(dt)
        self.assertTrue(nearest.shape == (0,))

        # test single value, left
        nearest = self.item.getNearestDates([dt], 'left')
        self.assertTrue(nearest[0][0] == 0)

        # test single value, right
        nearest = self.item.getNearestDates([dt], 'right')
        self.assertTrue(nearest[0][0] == 0)

        # test value in between two times
        dt = self.st + datetime.timedelta(minutes=30)
        nearest = self.item.getNearestDates([dt], 'left')
        self.assertTrue(nearest[0][0] == 0)
        nearest = self.item.getNearestDates([dt], 'right')
        self.assertTrue(nearest[0][0] == 0)

        # test list of values
        dt = [self.st + datetime.timedelta(minutes=30),
              self.st + datetime.timedelta(minutes=45),
              self.st + datetime.timedelta(minutes=123),
              self.st + datetime.timedelta(minutes=145),
              self.st + datetime.timedelta(minutes=230)]
        nearest = self.item.getNearestDates(dt)
        self.assertTrue(nearest[0][0] == 0)
        self.assertTrue(nearest[1][0] == 1)
        self.assertTrue(nearest[2][0] == 2)
        self.assertTrue(nearest[3][0] == 2)
        self.assertTrue(nearest[4][0] == 4)

