__author__ = 'Mario'

import wx
import wx.xrc

import wx

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
] = [wx.NewId() for _init_ctrls in range(4)]

class pnlDetails ( wx.Panel ):

    def __init__( self, prnt ):
        wx.Panel.__init__(self, id=wxID_PNLDETAILS, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        self._data = []
        bSizer5 = wx.BoxSizer( wx.VERTICAL )

        self.m_treeCtrl2 = wx.TreeCtrl( self, id=wx.ID_ANY, pos=wx.Point(50, 50), size=wx.Size(425,250) )
        bSizer5.Add( self.m_treeCtrl2, 0, wx.ALL, 5 )


        self.SetSizer( bSizer5 )
        self.Layout()


        #self._details = wx.StaticText(self,-1,'test',(0,0))


    def SetData(self,value):
        self._data = value

    def printData(self):

        sometext = "This is placeholder text.  We need to think about what should be displayed here. \n\n"
        sometext += self._data[0].name() +'\n'
        sometext+= self._data[1].name()

        #sometext = '\n'.join(self._data[0])



        #self.m_treeCtrl2.SetLabel(sometext)
        #self.m_treeCtrl2.InsertItem(0,0,sometext)


        self.SetLabel(sometext)
        #self.bizer1.Layout()
        self.Layout()





    def __del__( self ):
        pass