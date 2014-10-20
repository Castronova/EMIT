__author__ = 'Mario'

import wx
from collections import OrderedDict
from ObjectListView import FastObjectListView, ColumnDefn
from ObjectListView import ObjectListView as OLV
from frmMatPlotLib import MatplotFrame
import os
from wx.lib.pubsub import pub as Publisher
from api.ODM2.Results.services import readResults
from api.ODM2.Core.services import readCore
from wx.lib.pubsub import pub as Publisher

########################################################################
class Database(object):
    """
    Model of the Book object

    Contains the following attributes:
    'ISBN', 'Author', 'Manufacturer', 'Title'
    """
    #----------------------------------------------------------------------
    def __init__(self, resultid, featurecode, variable, unit, data_type, org, date_created):
        self.resultid = resultid
        self.featurecode = featurecode
        self.variable = variable
        self.unit = unit
        self.data_type = data_type
        self.org = org
        self.date_created = date_created


########################################################################
class OlvSeries(FastObjectListView):
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs ):
        FastObjectListView.__init__(self, *args, **kwargs)

        self.initialSeries = [Database("","", "",
                                  "", "",
                                  "", ""),
                         ]

        Publisher.subscribe(self.olvrefresh, "olvrefresh")

        self.setSeries()
        self.useAlternateBackColors = True
        self.oddRowsBackColor = wx.Colour(191, 217, 217)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)
        #self.Bind(wx.EVT_LEFT_DCLICK, self.onDoubleClick)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.LaunchContext)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelect)

        self.__list_obj = None
        self.__list_id = None


        # subscribers
        Publisher.subscribe(self.PlotData,'PlotData')

    #----------------------------------------------------------------------
    def setSeries(self, data=None):
        # keys = ["ResultID","Sitename", "Sitecode", "VariableName", "VariableUnit", "Time",
        #           "BeginDateTime", "EndDateTime"]
        #
        # values = ["resultid","sitename", "sitecode", "variablename", "variableunit", "Time", "begintime", "endtime"]
        #

        keys = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
        values = ["resultid", "featurecode", "variable", "unit", "data_type", "org", "date_created"]
        seriesColumns = [ ColumnDefn(key, align = "left", minimumWidth=150, valueGetter=value)
                            for key, value in OrderedDict(zip(keys, values)).iteritems()]

        self.SetColumns(seriesColumns)

        self.SetObjects(self.initialSeries)

    def LaunchContext(self, event):


        self.PopupMenu(ContextMenu(self,
                                   list_obj=event.GetEventObject(),
                                   list_id=event.GetIndex()), event.GetPosition())

    def OnListItemSelect(self, event):

        self.__list_obj = event.GetEventObject()
        self.__list_id = event.GetIndex()

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


    def PlotData(self, obj, id):

        # get row associated with the event
        #data = wx.FileDataObject()
        #obj = self.__list_obj
        #id = self.__list_id
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
        selected_db = self.Parent.connection_combobox.GetStringSelection()
        for key, db in self.Parent._databases.iteritems():
            # get the database session associated with the selected name
            if db['name'] == selected_db:
                return db['session']
        return None

    def getData(self,resultID):


        session = self.getDbSession()
        readres = readResults(session)
        results = readres.getTimeSeriesValuesByResultId(resultId=int(resultID))


        core = readCore(session)
        obj = core.getResultByID(resultID=int(resultID))

        dates = []
        values = []
        for val in results:
            dates.append(val.ValueDateTime)
            values.append(val.DataValue)

        #session.close()

        return dates,values,obj

    def olvrefresh(self):
        self.RepopulateList()
        self.Refresh()
        #print "Series Selector Refreshed"


class ContextMenu(wx.Menu):

    def __init__(self, parent, list_obj, list_id):
        super(ContextMenu, self).__init__()

        #self.cmd = parent.cmd
        self.parent = parent

        # mmi = wx.MenuItem(self, wx.NewId(), 'Add Model')
        # self.AppendItem(mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Add')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAdd, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Plot')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnPlot, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Delete')
        self.AppendItem(mmi)
        #self.Bind(wx.EVT_MENU, self.OnClickClear, mmi)

        # this is the list event from the right click
        self.__list_obj = list_obj
        self.__list_id = list_id

    def OnAdd(self, event):

        obj = self.__list_obj
        id = self.__list_id
        filename = obj.GetItem(id).GetText()

        Publisher.sendMessage('AddModel',filepath=filename, x = 0, y = 0) # sends message to CanvasController

        print filename



    def OnPlot(self, event):

        obj = self.__list_obj
        id = self.__list_id

        Publisher.sendMessage('PlotData',obj=obj, id=id) # sends message to ObjectListView PlotData function



        #self.parent.run()
    #
    # def OnClickClear(self, e):
    #     dlg = wx.MessageDialog(None, 'Are you sure you would like to clear configuration?', 'Question', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)
    #
    #     if dlg.ShowModal() !=wx.ID_NO:
    #         self.parent.clear()
    #
    #     # elif dlg.ShowModal() !=wx.ID_NO:
    #     #     self.parent.clear()
    #
    # def SaveConfiguration(self,e):
    #
    #     save = wx.FileDialog(self.parent.Canvas.GetTopLevelParent(), "Save Configuration","","",
    #                          "Simulation Files (*.sim)|*.sim", wx.FD_SAVE  | wx.FD_OVERWRITE_PROMPT)
    #
    #     if save.ShowModal() != wx.ID_OK:
    #         path = save.GetPath()
    #         self.parent.SaveSimulation(path)
    #
    # def OnMinimize(self, e):
    #     self.parent.Iconize()
    #
    # def OnClose(self, e):
    #     self.parent.Close()
    #
    # def Warn(parent, message, caption = 'Warning!'):
    #     dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
    #     dlg.ShowModal()
    #     dlg.Destroy()

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