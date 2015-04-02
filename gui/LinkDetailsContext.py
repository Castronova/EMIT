__author__ = 'mario'

import wx
import wx.xrc
import wx.propgrid as wxpg

class LinkDetailsContextActivatedFrame ( wx.Frame ):

    def __init__( self, parent, link, cmd ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.link = link
        # self.output = output
        self.FloatCanvas = parent
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.cmd = cmd
        # self.from_model = from_model
        # self.to_model = to_model

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.pg = pg = wxpg.PropertyGridManager(self.m_panel1,
                    style=wxpg.PG_SPLITTER_AUTO_CENTER |
                          wxpg.PG_AUTO_SORT |
                          wxpg.PG_PROP_READONLY)

        self.SetSizer( bSizer1 )


        self.pg.AddPage( "Link Details" )

        bSizer2.Add(self.pg, 1, wx.EXPAND|wx.ALL, 5)
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )
        self.m_panel1.SetSizer( bSizer2)
        self.m_panel1.Layout()
        bSizer2.Fit(self.m_panel1)

        # bSizer1.Add(pg, 1, wx.EXPAND)



        self.pg.Append( wxpg.PropertyCategory("Input Item") )
        self.pg.Append( wxpg.StringProperty("Variable Name (input)",value=str(self.link[0].source_exchange_item()._ExchangeItem__name ) ))
        self.pg.Append( wxpg.StringProperty("Variable Description (input)",value= str(self.link[0].source_exchange_item()._ExchangeItem__description) ))
        self.pg.Append( wxpg.StringProperty("Unit Code (input)", value= str(self.link[0].source_exchange_item()._ExchangeItem__unit)))
        # self.pg.Append( wxpg.StringProperty("Unit Abbreviation (input)", value=self.input.GetPropertyByName("Abbreviation").GetValue() or 'undefined'))
        # self.pg.Append( wxpg.StringProperty("Unit Type (input)", value=self.input.GetPropertyByName("Type").GetValue() or 'undefined'))

        self.pg.Append( wxpg.PropertyCategory("Output Item") )
        self.pg.Append( wxpg.StringProperty("Variable Name (output)",value= str(self.link[0].target_exchange_item()._ExchangeItem__name)))
        self.pg.Append( wxpg.StringProperty("Variable Description (output)",value= str(self.link[0].target_exchange_item()._ExchangeItem__description)))
        self.pg.Append( wxpg.StringProperty("Unit Code (output)", value= str(self.link[0].target_exchange_item()._ExchangeItem__unit)))
        # self.pg.Append( wxpg.StringProperty("Unit Abbreviation (output)", value=self.output.GetPropertyByName("Abbreviation").GetValue()  or 'undefined'))
        # self.pg.Append( wxpg.StringProperty("Unit Type (output)", value=self.output.GetPropertyByName("Type").GetValue()  or 'undefined'))


        self.Layout()

        self.Centre( wx.BOTH )

    def OnPropGridChange(self, event):
        p = event.GetProperty()

    def OnPropGridSelect(self, event):
        p = event.GetProperty()

    #def OnReserved(self, event):
    #    pass

    def OnPropGridPageChange(self, event):
        index = self.pg.GetSelectedPage()

    def __del__( self ):
        pass