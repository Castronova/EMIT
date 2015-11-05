__author__ = 'tonycastronova'

import collections
import xml.etree.ElementTree as et
from suds.client import Client


class wof(object):

    def __init__(self, wsdl):
        self.wsdl = wsdl
        self.conn = Client(wsdl)
        self.network_code = ""

    def _getSiteType(self, site):
        try:
            return site[0][5][3].value
        except IndexError:
            return site[0][5][2].value
        except ValueError:
            return ""

    # def buildSitesDictionary(self, start=None, end=None):
    #
    #     if start == None:
    #         start = 1
    #     if end  == None:
    #         end = start + 10
    #
    #     siteInfo_Dictionary = collections.OrderedDict()
    #     for site in self.objects[1][start:end]:
    #         if len(site) > 0:
    #             siteInfo_Dictionary[site[0][0]] = site[0][1][0][0]
    #
    #     return siteInfo_Dictionary

    def buildAllVariableDictionary(self, start=None, end=None):

        if start == None:
            start = 1
        if end == None:
            end = start + 10

        xml = self.getVariables()
        self.createXMLFileForReading(xml)
        vars = self.parseXML2Dict(xml, start, end)
        vars = iter(vars)
        next(vars)
        self.AllVariables = vars
        return vars

    def buildAllSiteCodeVariables(self, sitecode):
        siteObject = self.getSiteInfoObject(sitecode)

        try:
            seriesVariables = siteObject[1][0][1][0][2]
        except Exception as e:
            print e  # There exist no variables
            return {}

        variableDict = collections.OrderedDict()

        for i in range(0, len(seriesVariables)):
            # {Site code: [Variable Name, Units, Type, Category, Begin Date Time, End Date Time, Description]}
            variableDict[seriesVariables[i][0][0][0].value] = [seriesVariables[i][0][1],  # Variable Name
                                                               seriesVariables[i][0][6][2],  # Units
                                                               seriesVariables[i][0][3],  # Type
                                                               seriesVariables[i][0][4],  # Category
                                                               seriesVariables[i][2][0],  # Begin Date Time Objects
                                                               seriesVariables[i][2][1],  # End Date Time Objects
                                                               seriesVariables[i][3][1],  # Description
                                                               ]
        return variableDict

    def buildSiteVariables(self, siteCode):

        self.siteVarables = collections.OrderedDict()

    # def getSites(self):
    #     sites = self.createXMLFileForReading(self.getSites())
    #     return sites

    def getSiteInfo(self, start=None, end=None):

        if start == None:
            start = 0
        if end  == None:
            end = start + 9

        siteInfo = []
        for site in self.objects[1][start:end]:
            if len(site) > 0:
                # The structure of siteInfo list is [[Site Name, County, State, site type, site code]]
                siteInfo.append([site[0][0], site[0][5][0].value, site[0][5][1].value, self._getSiteType(site), site[0][1][0].value])

        return siteInfo

    def parseValues(self, sitecode, variable, start=None, end=None):
        data = self.getValues(sitecode, variable, start, end)
        valuesList = []
        for values in data[0].values[0].value:
            # values_list = [[date1, value1], [date2, value2]]
            valuesList.append([values._dateTime, values.value])
            pass
        return valuesList

    def connectToNetwork(self, link):
        connection = Client(link)
        return connection

    def createXMLFileForReading(self, xml_string):
        # Open this file in a browser to view it parsed
        file = open("test.xml", "w")
        file.write(xml_string)
        file.close()

    def createJSONFileForReading(self, json):
        # Open this file in a browser to view in parsed
        file = open("test.json", "w")
        file.write(str(json))
        file.close()

    def getSiteInfoMultipleObject(self):
        #  Returns a JSON
        #  Similar to getSiteInfoObject() but returns all locations, with a bit less information.
        data = self.conn.service.GetSiteInfoMultpleObject("")
        return data

    def getSiteInfoObject(self, sitecode):
        #  Returns a JSON
        #  Returns all the information for a given site.
        #  This includes all the variables associated with that location  description.
        data = self.conn.service.GetSiteInfoObject("iutah:" + str(sitecode))
        return data

    def getSitesByBoxObject(self, sitecode):
        # fixme: there is an error with the input string not in the correct format.
        data = self.conn.service.GetSitesByBoxObject(sitecode)
        return data

    def getSites(self, value=None):
        #  Returns JSON
        if value is None:
            siteobjects = self.conn.service.GetSitesObject("")
        else:
            siteobjects = self.conn.service.GetSitesObject(value)
        return siteobjects[1]


    def getValues(self, site_code, variable_code, beginDate=None, endDate=None):
        #  Passing only the sitecode returns the data values.
        #  Passing both variables returns that specified object.
        # Returns an XML
        network_code = self.network_code

        try:
            site = ':'.join([network_code, site_code])
            var = ':'.join([network_code, variable_code])
            if beginDate is None or endDate is None:
                data = self.conn.service.GetValuesObject(site, var)
            else:
                data = self.conn.service.GetValuesObject(site, var, beginDate, endDate)

            return data.timeSeries
        except:
            # error getting data
            print 'There was an getting data for %s:%s, %s:%s, %s %s' % (network_code, site_code, network_code, variable_code, str(beginDate), str(endDate))
            return None

    def getVariables(self, network_code=None, variable_code=None):
        #  Returns JSON
        if variable_code is not None and network_code is not None:
            value = ':'.join([network_code, variable_code])
            data = self.conn.service.GetVariableInfoObject(value)
        else:
            data = self.conn.service.GetVariableInfoObject()
        return data.variables











    def getValuesForASiteObject(self, siteid=None):
        network = "iutah:"
        x = self.conn.service.GetValuesForASiteObject(network + str(siteid))
        return x


    def parseXML2Dict(self, site, start=None, end=None):
        if start == None:
            start = 0

        if end == None:
            end = start + 10

        tree = et.fromstring(site)
        siteInfo_Dictionary = collections.OrderedDict()  # It will remember the order contents are added

        for site in tree:
            for siteInfo in site[start:end]:  # Using slicing to grab only 10 elements, otherwise it would grab 100+
                # for info in siteInfo:
                if len(siteInfo) > 0:
                    siteInfo_Dictionary[siteInfo.getchildren()[0].text] = siteInfo.getchildren()

        return siteInfo_Dictionary  # The key is the site name

