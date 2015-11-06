__author__ = 'ryan'

import test_ODM1 as tODM1
import collections

class WebServiceApi:

    '''
    TODO:
    allow for diffrent site codes.

    '''

    def __init__(self):
        self.odm1 = tODM1.ODM1()
        self.sites = {}
        self.objects = self.odm1.getSitesObject("iutah:RB_FortD_SD")

    def buildSitesDictionary(self,start=None, end=None):


        if start == None:
            start = 1
        if end  == None:
            end = start + 10

        self.siteInfo_Dictionary = collections.OrderedDict()
        for site in self.objects[1]:
            if len(site) > 0:
                self.siteInfo_Dictionary[site[0][0]] = site[0][1][0][0]

        return self.siteInfo_Dictionary

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

        queryInfoType = siteObject[0]
        siteInfo = siteObject[1][0][0]
        seriesCatalog = siteObject[1][0][1]

        try:
            seriesVariables = siteObject[1][0][1][0][2]
        except Exception as e:
            print e  # There exist no variables
            return {}

        variableDict = collections.OrderedDict()

        for i in range(0, len(seriesVariables[start:end])):
            variableDict[seriesVariables[i][0][0][0].value] = seriesVariables[i][0][1]


        return variableDict