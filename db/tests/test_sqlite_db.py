__author__ = 'mike'

import unittest
import os, sys
import coordinator.users as user
from environment import env_vars
from odm2api.ODMconnection import dbconnection
from odm2api.ODM2.services.readService import ReadODM2
from db.dbapi_v2 import sqlite
from utilities import geometry
import stdlib
from utilities import mdl, gui
import random
from datetime import datetime as dt
from datetime import timedelta

class test_sqlite_db(unittest.TestCase):

    def setUp(self):

        # define the paths for the empty and populated temp databases
        self.empty_db_path = os.path.abspath('./data/temp_empty.db')
        self.pop_db_path = os.path.abspath('./data/temp_pop.db')

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
        empty_dump_script = open('./data/empty_dump.sql','r').read()
        for line in empty_dump_script.split(';\n'):
            self.emptysqlite.cursor.execute(line)
        populated_dump_script = open('./data/populated_dump.sql','r').read()
        for line in populated_dump_script.split(';\n'):
            self.popsqlite.cursor.execute(line)



    def tearDown(self):

        # remove temp databases
        if os.path.exists(self.empty_db_path):
            os.remove(self.empty_db_path)
        if os.path.exists(self.pop_db_path):
            os.remove(self.pop_db_path)


    def test_get_people(self):

        people = self.popsqlite.read.getPeople()
        self.assertTrue(len(people) == 5)

        person = self.popsqlite.read.getPersonById(2)
        self.assertTrue(person.PersonFirstName == 'tony')


    def test_create_user(self):
        testPerson = {'firstName': 'Bob', 'lastName': 'Charles'}

        people = self.emptysqlite.read.getPeople()
        self.assertTrue(len(people) == 0)

        self.emptysqlite.create_user(testPerson)

        people = self.emptysqlite.read.getPeople()
        self.assertTrue(len(people) == 1)

        person = self.emptysqlite.read.getPersonByName('Bob', 'Charles')
        self.assertTrue('Bob' == person.PersonFirstName, msg="Match! Person was inserted in the database")

        p = self.emptysqlite.read.getPersonById(person.PersonID)
        self.assertTrue(person == p)


    def test_create_organization(self):
        testOrg = {'cvType': 'University', 'code': 'usu',
                      'name': 'GoAggies', 'desc': 'a university in utah',
                      'link': 'SomeLink', 'parentOrgId': None}

        orgs = self.emptysqlite.read.getOrganizations()
        self.assertTrue(len(orgs) == 0)

        self.emptysqlite.write.createOrganization(**testOrg)
        o = self.emptysqlite.read.getOrganizations()
        self.assertTrue(len(o) == 1)

        o = self.emptysqlite.read.getOrganizationByCode('usu')
        self.assertTrue(o.OrganizationName == 'GoAggies')

        o = self.emptysqlite.read.getOrganizationById(1)
        self.assertTrue(o.ParentOrganizationID is None)

        cvs = self.emptysqlite.read.getCVOrganizationTypes()
        self.assertTrue(len(cvs) > 1)


    # todo: re-write
    def test_create_simulation(self):


        # create an exchange item
        unit = mdl.create_unit('cubic meters per second')
        variable = mdl.create_variable('streamflow')

        # create exchange item
        item = stdlib.ExchangeItem(name='Test', desc='Test Exchange Item', unit=unit, variable=variable)

        # set exchange item geometries
        xcoords = [1,2,3]
        ycoords = [2,3,4]
        points = geometry.build_point_geometries(xcoords, ycoords)
        item.addGeometries2(points)
        self.assertTrue(len(item.getGeometries2()) == len(points))

        # set exchange item values
        start_time = dt.now()                       # set start time to 'now'
        end_time = start_time + timedelta(days=100) # set endtime to 100 days later
        current_time = start_time                   # initial time
        dates = []                                  # list to hold dates
        values = []                                 # list to hold values for each date

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

        self.assertTrue(len(item.getDates2()) == len(item.getValues2()))
        self.assertTrue(len(item.getGeometries2()) == len(item.getValues2()[0]))

        # preferences
        pref = None

        # config_params
        config = None

        # list of exchange items
        ei = [item]

        params = {'general': [{'simulation_end': '03/01/2014 23:00:00',
                               'simulation_start': '03/01/2014 12:00:00',
                               'description': 'Some description',
                               'name': 'test simulation'}],
                  'model': [{'code': 'TOPMODEL',
                             'name': 'test model',
                             'description': 'Some model descipription'}],
                  'time_step' : [{'abbreviation': 'hr',
                                  'unit_type_cv': 'hour',
                                  'name': 'hours',
                                  'value': '1'}]}


        # build user object
        user_json = '{"3987225b-9466-4f98-bf85-49c9aa82b079": {"affiliation": {"address": "8200 old main, logan ut, 84322","affiliationEnd": null,"email": "tony.castronova@usu.edu","isPrimaryOrganizationContact": false,"personLink": null,"phone": "435-797-0853","startDate": "2014-03-10T00:00:00"},"organization": {"code": "usu","description": null,"link": null,"name": "Utah State University","parent": null,"typeCV": "university"},"person": {"firstname": "tony","lastname": "castronova","middlename": null}},"ef323a55-39df-4cb8-b267-06e53298f1bb": {"affiliation": {"address": "8200 old main, logan ut, 84322","affiliationEnd": null,"email": "tony.castronova@usu.edu","isPrimaryOrganizationContact": false,"personLink": null,"phone": null,"startDate": "2014-03-10T00:00:00"},"organization": {"code": "uwrl","description": "description = research laboratory Affiliated with utah state university","link": null,"name": "Utah Water Research Laboratory","parent": "usu","typeCV": "university"},"person": {"firstname": "tony","lastname": "castronova","middlename": null}}}'
        user_obj = user.BuildAffiliationfromJSON(user_json)



        # get affiliation
        affiliation = self.emptysqlite.read.getAffiliationsByPerson('tony','castronova')

        # create the simulation
        st = dt(2014, 3, 1, 12, 0, 0)
        et = dt(2014, 3, 1, 23, 0, 0)
        description = 'Some model descipription'
        name = 'test simulation'
        self.emptysqlite.create_simulation('My Simulation', user_obj[0], params, item, st, et, 1, 'hours', description, name)

        # r = ReadODM2(self.pop_connection)
        # # affiliation = r.getAffiliationsByPerson('tony','castronova')
        # self.sqlite.create_simulation('My Simulation', user_obj[0], params, item)









    # todo: re-write
    def test_insert_many(self):

        # create an exchange item
        unit = mdl.create_unit('cubic meters per second')
        variable = mdl.create_variable('streamflow')

        # create exchange item
        item = stdlib.ExchangeItem(name='Test', desc='Test Exchange Item', unit=unit, variable=variable)


        # set exchange item geometries
        # coords = [(1,2),(2,3),(3,4)]
        xcoords = [i for i in range(1000)]
        ycoords = [i*1.5 for i in range(1000)]
        geoms = geometry.build_point_geometries(xcoords, ycoords)
        item.addGeometries2(geoms)
        self.assertTrue(len(item.getGeometries2()) == len(geoms))

        # set exchange item values
        start_time = dt.now()
        end_time = start_time+timedelta(days=2000)
        time_step = 60*60*24
        item.initializeDatesValues(start_datetime=start_time, end_datetime=end_time, timestep_in_seconds=time_step)
        dates = [start_time + i*timedelta(days=1) for i in range(2000)]
        values = [random.random() for g in geoms]

        for i in range(len(dates)):
            item.setValuesBySlice(values, time_index_slice=(i,i+1,1))


        self.assertTrue(len(item.getDates2()) == len(item.getValues2()))
        self.assertTrue(len(item.getGeometries2()) == len(item.getValues2()[0]))

        # preferences
        pref = None

        # config_params
        config = None

        # list of exchange items
        ei = [item]

        params = {'general': [{'simulation_end': '03/01/2014 23:00:00',
                               'simulation_start': '03/01/2014 12:00:00',
                               'description': 'Some description',
                               'name': 'test simulation'}],
                  'model': [{'code': 'TOPMODEL',
                             'name': 'test model',
                             'description': 'Some model descipription'}],
                  'time_step' : [{'abbreviation': 'hr',
                                'unit_type_cv': 'hour',
                                'name': 'hours',
                                'value': '1'}]}


        # build user object
        user_json = open(env_vars.USER_JSON).read()
        user_obj = user.BuildAffiliationfromJSON(user_json)[0]

        self.emptysqlite.create_simulation(  coupledSimulationName='my simulation',
                                             user_obj=user_obj,
                                             config_params=params,
                                             ei=ei,
                                             simulation_start = start_time,
                                             simulation_end = end_time,
                                             timestep_value = time_step,
                                             timestep_unit = 'seconds',
                                             description = 'my description',
                                             name = 'my test model'
                                        )
        print 'done'
