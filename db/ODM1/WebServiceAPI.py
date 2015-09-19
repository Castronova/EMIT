__author__ = 'ryan'

import collections
from db.ODM1.ODM1 import ODM1

class WebServiceApi:

    def __init__(self, website):

        self.odm1 = ODM1(website)
        self.objects = self.odm1.getSitesObject()

    def buildSitesDictionary(self, start=None, end=None):

        if start == None:
            start = 1
        if end  == None:
            end = start + 10

        siteInfo_Dictionary = collections.OrderedDict()
        for site in self.objects[1][start:end]:
            if len(site) > 0:
                siteInfo_Dictionary[site[0][0]] = site[0][1][0][0]

        return siteInfo_Dictionary

    def buildAllVariableDictionary(self, start=None, end=None):

        if start == None:
            start = 1
        if end == None:
            end = start + 10

        xml = self.odm1.getVariables()
        self.odm1.createXMLFileForReading(xml)
        vars = self.odm1.parseXML2Dict(xml, start, end)
        vars = iter(vars)
        next(vars)
        self.AllVariables = vars
        return vars

    def buildAllSiteCodeVariables(self, sitecode, start=None, end=None):
        if start is None:
            start = 1
        if end is None:
            end = start + 10

        siteObject = self.odm1.getSiteInfoObject(sitecode)

        try:
            seriesVariables = siteObject[1][0][1][0][2]
        except Exception as e:
            print e  # There exist no variables
            return {}

        variableDict = collections.OrderedDict()

        for i in range(0, len(seriesVariables[start:end])):
            variableDict[seriesVariables[i][0][0][0].value] = seriesVariables[i][0][1]

        return variableDict

    def buildSiteVariables(self, siteCode):

        self.siteVarables = collections.OrderedDict()

