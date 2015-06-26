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

import api.ODMconnection

class test_sqlite_db(unittest.TestCase):

    def setUp(self):
        dbpath = os.path.abspath('../scripts/odm2.sqlite')

        connection_string = "sqlite:///"+dbpath
        self.connection = odm2dbConnection.SessionFactory(connection_string,echo=False)

    def test_connectToDB(self):
        print "starting test_connectToDB"
        print self.dbpath
        if os.path.exists(self.dbpath):
            print "yes2"
        conn = sqlite3.connect(self.dbpath)
        if conn:
            print "yes"
