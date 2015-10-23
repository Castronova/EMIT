__author__ = 'tonycastronova'



from os import getcwd
from os.path import *
import unittest
from osgeo import ogr
from utilities import spatial
import stdlib




class test_spatial_utilities(unittest.TestCase):

    def setUp(self):



        self.point = abspath(join(getcwd(), 'data/sample gis/points.shp'))
        self.polygon = abspath(join(getcwd(), 'data/sample gis/polygons.shp'))
        self.polyline = abspath(join(getcwd(), 'data/sample gis/polylines.shp'))

    def tearDown(self):
        pass


    def test_read_shapefile_polygon(self):

        geoms, srs = spatial.read_shapefile(self.polygon)

        self.assertTrue(len(geoms) > 0)

        for i in range(len(geoms)):
            self.assertTrue(geoms[i].GetGeometryName() == stdlib.GeomType.POLYGON)
            self.assertTrue(isinstance(geoms[i], ogr._object))
            self.assertTrue(isinstance(geoms[i], stdlib.Geometry2))
            self.assertTrue("EMPTY" not in geoms[i].ExportToWkt())


    def test_read_shapefile_point(self):
        geoms, srs = spatial.read_shapefile(self.point)

        self.assertTrue(len(geoms) > 0)

        for i in range(len(geoms)):
            self.assertTrue(geoms[i].GetGeometryName() == stdlib.GeomType.POINT)
            self.assertTrue(isinstance(geoms[i], ogr._object))
            self.assertTrue(isinstance(geoms[i], stdlib.Geometry2))
            self.assertTrue("EMPTY" not in geoms[i].ExportToWkt())


    def test_read_shapefile_polyline(self):
        geoms, srs = spatial.read_shapefile(self.polyline)

        self.assertTrue(len(geoms) > 0)

        for i in range(len(geoms)):
            self.assertTrue(geoms[i].GetGeometryName() == stdlib.GeomType.LINESTRING)
            self.assertTrue(isinstance(geoms[i], ogr._object))
            self.assertTrue(isinstance(geoms[i], stdlib.Geometry2))
            self.assertTrue("EMPTY" not in geoms[i].ExportToWkt())



    def test_read_shapefile_multipolygon(self):
        pass

    def test_read_shapefile_multipoint(self):
        pass

    def test_read_shapefile_mulitpolyline(self):
        pass
