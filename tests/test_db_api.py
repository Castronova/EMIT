__author__ = 'tonycastronova'

import unittest
#from db_api import postgresdb, mssql
import utilities
from odm2.api.ODM2 import *
import odm2.api.ODM2.Results.services.read as results
from coordinator import main

class test_db_api(unittest.TestCase):

    def setUp(self):

        # create connections
        self.connections = utilities.create_database_connections_from_file('/Users/tonycastronova/Documents/projects/iUtah/EMIT/data/connections')


    def tearDown(self):
        # disconnect from db's
        for connection in self.connection:
            connection['session'].close()


    def test_get_results(self):
        coordinator = main.Coordinator()


        # query odm2 database
        db_connection_name = 'ODM2 Simulation database'

        # get the connection string
        session = self.connections[db_connection_name]['session']

        from odm2.api.ODM2.Simulation.services import read as simulation
        query = simulation.read(session)
        all = query.getAllSimulations()

        # create instance of results class
        from odm2.api.ODM2.Results.services import read as results
        query = results.read(session)
        all = query.getAllTimeSeriesResults()


        #ts = result_query.getAllTimeSeriesResults()





        # query odm1 database
        db_connection_name = 'ODM2 MySQL Observation database'


        # get the connection string
        session = self.connections[db_connection_name]['session']

        # create instance of read class
        result_query = results.read(session)

        import odm2.api.ODM2.SamplingFeatures.model as sm
        #sf = result_query.query(sm.Samplingfeature).all()
        sf = session.query(sm.Samplingfeature).all()

        #ts = result_query.getAllTimeSeriesResults()


        print 'test'


    # def test_all_timeseries_mssql(self):
    #     self.db = mssql('ODM','odm','arroyo.uwrl.usu.edu','TestODM2')
    #
    #     self.db.get_all_ts_meta()
