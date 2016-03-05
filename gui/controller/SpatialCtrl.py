from gui.views.SpatialView import SpatialView
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

        self.__input_data = None
        self.__output_data = None
        self.input_exchange_item = None
        self.output_exchange_item = None
        self.target_name = ""
        self.source_name = ""
        self.input_legend_label = ""
        self.output_legend_label = ""
        self.input_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox)
        self.output_checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox)
        self.plot.setAxisLabel("my X axis", "My y axis")

    def on_checkbox(self, event):
        self.plot.clearPlot()
        if self.input_checkbox.IsChecked():
            self.input_legend_label = self.target_name
            self.update_plot(self.target_name)
        else:
            self.input_legend_label = ""

        if self.output_checkbox.IsChecked():
            self.output_legend_label = self.source_name
            self.update_plot(self.source_name)
        else:
            self.output_legend_label = ""

    def clear_plot(self):
        self.plot.clearPlot()

    def edit_grid(self, grid, x_loc, y_loc, value):
        if grid == "input":
            grid = self.input_grid

        if grid == "output":
            grid = self.output_grid

        grid.SetCellValue(x_loc, y_loc, str(value))
        grid.AutoSizeColumns()
        self.stretch_grid(grid=grid)


    def get_input_exchange_item_by_id(self, id):
        return engineAccessors.getInputExchangeItems(id)

    def get_output_exchange_item_by_id(self, id):
        return engineAccessors.getOutputExchangeItems(id)

    def get_geometries(self, exchange_item):  # This method should work for both input and output
        if isinstance(exchange_item, list):
            igeoms = {}
            for item in exchange_item:
                name = item['name']
                # geoms = [geometry.fromWKB(g['wkb']) for g in item['geom']]
                geoms = [ogr.CreateGeometryFromWkb(g['wkb']) for g in item['geom']]
                igeoms[name] = geoms
            return igeoms
        else:
            elog.debug("Exchange item must be a list of dictionaries")
            elog.debug("Exchange item may be done")
            return {}

    def get_geoms_by_name(self, name):
        if name in self.__input_data:
            return self.__input_data[name]

        if name in self.__output_data:
            return self.__output_data[name]

        return None

    def set_data(self, target={}, source={}):  # target is input, source is output
        self.__input_data = target
        self.__output_data = source

    def set_selection_data(self, target_name=None, source_name=None):
        #  example of source name is some_value or random POLYGON 10-100
        if target_name in self.__input_data:
            self.input_exchange_item = self.__input_data[target_name]
            self.target_name = target_name
            self.input_legend_label = target_name

        if source_name in self.__output_data:
            self.output_exchange_item = self.__output_data[source_name]
            self.source_name = source_name
            self.output_legend_label = source_name

    def get_color_by_plot_name(self, name):
        if name in self.__input_data:
            return "#019477"
        if name in self.__output_data:
            return "#0DACFF"

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

    def plot_polygon(self, data, color):
        poly_list = []
        reference = data[0].GetGeometryRef(0)
        points = numpy.array(reference.GetPoints())
        a = tuple(map(tuple, points[:, 0:2]))
        poly_list.append(a)

        p_coll = PolyCollection(poly_list, closed=True, facecolor=color, alpha=0.5, edgecolor=None, linewidths=(2,))
        self.plot.axes.add_collection(p_coll, autolim=True)

    def plot_point(self, data, color):
        print "Its a point"
        # get x,y points
        x, y = zip(*[(g.GetX(), g.GetY()) for g in data])
        self.plot.axes.scatter(x, y, color=color)



    def plot_linestring(self, data):
        print "its a line string"

    def set_legend(self, location=0):
        labels = []
        if self.input_legend_label:
            labels.append(self.input_legend_label)
        if self.output_legend_label:
            labels.append(self.output_legend_label)

        self.plot.axes.legend(labels, loc=location)
