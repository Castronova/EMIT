__author__ = 'tonycastronova'

import unittest
from utilities import mdl

class testUnit(unittest.TestCase):


    def test_set_unit(self):

        name = 'meters per second'
        unit = mdl.create_unit(name)
        self.assertTrue(unit.UnitName() == 'meters per second')
        self.assertTrue(unit.UnitTypeCV() == 'velocity')
        self.assertTrue(unit.UnitAbbreviation() == 'm/s')

        name = 'NotInCV'
        unit = mdl.create_unit(name)
        self.assertTrue(unit.UnitTypeCV() == 'unknown')
