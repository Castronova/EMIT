__author__ = 'tonycastronova'

import ConfigParser
import cPickle as pickle
import datetime
import imp
import sys
import uuid
import time
from odm2api.ODMconnection import dbconnection as dbconnection2
import utilities.io as io
from api_old.ODMconnection import dbconnection
from emitLogging import elog
from sprint import *


class multidict(dict):
    _unique = 0

    def __setitem__(self, key, val):
        if isinstance(val, dict):
            self._unique += 1
            key += '^'+str(self._unique)
        dict.__setitem__(self, key, val)

class ini_types():
    # todo: add the ability to extend these types via inputfile
    name = 'str'
    description = 'str'
    value = 'int'
    unit_type_cv = 'str'
    variable_name_cv = 'str'
    simulation_start = '%m/%d/%Y %H:%M:%S'
    simulation_end = '%m/%d/%Y %H:%M:%S'
    elementset = 'str'
    epsg_code = 'int'
    filepath = 'str'
    classname = 'str'
    ignorecv = 'str'
    code = 'str'
    generic_string = 'str'
    directory = 'str'


def validate_config_ini(ini_path):  # Deprecated. Use utilities.models.validate_json_model
    try:

        cparser = ConfigParser.ConfigParser(None, multidict)

         # parse the ini
        cparser.read(ini_path)

        # get the ini sections from the parser
        parsed_sections = cparser.sections()

        # if no sections are found, than the file format must be incorrect
        if len(parsed_sections) == 0: raise Exception('> [Exception] Invalid model configuration file')

        # load lookup tables
        dir = os.path.dirname(__file__)

        var_cv = os.path.join(io.getAppDataDir(), 'dat/var_cv.dat') 
        unit_cv= os.path.join(io.getAppDataDir(), 'dat/units_cv.dat')
        var = pickle.load(open(var_cv, 'rb'))
        unit= pickle.load(open(unit_cv, 'rb'))

#        var = pickle.load(open(os.path.join(dir,'../data/var_cv.dat'),'rb'))
#        unit = pickle.load(open(os.path.join(dir,'../data/units_cv.dat'),'rb'))

        # check to see if 'ignorecv' option has been provided
        ignorecv = False
        for p in parsed_sections:
            if p.split('^')[0] == 'options':
                if cparser.has_option(p,'ignorecv'):
                    ignorecv = int(cparser.get(p,'ignorecv'))
                    break


        # validate
        for section in parsed_sections:
            # get ini options
            options = cparser.options(section)

            if not ignorecv:
                # validate units and variables parameters
                if section.split('_')[0] == 'output' or section.split('_')[0] == 'input':
                    # check that variable and unit exist
                    if 'variable_name_cv' not in options or 'unit_type_cv' not in options:
                        raise Exception ('Inputs and Outputs must contain "variable_name_cv" and "unit_type_cv" parameters ')

            # check each option individually
            for option in options:
                val = cparser.get(section,option)

                # validate date format
                if option == 'simulation_start' or option == 'simulation_end':
                    try:
                        datetime.datetime.strptime(val, getattr(ini_types, option))
                    except ValueError:
                        raise ValueError("Incorrect data format, should be "+getattr(ini_types, option))
                else:
                    # validate data type

                    #if not isinstance(val,type(getattr(ini_types, option))):
                    #        raise Exception(option+' is not of type '+getattr(ini_types, option))

                    if not ignorecv:
                        # check variable cv (i.e. lookup table)
                        if option == 'variable_name_cv':
                            if val not in var:
                                raise Exception (val+' is not a valid controlled vocabulary term')

                        # check unit type cv (i.e. lookup table)
                        if option == 'unit_type_cv':
                            if val not in unit:
                                raise Exception (val+' is not a valid controlled vocabulary term')


            if section.split('^')[0] == 'software':
                # check that software filepath is valid
                relpath = cparser.get(section,'filepath')
                basedir = os.path.realpath(os.path.dirname(ini_path))
                abspath = os.path.abspath(os.path.join(basedir,relpath))

                # add the base path to the sys.path
                sys.path.append(basedir)

                if not os.path.isfile(abspath):
                    raise Exception(abspath+' is not a valid file')

                #todo: check that software class name exists
                try:
                    classname = cparser.get(section,'classname')
                    filename = os.path.basename(abspath)
                    module = imp.load_source(filename.split('.')[0], abspath)
                    m = getattr(module, classname)
                except Exception, e:
                    elog.error('Configuration Parsing Error: '+str(e))
                    sPrint('Configuration Parsing Error: '+str(e), MessageType.ERROR)

    except Exception, e:
        elog.error('Configuration Parsing Error: '+str(e))
        sPrint('Configuration Parsing Error: '+str(e), MessageType.ERROR)
        return 0


    return 1


def parse_config(ini):  # Deprecated. Use utilities.models.parse_json
    """
    parses metadata stored in *.ini file.  This file is use by both the GUI and the ENGINE.
    """
    # isvalid = True
    # if validate:
    isvalid = validate_config_ini(ini)


    if isvalid:
        basedir = os.path.realpath(os.path.dirname(ini))
        config_params = {}
        cparser = ConfigParser.ConfigParser(None, multidict)
        cparser.read(ini)
        sections = cparser.sections()

        for s in sections:
            # get the section key (minus the random number)
            section = s.split('^')[0]

            # get the section options
            options = cparser.options(s)

            # save ini options as dictionary
            d = {}
            for option in options:
                value = cparser.get(s,option)

                try:
                    # convert anything that is recognized as a file path into an absolute paths
                    genpath = os.path.abspath(os.path.join(basedir, value))
                    if os.path.isfile(genpath):
                        value = genpath
                except TypeError:
                    pass

                d[option] = value
            d['type'] = section.upper()

            if section not in config_params:
                config_params[section] = [d]
            else:
                config_params[section].append(d)

        # save the base path of the model
        config_params['basedir'] = basedir

        return config_params
    else:
        return None


def connect_to_ODM2_db(title, desc, engine, address, db, user, pwd):

    # create a db session
    session = dbconnection2.createConnection(engine, address, db, user, pwd)

    db_connections = {}
    if session:

        # get the connection string
        connection_string = session.engine.url

        # save this session in the db_connections object
        db_id = uuid.uuid4().hex[:5]
        d['id'] = db_id
        db_connections[db_id] = {'name':title,
                                 'session': session,
                                 'connection_string':connection_string,
                                 'description':desc,
                                 'args': {'name':title,'desc':desc ,'engine':engine,'address':address,'db': db, 'user': user,'pwd': pwd}}

        elog.info('Connected to : %s [%s]'%(connection_string.__repr__(),db_id))
        sPrint('Connected to : %s [%s]'%(connection_string.__repr__(),db_id))
    else:
        elog.error('Could not establish a connection with the database')
        sPrint('Could not establish a connection with the database', MessageType.ERROR)
        return None

    return db_connections


def create_database_connections_from_args(title, desc, engine, address, db, user, pwd):

    # fixme: all database connections should use the updated ODM library
    if engine == 'sqlite':
        return connect_to_db(title, desc, engine, address, db, user, pwd)

    # old database connection api

    d = {'name':title,
         'desc':desc ,
         'engine':engine,
         'address':address,
         'db': db,
         'user': user,
         'pwd': pwd}

    # database connections dictionary
    db_connections = {}

    # build database connection

    #dbconn = odm2.api.dbconnection()
    session = dbconnection.createConnection(engine,address,db,user,pwd)


    # add connection string to dictionary (for backup/debugging)
    # d['connection_string'] = connection_string

    # create a session
    if session:

        # get the connection string
        connection_string = session.engine.url

        # save this session in the db_connections object
        db_id = uuid.uuid4().hex[:5]
        d['id'] = db_id
        db_connections[db_id] = {'name':d['name'],
                                 'session': session,
                                 'connection_string':connection_string,
                                 'description':d['desc'],
                                 'args': d}

        elog.info('Connected to : %s [%s]'%(connection_string.__repr__(),db_id))
        sPrint('Connected to : %s [%s]'%(connection_string.__repr__(),db_id))
    else:
        elog.error('Could not establish a connection with the database')
        sPrint('Could not establish a connection with the database', MessageType.ERROR)
        return None

    return db_connections

def load_model(config_params):
    """
    Creates an instance of the model by loading the contents of the configuration ini file.
    returns (model name,model instance)
    """

    try:
        # get source attributes
        software = config_params['software']
        classname = software[0]['classname']
        relpath = software[0]['filepath']

        sPrint('Classname: %s' % classname, MessageType.DEBUG)
        sPrint('Relpath: %s' % relpath, MessageType.DEBUG)

        # load the model
        basedir = config_params['basedir']
        abspath = os.path.abspath(os.path.join(basedir,relpath))
        sPrint('AbsPath: %s' % abspath, MessageType.DEBUG)

        # add the model dir to the system path so that submodule imports
        # work properly
        sys.path.append(os.path.dirname(os.path.abspath(relpath)))

        # load the model class
        module = imp.load_source(classname, abspath)
        model_class = getattr(module, classname)
        sPrint('Model Class Extracted Successfully', MessageType.DEBUG)

        # Initialize the model component
        instance = model_class(config_params)
        sPrint('Model Initialization Successful', MessageType.DEBUG)

    except Exception as e:
        sPrint('An error has occurred while loading model: %s' % e, MessageType.CRITICAL)
        raise Exception(e)

    return (instance.name(), instance)

def connect_to_db(title, desc, engine, address, db=None, user=None, pwd=None):

    d = {}
    session = dbconnection2.createConnection(engine, address, db, user, pwd)
    if not session:
        elog.error('Could not establish a connection with the database')
        sPrint('Could not establish a connection with the database', MessageType.ERROR)
        return


    # adjusting timeout
    session.engine.pool._timeout = 30

    connection_string = session.engine.url

    # save this session in the db_connections object
    db_id = uuid.uuid4().hex[:5]

    d[db_id] = {'name':title,
                 'session': session,
                 'connection_string':connection_string,
                 'description':desc,
                 'args': dict(address=connection_string, desc=desc, engine=engine,id=db_id,name=db,
                              user=None, pwd=None,default=False,db=None)}

    elog.info('Connected to : %s [%s]'%(connection_string.__repr__(),db_id))
    sPrint('Connected to : %s [%s]'%(connection_string.__repr__(),db_id))


    return d


def read_database_connection_from_file(ini):

    # database connections dictionary
    db_connections = []

    # parse the dataabase connections file
    cparser = ConfigParser.ConfigParser(None, multidict)
    cparser.read(ini)
    sections = cparser.sections()

    # create a session for each database connection in the ini file
    for s in sections:

        # put ini args into a dictionary
        d = {}
        options = cparser.options(s)
        d['name'] = s
        for option in options:
            d[option] = cparser.get(s,option)

        db_connections.append(d)

    return db_connections

# todo: remove this function and use the one above!
def create_database_connections_from_file(ini):

    # database connections dictionary
    db_connections = {}

    # parse the dataabase connections file
    cparser = ConfigParser.ConfigParser(None, multidict)
    cparser.read(ini)
    sections = cparser.sections()

    # create a session for each database connection in the ini file
    for s in sections:

        # put ini args into a dictionary
        d = {}
        options = cparser.options(s)
        d['name'] = s
        for option in options:
            d[option] = cparser.get(s,option)

        # build database connection
        session = dbconnection2.createConnection(d['engine'],d['address'],d['database'],d['username'],d['password'])

        if session:
            # adjusting timeout
            session.engine.pool._timeout = 30

            connection_string = session.engine.url

            # add connection string to dictionary (for backup/debugging)
            d['connection_string'] = connection_string


            # save this session in the db_connections object
            db_id = uuid.uuid4().hex[:5]
            d['id'] = db_id

            db_connections[db_id] = {'name':d['name'],
                                     'session': session,
                                     'connection_string':connection_string,
                                     'description':d['description'],
                                     'args': d}
            elog.info('Connected to : %s [%s]'%(connection_string.__repr__(),db_id))
            sPrint('Connected to : %s [%s]'%(connection_string.__repr__(),db_id))

        else:
            msg = 'Could not establish a connection with the following database: ***@%s/%s' % (d['address'],d['database'])
            elog.error(msg)
            sPrint(msg, MessageType.ERROR)

    return db_connections

def generate_link_key(link):
    """
    Generates a dictionary key based on link input modelid,exchangeid and output modelid, exchangeid
    :param link: link object
    :return: unique string key
    """

    return '_'.join([ link.source_component().name(),
                      link.source_exchange_item().name(),
                      link.target_component().name(),
                      link.target_exchange_item().name()])

    #return '_'.join([link[0][0].get_name(),link[0][1].name(),link[1][0].get_name(),link[1][1].name()])

def get_ts_from_database_link(dbapi, db_sessions, dbactions, links, target_model):
    """
    queries the data
    :param session: database session where the data is stored
    :param links: all links
    :param target_model:
    :return:
    """



    #if session is None:
    #    print '>  [error] no default database has been specified'
    #    return 0

    mapping = {}
    timeseries = {}
    tname = target_model.name()


    for id,link_inst in links.iteritems():
        f,t = link_inst.get_link()

        dbapi = db_sessions[f[0].id()]

        if t[0].name() == tname:
            mapping[t[1].name()] = f[1].name()
            #print '>  %s -> %s'%(f[1].name(), t[1].name())

            # get output exchange item
            from_unit = f[1].unit()
            from_var = f[1].variable()
            to_var = t[1].variable()
            to_item = t[1]
            name = f[0].name()
            # start = f[1].getStartTime()
            # end = f[1].getEndTime()

            start = t[0].instance().simulation_start()
            end = t[0].instance().simulation_end()

            #model = f[0]

            #actionid, type = dbactions[model.get_name()]

            # query timeseries data from db
            ts = dbapi.get_simulation_results(name,dbactions,from_var.VariableNameCV(),from_unit.UnitName(),to_var.VariableNameCV(), start,end)

            # store the timeseries based on exchange item
            #timeseries[f[1].name()] = ts
            timeseries.update(ts)


    return timeseries

# def get_ts_from_link(links, target_model):
#
#     mapping = {}
#     inputs = []
#
#
#     for id,link_inst in links.iteritems():
#         f,t = link_inst.get_link()
#
#
#         if t[0].get_name() == target_model.name():
#         #    mapping[t[1].name()] = f[1].name()
#
#             # get output exchange item
#             from_unit = f[1].unit()
#             from_var = f[1].variable()
#             to_var = t[1].variable()
#             to_item = t[1]
#
#             from_item = f[0].get_name()
#             to_item = t[0].get_name()
#
#             start = t[0].get_instance().simulation_start()
#             end = t[0].get_instance().simulation_end()
#
#             inputs.append((from_item,  from_var))
#
#
#     return inputs

def save_model_results():
    pass

def unresolved_exchange_items():
    # make sure that all input items are satisfied
    # warn the user if output items are not being used or saved in database
    pass

def get_start_end(model_instance):
    """
    calculates the global start and end time for a model simulation
    :param model_instance: the class instance of the desired model
    :return: global start and end time for all exchange items
    """
    pass


# TODO: Move into wrapper?
def get_data_by_exchange_item(exchangeitemlist, variableName, unitName):
    """
    returns the exchange item associated with a given variable and unit
    :param exchangeitemlist: list of exchange items
    :param variableName: desired variable
    :param unitName: desired unit
    :return: exchange item associated with variable and unit
    """
    pass

def loadAccounts():
    import coordinator.users as users
    known_users = []
    userjson = os.environ['APP_USER_PATH']

    #  Create the file if it does not exist
    if os.path.isfile(userjson):
        with open(userjson, 'r') as file:
            content = file.read()
            file.close()
        if not (content.isspace() or len(content) < 1):  # check if file is empty
            # file does exist so proceed like normal and there is content in it
            elog.debug('userjson ' + userjson)
            with open(userjson, 'r') as f:
                known_users.extend(users.BuildAffiliationfromJSON(f.read()))
                f.close()
    else:
        # file does not exist so we'll create one.
        file = open(userjson, 'w')
        file.close()

    return known_users

def get_todays_date():
    return time.strftime("%m/%d/%Y")
