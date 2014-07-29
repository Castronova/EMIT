__author__ = 'Mario'

import wx
import wx.xrc

import wx
from wx.lib.floatcanvas.FloatCanvas import FloatCanvas as Canvas
#from wx.lib.floatcanvas.NavCanvas import NavCanvas as Canvas
from wx.lib.pubsub import pub as Publisher

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS, wxID_PNLSUMMARYTREESUMMARY,
] = [wx.NewId() for _init_ctrls in range(5)]

class pnlDetails ( wx.Panel ):

    def __init__( self, prnt ):
        wx.Panel.__init__(self, id=wxID_PNLDETAILS, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        self._data = []
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        #
        # self.m_treeCtrl2 = wx.TreeCtrl( self, id=wx.ID_ANY, pos=wx.Point(50, 50), size=wx.Size(425,250) )
        # bSizer5.Add( self.m_treeCtrl2, 0, wx.ALL, 5 )
        self.treeSummary = MyTree(id=wxID_PNLSUMMARYTREESUMMARY,
               parent=self, pos=wx.Point(0, 0),
              size=wx.Size(423, 319), style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)

        self.SetSizer( bSizer5 )
        self.Layout()


        #self._details = wx.StaticText(self,-1,'test',(0,0))


    def SetData(self,value):
        self._data = value

    def printData(self):

        sometext = "This is placeholder text.  We need to think about what should be displayed here. \n\n"
        sometext += self._data[0].name() +'\n'
        sometext += self._data[1].name()

        #sometext = '\n'.join(self._data[0])



        #self.m_treeCtrl2.SetLabel(sometext)
        #self.m_treeCtrl2.InsertItem(0,0,sometext)


        self.SetLabel(sometext)
        #self.bizer1.Layout()
        self.Layout()

    def __del__( self ):
        pass

class MyTree(wx.TreeCtrl):

    def __init__(self, parent, id, pos, size, style):

        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        self.root = self.AddRoot('Series')
        self.m1 = self.AppendItem(self.root, 'Output Model')
        self.m2 = self.AppendItem(self.root, 'Input Model')
        self.v = self.AppendItem(self.root, 'Variable')

        self.sc=self.AppendItem(self.m1, 'ID: ')
        self.sn=self.AppendItem(self.m1, 'Name: ')

        self.sc=self.AppendItem(self.m2, 'ID: ')
        self.sn=self.AppendItem(self.m2, 'Name: ')

        self.vc=self.AppendItem(self.v, 'ID: ')
        self.vn=self.AppendItem(self.v, 'Name: ')
        self.vu=self.AppendItem(self.v, 'Units: ')
        self.vvt=self.AppendItem(self.v, 'Value Type: ')
        self.vts=self.AppendItem(self.v, 'Time Support: ')
        self.vtu=self.AppendItem(self.v, 'Time Units: ')
        self.vdt=self.AppendItem(self.v, 'Data Type: ')

        self.Bind(wx.EVT_LEFT_UP, self.onClick)

    def onClick(self, e):
        print 'TreeCntrl Clicked'
        #obj = Publisher.sendMessage("GetHitObject", (e, e.EventType))
        self.HitTest(e.GetPostionTuple)


