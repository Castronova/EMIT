__author__ = 'tonycastronova'

import wx
import matplotlib.pyplot as plt
from gui.views.viewSpatialPlot import ViewSpatialPlot

class LogicSpatialPlot(ViewSpatialPlot):

    def __init__(self, parent, title='', xlabel='', ylabel=''):

        ViewSpatialPlot.__init__(self, parent,title=title,xlabel=xlabel,ylabel=ylabel)

        self.__input_geoms = {}
        self.__output_geoms = {}

        self.__input_data = []
        self.__output_data = []

        self.inputCombo.Bind(wx.EVT_COMBOBOX, self.UpdatePlot)
        self.outputCombo.Bind(wx.EVT_COMBOBOX, self.UpdatePlot)

        # put up a figure
        # self.figure = plt.figure()
        # self.ax = self.figure.add_subplot(1,1,1)

        # self.ax.xaxis._visible = False
        # self.ax.yaxis._visible = False

        # self.intext = plt.figtext(0.12, 0.92, " ", fontsize='large', color='b', ha ='left')
        # self.outtext = plt.figtext(0.9, 0.92, " ",fontsize='large', color='r', ha ='right')


    def log(self, fmt, *args):
        print (fmt % args)

    def OnClick(self,event):
        self.log("button clicked, id#%d\n", event.GetId())

    def set_input_data(self, value):
        """
        :param value: dictionary {variable: [geoms]}
        :return:
        """
        self.inputCombo.SetItems([' ']+value.keys())
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
        self.outputCombo.SetItems([' ']+value.keys())
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

    def setInputSeries(self):

        inputs = self.input_data()
        colors = self.buildGradientColor(len(inputs))
        i = 0
        for geom in inputs:
            self.addSeries(geom,colors[i])
            i += 1

    def setOutputSeries(self):

        outputs = self.output_data()
        colors = self.buildGradientColor(len(outputs),'jet')
        i = 0
        for geom in outputs:
            self.addSeries(geom,colors[i])
            i += 1

    def UpdatePlot(self,event):

        self.ax.cla()

        # get parent control
        # parent = event.GetEventObject().Name
        iei = self.inputCombo.GetValue()
        oei = self.outputCombo.GetValue()

        var_name = event.GetString()

        datain = self.get_input_geom(iei)
        if datain is not None:
            colors = self.buildGradientColor(len(datain),'Blues')
            self.SetPlotDataIn(datain,colors=colors)
            self.inputCombo.SetSelection(event.GetSelection())
        # else:
        #     self.inputCombo.Disable()

        dataout = self.get_output_geom(oei)
        if dataout is not None:
            colors = self.buildGradientColor(len(dataout),'Reds')
            self.SetPlotDataOut(dataout,colors=colors)
            self.outputCombo.SetSelection(event.GetSelection())
        # else:
        #     self.outputCombo.Disable()

        self.set_titles(self.inputCombo.GetValue(),
                        self.outputCombo.GetValue())

        self.canvas.draw()

    def set_titles(self, input, output):
        self.outtext.set_text(output)
        self.intext.set_text(input)

    def SetPlotDataIn(self, datain, colors):

        geomsin = datain['data']
        typein = datain['type']
        i = 0

        try:
            self.ax.scatter.cla()
        except:
            pass

        try:
            self.ax.plot.cla()
        except:
            pass

        if typein == 'Point':
            tuple_geomsin = [g[0] for g in geomsin]
            x,y = zip(*tuple_geomsin)
            self.ax.scatter(x,y,color=colors)

        else:

            for g in geomsin:
                x,y = g.exterior.coords.xy
                self.ax.plot(x,y,color=colors[i])
                i += 1

        self.ax.grid()
        self.ax.axis('auto')
        self.ax.margins(0.1)


    def SetPlotDataOut(self, dataout, colors):

        geomsout = dataout['data']
        typeout = dataout['type']
        i = 0

        try:
            self.ax.scatter.cla()
        except:
            pass

        try:
            self.ax.plot.cla()
        except:
            pass

        if typeout == 'Point':
            tuple_geomsout = [g[0] for g in geomsout]
            x,y = zip(*tuple_geomsout)
            self.ax.scatter(x,y,color=colors)
        else:

            for g in geomsout:
                x,y = g.exterior.coords.xy
                self.ax.plot(x,y,color=colors[i])
                i += 1

        self.ax.grid()
        self.ax.axis('auto')
        self.ax.margins(0.1)
