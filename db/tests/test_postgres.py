__author__ = 'tonycastronova'

import os
import unittest
from db.dbapi import postgresdb
import odm2.api
import datetime as dt
from utilities import gui, mdl

from odm2.api.ODM2.Core.services import *

class test_simulation_services(unittest.TestCase):


    def setUp(self):
        engine = 'postgresql'
        address = 'localhost'
        db = 'odm2CamelCase'
        user = 'tonycastronova'
        pwd = 'water'
        dbconn = odm2.api.dbconnection()
        self.connection_string = dbconn.createConnection(engine,address,db,user,pwd)
        self.prefs = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/preferences'


    #def tearDown(self):
    #    self.session.close()

    def test_set_user_preferences(self):
        papi = postgresdb(self.connection_string)

        papi.set_user_preferences(self.prefs)

    def test_get_person(self):


        read = readCore(self.connection_string)

        person = read.getPersonByName('Tony','Castronova')

        print person

    def test_insert_ts_results(self):
        papi = postgresdb(self.connection_string)

        papi.insert_result_ts()

        pass

    def test_create_simulation(self):
        papi = postgresdb(self.connection_string)

        model_code = 'swat'
        sim_name = 'TonySwatSimulation'
        sim_description = 'My SWAT Simulation'
        #sim_start = dt.datetime(2014,01,01,0,0,0)
        #sim_end = dt.datetime(2014,02,01,0,0,0)
        timestepvalue = 1
        timestepunitid = None # query this
        inputdatasetid = None # query this
        #startoffset=-6
        #endoffset=-6

        # build exchange items from file
        config = os.path.realpath('../../tests/configuration.ini')
        params = gui.parse_config(config)
        eitems = mdl.build_exchange_items_from_config(params)

        # add some data to simulate 'output' exchange items
        vals= [(dt.datetime(2014,1,1,0,0,0) + dt.timedelta(days=i), i) for i in range(0,100)]
        output_item1 = eitems[1]
        output_item1.geometries()[0].datavalues().set_timeseries(vals)
        vals= [(dt.datetime(2014,1,1,0,0,0) + dt.timedelta(days=i), 2*i) for i in range(0,100)]
        output_item1.geometries()[1].datavalues().set_timeseries(vals)

        vals= [(dt.datetime(2014,1,1,0,0,0) + dt.timedelta(days=i), 2**i) for i in range(0,100)]
        output_item2 = eitems[2]
        output_item2.geometries()[0].datavalues().set_timeseries(vals)

        outputs = [output_item1,output_item2]

        sim = papi.create_simulation(preferences_path='/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/preferences',
                               config_params=params,
                               output_exchange_items= outputs)


        print 'Successfully inserted Simulation: %d'%sim.SimulationID




    def test_create_dataset(self):

        papi = postgresdb(self.connection_string)

        #resultids = []

    def test_get_simulation(self):

        simulations = self.conn.getAllSimulations()

    def test_get_simulation_id(self):
        pass

    def test_get_simulations_by_modelcode(self):
        simulations = self.conn.getSimulationsByModelCode('swat')

        print 'done'

    # def test_get_simulation_by_args(self):
    #
    #     d = {'ModelCode': 'swat'}
    #     simulations = self.conn.getSimulationByArgs(d)
    #
    #     d['SpatialReferenceID'] = 1
    #     simulations = self.conn.getSimulationByArgs(d)
    #
    #     print simulations


    def test_get_model_by_simulation_id(self):
        pass

    def test_get_simulation_creator(self):
        simulations = self.conn.getSimulationsByCreator('tony','castronova')




    def test_get_simulation_inputs(self):
        pass

    def test_get_simulation_outputs(self):
        pass
