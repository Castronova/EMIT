__author__ = 'tonycastronova'

import os
import unittest

from utilities import gui


class testExchangeItem(unittest.TestCase):


    def test_load_model(self):

        config = os.path.realpath('./configuration.ini')
        params = gui.parse_config(config)
        m = gui.load_model(params)

        #todo: make sure that this class is an instance of TestModel

        print 'done'