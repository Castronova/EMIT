__author__ = 'ryan'

import test_ODM1 as tODM1
from suds.client import Client


class WebServiceApi:


    def __init__(self):
        self.odm1 = tODM1.ODM1()
        self.sites = {}
        self.objects = self.odm1.getObjectSite(self.odm1.sitecode)

    def buildSitesDictionary(self):
        for site in self.objects.site:
            print site
            return
temp = WebServiceApi()
i = 1
