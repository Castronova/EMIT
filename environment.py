__author__ = 'mike'
import os
from coordinator.emitLogging import elog
import ast

# This is an interface for the settings file in the data directory
class EnvironmentVars(object):
    __monostate = None

    def __init__(self):
        if not EnvironmentVars.__monostate:
            EnvironmentVars.__monostate = self.__dict__
            settings_dict = self.parse_settings_file()
            for k, v in settings_dict.iteritems():
                setattr(self, k, v)
        else:
            self.__dict__ = EnvironmentVars.__monostate

    def parse_settings_file(self):
        currentdir = os.path.dirname(os.path.abspath(__file__))
        self.settingspath = os.path.abspath(os.path.join(currentdir, './data/settings'))
        d = {}
        with open(self.settingspath, 'r') as f:
            lines = f.readlines()
            for line in lines:
                if '=' in line:
                    data = line.split('=')
                    try:
                        val = ast.literal_eval(data[1].strip())
                        d[data[0].strip()] = val

                    except Exception:
                        elog.warning("Invalid environment parameter found in settings.")
                else:
                    elog.warning("Invalid environment parameter found in settings.")
        return d

    def set_environment_variable(self, var, value):
        try:
            setattr(self, var, value)
        except Exception:
            elog.warning("Invalid environment variable or value.")

# from environment import env_vars
# env_vars.set_environment_variable('settingspath', 'home/name...')
env_vars = EnvironmentVars()
