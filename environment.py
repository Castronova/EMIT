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

            self.config = ConfigParser.ConfigParser(allow_no_value = True)

            # if the settings path does not exist, then create it
            if not os.path.exists(self.settings_path):
                self.write_default_settings()

            else:
                self.config.read(self.settings_path)
                settings_dict = self.parse_settings_file()
                for k, v in settings_dict.iteritems():
                    setattr(self, k.upper(), v)

            EnvironmentVars.__monostate = self.__dict__
        else:
            self.__dict__ = EnvironmentVars.__monostate

    def set_environment_variable(self, section, var, value=None):

        try:
            # make sure all sections are uppercase
            section = section.upper()

            # create a class variable if the value is not None. Comments will have None value
            if value is not None:
                if not value.isdigit():
                    setattr(self, '_'.join([section, var.upper()]), value)
                else:
                    setattr(self, '_'.join([section, var.upper()]), int(value))

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
        for section in self.config.sections():
            for option in self.config.options(section):
                value = self.config.get(section, option)
                if not value.isdigit():
                    d['_'.join([section, option])] = value
                else:
                    d['_'.join([section, option])] = int(value)

        return d

    def write_default_settings(self):
        with open(self.settings_path, 'w') as f:

            # print some info
            self.set_environment_variable('LOGGING','; Controls the verbosity of the console dialog, 1 is on, 0 is off')
            self.set_environment_variable('LOGGING','; True or False values should be represented by 1 or 0')
            self.set_environment_variable('LOGGING', 'showinfo', '1')
            self.set_environment_variable('LOGGING', 'showwarning', '1')
            self.set_environment_variable('LOGGING', 'showcritical', '1')
            self.set_environment_variable('LOGGING', 'showerror', '1')
            self.set_environment_variable('LOGGING', 'showdebug', '0')

            self.set_environment_variable('LOCAL_DB','; Settings associated with the local SQLite database')
            self.set_environment_variable('LOCAL_DB', 'path', os.path.abspath(os.path.join(os.path.dirname (self.settings_path),'../db/local.db')))

            self.set_environment_variable('USER','; Settings associated with user profile')
            self.set_environment_variable('USER', 'json', os.path.abspath(os.path.join(os.path.dirname (self.settings_path),'../configuration/users.json')))




env_vars = EnvironmentVars()
