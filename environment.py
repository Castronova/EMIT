__author__ = 'mike'
import os, sys
import ConfigParser
from api_old.ODMconnection import  dbconnection
from sprint import *

# This is an interface for
class ConnectionVars(object):
    '''
    implemented as a singleton with 'from environment import con_vars'
    everything is parsed from
    '''
    def __init__(self):
        currentdir = os.path.dirname(os.path.abspath(__file__))
        self.connections_path = os.path.abspath(os.path.join(currentdir, './data/connections'))
        self.Config = ConfigParser.ConfigParser(allow_no_value=True)

    def load_connections(self, ConnPath = None):
        ConnPath = self.connections_path if ConnPath is None else ConnPath

        self.config = ConfigParser.ConfigParser(allow_no_value=True)

    def Write_New_Connection(self, ValueDic):
        currentdir = os.path.dirname(os.path.abspath(__file__))
        self.connections_path = os.path.abspath(os.path.join(currentdir, './data/connections'))
        f = open(self.connections_path, 'a')
        db = dbconnection()
        if db.createConnection(ValueDic[2],ValueDic[3], ValueDic[4], ValueDic[5], ValueDic[6]):
            f.write("\n")
            f.write("[connection]\n")
            f.write("name = " + ValueDic[0] +"\n")
            f.write("desc = " + ValueDic[1] +"\n")
            f.write("engine = " + ValueDic[2] +"\n")
            f.write("address = " + ValueDic[3] +"\n")
            f.write("db = " + ValueDic[4] +"\n")
            f.write("user = " + ValueDic[5] +"\n")
            f.write("pwd = " + ValueDic[6] +"\n")
            f.close()
            return True
        return False


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
            
            # create this directory if it doesn't exist yet
            if not os.path.exists(self.settings_path):
                sPrint('Settings file could not be found, loading default settings', MessageType.INFO, PrintTarget.CONSOLE)    
                os.mkdir(os.path.dirname(self.settings_path))

            self.config = ConfigParser.ConfigParser(allow_no_value = True)

            # if the settings path does not exist, then create it
            if not os.path.exists(self.settings_path):
                self.save_default_environment()

            # re-write this file if in debug mode to ensure that the settings are always up-to-date
            if sys.gettrace():
                self.save_default_environment()

            # load the environment variables
            self.load_environment(self.settings_path)

            EnvironmentVars.__monostate = self.__dict__
        else:
            self.__dict__ = EnvironmentVars.__monostate


    def load_environment(self, settings_path=None):
        settings_path = self.settings_path if settings_path is None else settings_path

        self.config = ConfigParser.ConfigParser(allow_no_value = True)

        self.config.read(self.settings_path)
        settings_dict = self.parse()
        for k, v in settings_dict.iteritems():
            setattr(self, k.upper(), v)


    def set_environment_variable(self, section, var, value=None):

        try:

            # make sure all sections are uppercase
            section = section.upper()

            # create a class variable if the value is not None. Comments will have None value
            if value is not None:

                env_name = '_'.join([section, var.upper()])
                if env_name in self.__dict__:
                    self.__dict__[env_name] = value
                else:
                    setattr(self, '_'.join([section, var.upper()]), value)


            # add section/var/value to configparser object
            # make sure that this section exists before adding var, value
            if not self.config.has_section(section):
                self.config.add_section(section)
            self.config.set(section, var, value)

        except Exception, e:
            # fixme: cannot import logging b/c of circular dependency
            # elog.error("Invalid environment variable or value: %s" % e.message)
            return 0


    def save_environment(self, settings_path=None):
        settings_path = self.settings_path if settings_path is None else settings_path
        try:
            fp = open(settings_path,'w+')
            self.config.write(fp)
            return 1
        except Exception, e:
            # fixme: cannot import logging b/c of circular dependency
            # elog.error("Error saving environment variables: %s" % e.message)
            return 0


    def parse(self):
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

    def save_default_environment(self):

        with open(self.settings_path, 'w') as f:

            #fixme: ConfigParser does not preserve comments!  Replace with cfgparse
            # set default environment variables
            # self.set_environment_variable('LOGGING','; Controls the verbosity of the console dialog, 1 is on, 0 is off')
            # self.set_environment_variable('LOGGING','; True or False values should be represented by 1 or 0')
            self.set_environment_variable('LOGGING', 'showinfo', 1)
            self.set_environment_variable('LOGGING', 'showwarning', 1)
            self.set_environment_variable('LOGGING', 'showcritical', 1)
            self.set_environment_variable('LOGGING', 'showerror', 1)
            self.set_environment_variable('LOGGING', 'showdebug', 0)

            # self.set_environment_variable('LOCAL_DB','; Settings associated with the local SQLite database')
            self.set_environment_variable('LOCAL_DB', 'path', os.path.abspath(os.path.join(os.path.dirname (self.settings_path),'../db/local.db')))

            # self.set_environment_variable('USER','; Settings associated with user profile')
            self.set_environment_variable('USER', 'json', os.path.abspath(os.path.join(os.path.dirname (self.settings_path),'../configuration/users.json')))


            self.set_environment_variable('LEGEND', 'locationright', 1)
            self.set_environment_variable('LEGEND', 'locationbottom', 0)

            self.set_environment_variable('IMAGES', 'path', os.path.abspath(os.path.join(os.path.dirname (self.settings_path),'../img')))

            self.set_environment_variable('TOOLBOX', 'path', os.path.abspath(os.path.join(os.path.dirname (self.settings_path),'../configuration/toolbox.ini')))

            # write environment variables to file
            self.save_environment()

            # self.set_environment_variable('LOGGING', 'showinfo',0)
            # self.write_environment_variables()


env_vars = EnvironmentVars()
