__author__ = 'tonycastronova'

import unittest

from stdlib import *
from coordinator import main
from utilities import gui
import datatypes
from api.ODMconnection import  dbconnection
from wrappers import odm2_data
from coordinator import main
import time

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
        connection[db_id] = {'name':conn['name'],
                                 'session': self.session,
                                 'connection_string':self.session.engine.url,
                                 'description':conn['desc'],
                                 'args': conn}

        self.sim.add_db_connection(value=connection)

        # set the default database for the simulation
        self.sim.set_default_database(db_id)

    def test_swmm_rainfall_coupling(self):


        # add swmm component
        swmm_path = r'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/caleb_swmm/src/swmm_time-step.mdl'
        swmm = self.sim.add_model(type=datatypes.ModelTypes.TimeStep, attrib={'mdl':swmm_path})
        swmm_name = swmm.get_name()



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
                                  to_id=swmm.get_id(),
                                  to_item_name='Rainfall')

        from transform.space import *
        from transform.time import *
        link.spatial_interpolation(SpatialInterpolation.NearestObject)
        link.temporal_interpolation(TemporalInterpolation.NearestNeighbor)



        # some assertions to make sure models loaded correctly
        self.assertTrue(self.sim.get_model_by_id(swmm.get_id()) is not None )
        self.assertTrue(self.sim.get_model_by_id(timeseries.id()) is not None )
        self.assertTrue(self.sim.get_links_btwn_models(timeseries.id(),swmm.get_id())[0] is not None )


        print 'Starting Simulation'
        st = time.time()
        # begin execution
        self.sim.run_simulation()
        print 'Simulation Complete \n Elapsed time = %3.2f seconds'%(time.time() - st)

    def test_swmm_swmm_rainfall_coupling(self):


        # add swmm1 component
        swmm1_path = r'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_1/src/swmm_time-step.mdl'
        swmm1 = self.sim.add_model(type=datatypes.ModelTypes.TimeStep, attrib={'mdl':swmm1_path})
        swmm1_name = swmm1.get_name()

        # add swmm1 component
        swmm2_path = r'/Users/tonycastronova/Documents/projects/iUtah/EMIT/models/swmm_timestep_2/src/swmm_time-step.mdl'
        swmm2 = self.sim.add_model(type=datatypes.ModelTypes.TimeStep, attrib={'mdl':swmm2_path})
        swmm2_name = swmm2.get_name()

        # create odm2 instance
        series_id = 21  # incremental rainfall
        timeseries = odm2_data.odm2(resultid=series_id, session=self.session)

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
                                  to_id=swmm1.get_id(),
                                  to_item_name='Rainfall')

        # add link between rainfall and swmm 2
        link2 = self.sim.add_link_by_name(from_id=timeseries.id(),
                                  from_item_name='rainfall',
                                  to_id=swmm2.get_id(),
                                  to_item_name='Rainfall')

        # add link between swmm 1 and swmm 2 (streamflow)
        link3 = self.sim.add_link_by_name(from_id=swmm1.get_id(),
                                  from_item_name='Flow_rate',
                                  to_id=swmm2.get_id(),
                                  to_item_name='Flow_rate')

        # add link between swmm 2 and swmm 1 (stage)
        link4 = self.sim.add_link_by_name(from_id=swmm2.get_id(),
                                  from_item_name='Hydraulic_head',
                                  to_id=swmm1.get_id(),
                                  to_item_name='Hydraulic_head')


        # set link tranformations
        from transform.space import *
        from transform.time import *
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