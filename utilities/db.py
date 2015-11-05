__author__ = 'tonycastronova'

import uuid
import ConfigParser
from api_old.ODMconnection import  dbconnection, SessionFactory


def build_session_from_connection_string(connection_string):

    s = SessionFactory(connection_string, False)

    return s

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

        print 'Connected to : %s [%s]'%(connection_string,db_id)
    else:
        print 'ERROR | Could not establish a connection with the database'
        return None

    return db_connections


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

            print 'Connected to : %s [%s]'%(connection_string,db_id)



        else:
            print 'ERROR | Could not establish a connection with the database'
            #return None



    return db_connections

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
