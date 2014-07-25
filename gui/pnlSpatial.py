__author__ = 'Mario'

import wx
import wx.xrc

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

        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_listCtrl4 = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON )
        self.m_listCtrl5 = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON )
        self.m_button3 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_button4 = wx.Button( self, wx.ID_ANY, u"MyButton", wx.DefaultPosition, wx.DefaultSize, 0 )

        bSizer6.Add( self.m_listCtrl4, 0, wx.ALL, 5 )
        bSizer6.Add( self.m_listCtrl5, 0, wx.ALL, 5 )
        bSizer5.Add( self.m_button3, 0, wx.ALL, 5 )
        bSizer5.Add( self.m_button4, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

    def __del__( self ):
        pass