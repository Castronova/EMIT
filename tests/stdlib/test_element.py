__author__ = 'tonycastronova'

import unittest

from stdlib import ElementType,Geometry


class testVariable(unittest.TestCase):


    def test_set_element(self):

        wkt_geometry = 'POINT (1.0 20.1)'

        g = Geometry()
        self.assertTrue(g.geom() == None)
        self.assertTrue(g.srs() == None)
        self.assertTrue(g.elev() == None)
        self.assertTrue(g.type() == None)

        g.srs('EPSG:2921')
        g.set_geom_from_wkt(wkt_geometry)
        g.type(ElementType.Point)

        self.assertTrue(g.srs() == 'EPSG:2921')
        self.assertTrue(g.geom().geometryType() == 'Point')
        self.assertTrue(len(g.geom().coords) == 1)
        self.assertTrue(g.geom().coords[0][0] == 1.0)
        self.assertTrue(g.geom().coords[0][1] == 20.1)



    def test_element_from_shp(self):
        pass