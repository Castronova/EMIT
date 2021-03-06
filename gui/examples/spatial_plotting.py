__author__ = 'tonycastronova'


import wx
import random
from osgeo import ogr
from gui.controller.SpatialPlotCtrl import *
import unittest
import utilities.geometry

class test_spatial_plotting(unittest.TestCase):

    def setUp(self):
        pass


    def test_polygons(self):
        app = wx.App()

        frame = wx.Frame(None, -1)

        plot = SpatialPlotCtrl(frame)


        # create some test polygons
        random.seed()
        geoms = []
        for j in range(100):
            cx = random.randint(0, 1000)
            cy = random.randint(0, 1000)

            # Create ring
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(cx-10, cy-10)
            ring.AddPoint(cx-8, cy+10)
            ring.AddPoint(cx, cy+12)
            ring.AddPoint(cx+10, cy+8)
            ring.AddPoint(cx+10, cy-8)
            ring.AddPoint(cx, cy-10)
            ring.AddPoint(cx-10, cy-10)

            # Create polygon
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)

            # save as wkb
            geoms.append(poly.ExportToWkb())

        poly = []
        for i in range(0, len(geoms)):
            g = ogr.CreateGeometryFromWkb(geoms[i])
            poly.append(g)

        # set the input data
        test_data = {'testvar':poly}
        plot.set_input_data(test_data)
        self.assertEqual(plot.get_input_geom('testvar'), test_data['testvar'],msg="Data was not set correctly in logicSpatialPlot")

        plot.set_selection_input('testvar')
        plot.updatePlot()

        del app


    def test_points(self):
        app = wx.App()

        frame = wx.Frame(None, -1)

        plot = SpatialPlotCtrl(frame)


        pts = []
        for i in range(0,100):
            pt = ogr.Geometry(ogr.wkbPoint)

            r1 = random.random()
            r2 = random.random()

            pt.AddPoint(r1,r2)

            pts.append(pt)

        # set the input data
        test_data = {'testvar':pts}
        plot.set_input_data(test_data)
        self.assertEqual(plot.get_input_geom('testvar'), test_data['testvar'],msg="Data was not set correctly in logicSpatialPlot")

        plot.set_selection_input('testvar')
        plot.updatePlot()

        del app


    def test_polylines(self):
        app = wx.App()

        frame = wx.Frame(None, -1)

        plot = SpatialPlotCtrl(frame)


        lines = []
        for i in range(0,100):
            r1 = random.random()
            r2 = random.random()
            line = ogr.Geometry(ogr.wkbLineString)
            line.AddPoint(r1, r2)
            line.AddPoint(r1+.05, r2+.1)
            line.AddPoint(r1+.1, r2-.1)
            line.AddPoint(r1+.15, r2+.1)
            line.AddPoint(r1+.2, r2-.1)
            lines.append(line)

        # set the input data
        test_data = {'testvar':lines}
        plot.set_input_data(test_data)
        self.assertEqual(plot.get_input_geom('testvar'), test_data['testvar'],msg="Data was not set correctly in logicSpatialPlot")

        plot.set_selection_input('testvar')
        plot.updatePlot()

        del app


    def test_poly_from_wkt(self):
        app = wx.App()

        frame = wx.Frame(None, -1)

        plot = SpatialPlotCtrl(frame)

        wkt = 'POLYGON ((30 10, 40 40, 20 40, 10 20, 30 10))'
        geom = utilities.geometry.fromWKT(wkt)

        # set the input data
        test_data = {'testvar':geom}
        plot.set_input_data(test_data)
        plot.set_selection_input('testvar')
        plot.updatePlot()

        del app