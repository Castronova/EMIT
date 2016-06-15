import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sb
sb.set_style("ticks")


class Plotter:
    def __init__(self, panel):
        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.axes.grid()

        self.axes.margins(0)
        self.plot = FigureCanvas(panel, -1, self.figure)

    def add_padding_to_plot(self, left=None, bottom=None, right=None, top=None, wspace=None, hspace=None):
        """
        Adjust the location of the plot. Parameters must be floats
        :param left:
        :param bottom:
        :param right:
        :param top:
        :param wspace:
        :param hspace:
        :return:
        """
        # self.figure.tight_layout() is also another possible way to do this
        self.figure.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

    def display_legend(self, location='upper right'):
        """
        Taken from http://matplotlib.org/api/figure_api.html
        'best'         : 0,
        'upper right'  : 1,
        'upper left'   : 2,
        'lower left'   : 3,
        'lower right'  : 4,
        'right'        : 5,
        'center left'  : 6,
        'center right' : 7,
        'lower center' : 8,
        'upper center' : 9,
        'center'       : 10,
        """
        self.axes.legend(loc=location)
        self.redraw()

    def redraw(self):
        """
        Call after adding all desired features to the graph
        :return:
        """
        self.plot.draw()

    def rotate_x_axis_label(self, angle=45):
        """
        Rotates the x-axis labels
        Must be called before redrawing to have effect
        :param angle: angle of rotation
        :return:
        """
        for label in self.axes.xaxis.get_ticklabels():
            label.set_rotation(angle)

    def set_axis_label(self, x="", y=""):
        self.axes.set_xlabel(x)
        self.axes.set_ylabel(y)

    def set_legend(self, labels, location=0):
        """
        Taken from http://matplotlib.org/api/figure_api.html
        'best'         : 0,
        'upper right'  : 1,
        'upper left'   : 2,
        'lower left'   : 3,
        'lower right'  : 4,
        'right'        : 5,
        'center left'  : 6,
        'center right' : 7,
        'lower center' : 8,
        'upper center' : 9,
        'center'       : 10,
        The len(labels) needs to match the number of graphs drawn to show all legends added
        :param labels: type([string])
        :param location: type(int)
        :return:
        """
        self.axes.legend(labels, loc=location)

    def set_title(self, title):
        self.axes.set_title(str(title))

    def set_x_axis_label_font_size(self, font_size=10):
        """
        Must be called before redrawing to have effect
        :param font_size:
        :return:
        """
        for label in self.axes.xaxis.get_ticklabels():
            label.set_fontsize(font_size)
