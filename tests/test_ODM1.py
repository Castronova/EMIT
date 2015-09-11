__author__ = 'francisco'

from suds.client import Client
import xml.etree.ElementTree as et

#  Put a break point on the pass to see the values

class ODM1:

    def __init__(self):
        redButteCreek = "http://data.iutahepscor.org/RedButteCreekWOF/cuahsi_1_1.asmx?WSDL"
        provoRiver = "http://data.iutahepscor.org/ProvoRiverWOF/cuahsi_1_1.asmx?WSDL"
        loganRiver = "http://data.iutahepscor.org/LoganRiverWOF/cuahsi_1_1.asmx?WSDL"

        sitecode = sitecode = ["iutah:RB_FortD_SD"]
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
        conn = self.connectToNetwork(redButteCreek)
        site = self.getSite(conn, sitecode)
        self.parseSite(site)


    def connectToNetwork(self, link):
        connection = Client(link)
        return connection

    def getSite(self, conn, sitecode):
        # Returns an XML in a array of arrays
        xmlSite = conn.service.GetSites(sitecode)
        return xmlSite

    def parseSite(self, site):
        tree = et.fromstring(site)
        # queryInfo = tree[0]
        # site = tree[1]
        # siteInfo = tree[1][0]
        # siteCode = tree[1][0][1]

        for site in tree:
            print site.tag
            for siteInfo in site:
                print siteInfo
                for info in siteInfo:
                    print info
        pass

if __name__ == '__main__':
    odm1 = ODM1()