import wx
import wx.xrc
import LinkWizard

###########################################################################
## Class MyFrame1
###########################################################################

class LinkStart ( wx.Frame ):

    def __init__( self, parent, input, output):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.input = input
        self.output = output
        self.FloatCanvas = parent
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_listCtrl1 = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LC_ICON )
        bSizer1.Add( self.m_listCtrl1, 0, wx.ALL, 5 )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_button1 = wx.Button( self, wx.ID_ANY, u"Add", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button1, 0, wx.ALL, 5 )

        self.m_button2 = wx.Button( self, wx.ID_ANY, u"Remove", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button2, 0, wx.ALL, 5 )

        self.m_button3 = wx.Button( self, wx.ID_ANY, u"Close", wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer2.Add( self.m_button3, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer2, 1, wx.EXPAND, 5 )

        self.m_button1.Bind(wx.EVT_LEFT_DOWN, self.AddClick)
        self.m_button2.Bind(wx.EVT_LEFT_DOWN, self.RemoveClick)
        self.m_button3.Bind(wx.EVT_LEFT_DOWN, self.CloseClick)


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

    def AddClick(self, event):
        linkwiz = LinkWizard.wizLink(self.FloatCanvas, self.input, self.output)


    def RemoveClick(self, event):
        pass

    def CloseClick(self, event):
        self.Destroy()


    def __del__( self ):
        pass
