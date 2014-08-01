__author__ = 'Mario'

import wx
from ObjectListView import ObjectListView, ColumnDefn

########################################################################
class Database(object):
    """
    Model of the Book object

    Contains the following attributes:
    'ISBN', 'Author', 'Manufacturer', 'Title'
    """
    #----------------------------------------------------------------------
    def __init__(self, timeunit, varname, varunit, sitecode, sitename, begintime, endtime):
        self.sitename = sitename
        self.sitecode = sitecode
        self.variablename = varname
        self.variableunit = varunit
        self.Time = timeunit
        self.begintime = begintime
        self.endtime = endtime


########################################################################
class MainPanel(wx.Panel):
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.products = [Database("Main Lake1", "19",
                                  "Chlorophyll a", "micrograms per liter",
                                  "day", "1992-05-07 11:45:00", "1996-01-02 00:00:00"),
                         ]

        self.dataOlv = ObjectListView(self, wx.ID_ANY, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.setBooks()

        # Allow the cell values to be edited when double-clicked
        self.dataOlv.cellEditMode = ObjectListView.CELLEDIT_SINGLECLICK

        # create an update button
        # updateBtn = wx.Button(self, wx.ID_ANY, "Update OLV")
        # updateBtn.Bind(wx.EVT_BUTTON, self.updateControl)

        # Create some sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        mainSizer.Add(self.dataOlv, 1, wx.ALL|wx.EXPAND, 5)
        # mainSizer.Add(updateBtn, 0, wx.ALL|wx.CENTER, 5)
        self.SetSizer(mainSizer)

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
        self.dataOlv.SetColumns([
            ColumnDefn("Sitename", "left", 180, "sitename"),
            ColumnDefn("Sitecode", "left", 180, "sitecode"),
            ColumnDefn("VariableName", "left", 220, "variablename"),
            ColumnDefn("VariableUnit", "right", 100, "variablename"),
            ColumnDefn("Time", "left", 180, "Time"),
            ColumnDefn("BeginDateTime", "left", 180, "begintime"),
            ColumnDefn("EndDateTime", "left", 180, "endtime")
        ])

        self.dataOlv.SetObjects(self.products)

########################################################################
#For Unittest Use
########################################################################
class MainFrame(wx.Frame):
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, parent=None, id=wx.ID_ANY,
                          title="ObjectListView Demo", size=(800,600))
        panel = MainPanel(self)

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