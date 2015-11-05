__author__ = 'tonycastronova'

import unittest

from stdlib import *
from coordinator import main
from utilities import gui
import datatypes
from api_old.ODMconnection import  dbconnection
from wrappers import odm2_data
from coordinator import main
import time
from ctypes import *
from transform.space import *
from transform.time import *
from models.caleb_swmm.src.structures import *
import threading
import multiprocessing
from multiprocessing import Process, Pipe, Queue

class test_run_swmm(unittest.TestCase):

    def setUp(self):

        # create instance of coordinator
        self.sim = main.Coordinator()

        # connect to database
        conn = {
                'name' : 'ODM2 Simulation database - Live',
                'desc' :'PostgreSQL database with hydrology simulations',
                'engine' :'postgresql',
                'address' :'castro-server.bluezone.usu.edu',
                'db' :'ODM2-Live',
                'user' :'postgres',
                'pwd' :'water',
                }

        self.session = dbconnection.createConnection(conn['engine'],
                                                     conn['address'],
                                                     conn['db'],
                                                     conn['user'],
                                                     conn['pwd'])
        connection  = {}
        db_id = uuid.uuid4().hex[:5]

        try:
            connection[db_id] = {'name':conn['name'],
                                     'session': self.session,
                                     'connection_string':self.session.engine.url,
                                     'description':conn['desc'],
                                     'args': conn}

            self.sim.add_db_connection(value=connection)

            # set the default database for the simulation
            self.sim.set_default_database(db_id)
        except:
            pass

        self.q = Queue()


    def swmm_open_process(self,lib,i1,r1,o1):
        self.q.put(lib.swmm_open(i1,r1,o1))

    def test_dll_loading(self):


        dll1 = b'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_1/src/swmm.dylib'
        i1 =   b'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_1/data/Logan.inp'
        r1 =   b'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_1/data/Logan.rpt'
        o1 =   b'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_1/data/Logan.out'


        dll2 = b'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_2/src/swmm.dylib'
        i2 =   b'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_2/data/Logan.inp'
        r2 =   b'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_2/data/Logan.rpt'
        o2 =   b'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_2/data/Logan.out'


        lib1 = cdll.LoadLibrary(dll1)
        lib1.swmm_open.restype = POINTER(c_void_p)
        lib1.getSubcatch.restype = POINTER(TSubcatch)
        lib1.setSubcatch.argtypes = [POINTER(c_void_p), POINTER(TSubcatch), c_char_p]

        lib2 = cdll.LoadLibrary(dll2)
        lib2.swmm_open.restype = POINTER(c_void_p)
        lib2.getSubcatch.restype = POINTER(TSubcatch)
        lib2.setSubcatch.argtypes = [POINTER(c_void_p), POINTER(TSubcatch), c_char_p]


        ptr1 = lib1.swmm_open(i1,r1,o1)

        err = lib1.swmm_getErrorCode(ptr1)
        self.assertTrue(err == 0)

        count1 = lib1.getObjectTypeCount(ptr1, SWMM_Types.SUBCATCH)
        self.assertTrue(count1 > 0)

        err = lib1.swmm_start(ptr1, 1)
        self.assertTrue(err == 0)

        ptr2 = lib2.swmm_open(i2,r2,o2)

        err = lib2.swmm_getErrorCode(ptr2)
        self.assertTrue(err == 0)

        count2 = lib2.getObjectTypeCount(ptr2, SWMM_Types.SUBCATCH)
        self.assertTrue(count2 > 0)

        err = lib2.swmm_start(ptr2, 1)
        self.assertTrue(err == 0)

        # set some rainfall
        for i in range(0,count1):
            sub = lib1.getSubcatch(ptr1, c_int(i))
            sub.contents.rainfall = c_double(2.0)
            lib1.setSubcatch(ptr1, sub, c_char_p('rainfall'))


        step1 = c_double()
        err = lib1.swmm_step(ptr1, byref(step1))
        self.assertTrue(err == 0)


        flow1 = lib1.getSubcatch(ptr1, c_int(0)).contents.newRunoff
        flow2 = lib2.getSubcatch(ptr2, c_int(0)).contents.newRunoff

        self.assertTrue(flow1 != flow2)

        err = lib1.swmm_end(ptr1)
        self.assertTrue(err == 0)

        err = lib2.swmm_end(ptr2)
        self.assertTrue(err == 0)

    def test_new_dll_loading(self):


        dll1 = r'/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/libTestLib.dylib'
        lib = cdll.LoadLibrary(dll1)


        lib.createAgeObject.restype = c_void_p
        lib.getAgeFromObject.restype = c_double
        lib.getAgeFromObject.argtypes = [c_void_p]
        lib.setAgeForObject.argtypes = [c_void_p,c_double]
        lib.deleteAgeObject.argtypes = [c_void_p]
        lib.getAge.restype = c_double
        lib.setAge.argtypes = [c_double]


        obj1 = lib.createAgeObject()
        obj2 = lib.createAgeObject()

        lib.setAgeForObject(obj1, c_double(10.1))

        print lib.getAgeFromObject(obj1)
        print lib.getAgeFromObject(obj2)

        lib.deleteAgeObject(obj1)
        lib.deleteAgeObject(obj2)


        dll2 = r'/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/libTestLib2.dylib'
        lib2 = cdll.LoadLibrary(dll2)
        lib2.getAge.restype = c_double
        lib2.setAge.argtypes = [c_double]


        lib.setAge(c_double(3))
        print lib.getAge()
        print lib2.getAge()

    def test_swmm_rainfall_coupling(self):


        # add swmm component
        swmm_path = r'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/caleb_swmm/src/swmm_time-step.mdl'
        swmm = self.sim.add_model(type=datatypes.ModelTypes.TimeStep, attrib={'mdl':swmm_path})
        swmm_name = swmm.name()



        # create odm2 instance
        series_id = 21  # incremental rainfall
        timeseries = odm2_data.odm2(resultid=series_id, session=self.session)

        # create a model instance
        oei = timeseries.outputs().values()
        thisModel = main.Model(id=timeseries.id(),
                               name=timeseries.name(),
                               instance=timeseries,
                               desc=timeseries.description(),
                               input_exchange_items= [],
                               output_exchange_items=  oei,
                               params=None)

        thisModel.type(datatypes.ModelTypes.Data)

        # save the model
        self.sim.Models(thisModel)


        # add link between rainfall and timeseries
        link = self.sim.add_link_by_name(from_id=timeseries.id(),
                                         from_item_name='rainfall',
                                         to_id=swmm.id(),
                                         to_item_name='Rainfall')

        link.spatial_interpolation(SpatialInterpolation.NearestObject)
        link.temporal_interpolation(TemporalInterpolation.NearestNeighbor)



        # some assertions to make sure models loaded correctly
        self.assertTrue(self.sim.get_model_by_id(swmm.id()) is not None)
        self.assertTrue(self.sim.get_model_by_id(timeseries.id()) is not None )
        self.assertTrue(self.sim.get_links_btwn_models(timeseries.id(), swmm.id())[0] is not None)


        print 'Starting Simulation'
        st = time.time()
        # begin execution
        self.sim.run_simulation()
        print 'Simulation Complete \n Elapsed time = %3.2f seconds'%(time.time() - st)

    def test_swmm_swmm_rainfall_coupling(self):


        # add swmm1 component
        swmm1_path = r'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_1/src/model1.mdl'
        swmm1 = self.sim.add_model(type=datatypes.ModelTypes.TimeStep, attrib={'mdl':swmm1_path})
        swmm1_name = swmm1.name()


        # add swmm1 component
        # swmm2_path = r'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_2/src/swmm_time-step.mdl'
        swmm2_path = r'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_1/src/model2.mdl'
        swmm2 = self.sim.add_model(type=datatypes.ModelTypes.TimeStep, attrib={'mdl':swmm2_path})
        swmm2_name = swmm2.name()

        # create odm2 instance
        series_id = 21  # incremental rainfall
        timeseries = odm2_data.odm2(resultid=series_id, session=self.session)

        # hard code some values for testing
        ts = zip([datetime.datetime(2002, 1, 1, 0, 0), datetime.datetime(2002, 1, 1, 0, 30), datetime.datetime(2002, 1, 1, 1, 0)], [.5,.5,.5])
        k = timeseries.outputs()['rainfall'].get_geoms_and_timeseries().keys()[0]
        timeseries.outputs()['rainfall'].set_timeseries_by_id(k.id(), ts)

        # create a timeseries model instance for the rainfall
        oei = timeseries.outputs().values()
        thisModel = main.Model(id=timeseries.id(),
                               name=timeseries.name(),
                               instance=timeseries,
                               desc=timeseries.description(),
                               input_exchange_items= [],
                               output_exchange_items=  oei,
                               params=None)

        thisModel.type(datatypes.ModelTypes.Data)

        # save the model
        self.sim.Models(thisModel)


        # add link between rainfall and swmm 1
        link1 = self.sim.add_link_by_name(from_id=timeseries.id(),
                                          from_item_name='rainfall',
                                          to_id=swmm1.id(),
                                          to_item_name='Rainfall')

        # add link between rainfall and swmm 2
        link2 = self.sim.add_link_by_name(from_id=timeseries.id(),
                                          from_item_name='rainfall',
                                          to_id=swmm2.id(),
                                          to_item_name='Rainfall')

        # add link between swmm 1 and swmm 2 (streamflow)
        link3 = self.sim.add_link_by_name(from_id=swmm1.id(),
                                          from_item_name='Flow_rate',
                                          to_id=swmm2.id(),
                                          to_item_name='Flow_rate')

        # add link between swmm 2 and swmm 1 (stage)
        link4 = self.sim.add_link_by_name(from_id=swmm2.id(),
                                          from_item_name='Hydraulic_head',
                                          to_id=swmm1.id(),
                                          to_item_name='Hydraulic_head')


        # set link tranformations

        link1.spatial_interpolation(SpatialInterpolation.NearestObject)
        link1.temporal_interpolation(TemporalInterpolation.NearestNeighbor)

        link2.spatial_interpolation(SpatialInterpolation.NearestObject)
        link2.temporal_interpolation(TemporalInterpolation.NearestNeighbor)

        link3.spatial_interpolation(SpatialInterpolation.ExactMatch)
        link3.temporal_interpolation(TemporalInterpolation.NearestNeighbor)

        link4.spatial_interpolation(SpatialInterpolation.ExactMatch)
        link4.temporal_interpolation(TemporalInterpolation.NearestNeighbor)



        # some assertions to make sure models loaded correctly
        #self.assertTrue(self.sim.get_model_by_id(swmm.get_id()) is not None )
        #self.assertTrue(self.sim.get_model_by_id(timeseries.id()) is not None )
        #self.assertTrue(self.sim.get_links_btwn_models(timeseries.id(),swmm.get_id())[0] is not None )


        print 'Starting Simulation'
        st = time.time()
        # begin execution
        self.sim.run_simulation()
        print 'Simulation Complete \n Elapsed time = %3.2f seconds'%(time.time() - st)


