__author__ = 'Mario'

import wx
import wx.xrc

import wx

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
] = [wx.NewId() for _init_ctrls in range(4)]

class pnlTemporal ( wx.Panel ):

    def __init__( self, prnt ):
        wx.Panel.__init__(self, id=wxID_PNLTEMPORAL, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        m_radioBox1Choices = [ u"PlaceHolder", "PlaceHolder",  "PlaceHolder"]
        self.m_radioBox1 = wx.RadioBox( self, wx.ID_ANY, u"Temporal Shift", wx.DefaultPosition, wx.DefaultSize, m_radioBox1Choices, 1, wx.RA_SPECIFY_COLS )
        self.m_radioBox1.SetSelection( 0 )
        bSizer6.Add( self.m_radioBox1, 0, wx.ALL, 5 )

        m_radioBox2Choices = [ u"PlaceHolder", "PlaceHolder", "PlaceHolder", "PlaceHolder", "PlaceHolder" ]
        self.m_radioBox2 = wx.RadioBox( self, wx.ID_ANY, u"Time Range", wx.DefaultPosition, wx.DefaultSize, m_radioBox2Choices, 1, wx.RA_SPECIFY_COLS )
        self.m_radioBox2.SetSelection( 0 )
        bSizer6.Add( self.m_radioBox2, 0, wx.ALL, 5 )

        self.m_radioBtn1 = wx.RadioButton( self, wx.ID_ANY, u"PlaceHolder", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_radioBtn1, 0, wx.ALL, 5 )


        self.SetSizer( bSizer6 )
        self.Layout()

    def __del__( self ):
        pass