import unittest
import os
from odm2api.ODMconnection import dbconnection
import coordinator.users as user
from db.dbapi_v2 import sqlite
from utilities import geometry
import stdlib
from utilities import mdl
import random
from datetime import datetime as dt
from datetime import timedelta
import time
import numpy

import environment


def temp_build_database(dbpath):

    # remove temp database
    if os.path.exists(dbpath):
        os.remove(dbpath)

    # connect to each database
    db = dbconnection.createConnection('sqlite', dbpath)
    db_instance = sqlite(db)



    return db_instance


def cleanup(dbpath):

    # remove temp database
    if os.path.exists(dbpath):
        os.remove(dbpath)

def prepare_database(db, dump_schema_array):

    # initialize the in-memory database, loop through each command
    for line in dump_schema_array:
        db.cursor.execute(line+')')



    # build user object
    user_json = '{"3987225b-9466-4f98-bf85-49c9aa82b079": {"affiliation": {"address": "8200 old main, logan ut, 84322","affiliationEnd": null,"email": "tony.castronova@usu.edu","isPrimaryOrganizationContact": false,"personLink": null,"phone": "435-797-0853","startDate": "2014-03-10T00:00:00"},"organization": {"code": "usu","description": null,"link": null,"name": "Utah State University","parent": null,"typeCV": "university"},"person": {"firstname": "tony","lastname": "castronova","middlename": null}},"ef323a55-39df-4cb8-b267-06e53298f1bb": {"affiliation": {"address": "8200 old main, logan ut, 84322","affiliationEnd": null,"email": "tony.castronova@usu.edu","isPrimaryOrganizationContact": false,"personLink": null,"phone": null,"startDate": "2014-03-10T00:00:00"},"organization": {"code": "uwrl","description": "description = research laboratory Affiliated with utah state university","link": null,"name": "Utah Water Research Laboratory","parent": "usu","typeCV": "university"},"person": {"firstname": "tony","lastname": "castronova","middlename": null}}}'
    user_obj = user.BuildAffiliationfromJSON(user_json)

    return user_obj



def insert_simulation(db, user, geomcount, valuecount):

    print '%d geometries, %d values per geometry' % (geomcount, valuecount)
    print 'Total number of data values: %d' % (valuecount * geomcount)

    # create an exchange item
    unit = mdl.create_unit('cubic meters per second')
    variable = mdl.create_variable('streamflow')

    # create exchange item
    item = stdlib.ExchangeItem(name='Test', desc='Test Exchange Item', unit=unit, variable=variable)

    # set exchange item geometries
    xcoords = numpy.random.rand(geomcount)
    ycoords = numpy.random.rand(geomcount)
    points = geometry.build_point_geometries(xcoords, ycoords)
    item.addGeometries2(points)

    # set exchange item values
    start_time = dt.now()                                   # set start time to 'now'
    end_time = start_time + timedelta(days=valuecount-1)    # create endtime base on the number of values
    current_time = start_time                               # initial time
    dates = []                                              # list to hold dates
    values = []                                             # list to hold values for each date

    # populate dates list
    while current_time <= end_time:

        # add date
        dates.append(current_time)

        # add some random values for each geometry
        values.append([random.random() for pt in points] )

        # increment time by 1 day
        current_time += timedelta(days=1)

    # set dates and values in the exchange item
    item.setValues2(values, dates)

    # create the simulation
    st = dt(2014, 3, 1, 12, 0, 0)
    et = dt(2014, 3, 1, 23, 0, 0)
    description = 'Some model descipription'
    name = 'test simulation'

    # turn off verbosity for simulation insert
    os.environ['LOGGING_SHOWINFO'] = '0'
    os.environ['LOGGING_SHOWDEBUG'] = '0'
    db.create_simulation('My Simulation', user[0], None, item, st, et, 1, 'days', description, name)
    os.environ['LOGGING_SHOWINFO'] = '1'

    # query simulations
    simulations = db.read.getAllSimulations()
    simulation = db.read.getSimulationByName('My Simulation')
    assert simulation is not None

# create a temporary database
dirpath = os.path.dirname(os.path.abspath(__file__))
tempdb_path = os.path.join(dirpath,'temp.db')
db = temp_build_database(tempdb_path)

# prepare the database
raw_sql_commands = open( os.path.join(dirpath, '../tests/db/data/empty_dump.sql'),'r').read()[19:-8]
sqlcommands = raw_sql_commands.split(');')[:-1]
user = prepare_database(db, sqlcommands)


print 50*'-'
st = time.time()
insert_simulation(db, user, geomcount=10, valuecount=10)
print 'Elapsed time: %3.2f sec' % (time.time() - st)

print 50*'-'
st = time.time()
insert_simulation(db, user, geomcount=100, valuecount=10)
print 'Elapsed time: %3.2f sec' % (time.time() - st)

print 50*'-'
st = time.time()
insert_simulation(db, user, geomcount=1000, valuecount=10)
print 'Elapsed time: %3.2f sec' % (time.time() - st)

print 50*'-'
st = time.time()
insert_simulation(db, user, geomcount=10000, valuecount=10)
print 'Elapsed time: %3.2f sec' % (time.time() - st)

print 50*'-'
st = time.time()
insert_simulation(db, user, geomcount=10, valuecount=10)
print 'Elapsed time: %3.2f sec' % (time.time() - st)

print 50*'-'
st = time.time()
insert_simulation(db, user, geomcount=10, valuecount=100)
print 'Elapsed time: %3.2f sec' % (time.time() - st)

print 50*'-'
st = time.time()
insert_simulation(db, user, geomcount=10, valuecount=1000)
print 'Elapsed time: %3.2f sec' % (time.time() - st)

print 50*'-'
st = time.time()
insert_simulation(db, user, geomcount=10, valuecount=10000)
print 'Elapsed time: %3.2f sec' % (time.time() - st)


# cleanup
print 50*'-'
cleanup(tempdb_path)