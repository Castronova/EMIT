import ConfigParser
import sys
import os

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



def writeDefaultEnvironment(settings=None):

    if settings is None:
        currentdir = os.path.dirname(os.path.abspath(__file__))
        settings = os.path.abspath(os.path.join(currentdir, './app_data/config/.settings.ini'))

        # get the default location relative to the packeage
        if getattr(sys, 'frozen', False):
            settings = os.path.join(sys._MEIPASS, 'app_data/config/.settings.ini')

    # set the relative path for the app_data directory
    app_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_data'))
    if getattr(sys, 'frozen', False):
        app_path = os.path.join(sys._MEIPASS, 'app_data')

    config = ConfigParser.ConfigParser(allow_no_value = True)
    config.add_section('LOGGING')
    config.set('LOGGING', 'SHOWINFO', 1)
    config.set('LOGGING', 'SHOWWARNING', 1)
    config.set('LOGGING', 'SHOWCRITICAL', 1)
    config.set('LOGGING', 'SHOWERROR', 1)
    config.set('LOGGING', 'SHOWDEBUG', 1)


    config.add_section('APP')
    config.set('APP', 'IMAGES_PATH',   os.path.abspath(os.path.join(app_path, 'img')))
    config.set('APP', 'LOCAL_DB_PATH', os.path.abspath(os.path.join(app_path, 'db/local.db')))
    config.set('APP', 'SETTINGS_PATH', os.path.abspath(os.path.join(app_path, 'config/.settings.ini')))
    config.set('APP', 'TOOLBOX_PATH',  os.path.abspath(os.path.join(app_path, 'config/toolbox.ini')))
    config.set('APP', 'USER_PATH',     os.path.abspath(os.path.join(app_path, 'config/users.json')))

    config.add_section('LEGEND')
    config.set('LEGEND', 'locationright', 1)
    config.set('LEGEND', 'locationbottom', 0)

    # set the relative path for the gdal_data directory
    gdal_path = os.path.abspath(os.path.join(os.path.dirname(sys.executable), '../share/gdal'))
    if getattr(sys, 'frozen', False):
        gdal_path = os.path.join(sys._MEIPASS, 'gdal')

    config.add_section('GDAL')
    config.set('GDAL', 'DATA', gdal_path)


    with open(settings, 'w') as f:
        config.write(f)


def setEnvironmentVar(section, var, value=None, settings=None):

    # get the default location for the filepath if it is not provided
    if settings is None:
        currentdir = os.path.dirname(os.path.abspath(__file__))
        settings = os.path.abspath(os.path.join(currentdir, './app_data/config/.settings.ini'))

    # get the default location relative to the packeage
    if getattr(sys, 'frozen', False):
        settings = os.path.join(sys._MEIPASS, 'app_data/config/.settings.ini')

    # parse the settings file into a config parser object
    config = readEnvironment(settings)

    # add section, var, value to the config parser object
    section = section.upper()
    var = var.upper()
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, var, str(value))

    # reload the environment variables
    loadEnvironment(config)

    # save the environment variable
    with open(settings, 'w') as f:
        config.write(f)

def readEnvironment(settings):


    # parse the settings file
    config = ConfigParser.ConfigParser(allow_no_value = True)
    config.read(settings)

    return config

    # settings_dict = parse(config)

    # return settings_dictx

def loadEnvironment(config):

    # set the environment variables
    settings_dict = parseConfigIntoDict(config)
    for k, v in settings_dict.iteritems():
        os.environ[k.upper()] = str(v)

def parseConfigIntoDict(config):
    '''
    The settings file is divided into sections, such as logging
    and local_db. In each section there are options, which contain
    the variables and values. Parsing with ConfigParser, all values
    are considered STRINGS and need to be converted if necessary to
    booleans or ints.
    '''
    d = {}
    for section in config.sections():
        for option in config.options(section):
            value = config.get(section, option)
            d['_'.join([section, option])] = str(value)

    return d

def getDefaultSettingsPath():

    currentdir = os.path.dirname(os.path.abspath(__file__))
    settings = os.path.abspath(os.path.join(currentdir, './app_data/config/.settings.ini'))

    # get the default location relative to the packeage
    if getattr(sys, 'frozen', False):
        settings = os.path.join(sys._MEIPASS, 'app_data/config/.settings.ini')

    return settings


def getDefaultUsersJsonPath():
    currentdir = os.path.dirname(os.path.abspath(__file__))
    users_path = os.path.abspath(os.path.join(currentdir, './app_data/config/users.json'))

    # get the default location relative to the packeage
    if getattr(sys, 'frozen', False):
        users_path = os.path.join(sys._MEIPASS, 'app_data/config/users.json')

    return users_path


def getEnvironmentVars(settings=None):

    # get the default location for the filepath if it is not provided
    if settings is None:
        settings = getDefaultSettingsPath()

    # write the default file path if it doesn't exist
    msg = None
    if not os.path.exists(settings):
        writeDefaultEnvironment(settings)
        msg = 'writing default environment variables to settings. This is because no settings file could be found.'
    # re-write this file if in debug mode to ensure that the settings are always up-to-date
    elif sys.gettrace():
        msg = 'writing default environment variables to settings. This is because you are running in debug mode.'
        writeDefaultEnvironment(settings)

    # read the default settings
    config = readEnvironment(settings)

    # load the default environment
    loadEnvironment(config)

    sPrint(msg, MessageType.INFO)

getEnvironmentVars()