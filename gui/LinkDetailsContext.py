__author__ = 'mario'

import wx
import wx.xrc
import wx.propgrid as wxpg

class LinkDetailsContextActivatedFrame ( wx.Frame ):

    def __init__( self, parent, from_model, to_model, input, output, cmd ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.input = input
        self.output = output
        self.FloatCanvas = parent
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.cmd = cmd
        self.from_model = from_model
        self.to_model = to_model

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel1 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer1.Add( self.m_panel1, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( bSizer1 )

        self.pg = pg = wxpg.PropertyGridManager(self.m_panel1,
                    style=wxpg.PG_SPLITTER_AUTO_CENTER |
                          wxpg.PG_AUTO_SORT |
                          wxpg.PG_PROP_READONLY)

        # self.input.GetPropertyByName()
        self.input.GetPropertyByName("Name").GetValue()

        self.pg.Append( wxpg.PropertyCategory("Input Item") )
        self.pg.Append( wxpg.StringProperty("Variable Name (input)",value=self.input.GetPropertyByName("Name").GetValue() or 'undefined' ))
        self.pg.Append( wxpg.StringProperty("Variable Definition (input)",value=self.input.GetPropertyByName("Definition").GetValue() or 'undefined'))
        self.pg.Append( wxpg.StringProperty("Unit Code (input)", value=self.input.GetPropertyByName("Code").GetValue() or 'undefined'))
        self.pg.Append( wxpg.StringProperty("Unit Abbreviation (input)", value=self.input.GetPropertyByName("Abbreviation").GetValue() or 'undefined'))
        self.pg.Append( wxpg.StringProperty("Unit Type (input)", value=self.input.GetPropertyByName("Type").GetValue() or 'undefined'))

        self.pg.Append( wxpg.PropertyCategory("Output Item") )
        self.pg.Append( wxpg.StringProperty("Variable Name (output)",value=self.output.GetPropertyByName("Name").GetValue()  or 'undefined' ))
        self.pg.Append( wxpg.StringProperty("Variable Definition (output)",value=self.output.GetPropertyByName("Definition").GetValue() or 'undefined'))
        self.pg.Append( wxpg.StringProperty("Unit Code (output)", value=self.output.GetPropertyByName("Code").GetValue()  or 'undefined' ))
        self.pg.Append( wxpg.StringProperty("Unit Abbreviation (output)", value=self.output.GetPropertyByName("Abbreviation").GetValue()  or 'undefined'))
        self.pg.Append( wxpg.StringProperty("Unit Type (output)", value=self.output.GetPropertyByName("Type").GetValue()  or 'undefined'))


        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass