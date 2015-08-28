__author__ = 'tonycastronova'

import wx
import seaborn as sns
from gui.views.viewPlot import ViewPlot, Data
from PIL import Image, ImageDraw
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
from gui.controller.enums import PlotEnum
from wx.lib.pubsub import pub as Publisher

sns.set_style("ticks")


class LogicPlot(ViewPlot):

    def __init__(self, parent, title='', xlabel='', ylabel='', selector=True):

        ViewPlot.__init__(self, parent, title=title, xlabel=xlabel, ylabel=ylabel, selector=selector)


    def getSymbology(self, value):
        return value.resultid

    def HandleCheckbox(self, e):
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
            self.cmap = value
        return self.cmap

    def OnPlotPoint(self,event):

        self.plot_type = PlotEnum.point
        self.build_legend()
        self.plot_initial(type=PlotEnum.point)

    def OnPlotLine(self,event):
        self.plot_type = PlotEnum.line
        self.build_legend()
        self.plot_initial(type=PlotEnum.line)

    def OnPlotBar(self,event):

        # get the series that are 'checked' in the legend
        self.plot_type = PlotEnum.bar
        self.build_legend()
        self.plot_initial(type=PlotEnum.bar)

    def rip_data_from_axis(self):
        attrib = []
        attrib.append('self.axis.set_title("%s")'% self.axis.get_title())
        attrib.append('self.axis.set_ylabel("%s")'% self.axis.get_ylabel())
        attrib.append('self.axis.set_xlabel("%s")' % self.axis.get_xlabel())

        # get the cmap
        cmap = self.cmap

        # generate series colors
        num_colors = len(self.xdata)

        return attrib

    def update_plot(self):

        # update the checked items list
        self.checked_indices = [self.legend.GetObjects().index(item) for item in self.legend.GetCheckedObjects()]

        self.plot_initial(self.plot_type)


    def create_legend_thumbnail(self):

        type = self.plot_type
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

        self.clear_legend()

        data = []
        for l in self.label:
            data.append(Data(str(l),''))

        self.legend.SetObjects(data)

        self.create_legend_thumbnail()


        # check the first item
        for item in self.checked_indices:
            self.legend.ToggleCheck(self.legend.GetObjects()[item])

    def plot(self, xlist, ylist, labels, cmap=plt.cm.jet):

        # --- this is the entry point for plotting ---

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

        if self.selector:

            # rebuild the figure legend
            self.build_legend()

        else:
            self.figure = self.plot_initial()

        self.axis = self.figure.axes[0]

        # build legend
        handles, labels = self.axis.get_legend_handles_labels()
        self.axis.legend(handles, labels, title="Result ID", bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


    def CreateThumb(self, pilImage, size):
        pilImage.thumbnail(size)#, Image.ANTIALIAS)
        image = wx.EmptyImage(pilImage.size[0],pilImage.size[1])
        image.SetData(pilImage.convert("RGB").tostring())
        bitmap = wx.BitmapFromImage(image)
        return bitmap

    def plot_initial(self, type=PlotEnum.point):

        # get the series that are 'checked' in the legend
        checked_items = self.legend.GetCheckedObjects()

        # clear the plot and return if no series are checked
        self.axis.cla()
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
                    sns.despine(right=True, top=True)
            if type == PlotEnum.line:
                for x,y,label,color in zip(plt_xdata,plt_ydata,plt_labels,plt_colors):
                    self.axis.plot(x, y, label = label, linestyle='-',linewidth=1.5, color = color)
                    sns.despine(right=True, top=True)

            if type == PlotEnum.bar:
                i = 0
                for x,y,label,color in zip(plt_xdata,plt_ydata,plt_labels,plt_colors):
                    # calculate the column width (90% of the difference btwn successive measurements)
                    column_width = min(x[1:-1] - x[0:-2])*.9
                    column_width /= len(plt_labels)
                    # adjust the x values such that they are center aligned on their original x value
                    offset_x = [val - .5*column_width*len(plt_labels)+(i*.5*column_width) for val in x]
                    self.axis.bar(offset_x, y, label = label, color = color, width=column_width)
                    sns.despine(right=True, top=True)

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

            self.axis.set_ylabel(self.y_label)
            self.axis.set_xlabel(self.x_label)
            self.figure.suptitle(self.title)

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