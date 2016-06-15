import wx
from gui.views.SimulationsPlotView import SimulationsPlotView
from utilities import geometry
import matplotlib


class SimulationsPlotCtrl(SimulationsPlotView):
    def __init__(self, parent, columns=None):
        SimulationsPlotView.__init__(self, parent)

        if columns:
            self.table.set_columns(columns)

        self.data = {}  # Dictionary to hold the data respective to the row ID
        self.geometries = {}  # Holds the geometries respective to the row ID
        self.start_date_object = wx.DateTime_Now() - 1 * wx.DateSpan_Day()  # Default date is yesterday
        self.end_date_object = wx.DateTime_Now()  # Default date is today
        self._row_start_date = None
        self._row_end_date = None

        self.start_date_picker.SetValue(self.start_date_object)
        self.end_date_picker.SetValue(self.end_date_object)

        # Adding room for the x axis labels to be visible
        self.temporal_plot.add_padding_to_plot(bottom=0.15)
        self.spatial_plot.add_padding_to_plot(bottom=0.15)

        # Bindings
        self.plot_button.Bind(wx.EVT_BUTTON, self.on_plot)
        self.table.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_row_selected)
        self.start_date_picker.Bind(wx.EVT_DATE_CHANGED, self.on_start_date_change)
        self.end_date_picker.Bind(wx.EVT_DATE_CHANGED, self.on_end_date_change)
        self.spatial_plot.plot.mpl_connect('pick_event', self.on_pick_spatial)

    def on_pick_spatial(self, event):
        if isinstance(event.artist, matplotlib.collections.PathCollection):
            self.spatial_plot.highlight_vertex(event)
        elif isinstance(event.artist, matplotlib.collections.PolyCollection):
            self.spatial_plot.highlight_polygon(event)
        elif isinstance(event.artist, matplotlib.collections.LineCollection):
            self.spatial_plot.highlight_line(event)
        else:
            print "More to come"

        self.plot_highlighted_timeseries()

    def get_highlighted_geometry(self):
        """
        Return index and object or coordinate of the highlighted spatial
        :return: type(dict)
        """
        if len(self.spatial_plot.get_highlighted_polygons()):
            return self.spatial_plot.get_highlighted_polygons()

        if len(self.spatial_plot.get_highlighted_vertices()):
            return self.spatial_plot.get_highlighted_vertices()

        if len(self.spatial_plot.get_highlighted_lines()):
            return self.spatial_plot.get_highlighted_lines()

        return {}

    def get_selected_id(self):
        """
        :return: the ID type(Int) of the selected row or -1 if no row is selected
        """
        row = self.table.get_selected_row()
        if row:
            return int(row[0])
        return -1

    def get_geometries(self, ID):
        """
        Converts the geometry string to objects
        :param ID: Int
        :return: a list of geometry objects
        """
        geometries = []
        for item in self.geometries[ID]:
            geometries.append(geometry.fromWKT(item)[0])
        return geometries

    def parse_data_to_range(self, data):
        """
        List are pass by reference so need to reverse twice to keep the original
        Gets two indexs where the data can be sliced to get the data within
        the dates in the picker
        :param data:
        :return:
        """
        start_index = 0
        end_index = -1
        date = wx.DateTime()
        for i in range(len(data)):
            date.ParseFormat(str(data[i][0]), "%Y-%m-%d %H:%M:%S")
            if self.start_date_object > date:
                start_index = i
            else:
                break

        data.reverse()

        for i in range(len(data)):
            date.ParseFormat(str(data[i][0]), "%Y-%m-%d %H:%M:%S")
            if self.end_date_object < date:
                end_index = i
            else:
                break
        data.reverse()  # Reverse back

        return start_index, end_index

    def plot_highlighted_timeseries(self):
        """
        Plots the time series for the highlighted geometries
        :return:
        """
        if self.get_selected_id() == -1:
            return

        row_data = self.data[self.get_selected_id()]
        time_series_data = []

        # Get the highlighted time series data
        geometry = self.get_highlighted_geometry()
        for key, value in geometry.iteritems():
            time_series_data.append(row_data[key])

        self.temporal_plot.clear_plot()
        self.temporal_plot.rotate_x_axis_label()
        units = self.table.get_selected_row()[2]
        name = self.get_geometries(self.get_selected_id())[0]
        name = name.GetGeometryName()
        for data in time_series_data:
            date_object, value = data

            d = []
            for i in range(len(date_object)):
                d.append((date_object[i], value[i]))

            start_index, end_index = self.parse_data_to_range(d)
            self.temporal_plot.plot_dates(d[start_index + 1: -end_index], name, None, units)

    def plot_spatial(self, ID, title):
        """
        Plots the spatial of the selected row
        :param ID: type(Int). Must match a row the selected row's ID
        :return:
        """
        self.spatial_plot.clear_plot()

        geometries = self.get_geometries(ID)
        self.spatial_plot.rotate_x_axis_label()
        self.spatial_plot.plot_geometry(geometries, title)
        self.spatial_plot.set_legend([title])
        self.spatial_plot.redraw()

    ##########################
    # EVENTS
    ##########################

    def on_end_date_change(self, event):
        """
        Prevents the end date from being set to before the start date and
        prevent the end date from being set to a day after today
        :param event:
        :return:
        """
        if not self._row_end_date:
            return  # End date has not been set. Select a row to set date

        if self.end_date_picker.GetValue() > self._row_end_date:
            self.end_date_picker.SetValue(self._row_end_date)
        elif self.start_date_picker.GetValue() > self.end_date_picker.GetValue():  # Prevent start date to overlap end
            self.end_date_picker.SetValue(self.end_date_object)
        elif self.end_date_picker.GetValue() > wx.DateTime_Now():
            self.end_date_picker.SetValue(self.end_date_object)  # Prevent end date to be set to after today
        else:
            self.end_date_object = self.end_date_picker.GetValue()

    def on_row_selected(self, event):
        """
        Set the date pickers to match the start and end date of the row selected dates
        The date variable needs to be reset in order to get the start dates to stick
        :param event:
        :return:
        """
        self.spatial_plot.reset_highlighter()
        date = wx.DateTime()
        start_date_string = self.table.get_selected_row()[3]
        if date.ParseFormat(start_date_string, "%Y-%m-%d") == -1:
            raise Exception("start_date_string is not in the right format")
        self._row_start_date = date
        self.start_date_picker.SetValue(date)
        self.start_date_object = date

        date = wx.DateTime()  # Need to reset the date

        end_date_string = self.table.get_selected_row()[4]
        if str(end_date_string) == "None":
            self.end_date_picker.SetValue(wx.DateTime_Now())
        elif date.ParseFormat(end_date_string, "%Y-%m-%d") == -1:
            raise Exception("end_date_string is not in the right format")
        else:
            self.end_date_picker.SetValue(date)
            self.end_date_object = date
        self._row_end_date = self.end_date_picker.GetValue()

        #  Plot Spatial
        self.plot_spatial(self.get_selected_id(), self.table.get_selected_row()[1])

    def on_plot(self, event):
        self.plot_highlighted_timeseries()

    def on_start_date_change(self, event):
        """
        Prevents the start date from being set to after the end date and
        prevent start date from being set to before the row's start date
        :param event:
        :return:
        """
        if not self._row_start_date:
            return  # Start date has not been set

        if self.start_date_picker.GetValue() < self._row_start_date:
            self.start_date_picker.SetValue(self._row_start_date)
        elif self.start_date_picker.GetValue() > self.end_date_picker.GetValue():
            self.start_date_picker.SetValue(self.start_date_object)
        else:
            self.start_date_object = self.start_date_picker.GetValue()
