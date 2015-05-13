__author__ = 'tonycastronova'


import unittest
from stdlib import *
import datetime
from utilities import spatial

class testDataValues(unittest.TestCase):

    def setUp(self):
        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        self.geometry = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        self.srscode = '2921'


    def test_datavalues(self):

        # create element
        elem = Element()
        elem.set_geom_from_wkt(self.geometry)
        elem.type(ElementType.Polygon)
        srs = spatial.get_srs_from_epsg(self.srscode)
        elem.srs(srs)

        # create datavalues object
        dv = DataValues(elem,self.vals)

        self.assertTrue(dv.element().type() == 'Polygon')
        self.assertTrue(len(dv.timeseries()) == 100)


        earliest = dv.earliest_date()
        latest = dv.latest_date()

        self.assertTrue(earliest == zip(*self.vals)[0][0])
        self.assertTrue(latest == zip(*self.vals)[0][-1])


