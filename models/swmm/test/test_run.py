__author__ = 'tonycastronova'

from os.path import *
import unittest
from datetime import datetime
import utilities

import matplotlib.pyplot as plt
from descartes.patch import *

from examples.swmm.src import geometry
from examples.swmm.src import swmm_wrapper


# from ..src.parse_swmm import *

import time

class test_swmm(unittest.TestCase):

    def test_init(self):

        # get the configuration file
        mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))

        # parse the configuration parameters
        params = utilities.parse_config_without_validation(mdl)

        # initialize swmm
        swmm = swmm_wrapper.swmm(params)

        # verify that the model has initialized properly
        self.assertTrue(swmm.simulation_start() == datetime(2013,2,4,0,0,0))
        self.assertTrue(swmm.simulation_end() == datetime(2013,2,5,0,0,0))
        self.assertTrue(swmm.time_step() == (5,'minute'))
        self.assertTrue(swmm.name() == 'SWMM')


    def test_execute_no_inputs(self):

        # initialize swmm
        mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
        params = utilities.parse_config_without_validation(mdl)
        swmm = swmm_wrapper.swmm(params)

        # run the simulation
        inputs = []
        self.assertTrue(swmm.run(inputs))

        # parse outputs
        print 'done'


    def test_build_swmm_geoms(self):
        # initialize swmm
        mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
        params = utilities.parse_config_without_validation(mdl)
        swmm = swmm_wrapper.swmm(params)

        inp =abspath(join(dirname(__file__),'../data/sim.inp'))

        # build link geometries
        link_geoms = swmm.build_swmm_geoms(inp,'vertices')


        import matplotlib.pyplot as plt
        from numpy import asarray
        cmap = plt.cm.Blues


        num_colors = len(link_geoms)
        colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

        for i in range(0,len(link_geoms)):

            #rgb = tuple([last[i] + inc[i] for i in range(0,len(last)-1)] + [1.0])

            #last = rgb

            l = asarray(link_geoms[i][1])
            plt.plot(l[:,0], l[:,1],color='k')


        plt.show()
        #plt.ioff() # turn off interactive mode

        # parse outputs
        print 'done'



    def test_build_polygons(self):

        # initialize swmm
        mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
        params = utilities.parse_config_without_validation(mdl)
        swmm = swmm_wrapper.swmm(params)

        inp =abspath(join(dirname(__file__),'../data/sim.inp'))

        # build link geometries
        geoms = geometry.build_catchments(inp)




        plt.ion()

        fig = plt.figure(1, figsize=(5,5), dpi=180)
        ax = fig.add_subplot(111)

        cmap = plt.cm.Blues
        num_colors = len(geoms)
        colors = [cmap(1.*i/num_colors) for i in range(num_colors)]


        for i in range(0,len(geoms)):


            geom = geoms[i][1]

            patch = PolygonPatch(geom,facecolor=colors[i])
            ax.add_patch(patch)


        ax.axis('auto')
        plt.draw()

        plt.ioff()
        plt.show()
       # time.sleep(2)


    def test_build_coordinates(self):

        # initialize swmm
        mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
        params = utilities.parse_config_without_validation(mdl)
        swmm = swmm_wrapper.swmm(params)

        inp =abspath(join(dirname(__file__),'../data/sim.inp'))

        # build link geometries
        geoms = geometry.build_coordinates(inp)


        plt.ion()

        fig = plt.figure(1, figsize=(5,5), dpi=180)
        ax = fig.add_subplot(111)
        ax.axis('auto')

        cmap = plt.cm.Blues
        num_colors = len(geoms)
        colors = [cmap(1.*i/num_colors) for i in range(num_colors)]


        for i in range(0,len(geoms)):

            geom = geoms[i][1]

            patch = PolygonPatch(geom.buffer(10),facecolor=colors[i])
            ax.add_patch(patch)


            ax.axis('auto')

            plt.draw()



        time.sleep(2)


    def test_build_links(self):

        # initialize swmm
        mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
        params = utilities.parse_config_without_validation(mdl)
        swmm = swmm_wrapper.swmm(params)

        inp =abspath(join(dirname(__file__),'../data/sim.inp'))

        # build link geometries
        #geoms = geometry.build_links(inp)
        geoms = geometry.connect_coordinates(inp)

        #geoms.extend(geometry.build_coordinates(inp))


        plt.ion()

        fig = plt.figure(1, figsize=(5,5), dpi=180)
        ax = fig.add_subplot(111)

        cmap = plt.cm.Blues
        num_colors = len(geoms)
        colors = [cmap(1.*i/num_colors) for i in range(num_colors)]


        for i in range(0,len(geoms)):


            geom = geoms[i]

            patch = PolygonPatch(geom.buffer(2),facecolor=colors[i])
            ax.add_patch(patch)


            ax.axis('auto')
            plt.draw()

        plt.ioff()
        plt.show()


    def test_get_output(self):
        o =abspath(join(dirname(__file__),'../data/sim.out'))



        # get variables
        vars = listvariables(o)

        for k, v in vars.iteritems():
            print k,v
