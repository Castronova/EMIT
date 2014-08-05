__author__ = 'Mario'

import wx
from collections import OrderedDict
from ObjectListView import FastObjectListView, ColumnDefn
from frmMatPlotLib import MatplotFrame
import os
from wx.lib.pubsub import pub as Publisher

########################################################################
class Database(object):
    """
    Model of the Book object

    Contains the following attributes:
    'ISBN', 'Author', 'Manufacturer', 'Title'
    """
    #----------------------------------------------------------------------
    def __init__(self, resultid, sitename, sitecode, varname, varunit, timeunit, begintime, endtime):
        self.resultid = resultid
        self.sitename = sitename
        self.sitecode = sitecode
        self.variablename = varname
        self.variableunit = varunit
        self.Time = timeunit
        self.begintime = begintime
        self.endtime = endtime


########################################################################
class OlvSeries(FastObjectListView):
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs ):
        FastObjectListView.__init__(self, *args, **kwargs)
        # self.products = [Database("1","Main Lake1", "19",
        #                           "Chlorophyll a", "micrograms per liter",
        #                           "day", "1992-05-07 11:45:00", "1996-01-02 00:00:00"),
        #                  ]

        self.products = [Database("","", "",
                                  "", "",
                                  "", "", ""),
                         ]


        self.setBooks()
        # self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)

        # Allow the cell values to be edited when double-clicked
        # self.cellEditMode = FastObjectListView.CELLEDIT_SINGLECLICK

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDoubleClick)




    #----------------------------------------------------------------------
    def setBooks(self, data=None):
        keys = ["ResultID","Sitename", "Sitecode", "VariableName", "VariableUnit", "Time",
                  "BeginDateTime", "EndDateTime"]

        values = ["resultid","sitename", "sitecode", "variablename", "variableunit", "Time", "begintime", "endtime"]

        seriesColumns = [ ColumnDefn(key, align = "left", minimumWidth=100, valueGetter=value)
                            for key, value in OrderedDict(zip(keys, values)).iteritems()]

        self.SetColumns(seriesColumns)

        self.SetObjects(self.products)

    def onDrag(self, event):
        data = wx.FileDataObject()
        obj = event.GetEventObject()
        id = event.GetIndex()

        resultID = obj.GetItem(id,0).GetText()

        #x,y = self.getData(resultID)

        filename = obj.GetItem(id).GetText()
        dataname = str(filename)

        data.AddFile(dataname)

        dropSource = wx.DropSource(obj)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop()
        print filename

    def onDoubleClick(self, event):

        # get row associated with the event
        data = wx.FileDataObject()
        obj = event.GetEventObject()
        id = event.GetIndex()
        resultID = obj.GetItem(id,0).GetText()

        # get data for this row
        x,y, resobj = self.getData(resultID)

        # get metadata
        xlabel = '%s, [%s]' % (resobj.UnitObj.UnitsName, resobj.UnitObj.UnitsAbbreviation)
        title = '%s' % (resobj.VariableObj.VariableCode)

        # plot the data
        PlotFrame = MatplotFrame(self.Parent, x, y, title, xlabel)
        PlotFrame.Show()

    def getDbSession(self):
        selected_db = self.Parent.m_choice3.GetStringSelection()
        for key, db in self.Parent._databases.iteritems():
            # get the database session associated with the selected name
            if db['name'] == selected_db:
                return db['session']
        return None

    def getData(self,resultID):

        from ODM2.Results.services import readResults
        session = self.getDbSession()
        readres = readResults(session)
        results = readres.getTimeSeriesValuesByResultId(resultId=int(resultID))

        from ODM2.Core.services import readCore
        core = readCore(session)
        obj = core.getResultByID(resultID=int(resultID))

        dates = []
        values = []
        for val in results:
            dates.append(val.ValueDateTime)
            values.append(val.DataValue)

        return dates,values,obj



########################################################################
###                      For Unittest Use                            ###
########################################################################
class MainFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title="ObjectListView Demo", size=(800,600))
        panel = OlvSeries(self)

########################################################################
class GenApp(wx.App):

    #----------------------------------------------------------------------
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)

    #----------------------------------------------------------------------
    def OnInit(self):
        # create frame here
        frame = MainFrame()
        frame.Show()
        return True

#----------------------------------------------------------------------
def main():
    """
    Run the demo
    """
    app = GenApp()
    app.MainLoop()

if __name__ == "__main__":
    main()