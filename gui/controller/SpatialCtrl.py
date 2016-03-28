from gui.views.SpatialView import SpatialView, stretch_grid
from coordinator import engineAccessors
from utilities import geometry
from coordinator.emitLogging import elog
import numpy
from matplotlib.collections import PolyCollection, LineCollection
import wx
from osgeo import ogr


class SpatialCtrl(SpatialView):

    def __init__(self, parent):
        SpatialView.__init__(self, parent)

        self.raw_input_data = None
        self.raw_output_data = None

        self.__input_data = None
        self.__output_data = None
        self.input_legend_label = ""
        self.output_legend_label = ""

        # Set the combo box to ---
        self.input_combobox.SetSelection(0)
        self.output_combobox.SetSelection(0)
        self.input_combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.output_combobox.Bind(wx.EVT_COMBOBOX, self.on_combo)
        self.plot.setAxisLabel("my X axis", "My y axis")

    def add_input_combo_choices(self, items):
        self.input_combobox.AppendItems(items)

    def add_output_combo_choices(self, items):
        self.output_combobox.AppendItems(items)

    def clear_plot(self):
        self.plot.clearPlot()

    def clear_table(self):
        pass

    def edit_grid(self, grid, x_loc, y_loc, value):
        if grid == "input":
            grid = self.input_grid

        if grid == "output":
            grid = self.output_grid

        grid.SetCellValue(x_loc, y_loc, str(value))
        grid.AutoSizeColumns()
        stretch_grid(grid=grid)

    def get_color_by_plot_name(self, name):
        if name in self.__input_data:
            return "#019477"
        if name in self.__output_data:
            return "#0DACFF"

    def get_exchange_items_names(self, model_id, model_type="INPUT"):
        # model_type must match INPUT or OUTPUT
        items = engineAccessors.getExchangeItems(modelid=model_id, exchange_item_type=model_type.upper(), returnGeoms=False)
        if items is not None:
            return [item['name'] for item in items]
        return [""]

    def get_input_combo_choices(self):
        items = []
        for i in range(self.input_combobox.GetCount()):
            items.append(self.input_combobox.GetString(i))
        return items

    def get_output_combo_choies(self):
        items = []
        for i in range(self.output_combobox.GetCount()):
            items.append(self.output_combobox.GetString(i))
        return items

    def get_input_exchange_item_by_id(self, id):
        return engineAccessors.getExchangeItems(id, 'INPUT')

    def get_output_exchange_item_by_id(self, id):
        return engineAccessors.getExchangeItems(id, 'OUTPUT')

    def get_geometries(self, exchange_item):  # This method should work for both input and output
        if isinstance(exchange_item, list):
            igeoms = {}
            for item in exchange_item:
                name = item['name']
                geoms = [ogr.CreateGeometryFromWkb(g) for g in item['geometry']['wkb']]
                igeoms[name] = geoms
            return igeoms
        else:
            elog.debug("Exchange item must be a list of dictionaries")
            elog.debug("Exchange item may be None")
            return {}

    def get_geoms_by_name(self, name):
        if name in self.__input_data:
            return self.__input_data[name]

        if name in self.__output_data:
            return self.__output_data[name]
        return None

    def get_item_in_raw_data(self, raw_data, item):
        if raw_data:
            for data in raw_data:
                if data.has_key("name"):
                    if data["name"] == item:
                        return data
        return None  # None if item not found in raw_data

    def get_selected_input_exchange_item(self):
        if self.input_combobox.GetValue() == "---":
            return {}

        return {self.input_combobox.GetValue(): self.__input_data[self.input_combobox.GetValue()][0]}


    def get_selected_output_exchange_item(self):
        if self.output_combobox.GetValue() == "---":
            return {}

        return {self.output_combobox.GetValue(): self.__output_data[self.output_combobox.GetValue()][0]}

    def on_combo(self, event):
        self.clear_plot()
        if self.input_combobox.GetValue() == "---":
            self.input_legend_label = ""
        else:
            self.input_legend_label = self.input_combobox.GetValue()
            self.update_plot(self.input_combobox.GetValue())
            self.update_input_table()

        if self.output_combobox.GetValue() == "---":
            self.output_legend_label = ""
        else:
            self.output_legend_label = self.output_combobox.GetValue()
            self.update_plot(self.output_combobox.GetValue())
            self.update_output_table()

    def plot_polygon(self, data, color):
        poly_list = []
        reference = data[0].GetGeometryRef(0)
        points = numpy.array(reference.GetPoints())
        a = tuple(map(tuple, points[:, 0:2]))
        poly_list.append(a)

        p_coll = PolyCollection(poly_list, closed=True, facecolor=color, alpha=0.5, edgecolor=None, linewidths=(2,))
        self.plot.axes.add_collection(p_coll, autolim=True)

    def plot_point(self, data, color):
        # get x,y points
        x, y = zip(*[(g.GetX(), g.GetY()) for g in data])
        self.plot.axes.scatter(x, y, color=color)

    def plot_linestring(self, data):
        elog.debug("plot_linestring has not been implemented")

    def set_data(self, target={}, source={}):  # target is input, source is output
        self.__input_data = target
        self.__output_data = source

    def set_legend(self, location=0):
        labels = []
        if self.input_legend_label:
            labels.append(self.input_legend_label)
        if self.output_legend_label:
            labels.append(self.output_legend_label)

        self.plot.axes.legend(labels, loc=location)

    def update_plot(self, data_in, plot_title=""):
        # Data_in is the variable name
        data = self.get_geoms_by_name(data_in)
        if data is None:
            return

        # We can use either a set color or use the getNextColor() from PlotForSiteViewerCtrl.py
        # color = self.plot.getNextColor()
        # color = "#019477"
        color = self.get_color_by_plot_name(data_in)

        if data[0].GetGeometryName().upper() == "POLYGON":
            self.plot_polygon(data, color)
        elif data[0].GetGeometryName().upper() == "POINT":
            self.plot_point(data, color)
        elif data[0].GetGeometryName().upper() == "LINESTRING":
            self.plot_linestring(data)
        else:
            return

        self.plot.setTitle(plot_title)
        self.set_legend()

        self.plot.axes.grid(True)

        # If margin is 0 the graph will fill the plot.
        self.plot.axes.margins(0.1)
        self.plot.reDraw()

    def update_input_table(self):
        item = self.get_selected_input_exchange_item()
        raw_data = self.get_item_in_raw_data(self.raw_input_data, item.keys()[0])
        if raw_data:
            self.edit_grid("input", 1, 1, item.keys())
            self.edit_grid("input", 2, 1, item.values()[0].GetGeometryName())
            self.edit_grid("input", 3, 1, item.values()[0].GetCoordinateDimension())
            self.edit_grid("input", 4, 1, raw_data["geometry"]["extent"])
            self.edit_grid("input", 5, 1, raw_data["geometry"]["count"])
        else:
            elog.debug("Raw data is None, failed to update table")

    def update_output_table(self):
        item = self.get_selected_output_exchange_item()
        raw_data = self.get_item_in_raw_data(self.raw_output_data, item.keys()[0])
        if raw_data:
            self.edit_grid("output", 1, 1, item.keys())
            self.edit_grid("output", 2, 1, item.values()[0].GetGeometryName())
            self.edit_grid("output", 3, 1, item.values()[0].GetCoordinateDimension())
            self.edit_grid("output", 4, 1, raw_data["geometry"]["extent"])
            self.edit_grid("output", 5, 1, raw_data["geometry"]["count"])
        else:
            elog.debug("Raw data is None, failed to update table")
