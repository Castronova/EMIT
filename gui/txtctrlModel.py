__author__ = 'Mario'

import os
import wx


import wx
import wx.xrc
from pnlSpatial import pnlSpatial
from pnlDetails import pnlDetails
import utilities

from wx.lib.pubsub import pub as Publisher

###########################################################################
## Class ModelTxtCtrl
###########################################################################

class ModelTxtCtrl ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition,
                            size = wx.Size( 500,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )


        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )


        #Define Objects
        self.txtNotebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txtctrlView = wx.Panel( self.txtNotebook, wx.ID_ANY, wx.DefaultPosition,
                                     wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.TextDisplay = wx.TextCtrl( self.txtctrlView, wx.ID_ANY, wx.EmptyString,
                                        wx.DefaultPosition, wx.Size(450, 350), wx.TE_MULTILINE|wx.TE_WORDWRAP )

        self.treectrlView = wx.Panel( self.txtNotebook, wx.ID_ANY, wx.DefaultPosition,
                                      wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.DetailTree = MyTree( self.treectrlView, id=wx.ID_ANY,
                pos=wx.Point(0, 0),
              size=wx.Size(423, 319), style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT )
        # self.DetailTree = wx.TreeCtrl( self.treectrlView )
        self.matplotView = pnlSpatial( self.txtNotebook )

        self.txtNotebook.AddPage( self.treectrlView, u"Detail View", False )
        self.txtNotebook.AddPage( self.txtctrlView, u"Edit", True )
        self.txtNotebook.AddPage( self.matplotView, u"Spatial View", False )

        self.SaveButton = wx.Button( self.txtctrlView, wx.ID_ANY, u"Save Changes", wx.DefaultPosition, wx.DefaultSize, 0 )


        #InitSubscibers
        #Publisher.subscribe(self.OnOpen, 'texteditpath')

        #Sizers
        NBSizer = wx.BoxSizer( wx.VERTICAL )
        txtctrlSizer = wx.BoxSizer( wx.VERTICAL )
        treectrlSizer = wx.BoxSizer( wx.VERTICAL )

        self.txtctrlView.SetSizer( txtctrlSizer )
        self.treectrlView.SetSizer( treectrlSizer )

        txtctrlSizer.Add( self.TextDisplay, 0, wx.ALL|wx.EXPAND, 5 )
        txtctrlSizer.Add( self.SaveButton, 0, wx.ALL, 5 )
        treectrlSizer.Add( self.DetailTree, 0, wx.ALL, 5 )
        # treectrlSizer.Add( self.DetailTree, 0, wx.ALL, 5 )
        NBSizer.Add( self.txtNotebook, 1, wx.EXPAND |wx.ALL, 5 )


        #Bindings
        self.SaveButton.Bind( wx.EVT_BUTTON, self.OnSave )

        self.txtctrlView.Layout()
        txtctrlSizer.Fit( self.txtctrlView )

        self.treectrlView.Layout()
        treectrlSizer.Fit( self.treectrlView )

        self.SetSizer( NBSizer )
        self.Layout()

        self.Centre( wx.BOTH )

    def PopulateEdit(self, fileExtension):

        # Open the file, read the contents and set them into
        # the text edit window
        filehandle=open(fileExtension)
        self.TextDisplay.SetValue(filehandle.read())
        filehandle.close()

        # Report on name of latest file read
        self.SetTitle("Editor")
        # Later - could be enhanced to include a "changed" flag whenever
        # the text is actually changed, could also be altered on "save" ...

    def PopulateDetails(self, fileExtension):
        d = utilities.parse_config_without_validation(fileExtension)

        for i in d:
            return i


        print d.keys()

        # self.DetailTree



    def OnSave(self, fileExtension):
        Publisher.subscribe(self.OnSave, 'textsavepath')
        # Grab the content to be saved
        itcontains = self.TextDisplay.GetValue()

        # Open the file for write, write, close

        filehandle=open((fileExtension),'w')
        filehandle.write(itcontains)
        filehandle.close()

class MyTree(wx.TreeCtrl):

    def __init__(self,*args, **kwargs):

        wx.TreeCtrl.__init__(self, *args, **kwargs)
        self.root = self.AddRoot('Series')
        self.m1 = self.AppendItem(self.root, 'Output Model')
        self.m2 = self.AppendItem(self.root, 'Input Model')
        self.v = self.AppendItem(self.root, 'Variable')

        self.sc=self.AppendItem(self.m1, 'ID: ')

        #tmpId = self.AppendItem(self.treeRoot, str(i))
        #key = self.makeNewKey()
        #self.items[key] = ['node', i]
        self.SetItemPyData(self.sc, 'value')



        self.sn=self.AppendItem(self.m1, 'Name: ')

        self.sc=self.AppendItem(self.m2, 'ID: ')
        self.sn=self.AppendItem(self.m2, 'Name: ')

        self.vc=self.AppendItem(self.v, 'ID: ')
        self.vn=self.AppendItem(self.v, 'Name: ')
        self.vu=self.AppendItem(self.v, 'Units: ')
        self.vvt=self.AppendItem(self.v, 'Value Type: ')
        self.vts=self.AppendItem(self.v, 'Time Support: ')
        self.vtu=self.AppendItem(self.v, 'Time Units: ')
        self.vdt=self.AppendItem(self.v, 'Data Type: ')


        self.Bind(wx.EVT_LEFT_UP,self.OnLeftUp)

    def PopulateDetails(self, fileExtension):
        d = utilities.parse_config_without_validation(fileExtension)

        for i in d:
            return i


        print d.keys()

        # self.DetailTree

    def OnLeftUp(self, event):

        item, location = self.HitTest(event.GetPositionTuple())

        data = self.GetPyData(item)
        if data is not None: print data
