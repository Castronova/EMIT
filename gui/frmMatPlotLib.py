__author__ = 'Mario'

from matplotlib.dates import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavToolbar
from matplotlib.figure import Figure
import wx

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
] = [wx.NewId() for _init_ctrls in range(4)]

class MatplotFrame(wx.Frame):
    def __init__(self, parent, title='', xlabel=''):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = wx.EmptyString,
                          pos = wx.DefaultPosition, size = wx.Size( 700,500 ),
                          style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        Sizer = wx.BoxSizer(wx.VERTICAL)

        # set the color map
        self.cmap = plt.cm.jet

        # create an instance of the figure
        self.spatialPanel = pnlSpatial(self, title, xlabel, self.cmap)

        Sizer.Add( self.spatialPanel, 1, wx.ALL | wx.EXPAND |wx.GROW, 0)

        self.SetSizer(Sizer)
        self.Layout()
        self.Centre(wx.BOTH)


    def add_series(self,x,y):
        return self.spatialPanel.add_series(x,y)

    def set_cmap(self, value=None):
        if value is not None:
            self.cmap = value
        return self.cmap

    def plot_multiple_series(self, xlist, ylist, labels, cmap=plt.cm.jet):
        # plot time series
        axis = self.spatialPanel.plot_multiple(xlist, ylist, labels, cmap)

        # build legend
        handles, labels = axis.get_legend_handles_labels()
        axis.legend(handles, labels, title="Result ID", bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

class pnlSpatial ( wx.Panel ):

    def __init__( self, prnt, title, xlabel, cmap):
        wx.Panel.__init__(self, id=wxID_PNLSPATIAL, name=u'pnlIntro', parent=prnt,
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(10, 10))

        self.parent = prnt
        self.cmap = cmap

        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        # create a figure
        self.figure = plt.figure()

        # build very basic axis
        self.axis = self.figure.add_subplot(1,1,1)
        self.figure.autofmt_xdate()

        self.axis.grid()
        self.axis.set_title(title)
        self.axis.set_ylabel(xlabel)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavToolbar(self.canvas)
        self.figure.tight_layout()
        plt.subplots_adjust(
            right=.75, bottom = .15
        )
        #self.figure.tight_layout()

        sizer.Add(self.toolbar, 0, wx.ALIGN_CENTER|wx.ALL| wx.EXPAND| wx.GROW, 1)
        sizer.Add(self.canvas, 1, wx.ALIGN_CENTER|wx.ALL| wx.EXPAND| wx.GROW, 1)
        # sizer.Add(self.button, 0, wx.ALIGN_CENTER|wx.ALL)
        # sizer.Add(self.radiobutton1, 0, wx.ALIGN_CENTER|wx.ALL)
        # sizer.Add(self.radiobutton2, 0, wx.ALIGN_CENTER|wx.ALL)

        self.SetSizer(sizer)
        #self.Fit()

    def add_series(self, x, y):

        dates = date2num(x)
        ax = self.figure.axes[0]

        ax.plot_date(dates, y, cmap = self.cmap)

        #ax.plot(t,t*t)
        #ax.grid()

        #fig.autofmt_xdate()

        #return ax

    def log(self, fmt, *args):
        print (fmt % args)

    def OnClick(self,event):
        self.log("button clicked, id#%d\n", event.GetId())

    # def set_data(self, x,y):
    #     self._x = x
    #     self._y = y


    def drawplot(self, fig):


        dates = date2num(self.x)


        ax = fig.add_subplot(1,1,1)

        #t = np.arange(0,1,0.001)
        ax.plot_date(dates, self.y, cmap=self.cmap)

        #ax.plot(t,t*t)
        ax.grid()

        fig.autofmt_xdate()

        return ax

    def plot_multiple(self, xlist, ylist, labels, cmap):

        # build color map
        #c = getattr(plt.cm, cmap)
        num_colors = len(xlist)
        colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

        plots = []
        # ax = self.figure.axes[0]
        ax = self.axis
        i = 0
        for x,y in zip(xlist,ylist):

            dates = date2num(x)
            p = ax.plot_date(dates, y, label = labels[i], color = colors[i])
            plots.append(p)

            i += 1

        #fig.colorbar(plots)
        #plt.show()
        #self.figure.tight_layout()
        return ax