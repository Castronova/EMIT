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


import sys, time, math, os, os.path

import wx
_ = wx.GetTranslation
import wx.propgrid as wxpg


############################################################################
#
# MAIN PROPERTY GRID TEST PANEL
#
############################################################################

class TestPanel( wx.Panel ):

    def __init__( self, prnt, outputitems, inputitems ):
        wx.Panel.__init__(self, id=wxID_PNLTEMPORAL, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)

        self.SetClientSize(wx.Size(423, 319))

        # self.log = log
        self.inputitems = inputitems
        self.outputitems = outputitems

        self.panel = panel = wx.Panel(self, size=wx.Size(500,500))
        topsizer = wx.BoxSizer(wx.VERTICAL)

        # Difference between using PropertyGridManager vs PropertyGrid is that
        # the manager supports multiple pages and a description box.
        self.pg = pg = wxpg.PropertyGridManager(panel,
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT |
                              wxpg.PG_TOOLBAR)

        # Show help as tooltips
        pg.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        pg.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        pg.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChange )
        pg.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        # pg.Bind( wxpg.EVT_PG_RIGHT_CLICK, self.OnPropGridRightClick )


        # NOTE: Editor must be registered *before* adding a property that
        # uses it.

        # Add properties

        pg.AddPage( "Link Details" )

        pg.Append( wxpg.PropertyCategory("Basic Properties") )
        pg.Append( wxpg.StringProperty("String",value="Some Text") )
        pg.Append( wxpg.IntProperty("Int",value=100) )
        pg.Append( wxpg.FloatProperty("Float",value=100.0) )
        pg.Append( wxpg.BoolProperty("Bool",value=True) )
        pg.Append( wxpg.BoolProperty("Bool_with_Checkbox",value=True) )
        pg.SetPropertyAttribute("Bool_with_Checkbox", "UseCheckbox", True)

        # pg.Append( wxpg.PropertyCategory("2 - More Properties") )
        # pg.Append( wxpg.LongStringProperty("LongString",
        #     value="This is a\\nmulti-line string\\nwith\\ttabs\\nmixed\\tin."))
        # pg.Append( wxpg.DirProperty("Dir",value="C:\\Windows") )
        # pg.Append( wxpg.FileProperty("File",value="C:\\Windows\\system.ini") )
        # pg.Append( wxpg.ArrayStringProperty("ArrayString",value=['A','B','C']) )
        #
        # pg.Append( wxpg.EnumProperty("Enum","Enum",
        #                              ['wxPython Rules',
        #                               'wxPython Rocks',
        #                               'wxPython Is The Best'],
        #                              [10,11,12],
        #                              0) )
        # pg.Append( wxpg.EditEnumProperty("EditEnum","EditEnumProperty",
        #                                  ['A','B','C'],
        #                                  [0,1,2],
        #                                  "Text Not in List") )


        topsizer.Add(pg, 1, wx.EXPAND)

        rowsizer = wx.BoxSizer(wx.HORIZONTAL)
        but = wx.Button(panel,-1,"SetPropertyValues")
        but.Bind( wx.EVT_BUTTON, self.OnReserved )
        rowsizer.Add(but,1)

        panel.SetSizer(topsizer)
        topsizer.SetSizeHints(panel)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    # g=[]
    # l = []
    # for i in range(10):
    #     l.append(PyObjectProperty(g))

    def OnPropGridChange(self, event):
        p = event.GetProperty()

    def OnPropGridSelect(self, event):
        p = event.GetProperty()

    def OnReserved(self, event):
        pass

    def OnPropGridPageChange(self, event):
        index = self.pg.GetSelectedPage()

#---------------------------------------------------------------------------


class MemoDialog(wx.Dialog):
    """\
    Dialog for multi-line text editing.
    """
    def __init__(self,parent=None,title="",text="",pos=None,size=(500,500)):
        wx.Dialog.__init__(self,parent,-1,title,style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)

        topsizer = wx.BoxSizer( wx.VERTICAL )

        tc = wx.TextCtrl(self,11,text,style=wx.TE_MULTILINE)
        self.tc = tc
        topsizer.Add(tc,1,wx.EXPAND|wx.ALL,8)

        rowsizer = wx.BoxSizer( wx.HORIZONTAL )
        rowsizer.Add(wx.Button(self,wx.ID_OK,'Ok'),0,wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL,8)
        rowsizer.Add((0,0),1,wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL,8)
        rowsizer.Add(wx.Button(self,wx.ID_CANCEL,'Cancel'),0,wx.ALIGN_RIGHT|wx.ALIGN_CENTRE_VERTICAL,8)
        topsizer.Add(rowsizer,0,wx.EXPAND|wx.ALL,8)

        self.SetSizer( topsizer )
        topsizer.Layout()

        self.SetSize( size )
        if not pos:
            self.CenterOnScreen()
        else:
            self.Move(pos)

#----------------------------------------------------------------------

def runTest( frame, nb, log ):
    win = TestPanel( nb, log )
    return win

#----------------------------------------------------------------------


overview = """\
<html><body>
<P>
This demo shows all basic wxPropertyGrid properties, in addition to
some custom property classes.
</body></html>
"""

app = wx.App(False)
# frame = SimpleFrame(None)
# frame.Show(True)

app.MainLoop()

'''
if __name__ == '__main__':
    import sys,os
    import run
    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])
'''
