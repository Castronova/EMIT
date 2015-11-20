

import unittest
from transform import time
from utilities import geometry
import stdlib
import datetime
import numpy

class testTimeTransforms(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_nearest_neighbor(self):
        """
        tests the construction of a temporal map
        """

        nearest = time.temporal_nearest_neighbor()
        st = datetime.datetime(2014, 01, 01, 0, 0, 0)
        source_dates = [st + datetime.timedelta(hours=i) for i in range(50)]

        # test slightly offset dates
        st = datetime.datetime(2014, 01, 01, 0, 5, 0)
        target_dates = [st + datetime.timedelta(hours=i) for i in range(50)]
        map = nearest.map(source_dates, target_dates)
        self.assertTrue(list(map) == range(50) )

        # test unequal lengths
        st = datetime.datetime(2014, 01, 01, 5, 0, 0)
        target_dates = [st + datetime.timedelta(hours=i) for i in range(10)]
        map = nearest.map(source_dates, target_dates)
        self.assertTrue(len(map) < len(source_dates))
        self.assertTrue(list(map) == range(5, 15))

        # test many to one
        st = datetime.datetime(2014, 01, 01, 5, 0, 0)
        target_dates = [st + datetime.timedelta(minutes=i) for i in range(10)]
        map = nearest.map(source_dates, target_dates)
        self.assertTrue(len(map) < len(source_dates))
        self.assertTrue(list(map) == 10*[5])

        # test numpy
        st = datetime.datetime(2014, 01, 01, 5, 0, 0)
        target_dates = numpy.array([st + datetime.timedelta(minutes=i) for i in range(10)])
        map = nearest.map(source_dates, target_dates)
        self.assertTrue(len(map) < len(source_dates))
        self.assertTrue(list(map) == 10*[5])



    def test_map_values(self):
        '''
        tests the mapping of datavalues using a temporal map
        '''

        # build temporal map
        nearest = time.temporal_nearest_neighbor()
        st = datetime.datetime(2014, 01, 01, 0, 0, 0)
        source_dates = [st + datetime.timedelta(hours=i) for i in range(50)]
        source_values = numpy.array(range(50))
        st = datetime.datetime(2014, 01, 01, 5, 0, 0)
        target_dates = [st + datetime.timedelta(hours=i) for i in range(10)]
        map = nearest.map(source_dates, target_dates)
        self.assertTrue(len(map) < len(source_dates))
        self.assertTrue(list(map) == range(5, 15))

        # test value mapping
        target_vals = time.transform(map, source_values)
        self.assertTrue(len(target_vals) == len(target_dates))
        self.assertTrue(list(target_vals) == range(5,15))

        # test list values
        source_values = range(50)
        target_vals = time.transform(map, source_values)
        self.assertTrue(len(target_vals) == len(target_dates))
        self.assertTrue(list(target_vals) == range(5,15))

        # test invalid type
        target_vals = None
        try:
            source_values = 10
            target_vals = time.transform(map, source_values)
        except Exception, e:
            self.assertTrue(type(e) == ValueError)
        finally:
            self.assertTrue(target_vals is None)