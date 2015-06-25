__author__ = 'mike'

import unittest
import os
import pyspatialite.dbapi2 as sqlite3
import subprocess

class test_sqlite_db(unittest.TestCase):

    def connectToDB(self):
        dbpath = os.path.join(os.getcwd(), '../scripts')
        print dbpath



