__author__ = 'mike'

import unittest
import os, sys
import pyspatialite.dbapi2 as sqlite3
import subprocess

# odm2_api_path = os.path.abspath(os.path.join(__file__, '../../../ODM2PythonAPI'))
odm2_api_path = os.path.abspath(os.path.join(__file__, '../../../ODM2PythonAPI/src'))
sys.path.append(odm2_api_path)
# from api.ODMconnection import dbconnection
# from api.ODM2.services.readService import ReadODM2
from ODM2PythonAPI.src.api.ODMconnection import dbconnection
from ODM2PythonAPI.src.api.ODM2.services.readService import ReadODM2
from db.dbapi_v2 import sqlite

# from EM.src.api.ODMconnection import dbconnection
# from ODM2PythonAPI_.src.api.ODM2.services.readService import ReadODM2


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


        # get the database dump files
        empty_dump_script = open('./data/empty_dump.sql','r').read()
        populated_dump_script = open('./data/populated_dump.sql','r').read()

        # create temp databases
        empty_odm2_db = sqlite3.connect(self.empty_db_path) # create a memory database
        pop_odm2_db = sqlite3.connect(self.pop_db_path) # create a memory database

        # load the dump files into the in-memory databases
        empty_odm2_db.executescript(empty_dump_script)
        pop_odm2_db.executescript(populated_dump_script)

        self.sqlite = sqlite(self.pop_db_path)
        # create database connections that will be used in test cases
        self.empty_connection = dbconnection.createConnection('sqlite', self.empty_db_path)

        # self.pop_connection = dbconnection.createConnection('sqlite', self.pop_db_path)
        self.pop_connection = self.sqlite.connection



    def tearDown(self):

        # remove temp databases
        if os.path.exists(self.empty_db_path):
            os.remove(self.empty_db_path)
        if os.path.exists(self.pop_db_path):
            os.remove(self.pop_db_path)


    def test_get_people(self):
        r = ReadODM2(self.pop_connection)

        people = r.getPeople()
        # self.assertTrue(len(people) == 4)

        person = r.getPersonById(1)
        self.assertTrue(person.PersonFirstName == 'tony')

    # def test_get_simulations(self):
    #     r = ReadODM2(self.pop_connection)
    #
    #     # THIS SHOULD NOT RETURN NONE!!!!
    #     simulations = r.getAllSimulations()
    #
    #     self.assertTrue(len(simulations) == 1)

    def test_create_user(self):
        tempPerson = {'firstName': 'Bob', 'lastName': 'Charles'}
        self.sqlite.create_user(tempPerson)

    def test_validate_new_user(self):

        #  Validating that the person was added
        r = ReadODM2(self.pop_connection)
        person = r.getPersonByName('Bob', 'Charles')
        self.assertTrue('Bob' == person.PersonFirstName, msg="Match! Person was inserted in the database")

    def test_add_new_user(self):
        tempPerson = {'firstName': 'Bob', 'lastName': 'Charles'}
        self.sqlite.create_user(tempPerson)

        r = ReadODM2(self.pop_connection)
        person = r.getPersonByName('Bob', 'Charles')
        id = r.getPersonById(person.PersonID)
        self.assertTrue(person == id)

    def test_display_new_user(self):
        r = ReadODM2(self.pop_connection)
        print r.getPeople()

    def test_create_organization(self):
        temporgan = {'cvType': 'University', 'code': 'usu',
                      'name': 'GoAggies', 'desc': 'GoAggies',
                      'link': 'GoAggies', 'parentOrgId': 'GoAggies'}

        self.sqlite.create_organization(temporgan)

    # def test_validate_new_organization(self):
    #
    #     #  Validating that the organization was added
    #     r = ReadODM2(self.empty_connection)
    #     print r.getOrganizations()
    #     group = r.getOrganizationByCode('GoAggies')
    #
    #     id = r.getOrganizationById(group.OrganizationID)
    #     #     self.assertTrue(group == id)



    def test_create_simulation(self):
        pass

