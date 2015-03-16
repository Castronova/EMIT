__author__ = 'Mario'

import wx
from wx.lib.pubsub import pub as Publisher

from ObjectListView import FastObjectListView, ColumnDefn


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


