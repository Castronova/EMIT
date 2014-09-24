__author__ = 'Mario'

import wx
import wx.propgrid as wxpg

[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS, wxID_PNLSUMMARYTREESUMMARY,
] = [wx.NewId() for _init_ctrls in range(5)]

class pnlDetails ( wx.Panel ):

    def __init__( self, prnt ):
        wx.Panel.__init__(self, id=wxID_PNLDETAILS, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))
        self.panel = panel = wx.Panel(self, wx.ID_ANY)

        self._data = []
        bSizer5 = wx.BoxSizer( wx.VERTICAL )
        #
        # self.m_treeCtrl2 = wx.TreeCtrl( self, id=wx.ID_ANY, pos=wx.Point(50, 50), size=wx.Size(425,250) )
        # bSizer5.Add( self.m_treeCtrl2, 0, wx.ALL, 5 )
        self.pg = pg = wxpg.PropertyGridManager(panel,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT |
                              wxpg.PG_TOOLBAR)

        self.SetSizer( bSizer5 )

        # Show help as tooltips
        pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)
        self.Layout()

