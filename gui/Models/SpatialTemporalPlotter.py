import matplotlib as mpl
import numpy
from gui.Models.Plotter import Plotter
from matplotlib.collections import PolyCollection
from matplotlib.collections import LineCollection


class color_cycle(object):
    def __init__(self):

        # get the matplotlib color cycle
        self.__colors = [c['color'] for c in list(mpl.rcParams['axes.prop_cycle'])]
        self.current = -1
        self.max = len(self.__colors)

    def __iter__(self):
        'Returns itself as an iterator object'
        return self

    def next(self):
        'Returns the next value (cyclic)'
        self.current += 1
        if self.current == self.max:
            self.current = 0
        return self.__colors[self.current]


class SpatialTemporalPlotter(Plotter):
    def __init__(self, panel):
        Plotter.__init__(self, panel)

        # stores the plot objects
        self.plots = []
        self.__plot_count = 0
        # self.highlighted_vertices = set()  # Rename to selected_vertices
        self.highlighted_vertices = []  # Keeps track of the highlighted vertices index
        self.marker = None  # Must be a matplotlib line2D object
        self.x_scatter_data, self.y_scatter_data = None, None  # Holds the scatter data for highlighting
        self.poly_list = None  # Holds the data for the plotted polygon
        self.line_data = None  # Holds the line collection for highlighting
        self.highlight_color = "y"  # Yellow is used when highlighting
        self.color = "#0DACFF"  # The standard color for objects that are not highlighted

        # stores the axis objects
        self.__axis = []

        # matplotlib color cycle used to ensure primary and secondary axis are not displayed with the same color
        self.__color_cycle = color_cycle()

    def clear_plot(self):

        # clear axis
        self.axes.clear()
        for ax in self.__axis:
            ax.cla()

        # reset the axis container
        self.__axis = []

        self.axes.grid()
        self.axes.margins(0)

        # clear the plot objects
        self.__plot_count = 0
        self.plots = []

        self.redraw()

    def getNextColor(self):
         return next(self.__color_cycle)

    def get_highlighted_polygons(self):
        """
        Returns all the highlighted polygons
        :return: type(list)
        """
        data = []
        for polygon in self.axes.collections:
            if polygon.get_facecolor().all() == polygon.get_edgecolor().all():
                data.append(polygon)
        return data

    def highlight_line(self, event):
        print "highlight_line()"
        pass

    def highlight_polygon(self, pick_event):
        if pick_event.artist.get_facecolor()[0].all() == pick_event.artist.get_edgecolor()[0].all():
            pick_event.artist.set_facecolor(self.color)
            pick_event.artist.set_edgecolor(None)
        else:
            pick_event.artist.set_color(self.highlight_color)
        pick_event.artist.axes.figure.canvas.draw()

    def highlight_vertex(self, pick_event):
        """
        Only one marker can be used to highlight. self.marker is that one marker
        :param pick_event: matplotlib mouse pick event
        :return:
        """
        if not self.marker:
            self.marker, = pick_event.artist.axes.plot([], [], "o")  # Create a plot
            self.marker.set_color("y")  # Set color to yellow

        # Check if vertex has been highlighted
        if pick_event.ind[0] in self.highlighted_vertices:
            self.highlighted_vertices.remove(pick_event.ind[0])  # Remove highlight
        else:
            self.highlighted_vertices.append(pick_event.ind[0])  # Add highlight

        self.highlighted_vertices.sort()
        x = self._get_vertices_data_points(self.x_scatter_data, pick_event.ind[0])
        y = self._get_vertices_data_points(self.y_scatter_data, pick_event.ind[0])

        # Highlight only those in self.highlighted_vertices
        self.marker.set_data(x, y)
        pick_event.artist.axes.figure.canvas.draw()

    def _get_vertices_data_points(self, data, index):
        """
        :param data: x_data or y_data, type(tuple or list)
        :param index: index of the selected vertex, type(int)
        :return: type(list) contains the x & y values that are highlight and should be plotted
        """
        a = []
        for i in self.highlighted_vertices:
            a.append(data[i])

        return a

    def plot_dates(self, data, name, noDataValue, ylabel=""):
        """
        :param data: type([datetime, floats])
        :param name:
        :param noDataValue:
        :param ylabel:
        :return:
        """

        if len(data) == 0:
            return

        # unpack the dates, values and replace nodata with None
        dates, values = zip(*data)
        nvals = numpy.array(values, dtype=numpy.float)
        nvals[nvals == noDataValue] = None
        nvals[numpy.isnan(nvals)] = None

        # get the next line color
        color = self.getNextColor()

        if self.__plot_count == 0:
            # plot data on the primary axis
            p = self.axes.plot_date(dates, nvals, label=name, color=color, linestyle='-', marker=None)
            self.axes.legend(p, [pl.get_label() for pl in self.plots], loc=0)
            self.axes.set_ylabel(ylabel)

        elif self.__plot_count > 0:
            # plot data on the secondary axis
            ax = self.axes.twinx()
            self.__axis.append(ax)
            p = ax.plot_date(dates, nvals, label=name, color=color, linestyle='-', marker=None)
            ax.set_ylabel(ylabel)

        # save each of the plots
        self.plots.extend(p)

        # rebuild the legend
        self.axes.legend(self.plots, [pl.get_label() for pl in self.plots], loc=0)

        # increment the plot counter
        self.__plot_count += 1

        self.displayLegend(0)

        # redraw the cavas
        self.redraw()

    def plot_polygon(self, data, color):
        poly_list = []
        for item in data:
            reference = item.GetGeometryRef(0)
            points = numpy.array(reference.GetPoints())
            a = tuple(map(tuple, points[:, 0:2]))
            poly_list.append(a)

        self.poly_list = poly_list

        # Plot multiple polygons and add them to collection as individual polygons
        for poly in self.poly_list:
            p_coll = PolyCollection([poly], closed=True, facecolor=color, alpha=0.5, edgecolor=None, linewidths=(2,))
            p_coll.set_picker(True)  # Enable pick event
            self.axes.add_collection(p_coll, autolim=True)

    def plot_point(self, data, color):  # Rename to plot scatter
        # get x,y points
        x, y = zip(*[(g.GetX(), g.GetY()) for g in data])
        self.x_scatter_data, self.y_scatter_data = x, y
        collection = self.axes.scatter(x, y, marker="o", color=color, picker=True)
        return collection

    def plot_linestring(self, data, color):
        # x = []
        # y = []
        # for i in data[0].GetPoints():
        #     x.append(i[0])
        #     y.append(i[1])
        # self.axes.plot(x, y, marker="o", color=color, picker=True)

        segment = []
        points = []
        for point in data[0].GetPoints():
            points.append(point[:-1])

        for i in range(len(points) - 1):
            segment.append((points[i], points[i + 1]))

        self.line_data = segment
        l_coll = LineCollection(segment, color=color)
        l_coll.set_picker(True)
        self.axes.add_collection(l_coll, autolim=True)

    def plot_geometry(self, geometry_object, title, color=None):
        """
        A general plot method that will plot the respective type
        Must call redraw afterwards to have an effect
        :param geometry_object:
        :param title: title for the plot
        :param color: # Hexadecimal
        :return:
        """
        if not color:
            color = self.color

        if geometry_object[0].GetGeometryName().upper() == "POLYGON":
            self.plot_polygon(geometry_object, color)
        elif geometry_object[0].GetGeometryName().upper() == "POINT":
            self.plot_point(geometry_object, color)
        elif geometry_object[0].GetGeometryName().upper() == "LINESTRING":
            self.plot_linestring(geometry_object, color)
        else:
            raise Exception("plot_geometry() failed. Geometries must be POLYGON OR POINT")

        self.set_title(title)
        self.axes.grid(True)

        # If margin is 0 the graph will fill the plot
        self.axes.margins(0.1)

    def reset_highlighter(self):
        """
        Resets the variables needed to highlight
        :return:
        """
        self.marker = None
        self.highlighted_vertices = []
        self.x_scatter_data, self.y_scatter_data = None, None
        self.poly_list = None
        self.line_data = None
