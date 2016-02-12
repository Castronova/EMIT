__author__ = 'francisco'

import unittest
from time import sleep
from suds.client import Client
from utilities.timeout import timeout


class test_wof(unittest.TestCase):
    def test_wof_success(self):
        class wof(object):

            @timeout(3)
            def __init__(self, wsdl):
                self.wsdl = wsdl
                sleep(1)
                self.conn = Client(wsdl)
                self.network_code = ""

        try:
            api = wof("http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL")
        except Exception:
            api = None

        self.assertIsNotNone(obj=api, msg="It Not none")
        print api

    def test_wof_timeout(self):
        class wof(object):
            @timeout(1)
            def __init__(self, wsdl):
                self.wsdl = wsdl
                sleep(3)  # sleep to simulate a long task
                self.conn = Client(wsdl)
                self.network_code = ""

        try:
            api = wof("http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL")
        except Exception:
            api = None
            print "water one flow web service took to long."

        self.assertIsNone(api, "Its None")

    def test_connect_to_network(self):
        link = "http://data.iutahepscor.org/RedButteCreekWOF/cuahsi_1_1.asmx?WSDL"
        connection = Client(link)
        self.assertIsNotNone(connection)
        link = "http://data.iutahepscor.org/ProvoRiverWOF/cuahsi_1_1.asmx?WSDL"
        connection = Client(link)
        self.assertIsNotNone(connection)
        link = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"
        connection = Client(link)
        self.assertIsNotNone(connection)

    #################################################
    ##################   SITES   ####################
    #################################################
    def test_get_sites(self):
        pass

    def test_get_site_info(self):
        pass

    def test_get_site_info_object(self):
        pass

    def test_get_site_info_multiple_object(self):
        pass

    def test_get_sites_by_box_object(self):
        pass


    #################################################
    ################   VARIABLES   ##################
    #################################################
    def test_get_variables(self):
        pass

    def test_build_all_variable_dictionary(self):
        pass

    def test_build_sitecode_variables(self):
        pass

    def test_build_site_variables(self):
        pass

    #################################################
    ##################   VALUES   ###################
    #################################################
    def test_get_values(self):
        pass

    def test_parse_values(self):
        pass

    def test_get_values_for_site_object(self):
        pass


    #################################################
    #################   WRITING   ###################
    #################################################
    def test_create_xml_file(self):
        pass

    def test_create_json_file(self):
        pass

    def test_parse_xml_to_dict(self):
        pass

