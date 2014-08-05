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

class MatplotFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id = wx.ID_ANY, title = wx.EmptyString,
                          pos = wx.DefaultPosition, size = wx.Size( 500,300 ),
                          style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        Sizer = wx.BoxSizer(wx.VERTICAL)

        spatialPanel = pnlSpatial(self)

        Sizer.Add( spatialPanel)

        self.SetSizer(Sizer)
        self.Layout()
        self.Centre(wx.BOTH)

class pnlSpatial ( wx.Panel ):

    def __init__( self, prnt):
        wx.Panel.__init__(self, id=wxID_PNLSPATIAL, name=u'pnlIntro', parent=prnt,
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(10, 10))

        self.parent = prnt


        # create some sizers
        sizer = wx.BoxSizer(wx.VERTICAL)

        # A button
        self.button =wx.Button(self, label="Placeholder")
        self.radiobutton1 = wx.RadioButton(self, wx.ID_ANY, u"Placeholder")
        self.radiobutton2 = wx.RadioButton(self, wx.ID_ANY, u"Placeholder")
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)

        # put up a figure
        self.figure = plt.figure()
        self.axes = self.drawplot(self.figure)
        self.canvas = FigureCanvas(self, -1, self.figure)

        sizer.Add(self.canvas, 100, wx.ALIGN_CENTER|wx.ALL)
        sizer.Add(self.button, 0, wx.ALIGN_CENTER|wx.ALL)
        sizer.Add(self.radiobutton1, 0, wx.ALIGN_CENTER|wx.ALL)
        sizer.Add(self.radiobutton2, 0, wx.ALIGN_CENTER|wx.ALL)

        self.SetSizer(sizer)
        #self.Fit()
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