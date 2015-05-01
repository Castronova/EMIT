__author__ = 'tonycastronova'

import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class ViewSpatialPlot(wx.Panel):
    def __init__(self, parent, title='', xlabel='', ylabel=''):

        width = 700
        height = 500

        wx.Panel.__init__(self, id=wx.ID_ANY, name=u'SpatialPlot', parent=parent,
                          pos=wx.Point(571, 262), size=wx.Size(10, 10),
                          style=wx.TAB_TRAVERSAL)

        self.SetClientSize(wx.Size(10, 10))

        self.parent = parent

        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.inputCombo = wx.ComboBox(self, wx.ID_ANY,name='input_combo',choices=[])
        self.outputCombo = wx.ComboBox(self, wx.ID_ANY,name='output_combo', choices=[])

        self.inputLabel = wx.StaticText(self,wx.ID_ANY,label='Input Features: ')
        self.outputLabel = wx.StaticText(self,wx.ID_ANY,label='Output Features: ')

        # put up a figure
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(1,1,1)
        self.ax.xaxis._visible = False
        self.ax.yaxis._visible = False

        #self.axes = self.drawplot(self.figure)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer.Add(self.canvas, 100, wx.ALIGN_CENTER|wx.ALL)

        # add inputs controls to an iosizer
        iosizer = wx.BoxSizer(wx.HORIZONTAL)
        iosizer.Add(self.inputLabel, 1, wx.ALIGN_LEFT|wx.ALL)
        iosizer.Add(self.inputCombo, 1, wx.ALIGN_LEFT|wx.ALL)
        sizer.Add(iosizer)

        iosizer = wx.BoxSizer(wx.HORIZONTAL)
        iosizer.Add(self.outputLabel, 1, wx.ALIGN_LEFT|wx.ALL)
        iosizer.Add(self.outputCombo, 1, wx.ALIGN_LEFT|wx.ALL)
        sizer.Add(iosizer)

        self.SetSizer(sizer)

        self.intext = plt.figtext(0.12, 0.92, " ", fontsize='large', color='b', ha ='left')
        self.outtext = plt.figtext(0.9, 0.92, " ",fontsize='large', color='r', ha ='right')


