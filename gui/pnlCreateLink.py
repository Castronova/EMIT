__author__ = 'Mario'

import wx
#import wx.xrc
import wx
import sys
from wx.lib.pubsub import pub as Publisher
import wx.propgrid as wxpg


[wxID_PNLCREATELINK, wxID_PNLSPATIAL, wxID_PNLTEMPORAL,
 wxID_PNLDETAILS,
] = [wx.NewId() for _init_ctrls in range(4)]

class pnlCreateLink ( wx.Panel ):

    def __init__( self, prnt, outputitems,inputitems ):
        wx.Panel.__init__(self, id=wxID_PNLCREATELINK, name=u'pnlIntro', parent=prnt,
              pos=wx.Point(571, 262), size=wx.Size(439, 357),
              style=wx.TAB_TRAVERSAL)
        self.SetClientSize(wx.Size(423, 319))


        self.selectedinput = None
        self.selectedoutput = None
        self.links = [None, None]
        self.inputitems = inputitems
        self.outputitems = outputitems
        self.input = [item.name() for item in inputitems]
        self.output = [item.name() for item in outputitems]



        PanelSizer = wx.BoxSizer( wx.VERTICAL )
        PanelSizer.AddSpacer( ( 0, 75), 0, wx.EXPAND, 5 )
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        PanelSizer.Add( bSizer6, 1, wx.EXPAND, 5 )
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )


        self.outputs = MyTree(id=wxID_PNLCREATELINK,
               parent=self, pos=wx.Point(0, 145),
              size=wx.Size(210, 80), style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)

        self.inputs = MyTree(id=wxID_PNLCREATELINK,
               parent=self, pos=wx.Point(220, 145),
              size=wx.Size(210, 80), style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)
        # self.panelSizer = PanelSizer.AddSpacer( ( 20, 0), 0, wx.EXPAND, 5 )

        bSizer6.Add(self.outputs)
        bSizer6.AddSpacer( ( 20, 0), 0, wx.EXPAND, 5 )
        bSizer6.Add(self.inputs)
        self.Description_text = wx.StaticText(self, label =
                                "Select which output and input parameters that you wish to couple",
                                              pos=wx.Point(0,15))
        # self.output_text = wx.StaticText(self,id=wxID_PNLCREATELINK, label = "Inputs", pos=wx.Point(0,0),size=wx.Size(210,10))
        # self.input_text  = wx.StaticText(self,id=wxID_PNLCREATELINK, label = "Outputs", pos=wx.Point(225,0),size=wx.Size(210,10))
        # PanelSizer.AddSpacer((0,20), 0, wx.EXPAND, 5)


        ## This is the Property Grid related code

        self.pgout = pgout = wxpg.PropertyGridManager(self, size = wx.Size(210, 200),
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT)

        self.pgin = pgin = wxpg.PropertyGridManager(self, size = wx.Size(210, 200),
                        style=wxpg.PG_SPLITTER_AUTO_CENTER |
                              wxpg.PG_AUTO_SORT)


        pgin.SetExtraStyle(wxpg.PG_EX_HELP_AS_TOOLTIPS)

        pgout.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        pgout.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChangepgout )
        pgout.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )
        pgin.Bind( wxpg.EVT_PG_CHANGED, self.OnPropGridChange )
        pgin.Bind( wxpg.EVT_PG_PAGE_CHANGED, self.OnPropGridPageChangepgout )
        pgin.Bind( wxpg.EVT_PG_SELECTED, self.OnPropGridSelect )

        pgout.AddPage( "Output Details" )
        pgin.AddPage( "Input Details" )

        # Fill using dictionary
        pgout.SetPropertyValues( self.output)
        pgin.SetPropertyValues( self.input)


        self.nout = 0
        self.nin  = 0



        bSizer5.Add(self.pgout)
        bSizer5.AddSpacer( ( 20, 0), 0, wx.EXPAND, 5 )
        bSizer5.Add(self.pgin)
        PanelSizer.Add( bSizer5, 1, wx.EXPAND, 5 )

        # deactivate Next button
        self.activateLinkButton()
        # print outputitems, inputitems

        # self.outputs.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.PopulateOutputPropertyGrid(outputitems, self.nout))
        # self.inputs.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.PopulateOutputPropertyGrid(inputitems, self.nout))
        #
        self.PopulateOutputPropertyGrid(outputitems, self.nout)
        self.PopulateInputPropertyGrid(inputitems, self.nin)
        self.outputs.Populate(outputitems)
        self.inputs.Populate(inputitems)

        Publisher.subscribe(self.PopulateOutputPropertyGrid, "inputitemname")
        Publisher.subscribe(self.PopulateInputPropertyGrid, "outputitemname")

        self.SetSizer( PanelSizer )
        self.Layout()

        self.outputs.Bind(wx.EVT_LEFT_UP,self.OutputClick)
        self.inputs.Bind(wx.EVT_LEFT_UP,self.InputClick)

    def PopulateInputPropertyGrid(self, exchangeitems, nin):
        # for exchangeitem in exchangeitems:
        self.pgin.Append( wxpg.PropertyCategory("Variable Information") )
        self.pgin.Append( wxpg.StringProperty("Name",value=exchangeitems[nin].variable().VariableNameCV() ))
        self.pgin.Append( wxpg.StringProperty("VarDef",value=exchangeitems[nin].variable().VariableDefinition() ))

        self.pgin.Append( wxpg.PropertyCategory("Units"))
        self.pgin.Append( wxpg.StringProperty("UnitName", value=exchangeitems[nin].unit()._Unit__unitName))
        self.pgin.Append( wxpg.StringProperty("UnitAbbreviation", value=exchangeitems[nin].unit()._Unit__unitAbbreviation))
        self.pgin.Append( wxpg.StringProperty("UnitType", value=exchangeitems[nin].unit()._Unit__unitTypeCV))


    def PopulateOutputPropertyGrid(self, exchangeitems, nout):
        # for exchangeitem in exchangeitems:
        self.pgout.Append( wxpg.PropertyCategory("Variable Information") )
        self.pgout.Append( wxpg.StringProperty("Name",value=exchangeitems[nout].variable().VariableNameCV() ))
        self.pgout.Append( wxpg.StringProperty("VarDef",value=exchangeitems[nout].variable().VariableDefinition() ))

        self.pgout.Append( wxpg.PropertyCategory("Units"))
        self.pgout.Append( wxpg.StringProperty("UnitName", value=exchangeitems[nout].unit()._Unit__unitName))
        self.pgout.Append( wxpg.StringProperty("UnitAbbreviation", value=exchangeitems[nout].unit()._Unit__unitAbbreviation))
        self.pgout.Append( wxpg.StringProperty("UnitType", value=exchangeitems[nout].unit()._Unit__unitTypeCV))


    def OnPropGridPageChangepgout(self, event):
            index = self.pgout.GetSelectedPage()

    def OnPropGridPageChangepgin(self, event):
            index = self.pgin.GetSelectedPage()

    def OnPropGridChange(self, event):
        p = event.GetProperty()

    def OnPropGridSelect(self, event):
        p = event.GetProperty()

    def OutputClick(self, event):

        # get the selected item
        item, loc = self.outputs.HitTest(event.GetPositionTuple())


        if not item.IsOk():
            # nothing selected
            self.OutputDeselect(event)
            #self.output_text.SetLabel('')

        else:

            # get the data for the selected item
            data = self.outputs.GetPyData(item)

            #self.output_text.SetLabel(data)

            self.OutputSelect(self.output ,data)

            if data is not None:
                print data

    def InputClick(self, event):

        # get the selected item
        item, loc = self.inputs.HitTest(event.GetPositionTuple())

        if not item.IsOk():
            # nothing selected
            self.OutputDeselect(event)
            #self.input_text.SetLabel('')
        else:

            # get the data for the selected item
            data = self.inputs.GetPyData(item)

            #self.input_text.SetLabel(data)

            self.InputSelect(self.input, data)

            if data is not None:
                print data

    def activateLinkButton(self):

        #if self.selectedinput is not None and self.selectedoutput is not None:
        if None not in self.links:
            #self.links = [self.selectedinput, self.selectedoutput]

            #self.SaveButton.Enable()
            Publisher.sendMessage("activateNextButton")
        else:
            #self.SaveButton.Disable()
            Publisher.sendMessage("deactivateNextButton")

    def InputSelect(self, exchangeitems, input_item_name):

        #self.selectedinput = self.inputitems[event.GetIndex()]
        #self.selectedinput = event.Text

        item = self.GetExchangeItemByName(self.inputitems, input_item_name)
        self.nin = item._ExchangeItem__name
        # self.PopulateInputPropertyGrid(exchangeitems, nin=self.nin)
        # Publisher.sendMessage('inputitemname', nin=self.nin)
        if item is not None:
            #self.set_link(0,self.inputitems[event.GetIndex()])
            self.set_link(1,item)
            self.activateLinkButton()


    def InputDeselect(self, event):

        #self.selectedinput = None

        self.set_link(0, None)
        self.activateLinkButton()

    def OutputSelect(self, exchangeitems, output_item_name):

        #self.selectedoutput = self.outputitems[event.GetIndex()]

        item = self.GetExchangeItemByName(self.outputitems, output_item_name)
        self.nout = item._ExchangeItem__name
        # self.PopulateOutputPropertyGrid(exchangeitems, nout=self.nout)
        # Publisher.sendMessage('outputitemname', nout=self.nout)
        if item is not None:
            #self.set_link(1,self.outputitems[event.GetIndex()])
            self.set_link(0,item)
            self.activateLinkButton()

    def OutputDeselect(self, event):

        #self.selectedoutput = None

        self.set_link(1,None)
        self.activateLinkButton()

    def set_link(self,index,value):
        self.links[index] = value

    def get_link(self):
        return self.links

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

    def GetExchangeItemByName(self, exchangeitems, name):
        for item in exchangeitems:
            if item.name() == name:
                return item
        return None

    def __del__( self ):
        pass

class MyTree(wx.TreeCtrl):

    def __init__(self, parent, id, pos, size, style):

        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)
        # self.root = self.AddRoot('Series')
        # self.m1 = self.AppendItem(self.root, 'Output Model')
        # self.model = self.AppendItem(self.root, 'Input Model')
        # self.v = self.AppendItem(self.root, 'Variable')
        #
        # self.sc=self.AppendItem(self.m1, 'ID: ')
        # #tmpId = self.AppendItem(self.treeRoot, str(i))
        # #key = self.makeNewKey()
        # #self.items[key] = ['node', i]
        # self.SetItemPyData(self.sc, 'value')
        #
        #
        # self.sn=self.AppendItem(self.m1, 'Name: ')
        #
        # self.sc=self.AppendItem(self.model, 'ID: ')
        # self.sn=self.AppendItem(self.model, 'Name: ')
        #
        # self.vc=self.AppendItem(self.v, 'ID: ')
        # self.vn=self.AppendItem(self.v, 'Name: ')
        # self.vu=self.AppendItem(self.v, 'Units: ')
        # self.vvt=self.AppendItem(self.v, 'Value Type: ')
        # self.vts=self.AppendItem(self.v, 'Time Support: ')
        # self.vtu=self.AppendItem(self.v, 'Time Units: ')
        # self.vdt=self.AppendItem(self.v, 'Data Type: ')
        #
        self.Bind(wx.EVT_LEFT_UP,self.OnLeftUp)

    def OnLeftUp(self, event):

        item, location = self.HitTest(event.GetPositionTuple())

        data = self.GetPyData(item)
        if data is not None: print data

    def Populate(self, exchangeitems):

        root = self.AddRoot('Series')


        for exchangeitem in exchangeitems:
            item = self.AppendItem(root,exchangeitem.name())
            self.SetItemPyData(item, exchangeitem.name())

            # variable = self.AppendItem(item, 'Variable')
            # self.SetItemPyData(variable, exchangeitem.name())
            # vname = self.AppendItem(variable, 'Name: %s' % exchangeitem.variable().VariableNameCV())
            # self.SetItemPyData(vname, exchangeitem.name())
            # vdef = self.AppendItem(variable, 'Def: %s' % exchangeitem.variable().VariableDefinition())
            # self.SetItemPyData(vdef, exchangeitem.name())
            #
            # unit = self.AppendItem(item, 'Unit')
            # self.SetItemPyData(unit, exchangeitem.name())
            # uname = self.AppendItem(unit, 'Name: %s' % exchangeitem.unit().UnitName())
            # self.SetItemPyData(uname, exchangeitem.name())
            # uabbv = self.AppendItem(unit,'Abbv: %s' % exchangeitem.unit().UnitAbbreviation())
            # self.SetItemPyData(uabbv, exchangeitem.name())
            # utype = self.AppendItem(unit,'Type: %s' % exchangeitem.unit().UnitTypeCV())
            # self.SetItemPyData(utype, exchangeitem.name())
