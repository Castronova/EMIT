__author__ = 'tonycastronova'

import unittest
import time
from models.topmodel import topmodel
from utilities.gui import parse_config
from utilities import mdl
import stdlib
from coordinator import engineAccessors as engine
from transform.space import *
from transform.time import *

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
        from datetime import datetime as dt

        # load topmodel
        config_params = parse_config(self.mdl)
        top = topmodel.topmodel(config_params)


        # create exchange item
        unit = mdl.create_unit('international inch')
        variable = mdl.create_variable('Precipitation')
        item = stdlib.ExchangeItem(name='Weather Reader', unit=unit, variable=variable)
        data = '../data/precip_weather.csv'

        # read weather data
        incremental_precip = []
        dates = []
        with open(data, 'rU') as f:
            lines = f.readlines()
            # skip commented lines
            skip = 0
            for line in lines:
                if line[0] == '#':
                    skip += 1
                else:
                    # exit loop as soon as non-commented line is found
                    break

            # read all lines after header
            for line in lines[skip:]:
                data = line.split(',')

                # exit if the data is empty
                if data[0].strip() == '':
                    break

                # save dates to list
                dates.append(dt.strptime(data[0], "%m/%d/%y %H:%M"))

                # save incremental precipitation to list
                incremental_precip.append(float(data[2]))


        # set output data
        item.setValues2(incremental_precip, dates)



    def test_execute_simulation(self):

        import datatypes
        from coordinator import engine
        simulator = engine.Coordinator()



        # load randomizer component
        randomizer = simulator.add_model(id='randomizer',  attrib={'mdl':'../../test_models/randomizer/randomizer.mdl'})

        # load topmodel
        top = simulator.add_model(id='topmodel', attrib={'mdl':self.mdl})


        # add link between randomizer and topmodel
        link1 = simulator.add_link_by_name(from_id=randomizer['id'],
                                  from_item_name='random POINT 1-10',
                                  to_id=top['id'],
                                  to_item_name='precipitation')

        # set link tranformations
        spatial = SpatialInterpolation.NearestNeighbor
        spatial.set_param('max_distance', 1000)
        link1.spatial_interpolation(spatial)
        link1.temporal_interpolation(TemporalInterpolation.NearestNeighbor)

        print 'Starting Simulation'
        st = time.time()

        # begin execution
        simulator.run_simulation()

        print 'Simulation Complete \n Elapsed time = %3.2f seconds'%(time.time() - st)

