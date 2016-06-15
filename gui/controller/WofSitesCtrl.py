import csv
import datetime as dt
import threading
import time

import wx

import coordinator.engineAccessors as engine
from emitLogging import elog
from gui.views.TimeSeriesPlotView import TimeSeriesPlotView
from sprint import *


class WofSitesCtrl(TimeSeriesPlotView):
    def __init__(self, parent, siteObject, api):
        self.wof = api

        table_cols = ["Variable Name", "Unit", "Category", "Type", "Begin Date Time", "End Date Time", "Description"]
        TimeSeriesPlotView.__init__(self, parent, siteObject.site_name, table_cols)
        self.siteobject = siteObject
        # self.Bind(wx.EVT_BUTTON, self.previewPlot, self.PlotBtn)
        self.Bind(wx.EVT_BUTTON, self.onPreview, self.PlotBtn)
        self.Bind(wx.EVT_DATE_CHANGED, self.setStartDate, self.startDatePicker)
        self.Bind(wx.EVT_DATE_CHANGED, self.setEndDate, self.endDatePicker)
        self.Bind(wx.EVT_BUTTON, self.onExport, self.exportBtn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, self.addToCanvasBtn)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.enableBtns)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.disableBtns)
        self.disableBtns(None)
        self.done_querying = True

        # instantiate a container for the wof data
        self.wofSeries = wofSeries()

        # threaded web service call so that the gui does not hang
        t = threading.Thread(target=self.populateVariablesList, args=(api, siteObject.site_code), name='WOF_GetVariables')
        t.setDaemon(True)
        t.start()

    def enableBtns(self, event):
        if self.done_querying:
            self.PlotBtn.Enable()
            self.exportBtn.Enable()
            self.addToCanvasBtn.Enable()

    def disableBtns(self, event):
        self.PlotBtn.Disable()
        self.exportBtn.Disable()
        self.addToCanvasBtn.Disable()

    def setEndDate(self, event):
        self.end_date = self.endDatePicker.GetValue()

    def setStartDate(self, event):
        self.start_date = self.startDatePicker.GetValue()

    def _preparationToGetValues(self):
        code = self.getSelectedVariableCode()
        parent = self.Parent
        siteobject = self.siteobject

        # convert wx._misc.DateTime to python datetime
        start = dt.datetime.strptime('%sT%s'%(self.start_date.FormatISODate(), self.start_date.FormatISOTime()),
                                     "%Y-%m-%dT%H:%M:%S")
        end = dt.datetime.strptime('%sT%s'%(self.end_date.FormatISODate(), self.end_date.FormatISOTime()),
                                     "%Y-%m-%dT%H:%M:%S")
        return end, parent, siteobject, start, code

    def addToCanvas(self, event):
        end, parent, siteobject, start, variable_code = self._preparationToGetValues()

        var_codes_temp = self.getAllSelectedVariableSiteCodes()
        if len(var_codes_temp) > 1:
            elog.warning("We do not support adding more then one item to the canvas at this point. We added " + var_codes_temp[0])
        if variable_code is None:
            # no table row selected
            return

        args = dict(type='wof',
                    wsdl=self.parent.api.wsdl,
                    site=siteobject.site_code,
                    variable=variable_code,
                    start=start,
                    end=end,
                    network=siteobject.network
        )

        engine.addModel(attrib=args)
        self.Close()

    def dicToObj(self, data):
        temp = []
        for key, value in data.iteritems():
            d = {}
            d["code"] = key
            d["name"] = value[0]
            d["unit"] = value[1]
            d["category"] = value[2]
            d["type"] = value[3]
            d["begin_date"] = value[4]
            d["end_date"] = value[5]
            d["description"] = value[6]
            temp.append(DicToObj(d))
        return temp

    def onExport(self, event):
        var_codes_temp = self.getAllSelectedVariableSiteCodes()
        var_code = self.Parent.selectedVariables = self.getSelectedVariableSiteCode()
        if len(var_codes_temp) > 1:
            elog.warning("We currently only support exporting 1 variable at a time, we are exporting: " + var_codes_temp[0] + " for you")
        var_code = var_codes_temp[0]
        if var_code > 0 :
            save = wx.FileDialog(parent=self.GetTopLevelParent(), message="Choose Path",
                                 defaultDir=os.getcwd(),
                                 wildcard="CSV Files (*.csv)|*.csv",
                                 style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if save.ShowModal() == wx.ID_OK:
                path = save.GetPath()
                if path[-4] != '.':
                    path += '.csv'
                file = open(path, 'w')
                varInfo = self.getSelectedVariable()
                end, parent, siteobject, start, var_code = self._preparationToGetValues()
                code = '%s__%s__%s__%s' % (siteobject.site_code, var_code, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

                variables = [['V1', varInfo[0]]]

                values = []
                for v in self.wofSeries.getData(code)[0].values[0].value:
                    values.append([v._dateTime.strftime('%m-%d-%Y %H:%M:%S'), v.value])

                with open(path, 'w') as f:
                    hline = '#' + 75*'-' + '\n'
                    f.write(hline)
                    f.write('# \n')
                    f.write('# NOTICE: this data set that was exported by the EMIT model coupling framework, use at your own risk \n')
                    f.write("# \n")
                    f.write("# Date Exported: %s \n" % getTodayDate())
                    f.write("# Site Name: %s \n" % siteobject.site_name)
                    f.write("# Site Code: %s \n" % siteobject.site_code)
                    f.write("# Variable Name: %s \n" % varInfo[0])
                    f.write("# Variable Code: %s \n" % var_code)
                    f.write("# Unit: %s \n" % varInfo[1])
                    f.write("# Category: %s \n" % varInfo[2])
                    f.write("# Type: %s \n" % varInfo[3])
                    f.write("# Begin Date: %s \n" % varInfo[4])
                    f.write("# End Date: %s \n" % varInfo[5])
                    f.write("# Description: %s \n" % varInfo[6])
                    f.write(hline)
                    f.write("# \n")
                    f.write('# Column Legend \n')
                    for variable in variables:
                        f.write('# %s = %s\n' % (variable[0], variable[1]))
                    f.write("# \n")
                    f.write(hline)
                    f.write("# \n")
                    f.write("# \n")
                    for variable in variables:
                        f.write("# Date, %s\n" % ', '.join(v[0] for v in variables))
                    for d in values:
                        f.write('%s, %s \n' % (d[0], d[1]))

        else:
            elog.info("Select a variable to export")

    def getAllSelectedVariables(self):
        code = self.getAllSelectedVariableSiteCodes()
        variables = []
        for i in code:
            variables.append(self._data[i])
        return variables

    def getSelectedVariable(self):
        code = self.getSelectedVariableSiteCode()
        return self._data[code]

    def getAllSelectedVariableName(self):
        vars = []
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                vars.append(self.variableList.GetItemText(i))
        return vars

    def getSelectedVariableCode(self):
        variableCode = None
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                v_name = self.variableList.GetItemText(i)
                variableCode = self.getSiteCodeByVariableName(v_name)
                break
        return variableCode

    def getAllSelectedVariableSiteCodes(self):
        sites = []
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                v_name = self.variableList.GetItemText(i)
                sites.append(self.getSiteCodeByVariableName(v_name))
        return sites

    def getSelectedVariableSiteCode(self):
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                v_name = self.variableList.GetItemText(i)
                return self.getSiteCodeByVariableName(v_name)

    def getSiteCodeByVariableName(self, checkedVar):
        for key, value in self._data.iteritems():
            if value[0] == checkedVar:
                return key        # Column names

    def onPreview(self, event):

        # update the WOF plot data in a thread so that the gui is not blocked
        t = threading.Thread(target=self.updatePlotData, name='UpdateWofPlotData')
        t.setDaemon(True)
        t.start()

    def populateVariablesList(self, api, sitecode):
    # THREADED
        self.updateStatusBar("Querying ...")

        #  Theading the updateStatusBarLoading to animate loading
        self.threadStatusBarLoading()

        data = api.buildAllSiteCodeVariables(sitecode)
        sPrint('Finished querying WOF service for site variables, threaded', MessageType.DEBUG)

        # uses wx callafter to update the variables table.  This is necessary since wx is being called within a thread
        wx.CallAfter(self.updateVariablesTable, data)
        self.done_querying = True

    # THREADED
    def updatePlotData(self):
        self.updateStatusBar("Querying ...")

        self.threadStatusBarLoading()

        # get selected variables
        var_codes = self.getAllSelectedVariableSiteCodes()
        var_names = self.getAllSelectedVariableName()

        # get start and end dates
        sd = self.start_date.FormatISODate()
        ed = self.end_date.FormatISODate()

        #   - check which data needs to be queried
        series_keys = []
        for i in range(len(var_codes)):
            # add this series to the wof series container
            key = self.wofSeries.addDataSeries(self.siteobject.site_code, var_codes[i], var_names[i], sd, ed)

            # save the key that is returned
            series_keys.append(key)

            sPrint('Added key to wof series container: %s' % key, MessageType.DEBUG)

        # prune to only the keys that were added
        pruned = self.wofSeries.prune(series_keys)

        # query which data series are missing data
        series_missing_data = self.wofSeries.getSeriesMissingData()

        #   - query wof values
        for series in series_missing_data:

            # query the data using WOF
            sPrint('Querying WOF using this following parameters: %s, %s, %s, %s ' % (series.site_code, series.var_code, series.sd, series.ed), MessageType.INFO)
            data = self.wof.getValues(series.site_code, series.var_code, series.sd, series.ed)

            # save these data to the wofSeries object
            self.wofSeries.addData(series, data)

        # update the plot canvase
        wx.CallAfter(self.updatePlotArea, series_keys)

        self.done_querying = True

    # THREADED
    def threadStatusBarLoading(self):
        #  Theading the updateStatusBarLoading to animate loading
        self.done_querying = False
        status_bar_loading_thread = threading.Thread(target=self.updateStatusBarLoading, name="StatusBarLoading")
        status_bar_loading_thread.setDaemon(True)
        status_bar_loading_thread.start()

    def updatePlotArea(self, series_keys):
        """
        Updates the WOF plot with the selected data
        Args:
            series_keys: list of series keys of the data that will be plot
        Returns: None
        """

        self.plot.clear_plot()

        for key in series_keys:

            series_info = self.wofSeries.series_info[key]
            data = self.wofSeries.getData(key)

            plotData = []
            noData = None

            # make sure data is found
            if data is not None:

                # get the first data element only
                if len(data[0].values[0]) > 1:
                    values = data[0].values[0].value
                else:
                    elog.info("There are no values.  Try selecting a larger date range")
                    return

                for value in values:
                    plotData.append((value._dateTime, value.value))

                noData = data[0].variable.noDataValue

            ylabel = data[0].variable.unit.unitName
            self.plot.plot_dates(plotData, series_info.var_name, noData, ylabel)
            self.plot.display_legend(0)

    # THREADED
    def updateStatusBarLoading(self):
        #  self.done_querying must be set to True in the method that is running the long process
        status_list = ["Querying .", "Querying ..", "Querying ...", "Querying ....", "Querying ....."]
        i = 0
        self.disableBtns(None)
        while not self.done_querying:  # self.done_querying is created in the method that calls this one
            if i < len(status_list):
                self.updateStatusBar(status_list[i])
                i += 1
            else:
                i = 0
                self.updateStatusBar(status_list[i])
            time.sleep(0.5)
        self.enableBtns(None)
        # self.updateStatusBar("Ready")
        wx.CallAfter(self.updateStatusBar, "Ready")

    def updateStatusBar(self, text):
        self.status_bar.SetStatusText(str(text))
        wx.Yield()

    def updateVariablesTable(self, data):
        self._data = data
        self._objects = self.dicToObj(data)
        rowNumber = 0
        colNumber = 0
        for key, value, in data.iteritems():
            pos = self.variableList.InsertStringItem(rowNumber, str(key))
            for i in value:
                if colNumber is 4 or colNumber is 5:
                    self.variableList.SetStringItem(pos, colNumber, str(i.strftime("%m/%d/%y")))
                else:
                    self.variableList.SetStringItem(pos, colNumber, str(i))
                colNumber += 1
            colNumber = 0
            rowNumber += 1
        self.autoSizeColumns()
        self.alternateRowColor()


class wofSeries(object):
    """
    This class stores the wof data series that currently plotted in the WOFSitesViewer.  It has been optimized to
    reduce unnecessary webservice calls (i.e. redundant calls).
    """

    def __init__(self, cache = 5):

        self.series_info = {}
        self.data = {}
        self.cache = cache

    def getDataSeries(self):
        return self.series_info

    def getData(self, key):
        return self.data[key]


    def addDataSeries(self, site_code, var_code, var_name, sd, ed):
        info = seriesInfo(site_code, var_code, var_name, sd, ed)

        if str(info) not in self.series_info.keys():
            self.series_info[str(info)] = info

        return str(info)

    def addData(self, seriesInfo, data):

        self.data[str(seriesInfo)] = data

    def clearDataSeries(self):
        self.series_info = {}
        self.data = {}

    def prune(self, keys):
        """
        Prunes the data series to contain only the keys provided as args
        Args:
            keys: list of keys to keep in the wofSeries object
        Returns: list of removed keys
        """

        # find which keys to remove
        keys_to_remove = [k for k in self.series_info.keys() if k not in keys]

        total_series = len(self.series_info.keys())

        # only remove data series if storage exceeds the cache
        if total_series > self.cache:

            # remove series info and data for each of these keys
            for k in keys_to_remove:
                sPrint('Pruning the following keys: %s' % k, MessageType.DEBUG)
                self.series_info.pop(k)
                self.data.pop(k)

                # exits pruning loop when storage is within cache limit again
                if len(self.series_info.keys()) <= self.cache:
                    break

        return keys_to_remove

    def getSeriesMissingData(self):
        """
        Determines which of the data series are missing data
        Returns: seriesInfo objects for all data series that are missing data

        """
        series_missing_data = []
        for key in self.series_info.keys():
            if key not in self.data.keys():
                series_missing_data.append(self.series_info[key])
        return series_missing_data

class seriesInfo(object):
    def __init__(self, site_code, var_code, var_name, sd, ed):
        self.site_code = site_code
        self.var_code = var_code
        self.var_name = var_name
        self.sd = sd
        self.ed = ed

    def __str__(self):
        return '%s__%s__%s__%s' % (self.site_code, self.var_code, self.sd, self.ed)


class DicToObj(object):
    def __init__(self, dic):
        self.__dict__ = dic

def getTodayDate():
    return time.strftime("%m/%d/%Y")
