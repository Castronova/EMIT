__author__ = 'Mario'

from matplotlib.dates import date2num
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavToolbar
import wx
import wx.lib.newevent
from wx.lib.pubsub import pub as Publisher

from gui.controller.enums import PlotEnum


# todo: refactor
from ..ObjectListView import FastObjectListView, ColumnDefn

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
 ] = [wx.NewId() for _init_ctrls in range(4)]

OvlCheckEvent, EVT_OVL_CHECK_EVENT = wx.lib.newevent.NewEvent()


class Data(object):
    def __init__(self, resultid, symbology=''):
        self.resultid = resultid
        self.symbology = symbology


class ViewLegend(FastObjectListView):
    # ----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        FastObjectListView.__init__(self, *args, **kwargs)

        self.evenRowsBackColor = wx.Colour(255, 255, 255)
        self.oddRowsBackColor = wx.Colour(255, 255, 255)


class LogicLegend(ViewLegend):
    def __init__(self, parent):

        ViewLegend.__init__(self, parent, wx.ID_ANY, style=wx.LC_REPORT | wx.SUNKEN_BORDER)

        self.initialSeries = [Data("", "")]
        self.__list_obj = None
        self.__list_id = None
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnListItemSelect)

    def OnListItemSelect(self, event):

        self.__list_obj = event.GetEventObject()
        self.__list_id = event.GetIndex()

    def SetCheckState(self, modelObject, state):
        """
        This is the same code, just added the event inside
        """
        # print "SetCheckState called!"

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
        # print "_HandleLeftDownOnImage called!", rowIndex, " ", subItemIndex

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


class ViewPlot(wx.Frame):
    def __init__(self, parent, title='', xlabel='', ylabel='', selector=True):

        self.selector = selector
        self.__image_list = None
        if selector:
            # increase the panel width to fit the selector
            width = 800
            height = 500
        else:
            width = 700
            height = 500

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                          pos=wx.DefaultPosition, size=wx.Size(width, height),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.Sizer = wx.BoxSizer(wx.VERTICAL)
        self.HSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.parent = parent

        # set the color map
        self.cmap = plt.cm.jet

        # create an instance of the figure
        self.spatialPanel = pnlSpatial(self, title, xlabel, self.cmap)
        self.HSizer.Add(self.spatialPanel, 1, wx.ALL | wx.EXPAND | wx.GROW, 0)

        if selector:
            self.legend = LogicLegend(self)
            self.legend.SetColumns([
                ColumnDefn("ResultID", "left", 50, "resultid"),
                ColumnDefn("Symbology", "left", 80, "symbology", imageGetter=self.getSymbology),
            ])

            self.legend.SetObjects([])

            self.legend.CreateCheckStateColumn()
            self.legend.Bind(EVT_OVL_CHECK_EVENT, self.HandleCheckbox)

            # inherited from ViewPlot
            self.HSizer.Add(self.legend, 1, wx.ALL | wx.EXPAND | wx.GROW, 0)

            # store the base-level legend info to reset the legend later
            self.base_legend_small_imagemap = self.legend.smallImageList.nameToImageIndexMap
            self.base_legend_large_imagemap = self.legend.normalImageList.nameToImageIndexMap
            self.base_legend_small_image_list = self.legend.smallImageList.imageList
            self.base_legend_large_image_list = self.legend.normalImageList.imageList

            # set the default plot type
            self.plot_type = PlotEnum.point

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
            self.checked_indices = [0]
            self.x_label = xlabel
            self.y_label = ylabel
            self.title = title

            Publisher.subscribe(self.update_plot, "SeriesChecked")  # subscribes LegendListControl

        self.Sizer.Add(self.HSizer)
        self.SetSizer(self.Sizer)
        self.Layout()
        self.Centre(wx.BOTH)

        # build custom menu bar
        self.build_menu()


class pnlSpatial(wx.Panel):
    def __init__(self, prnt, title, xlabel, cmap):
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
        self.axis = self.figure.add_subplot(1, 1, 1)
        self.figure.autofmt_xdate()

        # self.axis.grid()
        self.axis.set_title(title)
        self.axis.set_ylabel(xlabel)

        self.canvas = FigureCanvas(self, -1, self.figure)
        self.toolbar = NavToolbar(self.canvas)
        self.figure.tight_layout()
        plt.subplots_adjust(
            top=.9, left=.1, right=.9, bottom=.15
        )
        #self.figure.tight_layout()

        sizer.Add(self.toolbar, 0, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND | wx.GROW, 1)
        sizer.Add(self.canvas, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND | wx.GROW, 1)
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
    # dates = date2num(x)
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
        colors = [cmap(1. * i / num_colors) for i in range(num_colors)]

        # plots = []
        # ax = self.figure.axes[0]
        #ax = self.axis
        i = 0
        for x, y in zip(xlist, ylist):
            dates = date2num(x)
            self.axis.plot_date(dates, y, label=labels[i], color=colors[i])
            # plots.append(p)

            i += 1

        #self.axis.grid()
        #self.figure.autofmt_xdate()

        #fig.colorbar(plots)
        #plt.show()
        #self.figure.tight_layout()
        return self.figure