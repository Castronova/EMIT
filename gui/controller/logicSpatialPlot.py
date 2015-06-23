__author__ = 'tonycastronova'

import wx
import matplotlib.pyplot as plt
from gui.views.viewSpatialPlot import ViewSpatialPlot
from coordinator.emitLogging import elog

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

    def set_selected_intput(self, selected_name):
        self.__iei = selected_name


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
        for geom in geom_list:
            # todo: broken
            if geom.geom_type == 'Point':
                tuple_geomsin = [g[0] for g in geom]
                x,y = zip(*tuple_geomsin)
                self.ax.scatter(x,y,color=colors)

            else:
                x,y = geom.exterior.coords.xy
                self.ax.plot(x,y,color=colors[i])
                i += 1

        self.ax.grid()
        self.ax.axis('auto')
        self.ax.margins(0.1)


    # def SetPlotDataOut(self, dataout, colors):
    #
    #     geomsout = dataout['data']
    #     typeout = dataout['type']
    #     i = 0
    #
    #     try:
    #         self.ax.scatter.cla()
    #     except:
    #         pass
    #
    #     try:
    #         self.ax.plot.cla()
    #     except:
    #         pass
    #
    #     if typeout == 'Point':
    #         tuple_geomsout = [g[0] for g in geomsout]
    #         x,y = zip(*tuple_geomsout)
    #         self.ax.scatter(x,y,color=colors)
    #     else:
    #
    #         for g in geomsout:
    #             x,y = g.exterior.coords.xy
    #             self.ax.plot(x,y,color=colors[i])
    #             i += 1
    #
    #     self.ax.grid()
    #     self.ax.axis('auto')
    #     self.ax.margins(0.1)
