__author__ = 'tonycastronova'



import unittest
from models.ueb import ueb


class testUEB(unittest.TestCase):


    def setup(self):
        pass

    def test_run(self):

        # intialize ueb
        UEB = ueb.ueb(None)

        # run
        UEB.run(None)

        # finish
        UEB.save()

        print 'done'
