__author__ = 'Mario'

import wx
from collections import OrderedDict
from ObjectListView import FastObjectListView, ColumnDefn

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

        self.dataOlv = FastObjectListView(self, )
        self.setBooks()

        # Allow the cell values to be edited when double-clicked
        self.dataOlv.cellEditMode = FastObjectListView.CELLEDIT_SINGLECLICK



    #----------------------------------------------------------------------
    def updateControl(self, event):
        """

        """
        print "updating..."
        product_dict = [{"varname":"Core Python Programming", "Value":"Wesley Chun",
                         "varunit":"0132269937", "time":"Prentice Hall"},
                        {"title":"Python Programming for the Absolute Beginner",
                         "author":"Michael Dawson", "isbn":"1598631128",
                         "mfg":"Course Technology"},
                        {"title":"Learning Python", "author":"Mark Lutz",
                         "isbn":"0596513984", "mfg":"O'Reilly"}
        ]
        data = self.products + product_dict
        self.dataOlv.SetObjects(data)

    #----------------------------------------------------------------------
    def setBooks(self, data=None):
        keys = ["Sitename", "Sitecode", "VariableName", "VariableUnit", "Time",
                  "BeginDateTime", "EndDateTime"]

        values = ["sitename", "sitecode", "variablename", "variableunit", "Time", "begintime", "endtime"]

        seriesColumns = [ ColumnDefn(key, align = "left", minimumWidth=-1, valueGetter=value)
                            for key, value in OrderedDict(zip(keys, values)).iteritems()]

        self.dataOlv.SetColumns(seriesColumns)

        self.dataOlv.SetObjects(self.products)

########################################################################
#For Unittest Use
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