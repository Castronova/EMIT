__author__ = 'tonycastronova'

import unittest
import time
import timeit
import os

import numpy
from osgeo import ogr

from models.topmodel import topmodel
from utilities.gui import parse_config
from transform.space import *
from transform.time import *
import stdlib


class test_topmodel(unittest.TestCase):

    def setUp(self):
        # add models
        self.mdl = '../topmodel.mdl'

        config_params = parse_config(self.mdl)
        self.ti =  config_params['model inputs'][0]['ti']

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
        geom_type = precip_geoms[0].GetGeometryName()
        self.assertTrue(geom_type == stdlib.GeomType.POLYGON)

        # check output exchange items
        # out_items = top.outputs()
        # self.assertTrue(len(out_items.keys()) == 1)
        # self.assertTrue('streamflow' in out_items.keys())
        # flow = out_items['streamflow']

        # # check that output geoms exist
        # flow_geoms = flow.getGeometries2()
        # self.assertTrue(len(flow_geoms) > 0)
        #
        # # check output geometry type
        # geom_type = flow_geoms[0].geom().geometryType()
        # self.assertTrue(geom_type == 'LineString')

    def test_geometry_parsing(self):

        geoms = []
        with open('./data/right_hand_fork_ti_trim.txt', 'r') as sr:

            lines = sr.readlines()
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
                        geom = stdlib.Geometry2(ogr.wkbPoint)
                        geom.AddPoint(x, y)
                        geoms.append(geom)
                    x += cellsize
                y -= cellsize

        return geoms

    def test_geometry_parsing_numpy(self):

        import numpy as np
        import matplotlib.pyplot as plt
        import utilities.geometry

        topo_input = './data/right_hand_fork_ti_trim.txt'

        # plt.ion()
        # plt.show()

        nrows = 0
        ncols = 0
        cellsize = 0
        lowerx = 0
        lowery = 0
        with open(topo_input, 'r') as sr:

            lines = sr.readlines()
            ncols = int(lines[0].split(' ')[-1].strip())
            nrows = int(lines[1].split(' ')[-1].strip())
            lowerx = float(lines[2].split(' ')[-1].strip())
            lowery = float(lines[3].split(' ')[-1].strip())
            cellsize = float(lines[4].split(' ')[-1].strip())
            nodata = float(lines[5].split(' ')[-1].strip())

            # read ti data
            data = np.genfromtxt(topo_input, delimiter=' ', skip_header=6)

        # build X and Y coordinate arrays
        xi = np.linspace(lowerx, lowerx+ncols*cellsize, ncols)
        yi = np.linspace(lowery+nrows*cellsize, lowery, nrows)
        x,y = np.meshgrid(xi,yi)    # generate 2d arrays from xi, yi
        x = x.ravel()   # convert to 1-d
        y = y.ravel()   # convert to 1-d
        data = data.ravel()  # convert to 1-d

        # remove all nodata points from x, y arrays
        nonzero = np.where(data != nodata)
        x = x[nonzero]
        y = y[nonzero]

        points = utilities.geometry.build_point_geometries(x,y)
        # self.create_point_shapefile(points, data)

        # # return points
        # X = x[::4]
        # Y = y[::4]
        # plt.scatter(X, Y, s=.5, edgecolors='none',color='blue')
        # plt.draw()
        # plt.show()

    def test_execute_simulation(self):

        from coordinator import engine
        simulator = engine.Coordinator()



        # load randomizer component
        weather = simulator.add_model(id='weather',  attrib={'mdl':'../../test_models/weather/weatherReader.mdl'})

        # load topmodel
        top = simulator.add_model(id='topmodel', attrib={'mdl':self.mdl})


        # add link between randomizer and topmodel
        link1 = simulator.add_link_by_name(from_id=weather['id'],
                                  from_item_name='Precipitation',
                                  to_id=top['id'],
                                  to_item_name='precipitation')

        # set link tranformations
        link1.spatial_interpolation(SpatialInterpolation.ExactMatch)
        link1.temporal_interpolation(TemporalInterpolation.NearestNeighbor)

        print 'Starting Simulation'
        st = time.time()

        # begin execution
        simulator.run_simulation()

        print 'Simulation Complete \n Elapsed time = %3.2f seconds'%(time.time() - st)

    def create_point_shapefile(self, point_list, data):
        # Save extent to a new Shapefile
        outShapefile = "/Users/tonycastronova/Documents/windows_shared/temp/check_pts.shp"
        outDriver = ogr.GetDriverByName("ESRI Shapefile")

        # Remove output shapefile if it already exists
        if os.path.exists(outShapefile):
            outDriver.DeleteDataSource(outShapefile)

        # Create the output shapefile
        datasource = outDriver.CreateDataSource(outShapefile)
        layer = datasource.CreateLayer("points", geom_type=ogr.wkbPoint)

        # Add an ID field
        layer.CreateField(ogr.FieldDefn("Value", ogr.OFTInteger))

        i = 0
        for i in range(0, len(point_list)):

            p = point_list[i]
            v = data[i]

            feature = ogr.Feature(layer.GetLayerDefn())
            feature.SetField("Value", v)

            feature.SetGeometry(p)
            layer.CreateFeature(feature)
            feature.Destroy()
            i+= 1

        datasource.Destroy()

    def test_read_topo_input(self):

        # ---- begin reading the values stored in the topo file
        with open(self.ti, 'r') as sr:

            lines = sr.readlines()
            cellsize = float(lines[4].split(' ')[-1].strip())
            nodata = lines[5].split(' ')[-1].strip()

            # generate topolist by parsing cell data
            topoList = [item for sublist in lines[6:] for item in sublist.strip().split(' ') if item != nodata]
            self._watershedArea = len(topoList) * cellsize


        # ---- calculate frequency of each topographic index
        # -- consolidate topo list into unique values
        d = {float(i):float(topoList.count(i)) for i in set(topoList)}

        # -- calculate topo frequency, then return both topographic index and topo frequency arrays
        total = len(topoList)
        ti = [round(k,4) for k in d.iterkeys()]
        freq = [round((k/total), 10) for k in d.iterkeys()]

        return ti, freq

    def test_read_topo_input_optimized(self):

        # read the header values in the topo file
        ncols = 0
        nrows = 0
        lowerx = 0
        lowery = 0
        cellsize = 0
        nodata = 0
        with open(self.ti, 'r') as sr:

            lines = sr.readlines()
            ncols = int(lines[0].split(' ')[-1].strip())
            nrows = int(lines[1].split(' ')[-1].strip())
            lowerx = float(lines[2].split(' ')[-1].strip())
            lowery = float(lines[3].split(' ')[-1].strip())
            cellsize = float(lines[4].split(' ')[-1].strip())
            nodata = float(lines[5].split(' ')[-1].strip())

        # read ti data
        data = numpy.genfromtxt(self.ti, delimiter=' ', skip_header=6)

        topoList = data.ravel() # convert into 1-d list
        topoList = topoList[topoList != nodata] # remove nodata values
        watershedArea = topoList.shape[0]*cellsize  # calculate watershed area


        topoList = numpy.round(topoList, 4)         # round topoList items
        total = topoList.shape[0]                   # total number of element in the topoList
        unique, counts = numpy.unique(topoList, return_counts=True)    # get bins for topoList elements

        ti = unique                         # topographic index list
        freq = unique/total                 # freq of topo indices
        freq = numpy.round(freq, 10)        # round the frequencies

        return ti, freq

    def test_benchmark(self):
        benchmarks = []

        # print 'Benchmarking  test_geometry_parsing ...',
        # t = timeit.Timer(lambda: self.test_geometry_parsing())
        # time = min(t.repeat(1,1))
        # benchmarks.append([time, '%3.5f sec:\t\ttest_geometry_parsing' % time ])
        # print 'done'
        #
        # print 'Benchmarking  test_geometry_parsing_numpy ...',
        # t = timeit.Timer(lambda: self.test_geometry_parsing_numpy())
        # time = min(t.repeat(1,1))
        # benchmarks.append([time, '%3.5f sec:\t\ttest_geometry_parsing_numpy' % time ])
        # print 'done'

        print 'Benchmarking  test_read_topo_input ...',
        t = timeit.Timer(lambda: self.test_read_topo_input())
        time = min(t.repeat(1,1))
        benchmarks.append([time, '%3.5f sec:\t\ttest_read_topo_input' % time ])
        print 'done'

        print 'Benchmarking  test_read_topo_input_optimized ...',
        t = timeit.Timer(lambda: self.test_read_topo_input_optimized())
        time = min(t.repeat(1,1))
        benchmarks.append([time, '%3.5f sec:\t\ttest_read_topo_input_optimized' % time ])
        print 'done'

        sorted_benchmarks = sorted(benchmarks,key=lambda x: x[0])
        print '\n' + 36*'-'
        print 'Fastest Algorithms'
        print 36*'-'
        for b in sorted_benchmarks:
            print b[1]

    def test_validate_optimizations(self):

        # this will fail because the optimized method uses gdal geoms instead of shapely geoms
        # g1 = self.test_geometry_parsing()
        # g2 = self.test_geometry_parsing_numpy()
        # self.assertTrue(len(g1) == len(g2))
        # self.assertItemsEqual(g1, g2)

        ti1, freq1 = self.test_read_topo_input()
        ti2, freq2 = self.test_read_topo_input_optimized()
        self.assertTrue(len(ti1) == len(ti2))
        self.assertTrue(len(freq1) == len(freq2))
        self.assertItemsEqual(ti1, ti2)
        self.assertItemsEqual(freq1, freq2)

