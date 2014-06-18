__author__ = 'tonycastronova'

import os, sys
this_file = os.path.realpath(__file__)
directory = os.path.dirname(os.path.dirname(os.path.dirname(this_file)))
sys.path.insert(0, directory)
print directory

import unittest
#from odm2.api.ODM2.Simulation.services import read
from db.api import postgresdb
#from odm2.api.ODMconnection import dbconnection,SessionFactory
#from odm2.api.ODM2.base import serviceBase
import odm2.api

class test_simulation_services(unittest.TestCase):


    def setUp(self):
        engine = 'postgresql'
        address = 'localhost'
        db = 'odm2CamelCase'
        user = 'tonycastronova'
        pwd = 'water'



        dbconn = odm2.api.dbconnection()
        self.connection_string = dbconn.createConnection(engine,address,db,user,pwd)
        #self.session_base = serviceBase(connection_string)
        #self.session = SessionFactory(connection_string,None).get_session()
        #self.session = self.session_base._session

        #self.conn = read.read(self.session)



        self.prefs = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/preferences'


    #def tearDown(self):
    #    self.session.close()

    def test_set_user_preferences(self):
        papi = postgresdb(self.connection_string)

        papi.set_user_preferences(self.prefs)

    def test_get_person(self):
        from odm2.api.ODM2.Core.services import *

        read = readCore(self.connection_string)

        person = read.getPersonByName('Tony','Castronova')

        print person


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
