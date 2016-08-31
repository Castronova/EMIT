

import os, sys
import time
import sprint
import unittest
import environment
from coordinator.engine import Coordinator
import stdlib
from utilities import models as model_utils
from transform import space, time


class testFeedForwardSimulation(unittest.TestCase):


    def setUp(self):
        # initialize environment variables
        environment.getEnvironmentVars()

        if sys.gettrace():
            print 'Detected Debug Mode'
            # initialize debug listener (reroute messages to console)
            self.d = sprint.DebugListener()

        self.engine = Coordinator()
        sprint.PrintTarget.CONSOLE = 1134


        self.basepath = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def test_feedforward_simulation(self):

        sprint.sPrint('test', sprint.MessageType.DEBUG)

        randomizer_path = os.path.join(self.basepath, '../../app_data/models/randomizer/randomizer.mdl')
        multiplier_mdl = os.path.join(self.basepath, '../../app_data/models/multiplier/multiplier.mdl')


        m1 = self.engine.add_model(id=1234,  attrib={'mdl':randomizer_path})
        self.assertTrue(m1)

        m2 = self.engine.add_model(id=1235,  attrib={'mdl':multiplier_mdl})
        self.assertTrue(m2)

        # assert that the models have been added correctly
        models = self.engine.get_all_models()
        self.assertTrue(len(models) == 2)


        # add a link from randomizer to multiplier
        rand_oei =  self.engine.get_exchange_item_info(modelid=1234, eitype=stdlib.ExchangeItemType.OUTPUT)
        mult_iei = self.engine.get_exchange_item_info(modelid=1235, eitype=stdlib.ExchangeItemType.INPUT)
        self.engine.add_link(from_id=1234, from_item_id=rand_oei[0]['name'],
                             to_id=1235, to_item_id=mult_iei[0]['name'],
                             spatial_interp=None,
                             temporal_interp=None,
                             uid=None)

        # assert that the link has been established correctly
        links = self.engine.get_all_links()
        self.assertTrue(len(links) == 1)



        # run the simulation, without saving results
        self.engine.run_simulation()

        status = stdlib.Status.UNDEFINED
        while status != stdlib.Status.FINISHED and status != stdlib.Status.ERROR:
            status = self.engine.get_status()
            time.sleep(1)

        # check that output data was generated
        m = self.engine.get_model_by_id(id = 1235)

        values = m.instance().outputs()['multipliedValue'].getValues2()
        self.assertTrue(len(values) > 0)
        self.assertTrue(values[0] != 0)

    def test_feedforward_unit_conversions(self):

        sprint.sPrint('test', sprint.MessageType.DEBUG)


        ###################################
        # Add the TOPMODEL component
        ###################################

        topmodel_path = os.path.join(self.basepath, '../../app_data/models/topmodel/topmodel.mdl')
        datadir = os.path.join(self.basepath, '../../app_data/models/topmodel/right_hand_fork')

        params = model_utils.parse_json(topmodel_path)
        params.update(dict(
            model_type='MDL',
           path=topmodel_path,
           # m=180.0,
           m=1.0,
           interception=0.0,
           r=9.66,
           tmax=250000,
           fac=os.path.join(datadir, 'fac_trim.txt'),
           ti=os.path.join(datadir, 'right_hand_fork_ti_trim.txt'))
                           )

        m1 = self.engine.add_model(**params)
        self.assertTrue(m1)

        ###################################
        # Add the Weather Reader component
        ###################################

        weather_path = os.path.join(self.basepath, '../../app_data/models/weather/weatherReader.mdl')
        datadir = os.path.join(self.basepath, '../../app_data/models/weather/data')

        params = model_utils.parse_json(weather_path)
        params.update(dict(
            model_type='MDL',
            path=weather_path,
            weather_csv=os.path.join(datadir, 'lrgc.csv')
        ))
        m2 = self.engine.add_model(**params)
        self.assertTrue(m2)



        # assert that the models have been added correctly
        models = self.engine.get_all_models()
        self.assertTrue(len(models) == 2)


        # add a link
        weather_oei = self.engine.get_exchange_items(modelid=m2.id(), exchange_item_type=stdlib.ExchangeItemType.OUTPUT)
        topmodel_iei = self.engine.get_exchange_items(modelid=m1.id(), exchange_item_type=stdlib.ExchangeItemType.INPUT)
        space_interp = space.SpatialInterpolation.NearestObject
        time_interp = time.TemporalInterpolation.NearestNeighbor

        self.engine.add_link(from_id=m2.id(), from_item_id=weather_oei[0].name(),
                             to_id=m1.id(), to_item_id=topmodel_iei[0].name(),
                             spatial_interp=space_interp,
                             temporal_interp=time_interp,
                             uid=None)

        # assert that the link has been established correctly
        links = self.engine.get_all_links()
        self.assertTrue(len(links) == 1)

        # run the simulation, without saving results
        self.engine.run_simulation()

        status = stdlib.Status.UNDEFINED
        while status != stdlib.Status.FINISHED and status != stdlib.Status.ERROR:
            status = self.engine.get_status()
            time.sleep(1)

        # check that output data was generated
        m = self.engine.get_model_by_id(id=m1.id())

        values = m.instance().outputs()['multipliedValue'].getValues2()
        self.assertTrue(len(values) > 0)
        self.assertTrue(values[0] != 0)

