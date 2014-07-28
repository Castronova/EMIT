__author__ = 'Mario'

import wx
import wx.xrc

import wx
import sys
from wx.lib.pubsub import pub as Publisher

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
] = [wx.NewId() for _init_ctrls in range(4)]

class pnlCreateLink ( wx.Panel ):

    def __init__( self, prnt, inputitems, outputitems ):
        wx.Panel.__init__(self, id=wxID_PNLCREATELINK, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))



        self.selectedinput = None
        self.selectedoutput = None
        self.links = []
        self.inputitems = inputitems
        self.outputitems = outputitems
        self.input = [item.name() for item in inputitems]
        self.output = [item.name() for item in outputitems]


        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_listCtrl1 = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(210, 200), wx.LC_REPORT )
        self.m_listCtrl2 = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(210, 200), wx.LC_REPORT )
        #self.m_button1 = wx.Button( self, wx.ID_ANY, u"Create Link", wx.DefaultPosition, wx.DefaultSize, 0)
        #self.m_button1.Disable()

        bSizer6.Add( self.m_listCtrl1, 0, wx.ALL, 5 )
        bSizer6.Add( self.m_listCtrl2, 0, wx.ALL, 5 )
        #bSizer5.Add( self.m_button1, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )

        #panel = pnlCreateLink(self)
        self.m_listCtrl1.InsertColumn(0, 'input')
        self.m_listCtrl1.SetColumnWidth(0, 200)
        self.m_listCtrl2.InsertColumn(0, 'output')
        self.m_listCtrl2.SetColumnWidth(0, 200)

        self.m_listCtrl1.Bind(wx.EVT_LIST_ITEM_SELECTED, self.InputSelect)
        self.m_listCtrl1.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.InputDeselect)
        self.m_listCtrl2.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OutputSelect)
        self.m_listCtrl2.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OutputDeselect)
        #self.m_button1.Bind(wx.EVT_LEFT_DOWN, self.CreateLink)
        self.Bind

        #wx.StaticText(self, -1,"Error", pos = (20, 200))

        # deactivate Next button
        self.activateLinkButton()


        for i in inputitems:
            self.m_listCtrl1.InsertStringItem(sys.maxint, i.name())


        for i in outputitems:
            self.m_listCtrl2.InsertStringItem(sys.maxint, i.name())

        self.SetSizer( bSizer1 )
        self.Layout()

    def activateLinkButton(self):
        if self.selectedinput is not None and self.selectedoutput is not None:
            #self.m_button1.Enable()
            Publisher.sendMessage("activateNextButton")
        else:
            #self.m_button1.Disable()
            Publisher.sendMessage("deactivateNextButton")

    def InputSelect(self, event):

        self.selectedinput = self.inputitems[event.GetIndex()]
        #self.selectedinput = event.Text

        self.activateLinkButton()

    def InputDeselect(self, event):

        self.selectedinput = None

        self.activateLinkButton()

    def OutputSelect(self, event):

        self.selectedoutput = self.outputitems[event.GetIndex()]

        self.activateLinkButton()

    def OutputDeselect(self, event):

        self.selectedoutput = None

        self.activateLinkButton()

    def CreateLink(self, event):
        link = [self.selectedinput, self.selectedoutput]
        if link not in self.links:
            self.links.append(link)
        else:
            error = wx.StaticText(self, "There was an error creating the links, please check your parameters.",
                                  pos=(0, 220))
            error.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
            # print an error message

        #deselect input
        #deselect output
        # deactivate link
        # return link info and print this below/above the "createlink" button
        # call cmdline function to create thge link object
        # change selected item background
        # inputselected (amd output) display item unit and variable somewhere


    def __del__( self ):
        pass