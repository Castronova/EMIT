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

class DataRecord():

    def __init__(self,name_value_tuple_list):
        """
            e.g. [(resultid,10),(date,11/7/14)]
        """
        # for n in dir():
        #     if n[0]!='_' and n != 'self' and n != 'name_value_tuple_list':
        #         delattr(DataRecord, n)

        for var, val in name_value_tuple_list:
            setattr(DataRecord, var, val)

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

        #self.setSeries()
        self.useAlternateBackColors = True
        self.oddRowsBackColor = wx.Colour(191, 217, 217)
        self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDoubleClick)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.LaunchContext)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelect)

        self.__list_obj = None
        self.__list_id = None

        self.__context_menu = None
        # subscribers
        # Publisher.subscribe(self.PlotData,'PlotData')

    #----------------------------------------------------------------------
    # def setSeries(self, data=None):
    #     # keys = ["ResultID","Sitename", "Sitecode", "VariableName", "VariableUnit", "Time",
    #     #           "BeginDateTime", "EndDateTime"]
    #     #
    #     # values = ["resultid","sitename", "sitecode", "variablename", "variableunit", "Time", "begintime", "endtime"]
    #     #
    #
    #     keys = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]
    #     values = ["resultid", "featurecode", "variable", "unit", "data_type", "org", "date_created"]
    #     seriesColumns = [ ColumnDefn(key, align = "left", minimumWidth=150, valueGetter=value)
    #                         for key, value in OrderedDict(zip(keys, values)).iteritems()]
    #
    #     self.SetColumns(seriesColumns)
    #
    #     self.SetObjects(self.initialSeries)

    def DefineColumns(self, cols):

        #cols = ["ResultID", "FeatureCode", "Variable", "Unit", "Type", "Organization", "Date Created"]

        variable_names = [col.lower().replace(' ','_') for col in cols]

        seriesColumns = [ ColumnDefn(col, align = "left", minimumWidth=150, valueGetter=col.lower().replace(' ','_'))
                            for col in cols]


        self.SetColumns(seriesColumns)

        initial_values  = ["" for col in cols]

        d = {key: value for (key, value) in zip(variable_names,["" for c in variable_names])}
        record_object = type('DataRecord', (object,), d)

        self.initialSeries = [record_object]

        self.SetObjects(self.initialSeries)


    def LaunchContext(self, event):

        if self.__context_menu is not None:
            self.__context_menu.Selected(event.GetEventObject(), event.GetIndex())
            self.PopupMenu(self.__context_menu, event.GetPosition())
            # self.PopupMenu(ContextMenu(self,
            #                            list_obj=event.GetEventObject(),
            #                            list_id=event.GetIndex()), event.GetPosition())

    def setContextMenu(self, value):
        self.__context_menu = value

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

    def onDoubleClick(self, event):
        id = event.GetIndex()
        obj = event.GetEventObject()
        filename = obj.GetItem(id).GetText()

        Publisher.sendMessage('AddModel',filepath=filename, x = 0, y = 0) # sends message to CanvasController

    def getDbSession(self):
        selected_db = self.Parent.connection_combobox.GetStringSelection()
        for key, db in self.Parent._databases.iteritems():
            # get the database session associated with the selected name
            if db['name'] == selected_db:
                return db['session']
        return None

    def olvrefresh(self):
        self.RepopulateList()
        self.Refresh()


class ContextMenu(wx.Menu):

    def __init__(self, parent):
        super(ContextMenu, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Add')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAdd, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Plot')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnPlot, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Delete')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnDelete, mmi)

        # this is the list event from the right click
        self.__list_obj = None
        self.__list_id = None

    def Selected(self, list_obj=None, list_id=None):
        if list_id is not None and list_obj is not None:
            self.__list_obj = list_obj
            self.__list_id = list_id
        return self.__list_obj, self.__list_id




    def OnAdd(self, event):

        obj = self.__list_obj
        id = self.__list_id
        filename = obj.GetItem(id).GetText()

        Publisher.sendMessage('AddModel',filepath=filename, x = 0, y = 0) # sends message to CanvasController

        #print filename

    def getData(self,resultID):



        session = self.parent.getDbSession()
        if session is not None:
            readres = readResults(session)
            results = readres.getTimeSeriesValuesByResultId(resultId=int(resultID))


            core = readCore(session)
            obj = core.getResultByID(resultID=int(resultID))

            dates = []
            values = []
            for val in results:
                dates.append(val.ValueDateTime)
                values.append(val.DataValue)

            return dates,values,obj

    def OnPlot(self, event):

        obj = self.__list_obj

        # create a plot frame
        PlotFrame = None
        xlabel = None
        title = None
        variable = None
        units = None
        warning = None
        x_series = []
        y_series = []
        labels = []
        id = self.parent.GetFirstSelected()
        while id != -1:
            # get the result
            resultID = obj.GetItem(id,0).GetText()

            # get data for this row
            x,y, resobj = self.getData(resultID)

            if PlotFrame is None:
                # set metadata based on first series
                xlabel = '%s, [%s]' % (resobj.UnitObj.UnitsName, resobj.UnitObj.UnitsAbbreviation)
                title = '%s' % (resobj.VariableObj.VariableCode)

                # save the variable and units to validate future time series
                variable = resobj.VariableObj.VariableCode
                units = resobj.UnitObj.UnitsName

                PlotFrame = MatplotFrame(self.Parent, title, ylabel=xlabel)

            if resobj.VariableObj.VariableCode == variable and resobj.UnitObj.UnitsName == units:
                # store the x and Y data
                x_series.append(x)
                y_series.append(y)
                labels.append(resultID)

                # PlotFrame.add_series(x,y)
            elif warning is None:
                warning = 'Multiple Variables/Units were selected.  I currently don\'t support plotting heterogeneous time series. ' +\
                          'Some of the selected time series will not be shown :( '

            # get the next selected item
            id = obj.GetNextSelected(id)

        if warning:
            dlg = wx.MessageDialog(self.parent, warning, '', wx.OK | wx.ICON_WARNING)
            dlg.ShowModal()
            dlg.Destroy()

        # plot the data
        PlotFrame.plot(xlist=x_series, ylist=y_series, labels=labels)
        PlotFrame.Show()

    def OnDelete(self,event):
        dlg = wx.MessageDialog(self.parent, 'Unfortunately, delete has not been implemented yet.', '', wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

