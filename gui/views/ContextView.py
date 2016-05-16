import csv
import time
import wx
from wx.lib.pubsub import pub as Publisher
import coordinator.engineAccessors as engine
from api_old.ODM2.Core.services import readCore
from api_old.ODM2.Results.services import readResults
from api_old.ODM2.Simulation.services import readSimulation
from emitLogging import elog
from gui import events
from gui.controller.ModelCtrl import ModelCtrl
from gui.controller.PreRunCtrl import PreRunCtrl
from sprint import *

__author__ = 'tonycastronova'


# todo:  this needs to be split up into view and logic code
class LinkContextMenu(wx.Menu):
    def __init__(self, parent, e):
        super(LinkContextMenu, self).__init__()

        self.arrow_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveLink, mmi)

    def RemoveLink(self, e):
        self.parent.remove_link(self.arrow_obj)


class ConsoleContextMenu(wx.Menu):
    """
    Context menu for when a user does a right click in the ConsoleOutput
    """

    def __init__(self, parent, event):
        wx.Menu.__init__(self)
        self.log = parent.log
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Clear Console')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClear, mmi)

    def OnClear(self, event):
        """
        User clears the gui console
        """
        self.log.Clear()
        self.parent.resetLineNumbers()


class ModelContextMenu(wx.Menu):
    def __init__(self, parent, e):
        super(ModelContextMenu, self).__init__()

        self.model_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.ShowModelDetails, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveModel, mmi)

    def ShowModelDetails(self, e):

        # create a frame to bind the details page to
        f = wx.Frame(self.GetParent())

        kwargs = {'edit': False, 'spatial': True}
        model_details = ModelCtrl(f, model_id=self.model_obj.ID, **kwargs)

        atts = engine.getModelById(self.model_obj.ID)['attrib']
        if 'mdl' in atts.keys():
            model_details.PopulateSummary(atts['mdl'])

        else:  # This means the model is coming from a database.
            oei = model_details.spatial_page.controller.get_output_exchange_item_by_id(self.model_obj.ID)
            iei = model_details.spatial_page.controller.get_input_exchange_item_by_id(self.model_obj.ID)
            model_details.PopulateProperties(engine.getModelById(self.model_obj.ID), iei=iei, oei=oei)

        model_details.Show()

    def RemoveModel(self, e):
        self.parent.RemoveModel(self.model_obj)


class ToolboxContextMenu(wx.Menu):
    def __init__(self, parent, e, removable, folder):
        super(ToolboxContextMenu, self).__init__()

        self.arrow_obj = e
        self.parent = parent
        if not folder:
            mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
            self.AppendItem(mmi)
            self.Bind(wx.EVT_MENU, self.OnViewDetails, mmi)

        if removable:
            # mr stands for menu remove
            mr = wx.MenuItem(self, wx.NewId(), 'Remove')
            self.AppendItem(mr)
            self.Bind(wx.EVT_MENU, self.OnRemove, mr)

    def OnViewDetails(self, e):
        self.parent.ShowDetails()

    def OnExpandAll(self, e):
        self.parent.OnExpandAll()

    def OnCollapseAll(self, e):
        self.parent.OnCollapseAll()

    def OnRemove(self, e):
        self.parent.Remove(e)


class ContextMenu(wx.Menu):
    def __init__(self, parent):
        super(ContextMenu, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Add')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAdd, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'View')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.on_view, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Delete')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnDelete, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Export')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.onExport, mmi)

        # this is the list event from the right click
        self.__list_obj = None
        self.__list_id = None

    def onExport(self, event):
        #  User will choose where to save the csv file
        save = wx.FileDialog(self.parent.GetTopLevelParent(), message="Choose Path",
                             wildcard="CSV Files (*.csv)|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save.ShowModal() == wx.ID_OK:
            path = save.GetPath()
            if path[-4] != '.':
                path += '.csv'
            file = open(path, 'w')
            #
            writer = csv.writer(file, delimiter=',')

            obj = self.__list_obj
            id = self.parent.GetFirstSelected()
            resultID = obj.GetItem(id, 0).GetText()
            dates, values, resobj = self.getData(resultID)

            writer.writerow([
                "#-------------------------Disclaimer:  This is a data set that was exported by EMIT ... use at your own risk..."])
            writer.writerow(["#"])
            writer.writerow(
                ["#Date Created: %s" % str(resobj.FeatureActionObj.ActionObj.BeginDateTime.strftime("%m/%d/%Y"))])
            writer.writerow(["#Date Exported: %s" % str(getTodayDate())])
            writer.writerow(["Result ID: %s" % str(resobj.ResultID)])
            writer.writerow(["#Variable: %s" % str(resobj.VariableObj.VariableCode)])
            writer.writerow(["#Unit: %s" % str(resobj.UnitObj.UnitsAbbreviation)])
            writer.writerow(["#Organization: %s" % str(
                resobj.FeatureActionObj.ActionObj.MethodObj.OrganizationObj.OrganizationName)])
            writer.writerow(["#"])
            writer.writerow(["#-------------------------End Disclaimer"])
            writer.writerow(["#"])
            writer.writerow(["Dates", "Values"])

            data = []
            j = 0  # j acts like i but its for the values variable
            for i in dates:
                data.append([i, values[j]])  # its done this way to dates and values are two different columns
                j += 1
            writer.writerows(data)

            file.close()

    def Selected(self, list_obj=None, list_id=None):
        if list_id is not None and list_obj is not None:
            self.__list_obj = list_obj
            self.__list_id = list_id
        return self.__list_obj, self.__list_id

    def OnAdd(self, event):

        obj = self.__list_obj
        id = self.__list_id
        filename = obj.GetItem(id).GetText()

        Publisher.sendMessage('AddModel', filepath=filename, x=0, y=0)  # sends message to CanvasController

    def getData(self, resultID):
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

            return dates, values, obj

    def on_view(self, event):
        # get the list control objects
        # obj = self.__list_obj
        # objects = obj.GetObjects()

        if self.parent.Parent.connection_combobox.GetStringSelection() in self.parent.Parent.get_possible_wof_connections():
            self.parent.Parent.open_wof_viewer(self.parent.GetSelectedObject())
            return
        if "ODM2" in self.parent.Parent.connection_combobox.GetStringSelection():
            self.parent.Parent.open_odm2_viewer(self.parent.GetSelectedObject())
            return

    def OnDelete(self, event):
        if 'local' in self.parent.Parent.connection_combobox.GetStringSelection():
            dlg = wx.MessageDialog(self.parent, 'Are you sure you want to delete this simulation?', 'Question',
                                   wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                try:
                    # From Time Series
                    self.parent.Parent.m_olvSeries.RemoveObject(self.parent.GetSelectedObject())  # Deleting
                    self.parent.Parent.m_olvSeries.SortBy(
                        self.parent.Parent.m_olvSeries.GetPrimaryColumnIndex())  # Sorting
                except:
                    # From Simulations
                    self.parent.Parent.conn.deleteRecord(self.parent.GetSelectedObject())
                    self.parent.Parent.table.RemoveObject(self.parent.GetSelectedObject())
                    self.parent.Parent.table.SortBy(self.parent.Parent.table.GetPrimaryColumnIndex())
            dlg.Destroy()
        else:
            elog.info("Deleting can only be done on the local database")


class TimeSeriesContextMenu(ContextMenu):
    def __init__(self, parent):
        super(TimeSeriesContextMenu, self).__init__(parent)

        # deactivate menu items
        menuID = self.FindItem('Add')
        self.FindItemById(menuID).Enable(False)

        menuID = self.FindItem('Delete')
        self.FindItemById(menuID).Enable(False)

        menuID = self.FindItem('Export')
        self.FindItemById(menuID).Enable(False)


class SimulationContextMenu(ContextMenu):
    def __init__(self, parent):
        super(SimulationContextMenu, self).__init__(parent)

        # deactivate menu items
        menuID = self.FindItem('Add')
        self.FindItemById(menuID).Enable(False)

        menuID = self.FindItem('Delete')
        self.FindItemById(menuID).Enable(False)

        menuID = self.FindItem('Export')
        self.FindItemById(menuID).Enable(False)

    def getData(self, simulationID):

        session = self.parent.getDbSession()
        if session is not None:
            if session.__module__ == 'db.dbapi_v2':
                conn = session

                results = []
                try:
                    sPrint('getting results for simulationId: %s' % simulationID, MessageType.DEBUG)
                    # results = conn.read.getResultsBySimulationID(simulationID)
                    results = conn.read.getResultsBySimulationID(simulationID)
                except Exception, e:
                    sPrint('Encountered and exeption: %s' % e, MessageType.ERROR)
                finally:
                    sPrint('Found %d result records: ' % len(results), MessageType.DEBUG)

                if len(results) == 0:
                    sPrint('No results found for simulation id %s.' % simulationID, MessageType.ERROR)
                    return {}

                res = {}
                for r in results:
                    variable_name = r.VariableObj.VariableCode

                    sPrint('retrieving time series results for resultid: %d' % r.ResultID, MessageType.DEBUG)
                    result_values = conn.read.getTimeSeriesResultValuesByResultId(r.ResultID)

                    sPrint('parsing dates and values from pandas object', MessageType.DEBUG)
                    dates = list(result_values.ValueDateTime)
                    values = list(result_values.DataValue)

                    if variable_name in res:
                        res[variable_name].append([dates, values, r])
                    else:
                        res[variable_name] = [[dates, values, r]]

                return res

            else:
                readsim = readSimulation(session)
                readres = readResults(session)
                results = readsim.getResultsBySimulationID(simulationID)

                res = {}
                for r in results:
                    variable_name = r.VariableObj.VariableCode
                    result_values = readres.getTimeSeriesValuesByResultId(int(r.ResultID))

                    dates = []
                    values = []
                    for val in result_values:
                        dates.append(val.ValueDateTime)
                        values.append(val.DataValue)

                    # save data series based on variable
                    if variable_name in res:
                        res[variable_name].append([dates, values, r])
                    else:
                        res[variable_name] = [[dates, values, r]]

                return res

    def on_view(self, event):
        object = self.parent.GetSelectedObject()
        self.parent.Parent.open_simulation_viewer(object)

    def onExport(self, event):
        #  User will choose where to save the csv file
        save = wx.FileDialog(self.parent.GetTopLevelParent(), message="Choose Path",
                             wildcard="CSV Files (*.csv)|*.csv", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if save.ShowModal() == wx.ID_OK:
            path = save.GetPath()
            if path[-4] != '.':
                path += '.csv'
            file = open(path, 'w')
            convert = csv.writer(file, delimiter=',')

            obj, id = self.Selected()
            id = self.parent.GetFirstSelected()
            simulationID = obj.GetItem(id, 0).GetText()

            #  The if below was taken from self.getData
            session = self.parent.getDbSession()
            if session is not None:

                readsim = readSimulation(session)
                readres = readResults(session)
                results = readsim.getResultsBySimulationID(simulationID)

                for r in results:

                    variable_name = r.VariableObj.VariableCode
                    result_values = readres.getTimeSeriesValuesByResultId(int(r.ResultID))

                    dates = []
                    values = []
                    for val in result_values:
                        dates.append(val.ValueDateTime)
                        values.append(val.DataValue)

                    # Organzing data so its in two columns
                    data = []
                    j = 0  # j acts like i but its for the values variable
                    for i in dates:
                        data.append([i, values[j]])
                        j += 1

                    # Writing to CSV file
                    convert.writerows([[variable_name]])
                    convert.writerows(data)

            file.close()


def getTodayDate():
    return time.strftime("%m/%d/%Y")
