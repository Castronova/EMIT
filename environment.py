__author__ = 'mike'
import os
import ConfigParser

# This is an interface for the settings file in the data directory
class EnvironmentVars(object):
    '''
    Implemented as singleton with 'from environment import env_vars'
    Variables can be accessed like 'env_vars.SHOWERROR'. All settings
    are parsed from app_data/config/.settings.ini using ConfigParser.

    '''
    __monostate = None
    def __init__(self):
        if not EnvironmentVars.__monostate:
            currentdir = os.path.dirname(os.path.abspath(__file__))
            self.settings_path = os.path.abspath(os.path.join(currentdir, './app_data/config/.settings.ini'))

            self.config = ConfigParser.ConfigParser()

            # if the settings path does not exist, then create it
            if not os.path.exists(self.settings_path):
                self.write_default_settings()


            self.config.read(self.settings_path)

            EnvironmentVars.__monostate = self.__dict__
            settings_dict = self.parse_settings_file()
            for k, v in settings_dict.iteritems():
                setattr(self, k.upper(), v)
        else:
            self.__dict__ = EnvironmentVars.__monostate

    def set_environment_variable(self, section, var, value):

        try:
            # make sure all sections are uppercase
            section = section.upper()

            setattr(self, var.upper(), value)

            # make sure that this section exists before adding var, value
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, var, value)


            settings_file = open(self.settings_path, 'w+')
            self.config.write(settings_file)
            settings_file.close()

        except Exception:
            # elog.warning("Invalid environment variable or value.")
            pass


    def parse_settings_file(self):
        '''
        The settings file is divided into sections, such as logging
        and local_db. In each section there are options, which contain
        the variables and values. Parsing with ConfigParser, all values
        are considered STRINGS and need to be converted if necessary to
        booleans or ints.
        '''
        d = {}
        logging = self.config.options("LOGGING")
        for option in logging:
            value = self.config.getboolean("LOGGING", option)
            d[option] = value

        localdb = self.config.options("LOCAL_DB")
        for option in localdb:
            value = self.config.get("LOCAL_DB", option)
            d[option] = value

        return d

    def write_default_settings(self):
        with open(self.settings_path, 'w') as f:
            self.set_environment_variable('logging', 'showinfo', 'True')
            self.set_environment_variable('logging', 'showwarning', 'True')
            self.set_environment_variable('logging', 'showcritical', 'True')
            self.set_environment_variable('logging', 'showerror', 'True')
            self.set_environment_variable('logging', 'showdebug', 'False')
            self.set_environment_variable('local_db', 'path', os.path.abspath(os.path.join(os.path.dirname (self.settings_path),'../db/local.db')))



env_vars = EnvironmentVars()
