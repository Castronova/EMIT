__author__ = 'francisco'

from gui.views.NetcdfViewer import NetcdfViewer
import os
import wx
from xml.etree import cElementTree
from urlparse import urljoin
import requests
import httplib
import urlparse
import urllib
from gui.controller.NetcdfDetailsCtrl import NetcdfDetailsCtrl
from gui.views.NetcdfDetailsView import NetcdfDetailsView
import netCDF4 as nc

class NetcdfCtrl(NetcdfViewer):

    def __init__(self, parent):  # What parameters does this need?
        # namespaces for XML parsing
        self.thredds = "http://www.unidata.ucar.edu/namespaces/thredds/InvCatalog/v1.0"
        self.xlink = "http://www.w3.org/1999/xlink"
        NetcdfViewer.__init__(self, parent=parent)
        self.Bind(wx.EVT_BUTTON, self.downloadFile, self.download_btn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, self.add_to_canvas_btn)
        self.Bind(wx.EVT_BUTTON, self.RunCrawler, self.get_btn)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.enableBtns)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.disableBtns)
        self.disableBtns(None)


    def addToCanvas(self, event):
        item = self.getSelectedInformation()
        # this will get the url we want
        url = self.TableValues[item][3]
        filename = self.TableValues[item][0]
        NetcdfDetailsCtrl(self, url, filename)

    def autoSizeColumns(self):
        for i in range(self.variable_list.GetColumnCount()):
            self.variable_list.SetColumnWidth(i, wx.LIST_AUTOSIZE)

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
        self.add_to_canvas_btn.Disable()
        self.download_btn.Disable()

    def downloadFile(self, event):

        # get the file url by rowid and colid
        rowid = self.getSelectedInformation()
        colid = self.getListCtrlColumnByName('url')
        url = self.TableValues[rowid][colid]

        # open a dialog to get save path
        saveFileDialog = wx.FileDialog(self, "Save NetCDF file", "", "", "nc files (*.nc)|*.nc", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
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
        self.add_to_canvas_btn.Enable()
        self.download_btn.Enable()

    def getSelectedInformation(self):
        num = self.variable_list.GetItemCount()
        for i in range(num):
            if self.variable_list.IsSelected(i):
                v_name = self.variable_list.GetItemText(1)
                return i
    
    def update_statusbar(self, status_bar, text):
        status_bar.SetStatusText(text);
        wx.Yield()

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
                    self.TableValues.append([name, fileSize, mod, url + dap_url])


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