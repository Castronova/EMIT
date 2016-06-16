import numpy
from matplotlib.collections import PolyCollection, LineCollection

import stdlib
from emitLogging import elog
from gui.views.SpatialPlotView import ViewSpatialPlot


class SpatialPlotCtrl(ViewSpatialPlot):  # Delete me. Unused code

    def __init__(self, parent, title='', xlabel='', ylabel=''):

        ViewSpatialPlot.__init__(self, parent, title=title,xlabel=xlabel,ylabel=ylabel)

        self.__input_data = []
        self.__output_data = []

        self.__iei = None
        self.__oei = None

    def log(self, fmt, *args):
        elog.info((fmt % args))

    def OnClick(self,event):
        self.log("button clicked, id#%d\n", event.GetId())

    def set_selection_output(self, oei_name):
        if oei_name in self.__output_data:
            self.__oei = oei_name
        else:
            self.__oei = None

    def set_selection_input(self, iei_name):
        if iei_name in self.__input_data:
            self.__iei = iei_name
        else:
            self.__iei = None

    def set_input_data(self, value):
        """
        :param value: dictionary {variable: [geoms]}
        :return:
        """
        self.__input_data = value

    def get_input_geom(self, var_name):
        if var_name in self.__input_data:
            return self.__input_data[var_name]
        return None

    def set_output_data(self, value):
        """
        :param value: dictionary {variable: [geoms]}
        :return:
        """
        self.__output_data = value

    def get_output_geom(self, var_name):
        if var_name in self.__output_data:
            return self.__output_data[var_name]
        return None

    def updatePlot(self, event=None):

        # clear the canvas
        self.ax.cla()

        # set the iei and oei geometries
        iei = self.__iei
        oei = self.__oei
        datain = self.get_input_geom(iei)
        if datain is not None:
            self.SetPlotData(datain, colors="#019477")  # Input color is light green

        dataout = self.get_output_geom(oei)
        if dataout is not None:
            self.SetPlotData(dataout, colors="#326ada")  # Output color is light blue

        # set the plot titles
        iei_title = iei if iei is not None else ''
        oei_title = oei if oei is not None else ''
        self.set_titles(iei_title, oei_title)

        # draw the canvas
        self.canvas.draw()

    def set_titles(self, input, output):
        self.outtext.set_text(output)
        self.intext.set_text(input)

    def SetPlotData(self, geom_list, colors):
        # build geometry object
        # todo: this should only be done once, not every time data is selected

        # POINT
        if geom_list[0].GetGeometryName() == stdlib.GeomType.POINT:

            # get x,y points
            x, y = zip(*[(g.GetX(), g.GetY()) for g in geom_list])
            self.ax.scatter(x, y, color=colors)

        # POLYGON
        elif geom_list[0].GetGeometryName() == stdlib.GeomType.POLYGON:

            poly_list = []
            # get geometry reference
            ref = geom_list[0].GetGeometryRef(0)

            # build a list of points
            pts = numpy.array(ref.GetPoints())
            a = tuple(map(tuple, pts[:, 0:2]))
            poly_list.append(a)

            # build a polygon collection
            pcoll = PolyCollection(poly_list, closed=True, facecolor=colors, alpha=0.5, edgecolor=None, linewidths=(2,))

            # add the polygon collection to the plot
            self.ax.add_collection(pcoll, autolim=True)

        # LINESTRING
        elif geom_list[0].GetGeometryName() == stdlib.GeomType.LINESTRING:

            line_list = []
                # build a list of points
            pts = numpy.array(geom_list[0].GetPoints())

            # p = pts[:,0:2]
            a = tuple(map(tuple, pts[:, 0:2]))
            line_list.append(a)

            # build a line collection
            lcoll = LineCollection(line_list, colors=colors)

            # add the line collection to the plot
            self.ax.add_collection(lcoll, autolim=True)

        else:
            elog.critical('Unsupported line geometry found in SpatialPlotCtrl.SetPlotData')

        self.ax.grid()
        self.ax.axis('auto')
        self.ax.margins(0.1)
