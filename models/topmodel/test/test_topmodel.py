__author__ = 'tonycastronova'

import unittest
import time
from models.topmodel import topmodel
from utilities.gui import parse_config_without_validation

class test_topmodel(unittest.TestCase):

    def setUp(self):
        # add models
        self.mdl = './topmodel.mdl'

    def test_initialize(self):

        config_params = parse_config_without_validation(self.mdl)
        # load topmodel
        top = topmodel.topmodel(config_params)

        print 'done'