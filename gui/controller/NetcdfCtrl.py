import httplib
import os
import urlparse
from urlparse import urljoin
from xml.etree import cElementTree

import netCDF4 as nc
import requests
import wx

from gui.controller.NetcdfDetailsCtrl import NetcdfDetailsCtrl
from gui.views.OpenDapExplorerView import OpenDapExplorerView
import threading
from sprint import *


class NetcdfCtrl(OpenDapExplorerView):

    def __init__(self, parent):  # What parameters does this need?
        # namespaces for XML parsing
        self.thredds = "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0"
        self.xlink = "http://www.w3.org/1999/xlink"
        self.thread = threading.Thread()
        OpenDapExplorerView.__init__(self, parent=parent)
        self.Bind(wx.EVT_BUTTON, self.on_download, self.download_btn)
        self.Bind(wx.EVT_BUTTON, self.onView, self.view_btn)
        # self.Bind(wx.EVT_BUTTON, self.RunCrawler, self.get_btn)
        self.get_btn.Bind(wx.EVT_BUTTON, self.on_get_crawler)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.enableBtns)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.disableBtns)
        self.disableBtns(None)

    def alternateRowColor(self, color="#DCEBEE"):
        for i in range(self.variable_list.GetItemCount()):
            if i % 2 == 1:
                self.variable_list.SetItemBackgroundColour(i, color)

    def autoSizeColumns(self):
        for i in range(self.variable_list.GetColumnCount()):
            self.variable_list.SetColumnWidth(i, wx.LIST_AUTOSIZE)

    def CalculateBytes(self, fileSize):
        if fileSize > 1000 and fileSize < 1000000:
            fileSize = fileSize / 1000.0
            return "%0.2f Kilobytes" % fileSize
        elif fileSize > 1000000 and fileSize < 1000000000:
            fileSize = fileSize / 1000000.0
            return "%0.2f Megabytes" %fileSize
        elif fileSize > 1000000000 and fileSize < 1000000000000:
            fileSize = float(fileSize) / 1000000000.0
            return "%0.2f Gigabytes" % fileSize
        else:
            return str(fileSize) + " bytes"

    def check_url(self, url):
        """
        Check if a URL exists without downloading the whole file.
        We only check the URL header.
        """
        # see also http://stackoverflow.com/questions/2924422
        good_codes = [httplib.OK, httplib.FOUND, httplib.MOVED_PERMANENTLY]
        return self.get_server_status_code(url) in good_codes

    def clearData(self):
        self.variable_list.DeleteAllItems()

    def crawler(self, catalog, results):
        r = requests.get(catalog)
        xml = cElementTree.fromstring(r.content)

        for subdir in xml.iterfind(".//{%s}catalogRef" % self.thredds):
            link = subdir.attrib["{%s}href" % self.xlink]

            self.crawler(urljoin(catalog, link), results)

        for dataset in xml.iterfind(".//{%s}dataset//{%s}dataset" % (self.thredds,self.thredds)):
            results.append(dataset)


        return results

    def disableBtns(self, event):
        self.view_btn.Disable()
        self.download_btn.Disable()

    def on_download(self, event):

        # get the file url by rowid and colid
        rowid = self.getSelectedIndexRow()
        colid = self.getListCtrlColumnByName('url')
        url = self.TableValues[rowid][colid]

        # open a dialog to get save path
        saveFileDialog = wx.FileDialog(self, message="Save NetCDF file", defaultDir=os.getcwd(), wildcard="nc files (*.nc)|*.nc", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if saveFileDialog.ShowModal() == wx.ID_CANCEL:
            return
        output_path = saveFileDialog.GetPath()

        # remove file if it already exists
        os.remove(output_path) if os.path.exists(output_path) else None

        # get the input data file and create the empty output file
        dsin = nc.Dataset(url)
        dsout = nc.Dataset(output_path, 'w')

        # write all dimensions to the output file
        for dname, the_dim in dsin.dimensions.iteritems():
            dsout.createDimension(dname, len(the_dim) if not the_dim.isunlimited() else None)

        # write all the variables to the output file
        for v_name, varin in dsin.variables.iteritems():

            # create the variable
            outVar = dsout.createVariable(v_name, varin.datatype, varin.dimensions)

            # copy variable attributes
            outVar.setncatts({k: varin.getncattr(k) for k in varin.ncattrs()})

            # copy variable data
            outVar[:] = varin[:]

        # close the input and output files
        dsin.close()
        dsout.close()

    def enableBtns(self, event):
        self.view_btn.Enable()
        self.download_btn.Enable()

    def getSelectedIndexRow(self):
        return self.variable_list.GetFirstSelected()
    
    def getListCtrlColumnByName(self, name):
        """
        Gets the list control column index by search for column name
        :param name: name of the column to search for
        :return: index of the column, -1 of none is found
        """

        # get the list control columns
        cols = [col_name.upper() for col_name in self.list_ctrl_columns]
        search_name = name.upper()
        i = 0
        for col in cols:
            if col == search_name:
                return i
            i += 1
        return -1

    def getSelectedURL(self):
        #  Returns -1 if none is selected
        index = self.getSelectedIndexRow()
        if index >= 0:
            return self.TableValues[index][3]
        return -1

    def getSelectedFileName(self):
        #  Returns -1 if none is selected
        index = self.getSelectedIndexRow()
        if index >= 0:
            return self.TableValues[index][0]
        return -1

    def onView(self, event):
        filename = self.getSelectedFileName()
        url = self.getSelectedURL()
        NetcdfDetailsCtrl(self, url, filename)

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

    def RunCrawler(self, event):
        #self.status_bar.SetStatusText("Loading")
        self.update_statusbar(self.status_bar, 'loading...')
        self.Enable(False)
        if self.variable_list.GetItemCount() > 0:
            self.clearData()
        results = []
        url = self.url_textbox.GetLineText(0)
        is_valid = self.check_url(url + "/catalog.xml")

        if is_valid:
            results = self.crawler(url + "/catalog.xml", results)
            self.TableValues = []
            for ds in results:
                # cElementTree.tostring(catalog, 'utf-8')

                dap = ds.find('.//{%s}access[@serviceName="dap"]' % self.thredds)
                if dap is not None:
                    wms = ds.find('.//{%s}access[@serviceName="wms"]' % self.thredds)
                    size = ds.find('.//{%s}dataSize' % self.thredds)
                    date = ds.find('.//{%s}date' % self.thredds)

                    fileSize = size.itertext().next()
                    lastmodified = date.itertext().next()
                    dap_url = dict(dap.items())['urlPath']
                    wms_url = dict(wms.items())['urlPath']
                    name = dict(ds.items())['name']
                    mod = lastmodified.replace("T", " ")
                    fileString = self.CalculateBytes(int(fileSize))
                    self.TableValues.append([name, fileString, mod, url + dap_url])


            #self.status_bar.SetStatusText("Almost done...")
            self.update_statusbar(self.status_bar, 'almost done...')
            self.updateFileList(self.TableValues)
            self.update_statusbar(self.status_bar, 'done')
        
            self.alternateRowColor()
            self.autoSizeColumns()
            self.Enable(True)
            #self.status_bar.SetStatusText("Done!")
        else:
            self.update_statusbar(self.status_bar, 'error connecting to the server')

    def updateFileList(self, data):
        rowNumber = 0
        colNumber = 0

        for x in data:
            pos = self.variable_list.InsertStringItem(rowNumber, "test")
            for y in x:
                self.variable_list.SetStringItem(pos, colNumber, str(y))
                colNumber += 1
            colNumber = 0
            rowNumber += 1

    def update_statusbar(self, status_bar, text):
        status_bar.SetStatusText(text)
        wx.Yield()

    def handle_crawler(self):
        # self.update_statusbar(self.status_bar, "its running")
        # for i in range(0, 100000000):
        #     pass
        #
        # print 123
        # self.update_statusbar(self.status_bar, "Done")

        self.update_statusbar(self.status_bar, "Loading...")

        if self.variable_list.GetItemCount > 0:
            self.clearData()
        results = []
        url = self.url_textbox.GetLineText(0)
        is_valid = self.check_url(url + "/catalog.xml")

        if is_valid:
            results = self.crawler(url + "/catalog.xml", results)
            self.TableValues = []
            for ds in results:
                dap = ds.find('.//{%s}access[@serviceName="dap"]' % self.thredds)
                if dap is not None:
                    wms = ds.find('.//{%s}access[@serviceName="wms"]' % self.thredds)
                    size = ds.find('.//{%s}dataSize' % self.thredds)
                    date = ds.find('.//{%s}date' % self.thredds)

                    fileSize = size.itertext().next()
                    lastmodified = date.itertext().next()
                    dap_url = dict(dap.items())['urlPath']
                    name = dict(ds.items())['name']
                    mod = lastmodified.replace("T", " ")
                    fileString = self.CalculateBytes(int(fileSize))
                    self.TableValues.append([name, fileString, mod, url + dap_url])

            self.update_statusbar(self.status_bar, 'Almost done...')
            self.updateFileList(self.TableValues)
            self.update_statusbar(self.status_bar, 'Done')

            self.alternateRowColor()
            self.autoSizeColumns()
            self.enableBtns(None)
            # self.status_bar.SetStatusText("Done!")
        else:
            self.update_statusbar(self.status_bar, 'error connecting to the server')

    ##################################
    # EVENTS
    ##################################

    def on_get_crawler(self, event):
        if not isinstance(self.thread, threading.Thread):
            sPrint("NetcdfCtrl.thread must be threading.Thread", messageType=MessageType.DEBUG)
            return

        if self.thread.isAlive():
            sPrint("NetcdfCtrl.thread is alive", messageType=MessageType.DEBUG)
            sPrint("Working on getting data", messageType=MessageType.INFO)
            return

        self.thread = threading.Thread(target=self.handle_crawler)
        self.thread.start()  # Do not call thread.join


