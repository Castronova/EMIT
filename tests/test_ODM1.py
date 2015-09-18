__author__ = 'francisco'

from suds.client import Client
import xml.etree.ElementTree as et
import collections

class ODM1:

    def __init__(self):
        self.redButteCreek = "http://data.iutahepscor.org/RedButteCreekWOF/cuahsi_1_1.asmx?WSDL"
        self.provoRiver = "http://data.iutahepscor.org/ProvoRiverWOF/cuahsi_1_1.asmx?WSDL"
        self.loganRiver = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"

        # sitecode = sitecode = ["iutah:RB_FortD_SD"]
        '''
            This site code is only one of many.  To get more site code go to
            http://data.iutahepscor.org/tsa/

            Check one of the networks on the left side of the window. For example...check Red Butte
            Creek.

            Click on any of the circles on the map.  This will zoom in on the area you clicked.

            Once zoomed, click another circle, and it will probably zoom in again.

            Click another icon on the map it will give you site code.
            The site code is below the name of the location.Its the small bold text.

            Make sure to include 'iutah:' in front of the site code
        '''

        self.conn = self.connectToNetwork(self.redButteCreek)
        # site = self.getSites()
        # var = self.getVariables()
        # # valuesObject = self.getValuesObject("RB_KF_C", "AirTemp_Avg")  # this will take about 3 min to load.
        # self.parseXML2Dict(site)
        # self.parseXML2Dict(var)


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
        data = self.conn.service.GetSiteInfoObject(sitecode)
        return data

    def getSites(self):
        #  Returns an XML
        #  Returns all sites
        data = self.conn.service.GetSites("")
        return data

    def getSitesByBoxObject(self, sitecode):
        # fixme: there is an error with the input string not in the correct format.
        data = self.conn.service.GetSitesByBoxObject(sitecode)
        return data

    def getSitesObject(self, sitecode):
        #  Returns a JSON
        siteobjects = self.conn.service.GetSitesObject(sitecode)
        return siteobjects

    def getValues(self, sitecode, variable=None):
        #  Passing only the sitecode returns the data values.
        #  Passing both variables returns that specified object.
        # Returns an XML
        network = "iutah:"
        if variable is not None:
            variable = network + str(variable)

        data = self.conn.service.GetValues(network + str(sitecode), variable)
        return data

    def getValuesForASiteObject(self, siteid=None):
        network = "iutah:"
        x = self.conn.service.GetValuesForASiteObject(network + str(siteid))
        return x

    def getValuesObject(self, sitecode, variable):
        # sitecode = RB_KF_C, variable = AirTemp_Avg this is can example it working
        # Returns in a json format
        network = "iutah:"
        data = self.conn.service.GetValuesObject(network + str(sitecode), network + str(variable))
        return data

    def getVariableInfo(self, variable):
        #  Returns an XML
        if variable is not None:
            variable = "iutah:" + str(variable)

        data = self.conn.service.GetVariableInfo(variable)
        return data

    def getVariableInfoObject(self, variable=None):
        #  Returns a JSON
        if variable is not None:
            variable = "iutah:" + str(variable)

        data = self.conn.service.GetVariableInfoObject()
        return data

    def getVariables(self):
        # Returns an XML string
        data = self.conn.service.GetVariables()
        return data

    def getVariablesObject(self):
        #  Same as getXMLVariables() but it returns it in json format
        data = self.conn.service.GetVariablesObject()
        return data

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




if __name__ == '__main__':
    odm1 = ODM1()
