__author__ = 'francisco'

import unittest
from time import sleep
from suds.client import Client
from utilities.timeout import timeout
from webservice import wateroneflow


class test_wof(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

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
        link = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"
        connection = Client(link)
        sites = connection.service.GetSitesObject("")
        self.assertIsNotNone(sites)
        self.assertIsInstance(sites, object)

    def test_get_site_info(self):
        pass

    def test_get_site_info_object(self):
        sitecode = "LR_WaterLab_AA"
        link = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"
        connection = Client(link)
        site_object = connection.service.GetSiteInfoObject("iutah:" + sitecode)
        self.assertIsNotNone(site_object)
        self.assertIsInstance(site_object, object)
        pass

    def test_get_site_info_multiple_object(self):
        link = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"
        connection = Client(link)
        data = connection.service.GetSiteInfoMultpleObject("")
        self.assertIsInstance(data, object)

    def test_get_sites_by_box_object(self):
        pass


    #################################################
    ################   VARIABLES   ##################
    #################################################
    def test_get_variables(self):
        link = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"
        connection = Client(link)
        data = connection.service.GetVariableInfoObject()
        self.assertIsInstance(data, object)

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
        import wx
        site_url = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"
        api = wateroneflow.WaterOneFlow(site_url)

        site_code = "LR_WaterLab_AA"
        variable = "BattVolt"
        start_date = wx.DateTime_Now() - 7 * wx.DateSpan_Day()
        end_date = wx.DateTime_Now()

        # Dates must be in YEAR-MONTH-DAY format
        start_date = start_date.FormatISODate()
        end_date = end_date.FormatISODate()

        data = api.getValuesObject(site_code=site_code, variable_code=variable, beginDate=start_date, endDate=end_date)
        self.assertIsInstance(data, object)

    def test_parse_values(self):
        pass

    def test_get_values_for_site_object(self):
        pass


    #################################################
    #################   WRITING   ###################
    #################################################
    def test_create_file(self):
        import os
        currentdir = os.path.dirname(os.path.abspath(__file__))
        f = open(currentdir + "/test.xml", 'w')
        self.assertTrue(os.path.exists(currentdir + "/test.xml"))
        f.close()

        os.remove(currentdir + "/test.xml")
        self.assertFalse(os.path.exists(currentdir + "/test.xml"))

    def test_parse_xml_to_dict(self):
        pass

