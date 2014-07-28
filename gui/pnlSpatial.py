__author__ = 'Mario'

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
import wx

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
] = [wx.NewId() for _init_ctrls in range(4)]

class pnlSpatial ( wx.Panel ):

    def __init__( self, prnt ):
        wx.Panel.__init__(self, id=wxID_PNLSPATIAL, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        self.parent = prnt

        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        # A button
        self.button =wx.Button(self, label="Placeholder")
        self.radiobutton = wx.RadioButton(self, wx.ID_ANY, u"Set Unit as Smallest Possible")
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

        # put up a figure
        self.figure = plt.figure()
        self.axes = self.drawplot(self.figure)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer.Add(self.canvas, 0, wx.ALIGN_CENTER|wx.ALL)
        sizer.Add(self.button, 0, wx.ALIGN_CENTER|wx.ALL)
        sizer.Add(self.radiobutton, 0, wx.ALIGN_CENTER|wx.ALL)

        self.SetSizerAndFit(sizer)
        self.Fit()
    def log(self, fmt, *args):
        print (fmt % args)
    def OnClick(self,event):
        self.log("button clicked, id#%d\n", event.GetId())
    def drawplot(self, fig):
        ax = fig.add_subplot(1,1,1)
        t = np.arange(0,1,0.001)
        ax.plot(t,t*t)
        ax.grid()
        return ax

        # self.Sizer = wx.BoxSizer( wx.VERTICAL )
        # self.Sizerpnl = wx.BoxSizer(wx.VERTICAL)
        # self.Sizer2 = wx.BoxSizer(wx.VERTICAL)
        #
        # self.plotpnl = wx.Panel( self,id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(425,250), style=wx.TAB_TRAVERSAL )
        # self.Sizer.Add( self.plotpnl, 1, wx.EXPAND |wx.ALL, 5 )
        # self.Sizerpnl.Fit(self.plotpnl)
        #
        # self.m_panel2 = wx.Panel( self,id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(425,95), style=wx.TAB_TRAVERSAL )
        # self.Sizer.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )
        # self.Sizer2.Fit(self.m_panel2)
        #
        # self.m_radioBtn1 = wx.RadioButton( self, wx.ID_ANY, u"Set Unit as Smallest Possible", wx.DefaultPosition, wx.DefaultSize, 0 )
        # self.Sizer2.Add( self.m_radioBtn1, 0, wx.ALL, 5 )
        #
        # self.plotpnl.figure = Figure()
        # self.plotpnl.axes = self.plotpnl.figure.add_subplot(111)
        # self.plotpnl.canvas = FigureCanvas(self, -1, self.plotpnl.figure)
        # self.Sizerpnl.Add(self.plotpnl.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
        # self.SetSizer(self.Sizerpnl)
        # self.plotpnl.Fit()


##########################################################################################

        # np.random.seed(1234)
        #
        # Nsteps = 500
        # t = np.arange(Nsteps)
        #
        # mu = 0.002
        # sigma = 0.01
        #
        # # the steps and position
        # S = mu + sigma*np.random.randn(Nsteps)
        # X = S.cumsum()
        #
        # # the 1 sigma upper and lower analytic population bounds
        # lower_bound = mu*t - sigma*np.sqrt(t)
        # upper_bound = mu*t + sigma*np.sqrt(t)
        #
        # fig, ax = plt.subplots(1)
        # ax.plot(t, X, lw=2, label='walker position', color='blue')
        # ax.plot(t, mu*t, lw=1, label='population mean', color='black', ls='--')
        # ax.fill_between(t, lower_bound, upper_bound, facecolor='yellow', alpha=0.5,
        #                 label='1 sigma range')
        # ax.legend(loc='upper left')
        #
        # # here we use the where argument to only fill the region where the
        # # walker is above the population 1 sigma boundary
        # ax.fill_between(t, upper_bound, X, where=X>upper_bound, facecolor='blue', alpha=0.5)
        # ax.set_xlabel('num steps')
        # ax.set_ylabel('position')
        # ax.grid()

        # self.SetSizer( self.Sizer )
        # self.Layout()
