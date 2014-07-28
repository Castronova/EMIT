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

        self.Sizer = wx.BoxSizer( wx.VERTICAL )

        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.Sizer.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)

        Nsteps, Nwalkers = 100, 250
        t = np.arange(Nsteps)

        # an (Nsteps x Nwalkers) array of random walk steps
        S1 = 0.002 + 0.01*np.random.randn(Nsteps, Nwalkers)
        S2 = 0.004 + 0.02*np.random.randn(Nsteps, Nwalkers)

        # an (Nsteps x Nwalkers) array of random walker positions
        X1 = S1.cumsum(axis=0)
        X2 = S2.cumsum(axis=0)


        # Nsteps length arrays empirical means and standard deviations of both
        # populations over time
        mu1 = X1.mean(axis=1)
        sigma1 = X1.std(axis=1)
        mu2 = X2.mean(axis=1)
        sigma2 = X2.std(axis=1)

        # plot it!
        fig, ax = plt.subplots(1)
        ax.plot(t, mu1, lw=2, label='mean population 1', color='blue')
        ax.plot(t, mu1, lw=2, label='mean population 2', color='yellow')
        ax.fill_between(t, mu1+sigma1, mu1-sigma1, facecolor='blue', alpha=0.5)
        ax.fill_between(t, mu2+sigma2, mu2-sigma2, facecolor='yellow', alpha=0.5)
        ax.set_title('random walkers empirical $\mu$ and $\pm \sigma$ interval')
        ax.legend(loc='upper left')
        ax.set_xlabel('num steps')
        ax.set_ylabel('position')
        ax.grid()

        self.SetSizer( self.Sizer )
        self.Layout()
    '''
    def draw(self):
        Nsteps, Nwalkers = 100, 250
        t = np.arange(Nsteps)

        # an (Nsteps x Nwalkers) array of random walk steps
        S1 = 0.002 + 0.01*np.random.randn(Nsteps, Nwalkers)
        S2 = 0.004 + 0.02*np.random.randn(Nsteps, Nwalkers)

        # an (Nsteps x Nwalkers) array of random walker positions
        X1 = S1.cumsum(axis=0)
        X2 = S2.cumsum(axis=0)


        # Nsteps length arrays empirical means and standard deviations of both
        # populations over time
        mu1 = X1.mean(axis=1)
        sigma1 = X1.std(axis=1)
        mu2 = X2.mean(axis=1)
        sigma2 = X2.std(axis=1)

        # plot it!
        fig, ax = plt.subplots(1)
        ax.plot(t, mu1, lw=2, label='mean population 1', color='blue')
        ax.plot(t, mu1, lw=2, label='mean population 2', color='yellow')
        ax.fill_between(t, mu1+sigma1, mu1-sigma1, facecolor='blue', alpha=0.5)
        ax.fill_between(t, mu2+sigma2, mu2-sigma2, facecolor='yellow', alpha=0.5)
        ax.set_title('random walkers empirical $\mu$ and $\pm \sigma$ interval')
        ax.legend(loc='upper left')
        ax.set_xlabel('num steps')
        ax.set_ylabel('position')
        ax.grid()
    '''
