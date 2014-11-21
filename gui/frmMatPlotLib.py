__author__ = 'Mario'

from matplotlib.dates import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavToolbar
from matplotlib.figure import Figure
import wx
import wx.lib.mixins.listctrl as listmix
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from PIL import Image, ImageDraw
import sys
from wx.lib.pubsub import pub as Publisher
from ObjectListView import FastObjectListView, ColumnDefn
import wx.lib.newevent
import copy

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
] = [wx.NewId() for _init_ctrls in range(4)]

OvlCheckEvent, EVT_OVL_CHECK_EVENT = wx.lib.newevent.NewEvent()

class LegendListCtrl(wx.ListCtrl, listmix.CheckListCtrlMixin, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.CheckListCtrlMixin.__init__(self)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(3)

    def OnCheckItem(self, index, flag):
        #print 'Something Selected!'

        Publisher.sendMessage('SeriesChecked') # sends message to MatplotFrame


class LegendListCtrlPanel(wx.Panel, listmix.CheckListCtrlMixin):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

        tID = wx.NewId()

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.list = LegendListCtrl(self, tID,
                                 style=wx.LC_REPORT
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 | wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )


    def PopulateList(self, series_ids ):
        if 1:
            # for normal, simple columns, you can add them like this:
            self.list.InsertColumn(0, "Series ID")

        for series_id in series_ids:
            self.list.Append([series_id])

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE)

        # select the first element
        self.list.CheckItem(0)

class PlotEnum():
    point = 'POINT',
    line = 'LINE',
    bar = 'BAR'

class Data(object):
    def __init__(self, resultid, symbology=''):
        self.resultid = resultid
        self.symbology = symbology


class LegendOvl(FastObjectListView):
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs ):
        FastObjectListView.__init__(self, *args, **kwargs)

        self.initialSeries = [Data("","")]

        #self.setSeries()
        #self.useAlternateBackColors = True
        self.evenRowsBackColor = wx.Colour(255,255,255)
        self.oddRowsBackColor = wx.Colour(255,255,255)
        #self.oddRowsBackColor = wx.Colour(191, 217, 217)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelect)
        self.__list_obj = None
        self.__list_id = None

    def OnListItemSelect(self, event):

        self.__list_obj = event.GetEventObject()
        self.__list_id = event.GetIndex()

    def SetCheckState(self, modelObject, state):
        """
        This is the same code, just added the event inside
        """
        #print "SetCheckState called!"

        if self.checkStateColumn is None:
            return None
        else:
            r = self.checkStateColumn.SetCheckState(modelObject, state)

            # Just added the event here ===================================
            e = OvlCheckEvent(object=modelObject, value=state)
            wx.PostEvent(self, e)
            # =============================================================

            return r

    def _HandleLeftDownOnImage(self, rowIndex, subItemIndex):
        """
        This is the same code, just added the event inside
        """
        #print "_HandleLeftDownOnImage called!", rowIndex, " ", subItemIndex

        column = self.columns[subItemIndex]
        if not column.HasCheckState():
            return

        self._PossibleFinishCellEdit()
        modelObject = self.GetObjectAt(rowIndex)
        #print "modelObject", modelObject, " column", column
        if modelObject is not None:
            column.SetCheckState(modelObject, not column.GetCheckState(modelObject))

            # Just added the event here ===================================
            e = OvlCheckEvent(object=modelObject, value=column.GetCheckState(modelObject))
            wx.PostEvent(self, e)
            # =============================================================

            self.RefreshIndex(rowIndex, modelObject)

class MatplotFrame(wx.Frame):
    def __init__(self, parent, title='', xlabel='', selector=True):

        self.__selector = selector
        self.__image_list = None
        if self.__selector:
            # increase the panel width to fit the selector
            width = 800
            height = 500
        else:
            width = 700
            height = 500

        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = wx.EmptyString,
                          pos = wx.DefaultPosition, size = wx.Size( width,height ),
                          style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        Sizer = wx.BoxSizer(wx.VERTICAL)
        HSizer= wx.BoxSizer(wx.HORIZONTAL)
        self.parent = parent

        # set the color map
        self.__cmap = plt.cm.jet

        # create an instance of the figure
        self.spatialPanel = pnlSpatial(self, title, xlabel, self.cmap)
        HSizer.Add(self.spatialPanel, 1, wx.ALL | wx.EXPAND |wx.GROW, 0)

        if self.__selector:

            self.legend = LegendOvl(self, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
            self.legend.SetColumns([
            ColumnDefn("ResultID", "left", 50, "resultid"),
            ColumnDefn("Symbology", "left", 80, "symbology", imageGetter=self.getSymbology),
            ])

            self.legend.SetObjects([])


            self.legend.CreateCheckStateColumn()
            self.legend.Bind(EVT_OVL_CHECK_EVENT, self.HandleCheckbox)

            #self.legend = LegendListCtrlPanel(self)

            HSizer.Add(self.legend, 1, wx.ALL | wx.EXPAND |wx.GROW, 0)

            # store the base-level legend info to reset the legend later
            self.base_legend_small_imagemap = self.legend.smallImageList.nameToImageIndexMap
            self.base_legend_large_imagemap = self.legend.normalImageList.nameToImageIndexMap
            self.base_legend_small_image_list = self.legend.smallImageList.imageList
            self.base_legend_large_image_list = self.legend.normalImageList.imageList

        Sizer.Add(HSizer)



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
        self.cmap = None
        self.legend_colors = []
        self.__checked_indices = [0]

        Publisher.subscribe(self.update_plot, "SeriesChecked")  # subscribes LegendListControl

    def getSymbology(self, value):
        #print value.resultid
        return value.resultid

    def HandleCheckbox(self, e):

        # if e.value:
        #     print 'Item: %s Checked' % e.object.resultid
        # else:
        #     print 'Item: %s UnChecked' % e.object.resultid

        self.update_plot()

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

        self.__plot_type = PlotEnum.point
        self.build_legend()
        self.plot_initial(type=PlotEnum.point)

    def OnPlotLine(self,event):
        self.__plot_type = PlotEnum.line
        self.build_legend()
        self.plot_initial(type=PlotEnum.line)

    def OnPlotBar(self,event):

        # get the series that are 'checked' in the legend
        #checked_items = self.legend.GetCheckedObjects()

        # if len(checked_items) > 1:
        #         warning = 'Bar plots are not currently supported for multiple time series. :( '
        #         dlg = wx.MessageDialog(self.parent , warning, '', wx.OK | wx.ICON_WARNING)
        #         dlg.ShowModal()
        #         dlg.Destroy()
        #         return

        # else:
        self.__plot_type = PlotEnum.bar
        self.build_legend()
        self.plot_initial(type=PlotEnum.bar)

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
        cmap = self.cmap

        # generate series colors
        num_colors = len(self.xdata)
        #colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

        return attrib

    def update_plot(self):

        # update the checked items list
        self.__checked_indices = [self.legend.GetObjects().index(item) for item in self.legend.GetCheckedObjects()]


        self.plot_initial(self.__plot_type)

        #print 'update plot!'

    def create_legend_thumbnail(self):

        type = self.__plot_type
        i = 0

        if type == PlotEnum.point:
            for item in self.label:
                img = Image.new("RGB", (100,100), "#FFFFFF")
                draw = ImageDraw.Draw(img)

                draw.ellipse((25, 25, 75, 75), fill = self.legend_colors[i]) # fill=(255, 0, 0))
                large = self.CreateThumb(img,(32,32))
                small = self.CreateThumb(img,(16,16))

                self.legend.AddNamedImages(str(item), small, large)
                i+=1
        if type == PlotEnum.line:
            for item in self.label:
                img = Image.new("RGB", (100,100), "#FFFFFF")
                draw = ImageDraw.Draw(img)

                draw.line((0,50,100,50), width = 20, fill = self.legend_colors[i])
                large = self.CreateThumb(img,(32,32))
                small = self.CreateThumb(img,(16,16))

                self.legend.AddNamedImages(str(item), small, large)
                i+=1
        if type == PlotEnum.bar:
            for item in self.label:
                img = Image.new("RGB", (100,100), "#FFFFFF")
                draw = ImageDraw.Draw(img)

                draw.line((50,0,50,100), width = 40, fill = self.legend_colors[i])
                large = self.CreateThumb(img,(32,32))
                small = self.CreateThumb(img,(16,16))

                self.legend.AddNamedImages(str(item), small, large)
                i+=1

    def clear_legend(self):

        # reset all images from image lists
        self.legend.smallImageList.imageList = self.base_legend_small_image_list
        self.legend.normalImageList.imageList = self.base_legend_large_image_list
        self.legend.smallImageList.nameToImageIndexMap = self.base_legend_small_imagemap
        self.legend.normalImageList.nameToImageIndexMap = self.base_legend_large_imagemap

    def build_legend(self):

        #self.legend.ClearAll()
        self.clear_legend()

        data = []
        for l in self.label:
            data.append(Data(str(l),''))

        self.legend.SetObjects(data)

        self.create_legend_thumbnail()


        # check the first item
        # checked_items = self.legend.GetCheckedObjects()
        # if len(checked_items) == 0:
        #     self.legend.ToggleCheck(self.legend.GetObjects()[0])
        for item in self.__checked_indices:
            self.legend.ToggleCheck(self.legend.GetObjects()[item])

    def plot(self, xlist, ylist, labels, cmap=plt.cm.jet):

        # this is the entry point for plotting



        # save the xlist, ylist, and labels globally
        self.xdata = [date2num(x) for x in xlist]
        self.ydata = ylist
        self.label = [str(l) for l in labels]

        # build color map
        num_colors = len(self.xdata)
        self.cmap = [cmap(1.*i/num_colors) for i in range(num_colors)]
        for i in range(num_colors):
            color = list(cmap(1.*i/num_colors))
            self.legend_colors.append((int( color[0] * 255), int(color[1] * 255), int(color[2] * 255), int(color[3] * 100)))



        if self.__selector:

            # rebuild the figure legend
            self.build_legend()

            # initial plotting of the data
            #self.figure = self.plot_initial()



        else:
            self.figure = self.plot_initial()

        self.axis = self.figure.axes[0]

        # build legend
        handles, labels = self.axis.get_legend_handles_labels()
        self.axis.legend(handles, labels, title="Result ID", bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    def CreateThumb(self, pilImage, size):
        #pilImage = Image.open(pathin)
        #size = (16, 16)
        pilImage.thumbnail(size)#, Image.ANTIALIAS)
        image = wx.EmptyImage(pilImage.size[0],pilImage.size[1])
        image.SetData(pilImage.convert("RGB").tostring())
        #image.setAlphaData(pil.convert("RGBA").tostring()[3::4]

        ## use the wx.Image or convert it to wx.Bitmap
        bitmap = wx.BitmapFromImage(image)
        return bitmap

    def plot_initial(self, type=PlotEnum.point):

        # get the series that are 'checked' in the legend
        checked_items = self.legend.GetCheckedObjects()

        self.axis.cla()
        # clear the plot and return if no series are checked
        if len(checked_items) != 0:


            plt_xdata = []
            plt_ydata = []
            plt_labels = []
            plt_colors = []

            # get xlist, ylist, labels, and colors for only the checked items
            for item in checked_items:
                index = self.label.index(item.resultid)
                plt_xdata.append(self.xdata[index])
                plt_ydata.append(self.ydata[index])
                plt_labels.append(self.label[index])
                plt_colors.append(self.cmap[index])

            if type == PlotEnum.point:
                for x,y,label,color in zip(plt_xdata,plt_ydata,plt_labels,plt_colors):
                    self.axis.plot(x, y, label = label, linestyle='None', marker='o', color = color)

            if type == PlotEnum.line:
                for x,y,label,color in zip(plt_xdata,plt_ydata,plt_labels,plt_colors):
                    self.axis.plot(x, y, label = label, linestyle='-',linewidth=1.5, color = color)

            if type == PlotEnum.bar:
                i = 0
                for x,y,label,color in zip(plt_xdata,plt_ydata,plt_labels,plt_colors):
                    # calculate the column width (90% of the difference btwn successive measurements)
                    column_width = min(x[1:-1] - x[0:-2])*.9
                    column_width /= len(plt_labels)
                    # adjust the x values such that they are center aligned on their original x value
                    offset_x = [val - .5*column_width*len(plt_labels)+(i*.5*column_width) for val in x]
                    self.axis.bar(offset_x, y, label = label, color = color, width=column_width)
                    i+=1

            self.axis.xaxis_date()


            # buffer the axis so that values appear within the plot (i.e. not on the edges)
            xbuffer = self.bufferData(plt_xdata, 0.2)
            ybuffer = self.bufferData(plt_ydata,0.21)

            # set axis min and max using the buffer
            self.axis.set_xlim(xbuffer)
            self.axis.set_ylim(ybuffer)
            self.axis.grid()
            self.figure.autofmt_xdate()

            # build legend
            #handles, labels = self.axis.get_legend_handles_labels()
            #self.axis.legend(handles, labels, title="Result ID", bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

        # redraw the figure
        self.figure.canvas.draw()

        return self.figure

    def bufferData(self, datalist, buffer=0.1):
        '''
        calculates a data buffer for the timeseries such that all data will appear on plot (i.e. not along border)
        :param current: (min, max) tuple
        :param data_range: [val1, val2, ..., valn] list of data values
        :param buffer: percentage of value to buffer.  e.g. 0.1 buffers 10%
        :return: returns (min, max) adjusted tuple
        '''

        upper_limit = -9999999999
        lower_limit =  9999999999

        for data in datalist:

            dr = max(data) - min(data)
            upper = max(data) + dr*buffer
            lower = min(data) - dr*buffer

            if upper > upper_limit:
                upper_limit = upper
            if lower < lower_limit:
                lower_limit = lower

        return (lower_limit, upper_limit)


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