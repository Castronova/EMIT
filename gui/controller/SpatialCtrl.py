from gui.views.SpatialView import SpatialView
from coordinator import engineAccessors
from utilities import geometry
from coordinator.emitLogging import elog
import numpy
from matplotlib.collections import PolyCollection, LineCollection


class SpatialCtrl(SpatialView):

    def __init__(self, parent):
        SpatialView.__init__(self, parent)

        self.__input_data = None
        self.__output_data = None
        self.__iei = None
        self.__oei = None

    def clear_plot(self):
        self.plot.clearPlot()

    def get_input_exchange_item_by_id(self, id):
        return engineAccessors.getInputExchangeItems(id)

    def get_output_exchange_item_by_id(self, id):
        return engineAccessors.getOutputExchangeItems(id)

    def get_geometries(self, exchange_item):  # This method should work for both input and output
        if isinstance(exchange_item, list):
            igeoms = {}
            for item in exchange_item:
                name = item['name']
                geoms = [geometry.fromWKB(g['wkb']) for g in item['geom']]
                igeoms[name] = geoms
            return igeoms
        else:
            elog.debug("Exchange item must be a list of dictionaries")
        return

    def set_data(self, target={}, source={}):  # target is input, source is output
        self.__input_data = target
        self.__output_data = source

    def set_selection_data(self, target_name=None, source_name=None):
        #  example of source name is some_value or random POLYGON 10-100
        if target_name in self.__input_data:
            self.__iei = target_name

        if source_name in self.__output_data:
            self.__oei = source_name

    def get_geoms_by_name(self, name):
        if name in self.__input_data:
            return self.__input_data[name]

        if name in self.__output_data:
            return self.__output_data[name]

        return None

    def update_plot(self, data_in, data_out=None, plot_title=None):
        self.clear_plot()
        # Data_in/out is the variable name

        data = self.get_geoms_by_name(data_in)

        # We can use either a set color or use the getNextColor() from PlotForSiteViewerCtrl.py
        # color = self.plot.getNextColor()
        color = "#019477"

        switch = {
            "POLYGON": self.plot_polygon(data, color=color),
            "POINT": self.plot_point(data),
            "LINESTRING": self.plot_linestring(data)
        }
        switch.get(data[0].GetGeometryName().upper, None)  # Default is None

        # set the title here

        self.plot.axes.grid(True)
        # self.plot.axes.axis("auto")

        # If margin is 0 the graph will fill the plot.
        self.plot.axes.margins(0.1)
        self.plot.reDraw()

    def plot_polygon(self, data, color):
        print "Its a polygon"
        poly_list = []
        reference = data[0].GetGeometryRef(0)
        points = numpy.array(reference.GetPoints())
        a = tuple(map(tuple, points[:, 0:2]))
        poly_list.append(a)

        p_coll = PolyCollection(poly_list, closed=True, facecolor=color, alpha=0.5, edgecolor=None, linewidths=(2,))
        self.plot.axes.add_collection(p_coll, autolim=True)

    def plot_point(self, data):
        print "Its a point"
        pass

    def plot_linestring(self, data):
        print "its a line string"
        pass
