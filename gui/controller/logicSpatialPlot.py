__author__ = 'tonycastronova'

import wx
import matplotlib.pyplot as plt
from gui.views.viewSpatialPlot import ViewSpatialPlot
from coordinator.emitLogging import elog
import stdlib
from matplotlib.collections import PolyCollection, LineCollection
import numpy

class LogicSpatialPlot(ViewSpatialPlot):

    def __init__(self, parent, title='', xlabel='', ylabel=''):

        ViewSpatialPlot.__init__(self, parent, title=title,xlabel=xlabel,ylabel=ylabel)

        self.__input_data = []
        self.__output_data = []

        self.__iei = None
        self.__oei = None

        # self.inputCombo.Bind(wx.EVT_COMBOBOX, self.UpdatePlot)
        # self.outputCombo.Bind(wx.EVT_COMBOBOX, self.UpdatePlot)

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
    #
    # def set_selected_intput(self, selected_name):
    #     self.__iei = selected_name


    def set_input_data(self, value):
        """
        :param value: dictionary {variable: [geoms]}
        :return:
        """
        # self.inputCombo.SetItems([' ']+value.keys())


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
        # self.outputCombo.SetItems([' ']+value.keys())
        self.__output_data = value

    def get_output_geom(self, var_name):
        if var_name in self.__output_data:
            return self.__output_data[var_name]
        return None

    def buildGradientColor(self, num, cmap='Blues'):
        # get the color map
        c = getattr(plt.cm, cmap)

        # add two so that the median color is chosen if only one geometry
        num += 2

        # generate the color definitions
        colors = [c(1.*i/num) for i in range(0,num)]

        # omit the ends of the spectrum so that the correct number of colors is provided
        return colors[1:-1]

    def UpdatePlot(self,event=None):

        # clear the canvas
        self.ax.cla()

        # set the iei and oei geometries
        iei = self.__iei
        oei = self.__oei
        datain = self.get_input_geom(iei)
        print 'datain', datain
        if datain is not None:
            colors = self.buildGradientColor(len(datain),'Reds')
            self.SetPlotData(datain,colors=colors)

        dataout = self.get_output_geom(oei)
        if dataout is not None:
            colors = self.buildGradientColor(len(dataout),'Blues')
            self.SetPlotData(dataout,colors=colors)

        # set the plot titles
        iei_title = iei if iei is not None else ''
        oei_title = oei if oei is not None else ''
        self.set_titles(iei_title,oei_title)

        # draw the canvas
        self.canvas.draw()

    def set_titles(self, input, output):
        self.outtext.set_text(output)
        self.intext.set_text(input)

    def SetPlotData(self, geom_list, colors):

        try:
            self.ax.scatter.cla()
        except:
            pass

        try:
            self.ax.plot.cla()
        except:
            pass


        i = 0

        # build geometry object
        # todo: this should only be done once, not every time data is selected


        # POINT
        if geom_list[0].GetGeometryName() == stdlib.GeomType.POINT:

            # get x,y points
            x,y = zip(*[(g.GetX(), g.GetY()) for g in geom_list])
            self.ax.scatter(x, y, color=colors)


        # POLYGON
        elif geom_list[0].GetGeometryName() == stdlib.GeomType.POLYGON:

            poly_list= []
            for geom in geom_list:

                # get then number of polygons
                polycount = geom.GetGeometryCount()

                # loop through each polygon (most of the time this will only be 1)
                for i in range(polycount):

                    # get geometry reference
                    ring = geom.GetGeometryRef(i)

                    # get number of points
                    points = ring.GetPointCount()

                    # build a list of points
                    pts = numpy.array(ring.GetPoints())

                    # p = pts[:,0:2]
                    a = tuple(map(tuple, pts[:,0:2]))
                    poly_list.append(a)

            # build a polygon collection
            pcoll = PolyCollection(poly_list, closed=True, facecolor=colors, alpha=0.1, edgecolor='none')

            # add the polygon collection to the plot
            self.ax.add_collection(pcoll, autolim=True)


        # LINESTRING
        elif geom_list[0].GetGeometryName() == stdlib.GeomType.LINESTRING:

            line_list = []
            for geom in geom_list:
                # if geom.GetGeometryName() == stdlib.GeomType.LINESTRING:

                # build a list of points
                pts = numpy.array(geom.GetPoints())

                # p = pts[:,0:2]
                a = tuple(map(tuple, pts[:,0:2]))
                line_list.append(a)

            # build a line collection
            lcoll = LineCollection(line_list, colors=colors)

            # add the line collection to the plot
            self.ax.add_collection(lcoll, autolim=True)

        else:
            elog.critical('Unsupported line geometry found in logicSpatialPlot.SetPlotData')

        self.ax.grid()
        self.ax.axis('auto')
        self.ax.margins(0.1)
