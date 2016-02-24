__author__ = 'tonycastronova'

import collections
from suds.client import Client
from coordinator.emitLogging import elog
from utilities.timeout import timeout


def parseXML2Dict(site, start=None, end=None):
    import xml.etree.ElementTree as et
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


def createXMLFileForReading(xml_string):
    # Open this file in a browser to view it parsed
    file = open("test.xml", "w")
    file.write(xml_string)
    file.close()


class WaterOneFlow(object):

    @timeout(10)
    def __init__(self, wsdl, network):
        self.wsdl = wsdl
        # sleep(3)
        self.conn = Client(wsdl)
        self.network_code = network + ":"

    def _getSiteType(self, site):
        try:
            return site[0][5][3].value
        except IndexError:
            return site[0][5][2].value
        except ValueError:
            return ""

    def buildAllVariableDictionary(self, start=None, end=None):

        if start == None:
            start = 1
        if end == None:
            end = start + 10

        xml = self.getVariables()
        createXMLFileForReading(xml)
        vars = parseXML2Dict(xml, start, end)
        vars = iter(vars)
        next(vars)
        self.AllVariables = vars
        return vars

    def buildAllSiteCodeVariables(self, sitecode):
        site_object = self.getSiteInfoObject(sitecode)

        try:
            seriesVariables = site_object[1][0][1][0][2]
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

    def parseValues(self, sitecode, variable, start=None, end=None):
        data = self.getValues(sitecode, variable, start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d"))
        valuesList = []
        if data is not None:
            for values in data[0].values[0].value:
                # values_list = [[date1, value1], [date2, value2]]
                valuesList.append([values._dateTime, values.value])
        else:
            elog.debug("data is None")
            elog.error("Failed to retrieve data")

        return valuesList

    def connectToNetwork(self, link):
        connection = Client(link)
        return connection

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
        print self.network_code
        data = self.conn.service.GetSiteInfoObject(self.network_code + ":"+ str(sitecode))
        return data

    def getSitesByBoxObject(self, sitecode):
        # fixme: there is an error with the input string not in the correct format.
        data = self.conn.service.GetSitesByBoxObject(sitecode)
        return data

    def getSites(self, value=None):
        #  Returns JSON
        print value
        if value is None:
            site_objects = self.conn.service.GetSitesObject("")
        else:
            site_objects = self.conn.service.GetSitesObject(value)
        return site_objects[1]


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
            print 'There was an error getting data for %s:%s, %s:%s, %s %s' % (network_code, site_code, network_code, variable_code, str(beginDate), str(endDate))
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
        x = self.conn.service.GetValuesForASiteObject(self.network_code + ":" + str(siteid))
        return x
