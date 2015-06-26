__author__ = 'mike'

import unittest
import os, sys
import pyspatialite.dbapi2 as sqlite3
import subprocess
sys.path.append('./ODM2PythonAPI/src/api')

class test_sqlite_db(unittest.TestCase):

    def setUp(self):
        # self.dbpath = os.path.join(os.getcwd(), '../scripts/odm2.sqlite')
        self.dbpath = os.path.abspath('../scripts/odm2.sqlite')

    def test_connectToDB(self):
        print "starting test_connectToDB"
        print self.dbpath
        if os.path.exists(self.dbpath):
            print "yes2"
        conn = sqlite3.connect(self.dbpath)
        if conn:
            print "yes"
