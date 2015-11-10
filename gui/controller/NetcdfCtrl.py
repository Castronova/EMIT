__author__ = 'francisco'

from gui.views.NetcdfViewer import NetcdfViewer
import os
import wx
from xml.etree import cElementTree
from urlparse import urljoin
import requests
import httplib
import urlparse



class NetcdfCtrl(NetcdfViewer):

    def __init__(self, parent):  # What parameters does this need?


        # namespaces for XML parsing
        self.thredds = "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0"
        self.xlink = "http://www.w3.org/1999/xlink"
        NetcdfViewer.__init__(self, parent=parent)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, self.add_to_canvas_btn)
        self.Bind(wx.EVT_BUTTON, self.RunCrawler, self.get_btn)

    def addToCanvas(self, event):
        item = self.getSelectedInformation()
        # this will get the url we want
        url = self.TableValues[item][1]
        print url
        print "Adding to canvas: SEarch HELLO THIS IS ADDING"

    def getSelectedInformation(self):
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                v_name = self.variableList.GetItemText(1)
                return i


    def get_server_status_code(self, url):
        """
        Download just the header of a URL and
        return the server's status code.
        """
        # http://stackoverflow.com/questions/1140661
        host, path = urlparse.urlparse(url)[1:3]    # elems [1] and [2]
        try:
            conn = httplib.HTTPConnection(host)
            conn.request('HEAD', path)
            return conn.getresponse().status
        except StandardError:
            return None

    def check_url(self, url):
        """
        Check if a URL exists without downloading the whole file.
        We only check the URL header.
        """
        # see also http://stackoverflow.com/questions/2924422
        good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
        return self.get_server_status_code(url) in good_codes

    def updateFileList(self, data):
        rowNumber = 0
        colNumber = 0

        for x in data:
            pos = self.variableList.InsertStringItem(rowNumber, "test")
            for y in x:
                self.variableList.SetStringItem(pos, colNumber, str(y))
                colNumber +=1
            colNumber = 0
            rowNumber +=1


    def RunCrawler(self, event):
        results = [];
        url = self.url_textbox.GetLineText(0)
        isValid = self.check_url(url + "/catalog.xml")

        if isValid:
            results = self.crawler(url +"/catalog.xml",results)
            self.TableValues = [];
            spacing = 25
            print '\n\nFilename',(spacing-len('Filename'))*' ','DAP Path'
            print '--------',(spacing-len('Filename'))*' ','--------'
            for ds in results:
                # cElementTree.tostring(catalog, 'utf-8')

                dap = ds.find('.//{%s}access[@serviceName="dap"]'%self.thredds)
                if dap is not None:
                    wms = ds.find('.//{%s}access[@serviceName="wms"]'%self.thredds)
                    size = ds.find('.//{%s}dataSize'%self.thredds)
                    date = ds.find('.//{%s}date'%self.thredds)

                    dap_url = dict(dap.items())['urlPath']
                    wms_url = dict(wms.items())['urlPath']
                    name = dict(ds.items())['name']

                    self.TableValues.append([name, url + dap_url, url + dap_url + ".das"])
                    print name,(spacing-len(name))*' ',dap_url

            for x in self.TableValues:
                print x
            self.updateFileList(self.TableValues)


    def crawler(self,catalog, results):
        r = requests.get(catalog)
        xml = cElementTree.fromstring(r.content)

        for subdir in xml.iterfind(".//{%s}catalogRef" % self.thredds):
            link = subdir.attrib["{%s}href" % self.xlink]

            self.crawler(urljoin(catalog, link), results)

        for dataset in xml.iterfind(".//{%s}dataset//{%s}dataset" % (self.thredds,self.thredds)):
            results.append(dataset)


        return results




