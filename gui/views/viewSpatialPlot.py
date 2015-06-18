__author__ = 'tonycastronova'

import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class SelectionTypes():
    Listbox = 'LISTBOX'
    Checkbox = 'CHECKBOX'

class ViewSpatialPlot(wx.Panel):
    def __init__(self, parent, title='', xlabel='', ylabel='', selection=SelectionTypes.Listbox):

        width = 700
        height = 500

        wx.Panel.__init__(self, id=wx.ID_ANY, name=u'SpatialPlot', parent=parent,
                          pos=wx.Point(571, 262), size=wx.Size(700, 500),
                          style=wx.TAB_TRAVERSAL)

        self.parent = parent

        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.inputLabel = wx.StaticText(self,wx.ID_ANY,label='Input Features: ')
        self.outputLabel = wx.StaticText(self,wx.ID_ANY,label='Output Features: ')

        # put up a figure
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(1,1,1)
        self.ax.xaxis._visible = False
        self.ax.yaxis._visible = False

        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer.Add(self.canvas, 100, wx.ALIGN_CENTER|wx.ALL)

        self.outtext = plt.figtext(0.12, 0.92, " ", fontsize='large', color='b', ha ='left')
        self.intext = plt.figtext(0.9, 0.92, " ",fontsize='large', color='r', ha ='right')


