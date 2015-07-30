__author__ = 'mike'
import os
# from coordinator.emitLogging import elog
from ast import literal_eval as Eval
import ConfigParser

# This is an interface for the settings file in the data directory
class EnvironmentVars(object):
    __monostate = None

    def __init__(self):
        if not EnvironmentVars.__monostate:
            currentdir = os.path.dirname(os.path.abspath(__file__))
            self.settings_path = os.path.abspath(os.path.join(currentdir, './app_data/config/.settings.ini'))
            self.config = ConfigParser.ConfigParser()
            self.config.read(self.settings_path)

            EnvironmentVars.__monostate = self.__dict__
            settings_dict = self.parse_settings_file()
            for k, v in settings_dict.iteritems():
                setattr(self, k, v)
        else:
            self.__dict__ = EnvironmentVars.__monostate

    def parse_settings_file(self):
        '''
        showinfo = True
        showwarning = False
        showcritical = True
        showerror = True
        '''

        d = {}
        for section in self.config.sections():
            for option in self.config.options(section):
                value = self.config.get(section, option)
                d[option] = value
        return d

    def set_environment_variable(self, var, value):
        try:
            setattr(self, var, value)
            if os.path.exists(self.settings_path):
                print "here"
            if var not in open(self.settings_path).read():
                with open(self.settings_path, "w+") as f:
                    pass
                    # f.write("\n" + var + " = " + value)
        except Exception:
            elog.warning("Invalid environment variable or value.")

    def get_settings_section(self):
        pass


# from environment import env_vars
# env_vars.set_environment_variable('settingspath', 'home/name...')
env_vars = EnvironmentVars()
