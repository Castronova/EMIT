__author__ = 'Mario'

from matplotlib.dates import date2num
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavToolbar
import wx
import wx.lib.newevent
from wx.lib.pubsub import pub as Publisher
from environment import env_vars
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

class PlotPanel(wx.Panel):
    def __init__(self, parent):

        wx.Panel.__init__(self, id=wx.ID_ANY, name=u'PlotPanel', parent=parent, style=wx.TAB_TRAVERSAL)
        self.parent = parent

        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        # put up a figure
        self.figure = plt.figure()
        self.axes = self.figure.add_subplot(1, 1, 1)

        self.axes.grid()
        self.axes.axis('auto')
        self.axes.margins(0)

        self.canvas = FigureCanvas(self, -1, self.figure)
        sizer.Add(self.canvas, 100, wx.ALIGN_CENTER | wx.ALL)

    def Axis(self):
        return self.axes

    def Figure(self):
        return self.figure




class ViewPlot(wx.Frame):
    def __init__(self, parent, title='', xlabel='', ylabel='', selector=True):

        self.selector = selector
        self.__image_list = None
        if env_vars.LEGEND_LOCATIONRIGHT == 1:

            if selector:
                # increase the panel width to fit the selector
                width = 1000  # 800 if right
                height = 500  # 500 if right
            else:
                width = 700
                height = 500
        else:

            if selector:
                # increase the panel width to fit the selector
                width = 600  # 800 if right
                height = 600  # 500 if right
            else:
                width = 700
                height = 500

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString,
                          pos=wx.DefaultPosition, size=wx.Size(width, height),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        if env_vars.LEGEND_LOCATIONRIGHT == 1:
            #  self.Sizer = wx.BoxSizer(wx.VERTICAL)
            self.Sizer = wx.BoxSizer(wx.HORIZONTAL)
            self.HSizer = wx.BoxSizer(wx.HORIZONTAL)
            #  self.HSizer = wx.BoxSizer(wx.VERTICAL)
        else:
            self.Sizer = wx.BoxSizer(wx.VERTICAL)
            self.HSizer = wx.BoxSizer(wx.VERTICAL)

        self.parent = parent

        # set the color map
        self.cmap = plt.cm.jet

        # create an instance of the figure
        self.plotPanel = PlotPanel(parent)

        self.HSizer.Add(self.plotPanel, 1, wx.ALL | wx.EXPAND | wx.GROW, 0)

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
            self.axis = self.plotPanel.Axis()

            # intializer for figure
            self.figure = self.plotPanel.Figure()

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
        #self.build_menu()
