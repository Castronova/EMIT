__author__ = 'tonycastronova'

import os
import sys
import ConfigParser
import datetime
import cPickle as pickle
import imp
from dbapi.ODMconnection import  dbconnection
# from ODMconnection import dbconnection
import uuid

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
    description = 'str'
    generic_string = 'str'
    directory = 'str'

def validate_config_ini(ini_path):

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


        var = pickle.load(open(os.path.join(dir,'../data/var_cv.dat'),'rb'))
        unit = pickle.load(open(os.path.join(dir,'../data/units_cv.dat'),'rb'))

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
                except:
                    print '> [Error] Configuration Parsing Error: '+classname+' is not a valid class name'

    except Exception, e:
        print '> [Configuration Parsing Error] '+str(e)
        return 0


    return 1

def parse_config_without_validation(ini):
    """
    parses metadata stored in *.ini file
    """

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
            d[option] = cparser.get(s,option)
        d['type'] = section


        if section not in config_params:
            config_params[section] = [d]
        else:
            config_params[section].append(d)

    # save the base path of the model
    config_params['basedir'] = basedir = os.path.realpath(os.path.dirname(ini))

    return config_params

def parse_config(ini):
    """
    parses metadata stored in *.ini file
    """

    isvalid = validate_config_ini(ini)
    if isvalid:
        #raise Exception('Configuration file is not valid!')

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
                d[option] = cparser.get(s,option)
            d['type'] = section


            if section not in config_params:
                config_params[section] = [d]
            else:
                config_params[section].append(d)

        # save the base path of the model
        config_params['basedir'] = basedir = os.path.realpath(os.path.dirname(ini))

        return config_params
    else:
        return None

def create_database_connections_from_args(title, desc, engine, address, db, user, pwd):


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

        print '> Connected to : %s [%s]'%(connection_string,db_id)
    else:
        print 'Could not establish a connection with the database'
        return None

    return db_connections

def load_model(config_params):
    """
    Creates an instance of the model by loading the contents of the configuration ini file.
    returns (model name,model instance)
    """
    # parse module config
    #items = parse_config(ini)

    # get source attributes
    software = config_params['software']
    classname = software[0]['classname']
    relpath = software[0]['filepath']

    # load the model
    basedir = config_params['basedir']
    abspath = os.path.abspath(os.path.join(basedir,relpath))
    filename = os.path.basename(abspath)
    module = imp.load_source(filename, abspath)
    model_class = getattr(module, classname)

    # todo: Initialize model?
    instance = model_class(config_params)

    return (config_params['general'][0]['name'], instance)

def create_database_connections_from_file(ini):

    # database connections dictionary
    db_connections = {}

    # parse the dataabase connections file
    params = {}
    cparser = ConfigParser.ConfigParser(None, multidict)
    cparser.read(ini)
    sections = cparser.sections()

    # create a session for each database connection in the ini file
    for s in sections:

        # put ini args into a dictionary
        options = cparser.options(s)
        d = {}
        for option in options:
            d[option] = cparser.get(s,option)

        # build database connection
        #dbconn = odm2.api.dbconnection()
        session = dbconnection.createConnection(d['engine'],d['address'],d['db'],d['user'],d['pwd'])

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
                                     'description':d['desc'],
                                     'args': d}

            print '> Connected to : %s [%s]'%(connection_string,db_id)
        else:
            print 'Could not establish a connection with the database'
            #return None



    return db_connections

def get_ts_from_link(dbapi, dbactions, links, target_model):
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
        if t[0].get_name() == tname:
            mapping[t[1].name()] = f[1].name()
            #print '>  %s -> %s'%(f[1].name(), t[1].name())

            # get output exchange item
            from_unit = f[1].unit()
            from_var = f[1].variable()
            to_var = t[1].variable()
            to_item = t[1]
            name = f[0].get_name()
            # start = f[1].getStartTime()
            # end = f[1].getEndTime()

            start = t[0].get_instance().simulation_start()
            end = t[0].get_instance().simulation_end()

            #model = f[0]

            #actionid, type = dbactions[model.get_name()]

            # query timeseries data from db
            ts = dbapi.get_simulation_results(name,dbactions,from_var.VariableNameCV(),from_unit.UnitName(),to_var.VariableNameCV(), start,end)

            # store the timeseries based on exchange item
            #timeseries[f[1].name()] = ts
            timeseries.update(ts)


    return timeseries

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