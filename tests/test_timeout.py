__author__ = 'francisco'

import unittest
from time import sleep

from suds.client import Client

from utilities.timeout import timeout


class test_timeout(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
