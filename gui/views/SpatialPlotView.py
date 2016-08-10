__author__ = 'tonycastronova'

import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class SelectionTypes():
    Listbox = 'LISTBOX'
    Checkbox = 'CHECKBOX'

class ViewSpatialPlot(wx.Panel):
    def __init__(self, parent, title='', xlabel='', ylabel='', selection=SelectionTypes.Listbox):

        wx.Panel.__init__(self, id=wx.ID_ANY, name=u'SpatialPlot', parent=parent,
                          pos=wx.Point(571, 262), size=wx.Size(700, 500),
                          style=wx.TAB_TRAVERSAL)

        self.parent = parent

        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        # put up a figure
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.xaxis._visible = True
        self.ax.yaxis._visible = True

        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer.Add(self.canvas, 100, wx.ALIGN_CENTER|wx.ALL)

        self.intext = plt.figtext(0.12, 0.94, " ", fontsize='large', color='#019477', ha='left')
        self.outtext = plt.figtext(0.9, 0.94, " ", fontsize='large', color='#326ada', ha='right')
