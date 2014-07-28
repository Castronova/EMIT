import wx
import wx.xrc
import LinkWizard

###########################################################################
## Class MyFrame1
###########################################################################

class LinkStart ( wx.Frame ):

    def __init__( self, parent, from_model, to_model, input, output, cmd):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,250 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )



        self.input = input
        self.output = output
        self.FloatCanvas = parent
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.cmd = cmd
        self.from_model = from_model
        self.to_model = to_model

        bSizer1 = wx.BoxSizer( wx.HORIZONTAL )
        self.panel1 = wx.Panel( self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL)
        bSizer1.Add(self.panel1, 1, wx.EXPAND | wx.ALL, 5)

        self.m_listCtrl1 = wx.ListCtrl( self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(400, 230), style=wx.LC_REPORT )
        self.m_listCtrl1.InsertColumn(0, 'links')
        self.m_listCtrl1.SetColumnWidth(0, 200)

        self.panel1.AddChild( self.m_listCtrl1)

        bSizer2 = wx.BoxSizer( wx.VERTICAL )
        self.panel2 = wx.Panel( self, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.TAB_TRAVERSAL)
        bSizer2.Add(self.panel2, 1, wx.EXPAND | wx.ALL, 5)

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

        # populate listctrl with links
        self.PopulateLinks()


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

    def AddClick(self, event):
        linkwiz = LinkWizard.wizLink(self.FloatCanvas, self.from_model.get_id(), self.to_model.get_id(), self.output, self.input, self.cmd)

        self.PopulateLinks()

    def RemoveClick(self, event):
        pass

    def CloseClick(self, event):
        self.Destroy()

    def PopulateLinks(self):

        links = self.cmd.get_links_btwn_models(self.from_model.get_id(), self.to_model.get_id())

        for link in links:
            text = "%s : %s --> %s : %s"%(link[0][0].get_name(),link[0][1].name(),link[1][0].get_name(),link[1][1].name())

            #text = 'This is overflowing'
            self.m_listCtrl1.InsertStringItem(0, text)


    def __del__( self ):
        pass
