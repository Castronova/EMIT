__author__ = 'tonycastronova'

import unittest
import time
from models.topmodel import topmodel
from utilities.gui import parse_config

class test_topmodel(unittest.TestCase):

    def setUp(self):
        # add models
        self.mdl = '../topmodel.mdl'

    def test_initialize(self):

        config_params = parse_config(self.mdl)
        # load topmodel
        top = topmodel.topmodel(config_params)

        # check input exchange items
        in_items = top.inputs()
        self.assertTrue(len(in_items.keys()) == 1)
        self.assertTrue('precipitation' in in_items.keys())
        precip = in_items['precipitation']

        # check that input geometries were created
        precip_geoms = precip.getGeometries2()
        self.assertTrue(len(precip_geoms) > 0)

        # check input geometry type
        geom_type = precip_geoms[0].geom().geometryType()
        self.assertTrue(geom_type == 'Point')

        # check output exchange items
        out_items = top.outputs()
        self.assertTrue(len(out_items.keys()) == 1)
        self.assertTrue('streamflow' in out_items.keys())
        flow = out_items['streamflow']

        # check that output geoms exist
        flow_geoms = flow.getGeometries2()
        self.assertTrue(len(flow_geoms) > 0)

        # check output geometry type
        geom_type = flow_geoms[0].geom().geometryType()
        self.assertTrue(geom_type == 'LineString')

    def test_geometry_parsing(self):

        import time
        import numpy as np
        import matplotlib.pyplot as plt
        from shapely.geometry import Point
        import stdlib

        plt.ion()
        plt.show()

        geoms = []
        with open('./data/right_hand_fork_ti_trim.txt', 'r') as sr:

            lines = sr.readlines()
            # ncols = int(lines[0].split(' ')[-1].strip())
            nrows = int(lines[1].split(' ')[-1].strip())
            lowerx = float(lines[2].split(' ')[-1].strip())
            lowery = float(lines[3].split(' ')[-1].strip())
            cellsize = float(lines[4].split(' ')[-1].strip())
            nodata = lines[5].split(' ')[-1].strip()

            # set start x, y
            y = lowery + cellsize * nrows
            for line in lines[6:]:
                x = lowerx
                l = line.strip().split(' ')
                xy = []
                for element in l:
                    if element != nodata:
                        xy.append((x,y))


                        # plt.scatter(x,y)
                        # plt.draw()

                        # pt = Point(x,y)
                        # geoms.append(stdlib.Geometry(geom=pt))
                    x += cellsize
                if len(xy) > 0:
                    X,Y = zip(*xy)
                    plt.scatter(X,Y, c=np.random.rand(3,1))
                    plt.draw()
                y -= cellsize
            # plt.draw()
            print 'here'

    def test_run(self):

        # convert mdl into configuration parameters
        config_params = parse_config(self.mdl)

        # load topmodel
        top = topmodel.topmodel(config_params)

        # create some precipitation data at a random input location
        precip_gauge = top.inputs()['precipitation'].getGeometries2(100)

