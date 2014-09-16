__author__ = 'Mario'

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import wx

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
] = [wx.NewId() for _init_ctrls in range(4)]

class pnlSpatial ( wx.Panel ):

    def __init__( self, prnt):
        wx.Panel.__init__(self, id=wxID_PNLSPATIAL, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(10, 10),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(10, 10))

        self.parent = prnt

        self.__input_geoms = {}
        self.__output_geoms = {}

        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        # A button
        # self.button =wx.Button(self, label="Placeholder")
        # self.radiobutton1 = wx.RadioButton(self, wx.ID_ANY, u"Placeholder")
        # self.radiobutton2 = wx.RadioButton(self, wx.ID_ANY, u"Placeholder")
        # self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

        self.__input_data = []
        self.__output_data = []

        # self.inputCheckbox = wx.CheckBox(self, wx.ID_ANY,'Inputs')
        # self.outputCheckbox = wx.CheckBox(self, wx.ID_ANY,'Outputs')

        self.inputCombo = wx.ComboBox(self, wx.ID_ANY,name='input_combo',choices=[])
        self.outputCombo = wx.ComboBox(self, wx.ID_ANY,name='output_combo', choices=[])


        # self.inputCheckbox.Disable()
        # self.outputCheckbox.Disable()

        # self.inputCheckbox.Bind(wx.EVT_CHECKBOX, self.UpdatePlot)
        # self.outputCheckbox.Bind(wx.EVT_CHECKBOX, self.UpdatePlot)

        self.inputCombo.Bind(wx.EVT_COMBOBOX, self.UpdatePlot)
        self.outputCombo.Bind(wx.EVT_COMBOBOX, self.UpdatePlot)

        # put up a figure
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(1,1,1)
        # self.mapping = self.figure.add_subplot(1,3,2)
        # self.output = self.figure.add_subplot(1,3,3)

        # format plot axis (suppress)

        self.ax.xaxis._visible = False
        self.ax.yaxis._visible = False
        # self.mapping.xaxis._visible = False
        # self.mapping.yaxis._visible = False
        # self.output.xaxis._visible = False
        # self.output.yaxis._visible = False



        #self.axes = self.drawplot(self.figure)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer.Add(self.canvas, 100, wx.ALIGN_CENTER|wx.ALL)
        #sizer.Add(self.button, 0, wx.ALIGN_CENTER|wx.ALL)
        #sizer.Add(self.inputCheckbox, 0, wx.ALIGN_CENTER|wx.ALL)
        #sizer.Add(self.outputCheckbox, 0, wx.ALIGN_CENTER|wx.ALL)

        sizer.Add(self.inputCombo, 0, wx.ALIGN_LEFT|wx.ALL)
        sizer.Add(self.outputCombo, 0, wx.ALIGN_LEFT|wx.ALL)

        self.SetSizer(sizer)
        #self.Fit()



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

        return self.__input_data[var_name]

    def set_output_data(self, value):
        """
        :param value: dictionary {variable: [geoms]}
        :return:
        """
        self.outputCombo.SetItems([' ']+value.keys())
        self.__output_data = value

    def get_output_geom(self, var_name):

        return self.__output_data[var_name]

    def buildGradientColor(self, num, cmap='Blues'):
        c = getattr(plt.cm, cmap)
        num_colors = num
        return [c(1.*i/num_colors) for i in range(num_colors)]

    def setInputSeries(self):

        inputs = self.input_data()
        colors = self.buildGradientColor(len(inputs),'jet')
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
        parent = event.GetEventObject().Name

        # get variable name
        var_name = event.GetString()

        if parent == 'input_combo':
            data = self.get_input_geom(var_name)
            colors = self.buildGradientColor(len(data),'Blues')
            self.SetPlotData(geoms=data,colors=colors)
            self.outputCombo.SetSelection(0)
        if parent == 'output_combo':
            data = self.get_output_geom(var_name)
            colors = self.buildGradientColor(len(data),'Reds')
            self.SetPlotData(geoms=data,colors=colors)
            self.inputCombo.SetSelection(0)

        # if self.inputCheckbox.IsChecked():
        #     self.setInputSeries()
        # if self.outputCheckbox.IsChecked():
        #     self.setOutputSeries()

        self.canvas.draw()

    def SetPlotData(self, geoms, colors):

        i = 0
        for g in geoms:
            x,y = zip(*g)
            self.ax.plot(x,y,color=colors[i])
            i += 1

        self.ax.grid()
        self.ax.axis('auto')
        self.ax.margins(0.1)



class pnlSpatialMapping ( wx.Panel ):

    def __init__( self, prnt):
        wx.Panel.__init__(self, id=wxID_PNLSPATIAL, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(10, 10),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(10, 10))

        self.parent = prnt


        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        # A button
        # self.button =wx.Button(self, label="Placeholder")
        # self.radiobutton1 = wx.RadioButton(self, wx.ID_ANY, u"Placeholder")
        # self.radiobutton2 = wx.RadioButton(self, wx.ID_ANY, u"Placeholder")
        # self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

        self.__input_data = []
        self.__output_data = []

        self.inputCheckbox = wx.CheckBox(self, wx.ID_ANY,'Inputs')
        self.outputCheckbox = wx.CheckBox(self, wx.ID_ANY,'Outputs')

        self.inputCheckbox.Disable()
        self.outputCheckbox.Disable()

        self.inputCheckbox.Bind(wx.EVT_CHECKBOX, self.UpdatePlot)
        self.outputCheckbox.Bind(wx.EVT_CHECKBOX, self.UpdatePlot)
        #self.outputCheckbox.Bind(wx.EVT_CHECKBOX, self.redraw)

        # put up a figure
        self.figure = plt.figure()
        self.input = self.figure.add_subplot(1,3,1)
        self.mapping = self.figure.add_subplot(1,3,2)
        self.output = self.figure.add_subplot(1,3,3)

        # format plot axis (suppress)
        #self.input.set_axis_off()
        #self.input.set_xmargin(1)
        #self.input.set_ymargin(0)

        self.input.xaxis._visible = False
        self.input.yaxis._visible = False
        self.mapping.xaxis._visible = False
        self.mapping.yaxis._visible = False
        self.output.xaxis._visible = False
        self.output.yaxis._visible = False



        #self.axes = self.drawplot(self.figure)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer.Add(self.canvas, 100, wx.ALIGN_CENTER|wx.ALL)
        #sizer.Add(self.button, 0, wx.ALIGN_CENTER|wx.ALL)
        sizer.Add(self.inputCheckbox, 0, wx.ALIGN_CENTER|wx.ALL)
        sizer.Add(self.outputCheckbox, 0, wx.ALIGN_CENTER|wx.ALL)

        self.SetSizer(sizer)
        #self.Fit()



    def log(self, fmt, *args):
        print (fmt % args)

    def OnClick(self,event):
        self.log("button clicked, id#%d\n", event.GetId())

    def input_data(self, value=[]):
        if len(value) != 0:
            for val in value:
                self.__input_data.append(zip(*val))
            self.inputCheckbox.Enable()
        else:
            return self.__input_data

    def output_data(self, value=[]):
        if len(value) != 0:
            for val in value:
                self.__output_data.append(zip(*val))
            self.outputCheckbox.Enable()
        else:
            return self.__output_data

    def buildGradientColor(self, num, cmap='Blues'):
        c = getattr(plt.cm, cmap)
        num_colors = num
        return [c(1.*i/num_colors) for i in range(num_colors)]

    def setInputSeries(self):

        inputs = self.input_data()
        colors = self.buildGradientColor(len(inputs),'jet')
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
        if self.inputCheckbox.IsChecked():
            self.setInputSeries()
        if self.outputCheckbox.IsChecked():
            self.setOutputSeries()

        self.canvas.draw()

    def addSeries(self, geom, color):

        self.ax.plot(geom[0],geom[1],color=color)
        self.ax.grid()
        self.ax.axis('auto')
        self.ax.margins(0.1)


