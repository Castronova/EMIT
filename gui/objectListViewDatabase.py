__author__ = 'Mario'

import wx
from collections import OrderedDict
from ObjectListView import FastObjectListView, ColumnDefn
import os

########################################################################
class Database(object):
    """
    Model of the Book object

    Contains the following attributes:
    'ISBN', 'Author', 'Manufacturer', 'Title'
    """
    #----------------------------------------------------------------------
    def __init__(self, sitename, sitecode, varname, varunit, timeunit, begintime, endtime):
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
        self.products = [Database("Main Lake1", "19",
                                  "Chlorophyll a", "micrograms per liter",
                                  "day", "1992-05-07 11:45:00", "1996-01-02 00:00:00"),
                         ]

        self.setBooks()
        # self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)

        # Allow the cell values to be edited when double-clicked
        self.cellEditMode = FastObjectListView.CELLEDIT_SINGLECLICK




    #----------------------------------------------------------------------
    def setBooks(self, data=None):
        keys = ["Sitename", "Sitecode", "VariableName", "VariableUnit", "Time",
                  "BeginDateTime", "EndDateTime"]

        values = ["sitename", "sitecode", "variablename", "variableunit", "Time", "begintime", "endtime"]

        seriesColumns = [ ColumnDefn(key, align = "left", minimumWidth=100, valueGetter=value)
                            for key, value in OrderedDict(zip(keys, values)).iteritems()]

        self.SetColumns(seriesColumns)

        self.SetObjects(self.products)

    def onDrag(self, event):
        data = wx.FileDataObject()
        obj = event.GetEventObject()
        id = event.GetIndex()
        filename = obj.GetItem(id).GetText()
        dataname = str(filename)

        data.AddFile(dataname)

        dropSource = wx.DropSource(obj)
        dropSource.SetData(data)
        result = dropSource.DoDragDrop()
        print filename


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