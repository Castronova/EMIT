
import os
import copy
import unittest
import environment

class testEnvironment(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass



    def test_set_environment_vars(self):


        # get the current environment variables
        vars = os.environ

        self.assertTrue('LEGEND_LOCATIONBOTTOM' not in vars)
        self.assertTrue('LEGEND_LOCATIONRIGHT' not in vars)
        self.assertTrue('LOCAL_DB_PATH' not in vars)
        self.assertTrue('LOGGING_SHOWCRITICAL' not in vars)
        self.assertTrue('LOGGING_SHOWDEBUG' not in vars)
        self.assertTrue('LOGGING_SHOWERROR' not in vars)
        self.assertTrue('LOGGING_SHOWINFO' not in vars)
        self.assertTrue('LOGGING_SHOWWARNING' not in vars)
        self.assertTrue('APP_IMAGES_PATH' not in vars)
        self.assertTrue('APP_SETTINGS_PATH' not in vars)
        self.assertTrue('APP_TOOLBOX_PATH' not in vars)
        self.assertTrue('APP_USER_PATH' not in vars)
        self.assertTrue('GDAL_DATA' not in vars)

        environment.getEnvironmentVars()
        vars = os.environ

        self.assertTrue('LEGEND_LOCATIONBOTTOM' in vars)
        self.assertTrue('LEGEND_LOCATIONRIGHT' in vars)
        self.assertTrue('LOGGING_SHOWCRITICAL' in vars)
        self.assertTrue('LOGGING_SHOWDEBUG' in vars)
        self.assertTrue('LOGGING_SHOWERROR' in vars)
        self.assertTrue('LOGGING_SHOWINFO' in vars)
        self.assertTrue('LOGGING_SHOWWARNING' in vars)
        self.assertTrue('APP_IMAGES_PATH' in vars)
        self.assertTrue('APP_LOCAL_DB_PATH' in vars)
        self.assertTrue('APP_SETTINGS_PATH' in vars)
        self.assertTrue('APP_TOOLBOX_PATH' in vars)
        self.assertTrue('APP_USER_PATH' in vars)
        self.assertTrue('GDAL_DATA' in vars)


        # change some paths
        user1 = os.environ['APP_USER_PATH']
        environment.setEnvironmentVar('APP','USER_PATH', 'some_other_path')
        self.assertTrue(user1 != os.environ['APP_USER_PATH'])


        # add a new section
        environment.setEnvironmentVar('MyNewSection','test', '1')
        self.assertTrue('MYNEWSECTION_TEST' in os.environ.keys())

        environment.writeDefaultEnvironment()







