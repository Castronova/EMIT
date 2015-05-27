__author__ = 'tonycastronova'

import wx
from wx.lib.pubsub import pub as Publisher
from gui.views.viewDatabase import ViewDatabase
from utilities import db as dbutils

from ..ObjectListView import ColumnDefn


class LogicDatabase(ViewDatabase):
    def __init__(self, *args, **kwargs):

        ViewDatabase.__init__(self, *args, **kwargs)

        # initialize globals
        self.__list_obj = None
        self.__list_id = None
        self.__context_menu = None

        # self.Bind(wx.EVT_LIST_BEGIN_DRAG, self.onDrag)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.onDoubleClick)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.LaunchContext)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelect)

        Publisher.subscribe(self.olvrefresh, "olvrefresh")


    def DefineColumns(self, cols):
        """
            Define the columns that will be displayed in the Object List View control
        :param cols: a list of column names
        :return: None
        """

        variable_names = [col.lower().replace(' ', '_') for col in cols]

        seriesColumns = [ColumnDefn(col, align="left", minimumWidth=150, valueGetter=col.lower().replace(' ', '_'))
                         for col in cols]

        self.SetColumns(seriesColumns)

        d = {key: value for (key, value) in zip(variable_names, ["" for c in variable_names])}
        record_object = type('DataRecord', (object,), d)

        initialSeries = [record_object]

        self.SetObjects(initialSeries)
        # self.SetColumnWidth(6, 2000)

    def LaunchContext(self, event):

        if self.__context_menu is not None:
            self.__context_menu.Selected(event.GetEventObject(), event.GetIndex())
            self.PopupMenu(self.__context_menu, event.GetPosition())

    def setContextMenu(self, value):
        self.__context_menu = value

    def OnListItemSelect(self, event):

        self.__list_obj = event.GetEventObject()
        self.__list_id = event.GetIndex()

    def onDoubleClick(self, event):
        id = event.GetIndex()
        obj = event.GetEventObject()
        filename = obj.GetItem(id).GetText()
        uniqueId = obj.GetItem(id).GetText()
        Publisher.sendMessage('AddModel', filepath=filename, x=0, y=0, uniqueId=uniqueId)  # sends message to LogicCanvas.addModel

    def getDbSession(self):
        selected_db = self.Parent.connection_combobox.GetStringSelection()
        for key, db in self.Parent._databases.iteritems():
            # get the database session associated with the selected name
            if db['name'] == selected_db:
                session = dbutils.build_session_from_connection_string(db['connection_string'])
                return session

                # return db['session']
        return None

    def olvrefresh(self):
        self.RepopulateList()
        self.AutoSizeColumns()
        self.Refresh()
