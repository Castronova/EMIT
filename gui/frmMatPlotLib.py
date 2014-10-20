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


class PlotEnum():
    point = 'POINT',
    line = 'LINE',
    bar = 'BAR'

class MatplotFrame(wx.Frame):
    def __init__(self, parent, title='', xlabel=''):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = wx.EmptyString,
                          pos = wx.DefaultPosition, size = wx.Size( 700,500 ),
                          style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        Sizer = wx.BoxSizer(wx.VERTICAL)

        self.parent = parent

        # set the color map
        self.__cmap = plt.cm.jet

        # create an instance of the figure
        self.spatialPanel = pnlSpatial(self, title, xlabel, self.cmap)

        Sizer.Add( self.spatialPanel, 1, wx.ALL | wx.EXPAND |wx.GROW, 0)

        self.SetSizer(Sizer)
        self.Layout()
        self.Centre(wx.BOTH)

        # build custom menu bar
        self.build_menu()

        # set the default plot type
        self.__plot_type = PlotEnum.point

        # initializer for the figure axis
        self.axis = self.spatialPanel.Axis()

        # intializer for figure
        self.figure = self.spatialPanel.Figure()

        # initializer for x and y data
        self.xdata = []
        self.ydata = []
        self.label = []

    def build_menu(self):
        # create menu bar
        menuBar = wx.MenuBar()

        # create file menu
        viewmenu= wx.Menu()

        # create plot options menu
        plotoptions= wx.Menu()
        self.plot_point = plotoptions.Append(wx.ID_ANY, 'Point')
        self.plot_line  = plotoptions.Append(wx.ID_ANY, 'Line')
        self.plot_bar   = plotoptions.Append(wx.ID_ANY, 'Bar')

        # add plot options to Plot menu
        viewmenu.AppendMenu(wx.ID_ANY, 'Plot', plotoptions)


        # Creating the menubar.
        menuBar.Append(viewmenu,"&View")
        self.SetMenuBar(menuBar)
        self.Show(True)


        # add event handlers for the menu items
        self.Bind(wx.EVT_MENU, self.OnPlotPoint, self.plot_point)
        self.Bind(wx.EVT_MENU, self.OnPlotLine, self.plot_line)
        self.Bind(wx.EVT_MENU, self.OnPlotBar, self.plot_bar)

    def add_series(self,x,y):
        return self.spatialPanel.add_series(x,y)

    def cmap(self, value=None):
        if value is not None:
            self.__cmap = value
        return self.__cmap

    def OnPlotPoint(self,event):

        # redraw as point plot
        if self.__plot_type != PlotEnum.point:
            self.__plot_type = PlotEnum.point

            # redraw as point plot
            colors,attrib = self.rip_data_from_axis()
            labels = self.label
            xlist = self.xdata
            ylist = self.ydata

            self.axis.cla()

            i = 0
            xbuffer = (99999999,-99999999)
            ybuffer = (99999999,-99999999)
            for x,y in zip(xlist,ylist):

                # buffer the date range so that all values appear within the plot (i.e. not on the edges)
                xbuffer = self.bufferData(xbuffer,x, 0.1)
                ybuffer = self.bufferData(ybuffer,y,0.1)

                self.axis.plot_date(x, y, label = labels[i], linestyle='.', color = colors[i])
                #self.axis.xaxis_date()

                i += 1

            # set axis min and max using the buffer
            self.axis.set_xlim(xbuffer)
            self.axis.set_ylim(ybuffer)
            self.axis.grid()
            self.figure.autofmt_xdate()

            # build legend
            handles, labels = self.axis.get_legend_handles_labels()
            self.axis.legend(handles, labels, title="Result ID", bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

            for attribute in attrib:
                eval(attribute)

            self.figure.canvas.draw()

    def OnPlotLine(self,event):

        # redraw as line plot
        if self.__plot_type != PlotEnum.line:
            self.__plot_type = PlotEnum.line

            colors,attrib = self.rip_data_from_axis()
            labels = self.label
            xlist = self.xdata
            ylist = self.ydata

            self.axis.cla()

            i = 0
            xbuffer = (99999999,-99999999)
            ybuffer = (99999999,-99999999)
            for x,y in zip(xlist,ylist):

                # buffer the date range so that all values appear within the plot (i.e. not on the edges)
                xbuffer = self.bufferData(xbuffer,x, 0.1)
                ybuffer = self.bufferData(ybuffer,y,0.1)

                self.axis.plot(x, y, label = labels[i], linestyle='-',linewidth=1.5, color = colors[i])
                self.axis.xaxis_date()

                i += 1

            # set axis min and max using the buffer
            self.axis.set_xlim(xbuffer)
            self.axis.set_ylim(ybuffer)
            self.axis.grid()
            self.figure.autofmt_xdate()

            # build legend
            handles, labels = self.axis.get_legend_handles_labels()
            self.axis.legend(handles, labels, title="Result ID", bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

            for attribute in attrib:
                eval(attribute)


            self.figure.canvas.draw()

    def OnPlotBar(self,event):
        if self.__plot_type != PlotEnum.bar:
            self.__plot_type = PlotEnum.bar

            # redraw as bar plot
            colors,attrib = self.rip_data_from_axis()

            labels = self.label
            xlist = self.xdata
            ylist = self.ydata

            if len(xlist) > 1:
                warning = 'Bar plots are not currently supported for multiple time series. :( '
                dlg = wx.MessageDialog(self.parent , warning, '', wx.OK | wx.ICON_WARNING)
                dlg.ShowModal()
                dlg.Destroy()
                return

            self.axis.cla()

            i = 0
            xbuffer = (99999999,-99999999)
            ybuffer = (99999999,-99999999)
            for x,y in zip(xlist,ylist):


                # buffer the date range so that all values appear within the plot (i.e. not on the edges)
                xbuffer = self.bufferData(xbuffer,x, 0.1)
                ybuffer = self.bufferData(ybuffer,y,0.1)

                # calculate the column width (90% of the difference btwn successive measurements)
                column_width = min(x[1:-1] - x[0:-2])*.9

                # adjust the x values such that they are center aligned on their original x value
                offset_x = [val - .5*column_width for val in x]

                self.axis.bar(offset_x, y, label = labels[i], color = colors[i], width=column_width)
                self.axis.xaxis_date()

                i += 1

            # set axis min and max using the buffer
            self.axis.set_xlim(xbuffer)
            self.axis.set_ylim(ybuffer)
            self.axis.grid()
            self.figure.autofmt_xdate()

            # build legend
            handles, labels = self.axis.get_legend_handles_labels()
            self.axis.legend(handles, labels, title="Result ID", bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

            for attribute in attrib:
                eval(attribute)

            self.figure.canvas.draw()

    def rip_data_from_axis(self):
        # xlist = []
        # ylist = []
        # labels = []
        attrib = []
        # for line in self.axis.get_lines():
        #
        #     # get series data
        #     x,y = line.get_data()
        #
        #     # get series label
        #     labels.append(line.get_label())
        #
        #     # save x,y values
        #     xlist.append(x)
        #     ylist.append(y)


        attrib.append('self.axis.set_title("%s")'% self.axis.get_title())
        attrib.append('self.axis.set_ylabel("%s")'% self.axis.get_ylabel())
        attrib.append('self.axis.set_xlabel("%s")' % self.axis.get_xlabel())


        # get the cmap
        cmap = self.cmap()

        # generate series colors
        num_colors = len(self.xdata)
        colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

        return colors, attrib

    def plot(self, xlist, ylist, labels, cmap=plt.cm.jet):

        # plot time series
        #self.f1 = self.spatialPanel.plot_multiple(xlist, ylist, labels, cmap)
        self.figure = self.plot_initial(xlist, ylist, labels, cmap)

        self.axis = self.figure.axes[0]

        # build legend
        handles, labels = self.axis.get_legend_handles_labels()
        self.axis.legend(handles, labels, title="Result ID", bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    def plot_initial(self, xlist, ylist, labels, cmap):


        # build color map
        num_colors = len(xlist)
        colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

        i = 0
        xbuffer = (99999999,-99999999)
        ybuffer = (99999999,-99999999)
        for x_dates,y in zip(xlist,ylist):

            x = date2num(x_dates)

            # buffer the date range so that all values appear within the plot (i.e. not on the edges)
            xbuffer = self.bufferData(xbuffer,x, 0.1)
            ybuffer = self.bufferData(ybuffer,y,0.1)

            self.axis.plot_date(x, y, label = labels[i], linestyle='.', color = colors[i])
            # self.axis.xaxis_date()

            # store the x and y data for this session
            self.xdata.append(x)
            self.ydata.append(y)
            self.label.append(labels[i])

            i += 1

        # set axis min and max using the buffer
        self.axis.set_xlim(xbuffer)
        self.axis.set_ylim(ybuffer)
        #self.axis.set_xlim(left=min(x)-date_buffer, right=max(x)+date_buffer)
        self.axis.grid()
        self.figure.autofmt_xdate()

        # build legend
        handles, labels = self.axis.get_legend_handles_labels()
        self.axis.legend(handles, labels, title="Result ID", bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        #self.figure.canvas.draw()

        return self.figure

    def bufferData(self, current, data_range, buffer=0.1):
        '''
        calculates a data buffer for the timeseries such that all data will appear on plot (i.e. not along border)
        :param current: (min, max) tuple
        :param data_range: [val1, val2, ..., valn] list of data values
        :param buffer: percentage of value to buffer.  e.g. 0.1 buffers 10%
        :return: returns (min, max) adjusted tuple
        '''

        dr = max(data_range) - min(data_range)
        upper = max(data_range) + dr*buffer
        lower = min(data_range) - dr*buffer

        return (min(current[0],lower), max(current[1], upper))


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

        #self.axis.grid()
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

    def Axis(self):
        return self.axis
    def Figure(self):
        return self.figure


    # def add_series(self, x, y):
    #
    #     dates = date2num(x)
    #     ax = self.figure.axes[0]
    #
    #     ax.plot_date(dates, y, cmap = self.cmap)
    #
    #     #ax.plot(t,t*t)
    #     #ax.grid()
    #
    #     #fig.autofmt_xdate()
    #
    #     #return ax

    # def log(self, fmt, *args):
    #     print (fmt % args)
    #
    # def OnClick(self,event):
    #     self.log("button clicked, id#%d\n", event.GetId())

    # def set_data(self, x,y):
    #     self._x = x
    #     self._y = y


    # def drawplot(self, fig):
    #
    #
    #     dates = date2num(self.x)
    #
    #
    #     ax = fig.add_subplot(1,1,1)
    #
    #     #t = np.arange(0,1,0.001)
    #     ax.plot_date(dates, self.y, cmap=self.cmap)
    #
    #     #ax.plot(t,t*t)
    #     ax.grid()
    #
    #     fig.autofmt_xdate()
    #
    #     return ax

    def plot_multiple(self, xlist, ylist, labels, cmap):

        # build color map
        #c = getattr(plt.cm, cmap)
        num_colors = len(xlist)
        colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

        # plots = []
        # ax = self.figure.axes[0]
        #ax = self.axis
        i = 0
        for x,y in zip(xlist,ylist):

            dates = date2num(x)
            self.axis.plot_date(dates, y, label = labels[i], color = colors[i])
            # plots.append(p)

            i += 1

        #self.axis.grid()
        #self.figure.autofmt_xdate()

        #fig.colorbar(plots)
        #plt.show()
        #self.figure.tight_layout()
        return self.figure