__author__ = 'francisco'

import WebServiceApi as wsapi
import wx
import wx.grid

import test_ODM1


class GridFrame(wx.Frame):

    def __init__(self, parent):
        self.odm1 = test_ODM1.ODM1()

        self.WebAPI = wsapi.WebServiceApi()
        wx.Frame.__init__(self, parent)
        self.SetSize(wx.Size(900, 500))

        self.grid = wx.grid.Grid(self, -1)
        self.populateGridWithVariables("RB_KF_C")
        # self.populateGridWithSiteName()


        # self.grid.CreateGrid(100, 3)  # 20 rows and 3 columns


        self.Show()


    def populateGridWithSiteName(self):
        '''
            WebServiceApi is used to interface.

        xml = self.odm1.getSites()
        self.odm1.createXMLFileForReading(xml)
        data = self.odm1.parseXML2Dict(xml)
        '''

        data = self.WebAPI.buildSitesDictionary()

        self.grid.CreateGrid(len(data) + 1, 3)

        self.grid.SetCellValue(0, 0, 'Site Name')
        self.grid.SetCellValue(0, 1, "Site ID/Code")
        self.grid.SetCellValue(0, 2, "Variable ID/Code")
        # self.WebAPI.buildAllSiteCodeVariables("RB_KF_C")

        #'''
        row, col = 1, 0

        for key, value in data.iteritems():
            self.grid.SetCellValue(row, col, key + " #siteID" )#+ value[1][0][0])
            self.grid.SetCellValue(row, 1, value)
            #self.grid.SetCellValue(row, col, key + " #" + value[1].items()[0][0])
            #self.grid.SetCellValue(row, 1, value[1].text)

            row += 1

        row = 1
        '''
        xml = self.odm1.getVariables()
        self.odm1.createXMLFileForReading(xml)
        vars = self.odm1.parseXML2Dict(xml, 0, 17)
        #vars = iter(vars)  # Skip the first item because it is None.
        #next(vars)

        '''
        vars = self.WebAPI.buildAllVariableDictionary(0, 18)

        for key in vars:
            self.grid.SetCellValue(row, 2, str(key))
            row += 1

        self.grid.AutoSize()

    def populateGridWithVariables(self, sitecode):
        data = self.WebAPI.buildAllSiteCodeVariables(sitecode)

        self.grid.CreateGrid(len(data) + 1, 3)

        self.grid.SetCellValue(0, 0, 'Site Name')
        self.grid.SetCellValue(0, 1, "Value")
        self.grid.SetCellValue(0, 2, "Variables")

        row = 1

        for key, value, in data.iteritems():
            self.grid.SetCellValue(row, 1, str(key))
            self.grid.SetCellValue(row, 2, str(value))
            row += 1
        self.grid.AutoSize()
        pass


if __name__ == '__main__':

    app = wx.App(0)
    frame = GridFrame(None)
    app.MainLoop()
