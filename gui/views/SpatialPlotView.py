__author__ = 'tonycastronova'

import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas


class ViewSpatialPlot(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent=parent, name="SpatialPlot", size=(650, 700),
                          style=wx.TAB_TRAVERSAL | wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)

        self.parent = parent

        panel = wx.Panel(self)
        top_panel = wx.Panel(panel)
        bottom_panel = wx.Panel(panel)

        # top_panel.SetBackgroundColour("#AABBCC")

        #  Top Panel/Plotting Panel
        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(1, 1, 1)
        self.ax.xaxis._visible = True
        self.ax.yaxis._visible = True
        self.canvas = FigureCanvas(top_panel, -1, self.figure)

        vbox_plot_panel = wx.BoxSizer(wx.VERTICAL)
        gbs = wx.GridBagSizer(vgap=5, hgap=5)

        vbox_plot_panel.Add(self.canvas, 1, wx.ALL | wx.EXPAND, 2)
        top_panel.SetSizer(vbox_plot_panel)

        #  Bottom Panel/Info Panel
        textLabel = wx.StaticText(bottom_panel, wx.ID_ANY, label='Toggle the Input and Output exchange element sets: ')
        textLabel.SetFont(wx.Font(14, 70, 90, 92, False, wx.EmptyString))
        inputLabel = wx.StaticText(bottom_panel, label="Input Features: ")
        outputLabel = wx.StaticText(bottom_panel, label="Output Features: ")
        self.inputSelection = wx.CheckBox(bottom_panel, id=998, label="Input Exchange Item: ")
        self.outputSelection = wx.CheckBox(bottom_panel, id=999, label="Output Exchange Item: ")

        gbs.Add(textLabel, pos=(1, 0), span=(1, 3), flag=wx.LEFT, border=10)
        gbs.Add(inputLabel, pos=(2, 0), flag=wx.LEFT, border=10)
        gbs.Add(self.inputSelection, pos=(2, 1), flag=wx.LEFT, border=10)
        gbs.Add(outputLabel, pos=(3, 0), flag=wx.LEFT, border=10)
        gbs.Add(self.outputSelection, pos=(3, 1), flag=wx.LEFT, border=10)
        bottom_panel.SetSizer(gbs)

        # bottom_panel.SetBackgroundColour("#CCBBAA")

        main_sizer_panel = wx.BoxSizer(wx.VERTICAL)
        main_sizer_panel.Add(top_panel, 1, wx.EXPAND | wx.ALL, 2)
        main_sizer_panel.Add(bottom_panel, 1, wx.EXPAND | wx.ALL, 2)

        panel.SetSizer(main_sizer_panel)

        self.intext = plt.figtext(0.12, 0.94, " ", fontsize='large', color='b', ha='left')
        self.outtext = plt.figtext(0.9, 0.94, " ", fontsize='large', color='r', ha='right')

        self.CenterOnScreen()
        self.Show()
