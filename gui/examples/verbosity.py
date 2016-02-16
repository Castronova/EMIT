__author__ = 'tonycastronova'

import unittest
import environment
from environment import env_vars


class test_verbosity(unittest.TestCase):

    def setUp(self):
        self.env1 = environment.EnvironmentVars()
        self.env2 = environment.EnvironmentVars()

    def tearDown(self):
        self.env1 = environment.EnvironmentVars()
        self.env1.save_default_environment()

        del self.env1
        del self.env2

    def test_get_default(self):

        # check that the default values are set correctly
        self.assertTrue(self.env1.LOGGING_SHOWDEBUG == 0)
        self.assertTrue(self.env1.LOGGING_SHOWWARNING == 1)
        self.assertTrue(self.env1.LOGGING_SHOWERROR == 1)
        self.assertTrue(self.env1.LOGGING_SHOWINFO == 1)
        self.assertTrue(self.env1.LOGGING_SHOWCRITICAL == 1)

    def test_modify(self):

        # change the logging values in env1
        self.env1.set_environment_variable('LOGGING', 'SHOWDEBUG', 0)
        self.env1.set_environment_variable('LOGGING', 'SHOWWARNING', 0)
        self.env1.set_environment_variable('LOGGING', 'SHOWERROR', 0)
        self.env1.set_environment_variable('LOGGING', 'SHOWINFO', 0)
        self.env1.set_environment_variable('LOGGING', 'SHOWCRITICAL', 0)

        # assert that these changes are present in env2
        self.assertTrue(self.env2.LOGGING_SHOWDEBUG == 0)
        self.assertTrue(self.env2.LOGGING_SHOWWARNING == 0)
        self.assertTrue(self.env2.LOGGING_SHOWERROR == 0)
        self.assertTrue(self.env2.LOGGING_SHOWINFO == 0)
        self.assertTrue(self.env2.LOGGING_SHOWCRITICAL == 0)

    def test_get_saved(self):

        # change the logging values
        self.env1.set_environment_variable('LOGGING', 'SHOWDEBUG', 0)
        self.env1.set_environment_variable('LOGGING', 'SHOWWARNING', 0)
        self.env1.set_environment_variable('LOGGING', 'SHOWERROR', 0)
        self.env1.set_environment_variable('LOGGING', 'SHOWINFO', 0)
        self.env1.set_environment_variable('LOGGING', 'SHOWCRITICAL', 0)

        # write these changes to file
        self.env1.save_environment()

        # load the changes and check that they are correct
        self.env2.load_environment()
        self.assertTrue(self.env2.LOGGING_SHOWDEBUG == 0)
        self.assertTrue(self.env2.LOGGING_SHOWWARNING == 0)
        self.assertTrue(self.env2.LOGGING_SHOWERROR == 0)
        self.assertTrue(self.env2.LOGGING_SHOWINFO == 0)
        self.assertTrue(self.env2.LOGGING_SHOWCRITICAL == 0)

