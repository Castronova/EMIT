__author__ = 'tonycastronova'


import unittest
from stdlib import *
import datetime
import utilities as utils
from advanced_geometry import *

class testGeometry(unittest.TestCase):

    def setUp(self):
        self.vals = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,100)]
        self.geometry = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        self.srscode = '2921'


    def test_point_grid(self):

        import random

        # generate point geometries
        pt_geoms = []
        for x in range(0,3):
            for y in range(0,3):
                v = [(datetime.datetime(2014,1,1,12,0,0) + datetime.timedelta(days=i), i) for i in range(0,365)]
                g = 'POINT (%d %d)' % (x,y)
                dv = DataValues(v)
                geom = Geometry()
                geom.set_geom_from_wkt(g)
                geom.type(ElementType.Point)
                geom.srs(utils.get_srs_from_epsg(self.srscode))
                geom.datavalues(dv)
                pt_geoms.append(geom)

        # create element grid
        grid = GriddedGeometry(pt_geoms,5,5,3,3)




        print grid.get_time_slice(datetime.datetime(2014,1,10,6,0,0))
