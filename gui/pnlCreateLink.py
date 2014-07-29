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


        bSizer1 = wx.BoxSizer( wx.VERTICAL )
        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
        bSizer1.Add( bSizer6, 1, wx.EXPAND, 5 )
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        #self.m_listCtrl1 = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(210, 200), wx.LC_REPORT )
        #self.m_listCtrl2 = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size(210, 200), wx.LC_REPORT )
        #self.m_button1 = wx.Button( self, wx.ID_ANY, u"Create Link", wx.DefaultPosition, wx.DefaultSize, 0)
        #self.m_button1.Disable()

        self.outputs = MyTree(id=wxID_PNLCREATELINK,
               parent=self, pos=wx.Point(0, 0),
              size=wx.Size(210, 200), style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)

        self.inputs = MyTree(id=wxID_PNLCREATELINK,
               parent=self, pos=wx.Point(220, 0),
              size=wx.Size(210, 200), style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)

        self.output_text = wx.StaticText(self,id=wxID_PNLCREATELINK,pos=wx.Point(0,210),size=wx.Size(210,10))
        self.input_text  = wx.StaticText(self,id=wxID_PNLCREATELINK,pos=wx.Point(210,200),size=wx.Size(210,10))



        #bSizer6.Add( self.m_listCtrl1, 0, wx.ALL, 5 )
        #Sizer6.Add( self.m_listCtrl2, 0, wx.ALL, 5 )
        #bSizer5.Add( self.m_button1, 0, wx.ALL, 5 )


        bSizer1.Add( bSizer5, 1, wx.EXPAND, 5 )

        #panel = pnlCreateLink(self)
        # self.m_listCtrl1.InsertColumn(0, 'input')
        # self.m_listCtrl1.SetColumnWidth(0, 200)
        #self.m_listCtrl2.InsertColumn(0, 'output')
        #self.m_listCtrl2.SetColumnWidth(0, 200)

        # self.m_listCtrl1.Bind(wx.EVT_LIST_ITEM_SELECTED, self.InputSelect)
        # self.m_listCtrl1.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.InputDeselect)
        #self.m_listCtrl2.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OutputSelect)
        #self.m_listCtrl2.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OutputDeselect)
        #self.m_button1.Bind(wx.EVT_LEFT_DOWN, self.CreateLink)

        #self.Bind




        #wx.StaticText(self, -1,"Error", pos = (20, 200))

        # deactivate Next button
        self.activateLinkButton()


        self.outputs.Populate(outputitems)
        self.inputs.Populate(inputitems)

        # for i in inputitems:
        #     self.m_listCtrl1.InsertStringItem(sys.maxint, i.name())


        #for i in outputitems:
        #    self.m_listCtrl2.InsertStringItem(sys.maxint, i.name())

        self.SetSizer( bSizer1 )
        self.Layout()

        self.outputs.Bind(wx.EVT_LEFT_UP,self.OutputClick)
        self.inputs.Bind(wx.EVT_LEFT_UP,self.InputClick)


    # def OnLeftUp(self, event):
    #
    #     item, location = self.HitTest(event.GetPositionTuple())
    #
    #     data = self.GetPyData(item)
    #     if data is not None: print data

    def OutputClick(self, event):

        # get the selected item
        item, loc = self.outputs.HitTest(event.GetPositionTuple())


        if not item.IsOk():
            # nothing selected
            self.OutputDeselect(event)
            self.output_text.SetLabel('')

        else:

            # get the data for the selected item
            data = self.outputs.GetPyData(item)

            self.output_text.SetLabel(data)

            self.OutputSelect(data)

            if data is not None:
                print data

    def InputClick(self, event):

        # get the selected item
        item, loc = self.inputs.HitTest(event.GetPositionTuple())

        if not item.IsOk():
            # nothing selected
            self.OutputDeselect(event)
            self.input_text.SetLabel('')
        else:

            # get the data for the selected item
            data = self.inputs.GetPyData(item)

            self.input_text.SetLabel(data)

            self.InputSelect(data)

            if data is not None:
                print data

    def activateLinkButton(self):

        #if self.selectedinput is not None and self.selectedoutput is not None:
        if None not in self.links:
            #self.links = [self.selectedinput, self.selectedoutput]

            #self.m_button1.Enable()
            Publisher.sendMessage("activateNextButton")
        else:
            #self.m_button1.Disable()
            Publisher.sendMessage("deactivateNextButton")

    def InputSelect(self, input_item_name):

        #self.selectedinput = self.inputitems[event.GetIndex()]
        #self.selectedinput = event.Text

        item = self.GetExchangeItemByName(self.inputitems, input_item_name)
        if item is not None:
            #self.set_link(0,self.inputitems[event.GetIndex()])
            self.set_link(1,item)
            self.activateLinkButton()

    def InputDeselect(self, event):

        #self.selectedinput = None

        self.set_link(0, None)
        self.activateLinkButton()

    def OutputSelect(self, output_item_name):

        #self.selectedoutput = self.outputitems[event.GetIndex()]

        item = self.GetExchangeItemByName(self.outputitems, output_item_name)
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
        # self.m2 = self.AppendItem(self.root, 'Input Model')
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
        # self.sc=self.AppendItem(self.m2, 'ID: ')
        # self.sn=self.AppendItem(self.m2, 'Name: ')
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

            variable = self.AppendItem(item, 'Variable')
            self.SetItemPyData(variable, exchangeitem.name())
            vname = self.AppendItem(variable, 'Name: %s' % exchangeitem.variable().VariableNameCV())
            self.SetItemPyData(vname, exchangeitem.name())
            vdef = self.AppendItem(variable, 'Def: %s' % exchangeitem.variable().VariableDefinition())
            self.SetItemPyData(vdef, exchangeitem.name())

            unit = self.AppendItem(item, 'Unit')
            self.SetItemPyData(unit, exchangeitem.name())
            uname = self.AppendItem(unit, 'Name: %s' % exchangeitem.unit().UnitName())
            self.SetItemPyData(uname, exchangeitem.name())
            uabbv = self.AppendItem(unit,'Abbv: %s' % exchangeitem.unit().UnitAbbreviation())
            self.SetItemPyData(uabbv, exchangeitem.name())
            utype = self.AppendItem(unit,'Type: %s' % exchangeitem.unit().UnitTypeCV())
            self.SetItemPyData(utype, exchangeitem.name())


