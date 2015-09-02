__author__ = 'tonycastronova'



import unittest
from models.ueb import ueb


class testUEB(unittest.TestCase):


    def setup(self):
        pass

    def test_initialize(self):

        # intialize ueb
        UEB = ueb.ueb(None)

        print 'done'
