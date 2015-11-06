__author__ = 'tonycastronova'



import unittest
from models.ueb import ueb
from utilities.gui import parse_config

class testUEB(unittest.TestCase):


    def setup(self):
        pass

    def test_run(self):

        # intialize ueb
        mdl = '../ueb.mdl'
        config_params = parse_config(mdl)
        UEB = ueb.ueb(config_params)

        # run
        UEB.run(None)

        # finish
        UEB.save()

        print 'done'
