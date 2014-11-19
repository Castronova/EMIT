__author__ = 'tonycastronova'

from os.path import *
import unittest
from datetime import datetime
from utilities import gui
import matplotlib.pyplot as plt
from descartes.patch import *
from models.swmm.src import geometry
#from models.caleb_swmm.src import swmm_wrapper
from ctypes import *
import copy

# from ..src.parse_swmm import *

import time

from models.caleb_swmm.src.structures import *



# int  DLLEXPORT   swmm_run(char* f1, char* f2, char* f3)
# int  DLLEXPORT   swmm_open(char* f1, char* f2, char* f3)
# int  DLLEXPORT   swmm_start(int saveFlag)
# int  DLLEXPORT   swmm_step(double* elapsedTime)
# int  DLLEXPORT   swmm_end(void)
# int  DLLEXPORT   swmm_report(void)
# int  DLLEXPORT   swmm_getMassBalErr(float* runoffErr, float* flowErr, float* qualErr)
# int  DLLEXPORT   swmm_close(void)
# int  DLLEXPORT   swmm_getVersion(void)
#
# #additional
# double DLLEXPORT swmm_getDateTime(char* beginorend)
# void DLLEXPORT  datetime_decodeDateTime(DateTime dateTime, int* y, int* m, int* d, int* h, int* mm, int* s)
# SDLLEXPORT char * getErrorMsg(int errorCode)
# int DLLEXPORT getObjectTypeCount(int type)
#
# #TNode
# SDLLEXPORT TNode* STDCALL getNode(int index)
# SDLLEXPORT TNode* STDCALL getNodeById(char* id)
# void DLLEXPORT setNode(TNode* node , char* propertyName)
#
# #TLink
# SDLLEXPORT TLink*  STDCALL getLink(int index)
# SDLLEXPORT TLink* STDCALL getLinkById(char* id)
# void DLLEXPORT setLink(TLink* link, char* propertyName)
#
# #TSubcatch
# SDLLEXPORT TSubcatch*  STDCALL getSubcatch(int index)
# SDLLEXPORT TSubcatch* STDCALL getSubcatchById(char* id)
# void DLLEXPORT setSubcatch(TSubcatch* subCatch, char* propertyName)




class test_swmm(unittest.TestCase):

    def setUp(self):

        # get the input file path
        self.__inp =abspath(join(dirname(__file__),'../Debug/Logan.inp'))
        self.__rpt =abspath(join(dirname(__file__),'../Debug/Logan.rpt'))
        self.__out =abspath(join(dirname(__file__),'../Debug/Logan.out'))

        # load the dylib
        self.__swmmLib = CDLL("../Debug/libSWMMQOpenMI.dylib")

    def tearDown(self):

        print 'Ending...'
        # End the swmm simulation
        error = self.__swmmLib.swmm_end()

        print 'Reporting...'
        error = self.__swmmLib.swmm_report()

        print 'Closing...'
        # close the swmm model
        self.__swmmLib.swmm_close()

    def test_init(self):


        # Open the swmm model
        # int error = open(inputFile, reportFile, outPutFile)
        error = self.__swmmLib.swmm_open(self.__inp,self.__rpt,self.__out)
        self.assertFalse(error)

        error = self.__swmmLib.swmm_start(True)
        self.assertFalse(error)

        self.__swmmLib.swmm_getDateTime.restype = c_double
        begin = c_double( self.__swmmLib.swmm_getDateTime(c_char_p('begin')))
        end = c_double( self.__swmmLib.swmm_getDateTime(c_char_p('end')))

        year = c_int(0)
        month = c_int(0)
        day = c_int(0)
        hour = c_int(0)
        minute = c_int(0)
        second = c_int(0)

        self.__swmmLib.datetime_decodeDateTime(end, byref(year), byref(month), byref(day), byref(hour), byref(minute), byref(second))
        self.__end_time = datetime(year.value,month.value,day.value,hour.value,minute.value,second.value)

        self.__swmmLib.datetime_decodeDateTime(begin, byref(year), byref(month), byref(day), byref(hour), byref(minute), byref(second))
        self.__begin_time = datetime(year.value,month.value,day.value,hour.value,minute.value,second.value)

        print self.__begin_time
        print self.__end_time


        self.__swmmLib.getObjectTypeCount.restype = c_int
        count = self.__swmmLib.getObjectTypeCount(SWMM_Types.SUBCATCH)
        self.__swmmLib.getSubcatch.restype = POINTER(TSubcatch)
        self.__swmmLib.setSubcatch.argtypes = [POINTER(TSubcatch), c_char_p]

        print 'Running...'
        elapsedTime = 1
        step = c_double()

        while 1:

            for i in range(0, count):
                sub = self.__swmmLib.getSubcatch(c_int(i))
                sub.contents.rainfall = 1
                self.__swmmLib.setSubcatch(sub,c_char_p('rainfall'))


            error = self.__swmmLib.swmm_step(byref(step))
            self.assertFalse(error)

            elapsedTime = begin.value + step.value

            self.__swmmLib.datetime_decodeDateTime(c_double(elapsedTime), byref(year), byref(month), byref(day), byref(hour), byref(minute), byref(second))
            self._current_time = datetime(year.value,month.value,day.value,hour.value,minute.value,second.value)

            if step.value <= 0.:
                break




        #code = c_int(139)
        #self.__swmmLib.getErrorMsg.restype = c_char_p
        #response = self.__swmmLib.getErrorMsg(code)

        print 'done'

        #self.assertTrue(node.contents.outflow == 100)

        # make sure that the model loads properly
        #self.assertFalse(error)


    def test_run(self):

        error = self.__swmmLib.swmm_run(self.__inp,self.__rpt,self.__out)
        self.assertFalse(error)


    def test_perform_time_step(self):

        self.test_init()

        # start the simulation
        error = self.__swmmLib.swmm_start(True)
        self.assertFalse(error)

        # int  DLLEXPORT   swmm_step(double* elapsedTime)
        # current elapsed time in decimal days
        tstep = c_double(0.)
        error = self.__swmmLib.swmm_step(byref(tstep))
        self.assertFalse(error)







        # # get the configuration file
        # mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
        #
        # # parse the configuration parameters
        # params = gui.parse_config_without_validation(mdl)
        #
        # # initialize swmm
        # swmm = swmm_wrapper.swmm(params)
        #
        # # verify that the model has initialized properly
        # self.assertTrue(swmm.simulation_start() == datetime(2013,2,4,0,0,0))
        # self.assertTrue(swmm.simulation_end() == datetime(2013,2,5,0,0,0))
        # self.assertTrue(swmm.time_step() == (5,'minute'))
        # self.assertTrue(swmm.name() == 'SWMM')


    # def test_execute_no_inputs(self):
    #
    #     # initialize swmm
    #     mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
    #     params = gui.parse_config_without_validation(mdl)
    #     swmm = swmm_wrapper.swmm(params)
    #
    #     # run the simulation
    #     inputs = []
    #     self.assertTrue(swmm.run(inputs))
    #
    #     # parse outputs
    #     print 'done'
    #
    #
    # def test_build_swmm_geoms(self):
    #     # initialize swmm
    #     mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
    #     params = gui.parse_config_without_validation(mdl)
    #     swmm = swmm_wrapper.swmm(params)
    #
    #     inp =abspath(join(dirname(__file__),'../data/simulation.inp'))
    #
    #     # build link geometries
    #     link_geoms = swmm.build_swmm_geoms(inp,'vertices')
    #
    #
    #     import matplotlib.pyplot as plt
    #     from numpy import asarray
    #     cmap = plt.cm.Blues
    #
    #
    #     num_colors = len(link_geoms)
    #     colors = [cmap(1.*i/num_colors) for i in range(num_colors)]
    #
    #     for i in range(0,len(link_geoms)):
    #
    #         #rgb = tuple([last[i] + inc[i] for i in range(0,len(last)-1)] + [1.0])
    #
    #         #last = rgb
    #
    #         l = asarray(link_geoms[i][1])
    #         plt.plot(l[:,0], l[:,1],color='k')
    #
    #
    #     plt.show()
    #     #plt.ioff() # turn off interactive mode
    #
    #     # parse outputs
    #     print 'done'
    #
    #
    #
    # def test_build_polygons(self):
    #
    #     # initialize swmm
    #     mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
    #     params = gui.parse_config_without_validation(mdl)
    #     swmm = swmm_wrapper.swmm(params)
    #
    #     inp =abspath(join(dirname(__file__),'../data/simulation.inp'))
    #
    #     # build link geometries
    #     geoms = geometry.build_catchments(inp)
    #
    #
    #
    #
    #     plt.ion()
    #
    #     fig = plt.figure(1, figsize=(5,5), dpi=180)
    #     ax = fig.add_subplot(111)
    #
    #     cmap = plt.cm.Blues
    #     num_colors = len(geoms)
    #     colors = [cmap(1.*i/num_colors) for i in range(num_colors)]
    #
    #
    #     for i in range(0,len(geoms)):
    #
    #
    #         geom = geoms[i][1]
    #
    #         patch = PolygonPatch(geom,facecolor=colors[i])
    #         ax.add_patch(patch)
    #
    #
    #     ax.axis('auto')
    #     plt.draw()
    #
    #     plt.ioff()
    #     plt.show()
    #    # time.sleep(2)
    #
    #
    # def test_build_coordinates(self):
    #
    #     # initialize swmm
    #     mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
    #     params = gui.parse_config_without_validation(mdl)
    #     swmm = swmm_wrapper.swmm(params)
    #
    #     inp =abspath(join(dirname(__file__),'../data/simulation.inp'))
    #
    #     # build link geometries
    #     geoms = geometry.build_coordinates(inp)
    #
    #
    #     # plt.ion()
    #
    #     fig = plt.figure(1, figsize=(5,5), dpi=180)
    #     ax = fig.add_subplot(111)
    #     ax.axis('auto')
    #
    #     cmap = plt.cm.Blues
    #     num_colors = len(geoms)
    #     colors = [cmap(1.*i/num_colors) for i in range(num_colors)]
    #
    #
    #     for i in range(0,len(geoms)):
    #
    #         geom = geoms[i][1]
    #
    #         patch = PolygonPatch(geom.buffer(10),facecolor=colors[i])
    #         ax.add_patch(patch)
    #
    #
    #         ax.axis('auto')
    #
    #     plt.draw()
    #
    #
    #     plt.show()
    #     #time.sleep(2)
    #
    #
    # def test_build_links(self):
    #
    #     # initialize swmm
    #     mdl = abspath(join(dirname(__file__),'../src/swmm.mdl'))
    #     params = gui.parse_config_without_validation(mdl)
    #     swmm = swmm_wrapper.swmm(params)
    #
    #     inp =abspath(join(dirname(__file__),'../data/simulation.inp'))
    #
    #     # build link geometries
    #     #geoms = geometry.build_links(inp)
    #     geoms = geometry.connect_coordinates(inp)
    #
    #     #geoms.extend(geometry.build_coordinates(inp))
    #
    #
    #     # plt.ion()
    #
    #     fig = plt.figure(1, figsize=(5,5), dpi=180)
    #     ax = fig.add_subplot(111)
    #
    #     cmap = plt.cm.Blues
    #     num_colors = len(geoms)
    #     colors = [cmap(1.*i/num_colors) for i in range(num_colors)]
    #
    #
    #     for i in range(0,len(geoms)):
    #
    #
    #         geom = geoms[i]
    #
    #         patch = PolygonPatch(geom.buffer(2),facecolor=colors[i])
    #         ax.add_patch(patch)
    #
    #
    #         ax.axis('auto')
    #     plt.draw()
    #
    #     # plt.ioff()
    #     plt.show()
    #
    # def test_draw_links(self):
    #
    #     links = geometry.build_links(self._inp)
    #
    #     self.draw_geoms(links)
    #
    # def draw_geoms(self, geoms):
    #
    #
    #     fig = plt.figure(1, figsize=(5,5), dpi=180)
    #     ax = fig.add_subplot(111)
    #
    #     cmap = plt.cm.Blues
    #     num_colors = len(geoms)
    #     colors = [cmap(1.*i/num_colors) for i in range(num_colors)]
    #
    #
    #     i = 0
    #     for id,geom in geoms:
    #
    #         patch = PolygonPatch(geom.buffer(2),facecolor=colors[i])
    #         ax.add_patch(patch)
    #
    #         i += 1
    #
    #         ax.axis('auto')
    #     plt.draw()
    #
    #     plt.show()
    #
    #
    # # def test_get_output(self):
    # #     o =abspath(join(dirname(__file__),'../data/simulation.out'))
    # #
    # #
    # #
    # #     # get variables
    # #     vars = listvariables(o)
    # #
    # #     for k, v in vars.iteritems():
    # #         print k,v
