__author__ = 'mike'

import unittest
import os, sys
import pyspatialite.dbapi2 as sqlite3
import subprocess

# This change needs to be made in ODM2PythonAPI/src/api/ODMconnection.py
'''
class SessionFactory():
    def __init__(self, connection_string, echo):
        if 'sqlite' in connection_string:
            self.engine = create_engine(connection_string, encoding='utf-8', echo=echo)
        else:
            self.engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600, pool_timeout=5, pool_size=20,
                                        max_overflow=0)
            self.psql_test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600, pool_timeout=5,
                                        max_overflow=0,  connect_args={'connect_timeout': 1})
            self.ms_test_engine = create_engine(connection_string, encoding='utf-8', echo=echo, pool_recycle=3600, pool_timeout=5,
                                        max_overflow=0,  connect_args={'timeout': 1})


        # Create session maker
        self.Session = sessionmaker(bind=self.engine)
        # self.psql_test_Session = sessionmaker(bind=self.psql_test_engine)
        # self.ms_test_Session = sessionmaker(bind=self.ms_test_engine)

    def getSession(self):
        return self.Session()

    def __repr__(self):
        return "<SessionFactory('%s')>" % (self.engine)

'''

odm2_api_path = os.path.abspath(os.path.join(__file__, '../../../ODM2PythonAPI'))
sys.path.append(odm2_api_path)
import src.api.ODMconnection as odm2dbConnection
import src.api.ODM2.services.readService as odmread
import api.ODMconnection

class test_sqlite_db(unittest.TestCase):

    def setUp(self):

        # define the paths for the empty and populated temp databases
        self.empty_db_path = os.path.abspath('../scripts/temp_empty.db')
        self.pop_db_path = os.path.abspath('../scripts/temp_pop.db')

        # get the database dump files
        empty_dump_script = open('../scripts/empty_dump.sql','r').read()
        populated_dump_script = open('../scripts/populated_dump.sql','r').read()

        # create temp databases
        empty_odm2_db = sqlite3.connect(self.empty_db_path) # create a memory database
        pop_odm2_db = sqlite3.connect(self.pop_db_path) # create a memory database

        # load the dump files into the in-memory databases
        empty_odm2_db.executescript(empty_dump_script)
        pop_odm2_db.executescript(populated_dump_script)

        # create database connections that will be used in test cases
        self.empty_connection = odm2dbConnection.SessionFactory('sqlite:///'+self.empty_db_path, echo=False)
        self.pop_connection = odm2dbConnection.SessionFactory('sqlite:///'+self.pop_db_path, echo=False)


    def tearDown(self):

        # remove temp databases
        if os.path.exists(self.empty_db_path):
            os.remove(self.empty_db_path)
        if os.path.exists(self.pop_db_path):
            os.remove(self.pop_db_path)



    def test_get_people(self):
        people = odmread.People()
        people = r.People()
        print people.PersonFirstName

    def test_get_simulations(self):

        print '1'

        s = odmread.readSimulation(self.pop_connection)

        print '2'


    def test_connectToDB(self):
        print "starting test_connectToDB"
        print self.dbpath
        if os.path.exists(self.dbpath):
            print "yes2"
        conn = sqlite3.connect(self.dbpath)
        if conn:
            print "yes"
