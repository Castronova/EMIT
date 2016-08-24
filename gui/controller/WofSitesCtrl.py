import datetime as dt
import threading
import time
import wx
import coordinator.engineAccessors as engine
from emitLogging import elog
from gui.views.WofSitesView import WofSitesView
from sprint import *


class WofSitesCtrl(WofSitesView):
    def __init__(self, parent, siteObject, api):
        self.wof_api = api

        table_cols = ["Variable Name", "Unit", "Category", "Type", "Begin Date Time", "End Date Time", "Description"]
        WofSitesView.__init__(self, parent, siteObject.site_name, table_cols)
        self.site_objects = siteObject
        self.line_style_combo.SetEditable(False)

        self.line_style_combo.SetSelection(1)
        self.thread = threading.Thread()

        self.Bind(wx.EVT_BUTTON, self.onPreview, self.PlotBtn)
        self.Bind(wx.EVT_DATE_CHANGED, self.setStartDate, self.startDatePicker)
        self.Bind(wx.EVT_DATE_CHANGED, self.setEndDate, self.endDatePicker)
        self.Bind(wx.EVT_BUTTON, self.on_export_button, self.exportBtn)
        self.Bind(wx.EVT_BUTTON, self.addToCanvas, self.addToCanvasBtn)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_enable_button)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.on_disable_button)
        self.line_style_combo.Bind(wx.EVT_COMBOBOX, self.on_line_style)
        self.on_disable_button(None)
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # instantiate a container for the wof data
        self.wofSeries = wofSeries()

        self.populate_table(self.site_objects.site_code)
        self.plot.activate_panning()
        self.plot.activate_zooming()

    def enable_button(self):
        self.PlotBtn.Enable()
        self.exportBtn.Enable()
        self.addToCanvasBtn.Enable()
        self.line_style_combo.Enable()

    def disable_button(self):
        self.PlotBtn.Disable()
        self.exportBtn.Disable()
        self.addToCanvasBtn.Disable()
        self.line_style_combo.Disable()

    def _preparationToGetValues(self):
        code = self.get_selected_variable_code()
        siteobject = self.site_objects

        # convert wx._misc.DateTime to python datetime
        start = dt.datetime.strptime('%sT%s'%(self.start_date.FormatISODate(), self.start_date.FormatISOTime()),
                                     "%Y-%m-%dT%H:%M:%S")
        end = dt.datetime.strptime('%sT%s'%(self.end_date.FormatISODate(), self.end_date.FormatISOTime()),
                                     "%Y-%m-%dT%H:%M:%S")
        return end, siteobject, start, code

    def addToCanvas(self, event):
        if not self.variableList.get_selected_row():
            return  # No selected row

        end, siteobject, start, variable_code = self._preparationToGetValues()

        var_codes_temp = self.get_all_selected_variable_site_codes()
        if len(var_codes_temp) > 1:
            elog.warning("We do not support adding more then one item to the canvas at this point. We added " + var_codes_temp[0])
        if variable_code is None:
            # no table row selected
            return

        args = dict(model_type='wof',
                    wsdl=self.parent.api.wsdl,
                    site=siteobject.site_code,
                    variable=variable_code,
                    start=start,
                    end=end,
                    network=siteobject.network,
        )

        engine.addModel(**args)

        self.Close()

    def dicToObj(self, data):
        temp = []
        for key, value in data.iteritems():
            d = {"code": key,
                 "name": value[0],
                 "unit": value[1],
                 "category": value[2],
                 "type": value[3],
                 "begin_date": value[4],
                 "end_date": value[5],
                 "description": value[6]
                 }
            temp.append(DicToObj(d))
        return temp

    def _export_a_waterml(self, path):
        if not path[-3:] == "xml":
            return
        end, siteobject, start, var_code = self._preparationToGetValues()
        data = self.wof_api.getValues(siteobject.site_code, var_code, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

        if not data:
            sPrint("WofSitesCtrl._export_a_waterml() failed. data is None")
            return

        with open(path, 'w') as f:
            f.write(data)
            f.close()

    # Threaded
    def handle_export(self, path):
        """
        Exports the highest selected row
        :param path: type(string) the export path
        :return:
        """
        self.disable_button()
        self._thread_status_bar_loading()

        if path[-4] != '.':
            path += '.csv'

        if path[-3:] == "xml":
            self._export_a_waterml(path)
            return

        varInfo = self.variableList.get_selected_row()
        end, siteobject, start, var_code = self._preparationToGetValues()

        variables = [
            ['V1', varInfo[0], var_code, varInfo[1], varInfo[6], siteobject.latitude, siteobject.longitude]]

        code = '%s__%s__%s__%s' % (siteobject.site_code, var_code, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

        values = []
        if code in self.wofSeries.data:
            for v in self.wofSeries.getData(code)[0].values[0].value:  # Data has been previewed
                values.append([v._dateTime.strftime('%m-%d-%Y %H:%M:%S'), v.value])
        else:
            # Data has not been previewed so fetch data
            values = self.wof_api.parseValues(siteobject.site_code, var_code, start, end)

        with open(path, 'w') as f:
            hline = '#' + 75 * '-' + '\n'
            f.write(hline)
            f.write('# \n')
            f.write('# NOTICE: this data set that was exported by the EMIT model coupling framework. '
                    'Use at your own risk \n')
            f.write("# \n")
            f.write("# Date Exported: %s \n" % getTodayDate())
            f.write("# Site Name: %s \n" % siteobject.site_name)
            f.write("# Site Code: %s \n" % siteobject.site_code)
            f.write("# Category: %s \n" % varInfo[2])
            f.write("# Type: %s \n" % varInfo[3])
            f.write("# Begin Date: %s \n" % varInfo[4])
            f.write("# End Date: %s \n" % varInfo[5])
            f.write(hline)
            f.write("# \n")
            f.write('# Data Description \n')
            f.write("# \n")
            f.write('# V[idx] = Variable Name, Variable Code, Unit, Description, Latitude, Longitude \n')
            f.write("# \n")
            for variable in variables:
                f.write('# %s = %s\n' % (variable[0], ', '.join(variable[1:])))
            f.write("# \n")
            f.write(hline)
            f.write("# \n")
            f.write("# \n")
            f.write("# Date, %s\n" % ', '.join(v[0] for v in variables))
            for d in values:
                f.write('%s, %s \n' % (d[0], d[1]))

            f.close()

        self.enable_button()
        sPrint("Finished exporting", messageType=MessageType.INFO)

    def get_all_selected_variable_name(self):
        vars = []
        num = self.variableList.GetItemCount()
        for i in range(num):
            if self.variableList.IsSelected(i):
                vars.append(self.variableList.GetItemText(i))
        return vars

    def get_selected_variable_code(self):
        row = self.variableList.get_selected_row()
        if not row:
            return None

        return self.get_site_code_by_variable_name(row[0])

    def get_all_selected_variable_site_codes(self):
        rows = self.variableList.get_all_selected_rows()
        if not len(rows):
            return  # No rows selected

        site_codes = []
        for row in rows:
            site_codes.append(self.get_site_code_by_variable_name(row[0]))
        return site_codes

    def get_selected_site_code(self):
        row = self.variableList.get_selected_row()
        variable = row[0]
        return self.get_site_code_by_variable_name(variable)

    def get_site_code_by_variable_name(self, checkedVar):
        for key, value in self._data.iteritems():
            if value[0] == checkedVar:
                return key        # Column names

    def onPreview(self, event):
        if not self.variableList.get_selected_row():
            return  # No row is selected

        if not isinstance(self.thread, threading.Thread):
            sPrint("WofSiteCtrl.thread must be type(threading.Thread", messageType=MessageType.DEBUG)
            return

        if self.thread.isAlive():
            sPrint("WoftSiteCtrl.thread is alive", messageType=MessageType.DEBUG)
            return

        # update the WOF plot data in a thread so that the gui is not blocked
        self.thread = threading.Thread(target=self.updatePlotData, name='WofSiteCtrl.thread')
        self.thread.setDaemon(True)
        self.thread.start()

    def populate_table(self, sitecode):
        data = self.wof_api.buildAllSiteCodeVariables(sitecode)
        self.updateVariablesTable(data)

    # THREADED
    def updatePlotData(self):
        self.disable_button()

        self.line_style_combo.SetSelection(1)  # Default line style is scatter
        self._thread_status_bar_loading()

        # get selected variables
        var_codes = self.get_all_selected_variable_site_codes()
        var_names = self.get_all_selected_variable_name()

        # get start and end dates
        sd = self.start_date.FormatISODate()
        ed = self.end_date.FormatISODate()

        #   - check which data needs to be queried
        series_keys = []
        for i in range(len(var_codes)):
            # add this series to the wof series container
            key = self.wofSeries.addDataSeries(self.site_objects.site_code, var_codes[i], var_names[i], sd, ed)

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
            sPrint('Querying WOF using this following parameters: %s, %s, %s, %s ' % (series.site_code, series.var_code, series.start_date, series.end_date), MessageType.INFO)
            data = self.wof_api.getValuesObject(series.site_code, series.var_code, series.start_date, series.end_date)

            # save these data to the wofSeries object
            self.wofSeries.addData(series, data)

        # update the plot canvase
        # wx.CallAfter(self.updatePlotArea, series_keys)

        self.updatePlotArea(series_keys)
        self.enable_button()

    # Threaded
    def _thread_status_bar_loading(self):
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


            ylabel = data[0].variable.unit.unitName
            self.plot.plot_dates(plotData, series_info.var_name, ylabel)
            self.plot.display_legend(0)

    # THREADED
    def updateStatusBarLoading(self):
        status_list = ["Querying.", "Querying..", "Querying...", "Querying....", "Querying....."]
        i = 0
        self.on_disable_button(None)
        while self.thread.isAlive():
            if i < len(status_list):
                self.updateStatusBar(status_list[i])
                i += 1
            else:
                i = 0
                self.updateStatusBar(status_list[i])
            time.sleep(0.5)
        self.on_enable_button(None)
        self.updateStatusBar("Ready")

    def updateStatusBar(self, text):
        self.status_bar.SetStatusText(str(text))

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
        self.variableList.auto_size_table()
        self.variableList.alternate_row_color()

    ###############################
    # EVENTS
    ###############################

    def on_close(self, event):
        if self.thread.isAlive():
            self.Hide()
        else:
            self.Destroy()

    def on_disable_button(self, event):
        self.disable_button()

    def on_enable_button(self, event):
        if not self.thread.isAlive():
            self.enable_button()

    def on_export_button(self, event):
        if not self.variableList.get_selected_row():
            return  # No row is selected

        if not isinstance(self.thread, threading.Thread):
            sPrint("WofSiteCtrl.thread must be type threading.Thread", messageType=MessageType.DEBUG)
            return

        if self.thread.isAlive():
            sPrint("WofSiteCtrl.thread is alive", messageType=MessageType.DEBUG)
            sPrint("Currently exporting in background...", messageType=MessageType.INFO)
            return

        file_dialog = wx.FileDialog(parent=self, message="Choose Path", defaultDir=os.getcwd(),
                            wildcard="CSV File (*.csv)|*.csv |WaterML File (*.xml)|*.xml", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if file_dialog.ShowModal() == wx.ID_OK:
            export_path = file_dialog.GetPath()

            self.thread = threading.Thread(target=self.handle_export, args=(export_path,),
                                           name="WofSiteCtrl.on_export_button thread")
            self.thread.setDaemon(True)
            self.thread.start()

    def on_line_style(self, event):
        if not len(self.plot.plots):
            return  # Nothing is plotted

        if event.GetSelection() == 0:
            for plot in self.plot.plots:
                plot.set_linestyle('-')
        else:
            for plot in self.plot.plots:
                plot.set_linestyle('None')
        self.plot.redraw()

    def setEndDate(self, event):
        self.end_date = self.endDatePicker.GetValue()

    def setStartDate(self, event):
        self.start_date = self.startDatePicker.GetValue()


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
        if key in self.data:
            return self.data[key]
        else:
            return None


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
        self.start_date = sd
        self.end_date = ed

    def __str__(self):
        return '%s__%s__%s__%s' % (self.site_code, self.var_code, self.start_date, self.end_date)


class DicToObj(object):
    def __init__(self, dic):
        self.__dict__ = dic

def getTodayDate():
    return time.strftime("%m/%d/%Y")
