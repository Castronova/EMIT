import unittest
import os, sys
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2 import models
import coordinator.users as user
from db.dbapi_v2 import sqlite
from utilities import geometry
import stdlib
from utilities import mdl
import random
from datetime import datetime as dt
from datetime import timedelta
import environment
import sprint
import numpy
from collections import namedtuple


class test_sqlite_db(unittest.TestCase):

    def setUp(self):

        # define the paths for the empty and populated temp databases
        dirpath = os.path.dirname(os.path.abspath(__file__))
        self.empty_db_path = os.path.join(dirpath,'data/temp_empty.db')
        self.pop_db_path = os.path.join(dirpath, 'data/temp_pop.db')


        # remove temp databases
        if os.path.exists(self.empty_db_path):
            os.remove(self.empty_db_path)
        if os.path.exists(self.pop_db_path):
            os.remove(self.pop_db_path)

        # connect to each database
        empty_connection = dbconnection.createConnection('sqlite', self.empty_db_path)
        pop_connection = dbconnection.createConnection('sqlite', self.pop_db_path)

        self.emptysqlite = sqlite(empty_connection)
        self.popsqlite = sqlite(pop_connection)

        # initialize the in-memory database, loop through each command (skip first and last lines)
        empty_dump_script = open( os.path.join(dirpath, 'data/empty_dump.sql'),'r').read()
        for line in empty_dump_script.split(';\n'):
            self.emptysqlite.cursor.execute(line)

        populated_dump_script = open(os.path.join(dirpath, 'data/populated_dump.sql'),'r').read()
        for line in populated_dump_script.split(';\n'):
            self.popsqlite.cursor.execute(line)

        # initialize environment variables
        environment.getEnvironmentVars()
        if sys.gettrace():
            print 'Detected Debug Mode'
            # initialize debug listener (reroute messages to console)
            self.d = sprint.DebugListener()
        sprint.PrintTarget.CONSOLE = 1134

    def tearDown(self):

        # remove temp databases
        if os.path.exists(self.empty_db_path):
            os.remove(self.empty_db_path)
        if os.path.exists(self.pop_db_path):
            os.remove(self.pop_db_path)


    def test_create_user(self):


        people = self.emptysqlite.read.getPeople()
        self.assertTrue(len(people) == 0)

        p = namedtuple('Struct', 'first_name,last_name,middle_name')
        userInfo = namedtuple('Struct', 'person')
        p.first_name = 'tony'
        p.last_name = 'castronova'
        p.middle_name = ''
        userInfo.person = p
        self.emptysqlite.createPerson(userInfo)

        people = self.emptysqlite.read.getPeople()
        self.assertTrue(len(people) == 1)
        self.assertTrue(people[0].PersonFirstName == 'tony')


    # def test_create_organization(self):
    #     testOrg = {'cvType': 'University', 'code': 'usu',
    #                   'name': 'GoAggies', 'desc': 'a university in utah',
    #                   'link': 'SomeLink', 'parentOrgId': None}
    #
    #     orgs = self.emptysqlite.read.getOrganizations()
    #     self.assertTrue(len(orgs) == 0)
    #
    #     self.emptysqlite.write.createOrganization(**testOrg)
    #     o = self.emptysqlite.read.getOrganizations()
    #     self.assertTrue(len(o) == 1)
    #
    #     o = self.emptysqlite.read.getOrganizationByCode('usu')
    #     self.assertTrue(o.OrganizationName == 'GoAggies')
    #
    #     o = self.emptysqlite.read.getOrganizationById(1)
    #     self.assertTrue(o.ParentOrganizationID is None)
    #
    #     cvs = self.emptysqlite.read.getCVOrganizationTypes()
    #     self.assertTrue(len(cvs) > 1)


    def test_insert_many_tsrv(self):


        item, geometries  = self.setup_model(geomcount=1, valuecount=50000)
        timesteps, geomcount = item.getValues2().shape
        dates = item.getDates()[:, 1]

        sprint.sPrint('\n')
        sprint.sPrint('Inserting a simulation containing %d timesteps and %d '
                      'geometries' % (timesteps, geomcount),
                      sprint.MessageType.INFO)
        sprint.sPrint('\n')

        self.assertTrue(len(item.getDates2()) == len(item.getValues2()))
        self.assertTrue(len(item.getGeometries2()) == len(item.getValues2()[0]))

        description = 'Some description'
        name = 'test simulation with many result values'

        # build user object
        if not os.path.exists(os.environ['APP_USER_PATH']):
            self.assertTrue(1 == 0, 'No User.json found!')
        user_obj = user.json_to_dict(os.environ['APP_USER_PATH'])
        u = user_obj[user_obj.keys()[0]]  # grab the first user

        self.emptysqlite.create_simulation(coupledSimulationName=name,
                                           user_obj=u,
                                           action_date=dt.now(),
                                           action_utc_offset=-7,
                                           ei=item,
                                           simulation_start=dates[0],
                                           simulation_end=dates[-1],
                                           timestep_value=1,
                                           timestep_unit='minutes',
                                           description=description,
                                           name=name)

        s = self.emptysqlite.read.getSimulations()
        self.assertTrue(len(s) == 1)

        actionid = s[0].ActionID
        factions = self.emptysqlite.cursor.execute('SELECT * FROM '
                                                   'FeatureActions WHERE '
                                                   'ActionID = %d' % actionid)\
                                          .fetchall()

        sampling_feature_ids = [f[1] for f in factions]
        feature_action_ids = [f[0] for f in factions]

        results = self.emptysqlite.read.getResults(actionid=actionid)
        for i in range(len(results)):
            res = results[i]
            resgeom = res.FeatureActionObj.SamplingFeatureObj\
                                          .FeatureGeometryWKT
            resvalues = self.emptysqlite.read.getResultValues(res.ResultID)

            self.assertTrue(resgeom == geometries[i].ExportToWkt())
            self.assertTrue(len(resvalues) == timesteps)


    def test_insert_many_geoms(self):

        item, geometries  = self.setup_model(geomcount=1000, valuecount=2000)
        timesteps, geomcount = item.getValues2().shape
        dates = item.getDates()[:,1]

        sprint.sPrint('\nInserting a simulation containing %d timesteps and'
                      ' %d geometries\n' % (timesteps, geomcount),
                      sprint.MessageType.INFO)

        self.assertTrue(len(item.getDates2()) == len(item.getValues2()))
        self.assertTrue(len(item.getGeometries2()) == len(item.getValues2()[0]))

        description = 'Some description'
        name = 'test simulation with many feature geometries'

        # build user object
        if not os.path.exists(os.environ['APP_USER_PATH']):
            self.assertTrue(1 == 0, 'No User.json found!')
        user_obj = user.json_to_dict(os.environ['APP_USER_PATH'])
        u = user_obj[user_obj.keys()[0]]  # grab the first user

        self.emptysqlite.create_simulation(name, u, None, item, dates[0],
                                           dates[-1], 1, 'minutes',
                                           description, name)

        s = self.emptysqlite.read.getSimulations()
        self.assertTrue(len(s) == 1)

        actionid = s[0].ActionID
        factions = self.emptysqlite.cursor.execute('SELECT * FROM '
                                                   'FeatureActions WHERE '
                                                   'ActionID = %d' % actionid)\
                                          .fetchall()

        sampling_feature_ids = [f[1] for f in factions]
        feature_action_ids = [f[0] for f in factions]

        results = self.emptysqlite.read.getResults(actionid=actionid)
        for i in range(len(results)):
            res = results[i]
            resgeom = res.FeatureActionObj.SamplingFeatureObj.FeatureGeometryWKT
            resvalues = self.emptysqlite.read.getResultValues(res.ResultID)

            self.assertTrue(resgeom == geometries[i].ExportToWkt())
            self.assertTrue(len(resvalues) == timesteps)


    def setup_model(self, geomcount, valuecount):

        # create an exchange item
        unit = mdl.create_unit('cubic meters per second')
        variable = mdl.create_variable('streamflow')

        # create exchange item
        item = stdlib.ExchangeItem(name='Test', desc='Test Exchange Item',
                                   unit=unit, variable=variable)

        # set exchange item geometries
        xcoords = [i for i in range(geomcount)]
        ycoords = [i*1.5 for i in range(geomcount)]
        geoms = geometry.build_point_geometries(xcoords, ycoords)
        item.addGeometries2(geoms)

        # set exchange item values
        start_time = dt.now()
        end_time = start_time+timedelta(minutes=valuecount - 1)
        time_step = 60 # in seconds
        item.initializeDatesValues(start_datetime=start_time, end_datetime=end_time, timestep_in_seconds=time_step)
        values = numpy.random.rand(valuecount, geomcount)

        # for i in range(len(dates)):
        item.setValuesBySlice(values) #, time_index_slice=(0,num_timesteps,1))

        return item, geoms

