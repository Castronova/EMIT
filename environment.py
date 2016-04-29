import os
import sys
import ConfigParser
import encrypt
import sqlite3 as sqlite
from odm2api import dbconnection
from sprint import *


def saveConnection(connection):

    # check that the connection is valid
    session_factory = dbconnection.createConnection(connection['engine'], connection['address'], connection['database'], connection['username'], connection['password'])
    if not session_factory:
        sPrint('Failed to save database connection: invalid connection information', MessageType.ERROR)
        return False

    config = ConfigParser.ConfigParser(allow_no_value=True)
    connections_path = os.environ['APP_CONNECTIONS_PATH']
    config.read(connections_path)

    # make sure this database name doesn't already exist
    if connection['name'] in config.sections():
        sPrint('Failed to save database connection: database already exists', MessageType.ERROR)
        return False

    # encrypt password
    import secret
    cipher = encrypt.AESCipher(secret.key)
    uhash = cipher.encrypt(connection['username'])
    phash = cipher.encrypt(connection['password'])

    config.add_section(connection['name'])
    config.set(connection['name'], 'description', connection['description'])
    config.set(connection['name'], 'engine', connection['engine'])
    config.set(connection['name'], 'address', connection['address'])
    config.set(connection['name'], 'database', connection['database'])
    config.set(connection['name'], 'username', uhash)
    config.set(connection['name'], 'password', phash)
    with open(connections_path, 'wb') as f:
        config.write(f)

    return True


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
    config.set('APP', 'CONNECTIONS_PATH',     os.path.abspath(os.path.join(app_path, 'db/connections')))
    config.set('APP', 'SECRET',     os.path.abspath(os.path.join(app_path, 'secret.py')))


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


def getSettingsPath():
    """
    Determines the location of the setting file based on dev or app modes
    Returns: path to application settings file

    """

    currentdir = os.path.dirname(os.path.abspath(__file__))
    settings = os.path.abspath(os.path.join(currentdir, './app_data/config/.settings.ini'))

    # get the default location relative to the package
    if getattr(sys, 'frozen', False):
        settings = os.path.join(sys._MEIPASS, 'app_data/config/.settings.ini')

    return settings


def initSecret():
    """
    initializes the database secret file and creates a secret token used to encrypt database information
    Returns: None

    """

    # get path to secret
    secret = os.environ['APP_SECRET']

    # get the default location relative to the packeage
    if getattr(sys, 'frozen', False):
        secret = os.path.join(sys._MEIPASS, 'secret.py')

    # rebuild the secret file
    if not os.path.exists(secret):
        import uuid
        with open(secret, 'w') as f:
            f.write('#\n# This is a secret key for password encryption/decryption.  Do not share with anyone!\n#\n\n')
            f.write('key = "%s"' % uuid.uuid4().hex)

def initLocalDb():
    """
    initializes the local sqlite database if it does not exist
    Returns: None

    """

    # get the local database and database creation script paths
    local_db = os.environ['APP_LOCAL_DB_PATH']
    script_path = os.path.join(
        os.path.dirname(local_db),
        '.dbload'
    )

    # if the database is not found in the dev directory or app directory then create it
    if not os.path.exists(local_db):
        conn = sqlite.connect(local_db)
        script = open(script_path)
        with conn:
            cur = conn.cursor()
            cur.executescript(script.read())
        script.close()

def getEnvironmentVars():
    """
    Loads the environment variables stored in a settings file
    Returns: None

    """

    # get the default location for the filepath if it is not provided
    settings = getSettingsPath()

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

    # initialize the secret file (encryption/decryption)
    initSecret()

    # initalize the local database
    initLocalDb()

    sPrint(msg, MessageType.INFO)

getEnvironmentVars()