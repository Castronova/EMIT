__author__ = 'mike'
import os
# from coordinator.emitLogging import elog
import ConfigParser

# This is an interface for the settings file in the data directory
class EnvironmentVars(object):
    '''
    Implemented as singleton with 'from environment import env_vars'
    Variables can be accessed like 'env_vars.SHOWERROR'. All settings
    are parsed from app_data/config/.settings.ini using ConfigParser.

    IMPORTANT: All instance variables are in UPPERCASE, but are stored
    as lowercase in the settings.ini (ConfigParser does this).
    '''
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
                setattr(self, k.upper(), v)
        else:
            self.__dict__ = EnvironmentVars.__monostate

    def set_environment_variable(self, section, var, value):
        try:
            setattr(self, var.upper(), value)
            if not self.config.has_section(section.upper()):
                self.config.add_section(section.upper())
            self.config.set(section.upper(), var, value)
            settings_file = open(self.settings_path, 'w+')
            self.config.write(settings_file)
            settings_file.close()

        except Exception:
            print "Error setting environment variable"
            # elog doesn't work here for some reason
            # elog.warning("Invalid environment variable or value.")

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

env_vars = EnvironmentVars()
