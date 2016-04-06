__author__ = 'tonycastronova'

import stdlib
import numpy
import unittest
from utilities.geometry import *

class test_geometry(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gdal_requirements(self):
        pass

    # ---------------------------------------
    # TESTS FOR POINT GENERATION
    # ---------------------------------------
    def test_build_points_single_gdal(self):

        # create an x, y point
        x = 10
        y = 15

        # use utility function to build geometries
        geoms = build_point_geometries(x, y)

        pts = geoms[0].GetPoints()
        self.assertTrue(len(geoms) == 1)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == x)
        self.assertTrue(pts[0][1] == y)
        self.assertTrue(pts[0][2] == 0)

    def test_build_points_list_gdal(self):

        # create list of points
        x = [1,2,3,4,5]
        y = [5,4,3,2,1]

        # use utility function to build geometries
        geoms = build_point_geometries(x, y,)

        pts = geoms[0].GetPoints()
        self.assertTrue(len(geoms) == 5)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == x[0])
        self.assertTrue(pts[0][1] == y[0])
        self.assertTrue(pts[0][2] == 0)

    def test_build_points_numpy_gdal(self):
        # create list of points
        x = numpy.array([1,2,3,4,5])
        y = numpy.array([5,4,3,2,1])

        # use utility function to build geometries
        geoms = build_point_geometries(x, y)

        pts = geoms[0].GetPoints()
        self.assertTrue(len(geoms) == 5)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == x[0])
        self.assertTrue(pts[0][1] == y[0])
        self.assertTrue(pts[0][2] == 0)

    def test_build_points_mismatched_gdal(self):
        # create list of x points
        x = [1,2,3,4,5]

        # define y as a single point
        y = 5

        # use utility function to build geometries
        geoms = build_point_geometries(x, y)

        self.assertTrue(geoms == None)

    # ---------------------------------------
    # TESTS FOR POLYGON GENERATION
    # ---------------------------------------

    def test_build_polygon_list_gdal(self):

        # create x,y points for polygon
        coords = [
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                 ]

        # use utility function to build geometries
        geoms = build_polygon_geometries(coords)

        geomref = geoms[0].GetGeometryRef(0)
        pts = geomref.GetPoints()

        self.assertTrue(len(geoms) == 1)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == coords[0][0][0])
        self.assertTrue(pts[0][1] == coords[0][0][1])
        self.assertTrue(pts[0][2] == 0)

    def test_build_polygon_single_gdal(self):

        # create x,y points for polyline
        coords = [(0,0), (0,2), (2,2), (2,0), (0,0)]

        # use utility function to build geometries
        geoms = build_polygon_geometries(coords)

        geomref = geoms[0].GetGeometryRef(0)
        pts = geomref.GetPoints()

        self.assertTrue(len(geoms) == 1)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == coords[0][0])
        self.assertTrue(pts[0][1] == coords[0][1])
        self.assertTrue(pts[0][2] == 0)

    def test_build_polygon_many_gdal(self):

        # create x,y points for polygon
        coords = [
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                 ]

        # use utility function to build geometries
        geoms = build_polygon_geometries(coords)

        geomref = geoms[0].GetGeometryRef(0)
        pts = geomref.GetPoints()

        self.assertTrue(len(geoms) == 6)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == coords[0][0][0])
        self.assertTrue(pts[0][1] == coords[0][0][1])
        self.assertTrue(pts[0][2] == 0)

    def test_build_polygon_numpy_gdal(self):

        # create x,y points for polygon
        coords = numpy.array([
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                 ])

        # use utility function to build geometries
        geoms = build_polygon_geometries(coords)

        geomref = geoms[0].GetGeometryRef(0)
        pts = geomref.GetPoints()

        self.assertTrue(len(geoms) == 7)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == coords[0][0][0])
        self.assertTrue(pts[0][1] == coords[0][0][1])
        self.assertTrue(pts[0][2] == 0)


    # ---------------------------------------
    # TESTS FOR POLYLINE GENERATION
    # ---------------------------------------

    def test_build_polyline_list_gdal(self):

        # create x,y points for polyline
        coords = [
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                 ]

        # use utility function to build geometries
        geoms = build_polyline_geometries(coords)

        pts = geoms[0].GetPoints()

        self.assertTrue(len(geoms) == 1)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == coords[0][0][0])
        self.assertTrue(pts[0][1] == coords[0][0][1])
        self.assertTrue(pts[0][2] == 0)

    def test_build_polyline_single_gdal(self):

        # create x,y points for polyline
        coords = [(0,0), (0,2), (2,2), (2,0), (0,0)]

        # use utility function to build geometries
        geoms = build_polyline_geometries(coords)

        pts = geoms[0].GetPoints()

        self.assertTrue(len(geoms) == 1)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == coords[0][0])
        self.assertTrue(pts[0][1] == coords[0][1])
        self.assertTrue(pts[0][2] == 0)

    def test_build_polyline_numpy_gdal(self):

        # create x,y points for polyline
        coords = numpy.array([
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                 ])

        # use utility function to build geometries
        geoms = build_polyline_geometries(coords)

        pts = geoms[0].GetPoints()

        self.assertTrue(len(geoms) == 1)
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == coords[0][0][0])
        self.assertTrue(pts[0][1] == coords[0][0][1])
        self.assertTrue(pts[0][2] == 0)

    def test_build_polyline_many_gdal(self):

        # create x,y points for polyline
        coords = numpy.array([
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                    ((0,0), (0,2), (2,2), (2,0), (0,0)),
                 ])

        # use utility function to build geometries
        geoms = build_polyline_geometries(coords)

        pts = geoms[0].GetPoints()

        self.assertTrue(len(geoms) == coords.shape[0])
        self.assertTrue(isinstance(geoms[0], ogr._object))
        self.assertTrue(isinstance(geoms[0], stdlib.Geometry2))
        self.assertTrue(pts[0][0] == coords[0][0][0])
        self.assertTrue(pts[0][1] == coords[0][0][1])
        self.assertTrue(pts[0][2] == 0)

    # ---------------------------------------
    # TESTS FOR WKT GEOMETRY GENERATION
    # ---------------------------------------

    def test_point_from_wkt(self):

        wkt = 'POINT(15 12)'

        geoms = fromWKT(wkt)

        self.assertTrue(len(geoms) > 0)
        for i in range(len(geoms)):
            self.assertTrue(isinstance(geoms[i], ogr._object))
            self.assertTrue(isinstance(geoms[i], stdlib.Geometry2))
            self.assertTrue("EMPTY" not in geoms[i].ExportToWkt())

    def test_polygon_from_wkt(self):
        wkt = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'

        geoms = fromWKT(wkt)

        self.assertTrue(len(geoms) > 0)
        for i in range(len(geoms)):
            self.assertTrue(isinstance(geoms[i], ogr._object))
            self.assertTrue(isinstance(geoms[i], stdlib.Geometry2))
            self.assertTrue("EMPTY" not in geoms[i].ExportToWkt())

    def test_polyline_from_wkt(self):
        wkt = 'LINESTRING (30 10, 10 30, 40 40)'

        geoms = fromWKT(wkt)

        self.assertTrue(len(geoms) > 0)
        for i in range(len(geoms)):
            self.assertTrue(isinstance(geoms[i], ogr._object))
            self.assertTrue(isinstance(geoms[i], stdlib.Geometry2))
            self.assertTrue("EMPTY" not in geoms[i].ExportToWkt())

    def test_multipolyline_from_wkt(self):
        wkt = "MULTILINESTRING ((10 10, 20 20, 10 40), (40 40, 30 30, 40 20, 30 10))"

        geoms = fromWKT(wkt)

        self.assertTrue(len(geoms) > 0)
        for i in range(len(geoms)):
            self.assertTrue(isinstance(geoms[i], ogr._object))
            self.assertTrue(isinstance(geoms[i], stdlib.Geometry2))
            self.assertTrue("EMPTY" not in geoms[i].ExportToWkt())

    def test_multipoint_from_wkt(self):
        wkt = "MULTIPOINT ((10 40), (40 30), (20 20), (30 10))"

        geoms = fromWKT(wkt)

        self.assertTrue(len(geoms) > 0)
        for i in range(len(geoms)):
            self.assertTrue(isinstance(geoms[i], ogr._object))
            self.assertTrue(isinstance(geoms[i], stdlib.Geometry2))
            self.assertTrue("EMPTY" not in geoms[i].ExportToWkt())

    def test_multipolygon_from_wkt(self):
        wkt = "MULTIPOLYGON (((30 20, 45 40, 10 40, 30 20)),((15 5, 40 10, 10 20, 5 10, 15 5)))"

        geoms = fromWKT(wkt)

        self.assertTrue(len(geoms) > 0)
        for i in range(len(geoms)):
            self.assertTrue(isinstance(geoms[i], ogr._object))
            self.assertTrue(isinstance(geoms[i], stdlib.Geometry2))
            self.assertTrue("EMPTY" not in geoms[i].ExportToWkt())


