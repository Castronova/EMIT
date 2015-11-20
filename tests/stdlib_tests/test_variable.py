__author__ = 'tonycastronova'

import unittest
from utilities import mdl

class testVariable(unittest.TestCase):


    def test_set_variable(self):

        name = 'streamflow'
        variable = mdl.create_variable(name)
        self.assertTrue(variable.VariableNameCV() == 'streamflow')
        self.assertTrue(variable.VariableDefinition() == 'The volume of water flowing past a fixed point.  Equivalent to discharge')

        name = 'NotInCV'
        variable = mdl.create_variable(name)
        self.assertTrue(variable.VariableDefinition() == 'unknown')
