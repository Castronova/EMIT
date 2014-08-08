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


        self.current_file = None

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
        self.current_file = fileExtension

        filehandle=open(fileExtension)
        self.TextDisplay.SetValue(filehandle.read())
        filehandle.close()

        # Report on name of latest file read
        self.SetTitle("Editor")
        # Later - could be enhanced to include a "changed" flag whenever
        # the text is actually changed, could also be altered on "save" ...


    def PopulateSpatial(self, coordlist, type):
        #pass


        #colors = self.matplotView.buildGradientColor(len(coordlist),cmap='jet')

        if type == 'input':
            self.matplotView.input_data(coordlist)
        elif type == 'output':
            self.matplotView.output_data(coordlist)
        #
        # i = 0
        # for coords in coordlist:
        #     self.matplotView.addSeries(zip(*coords),color=colors[i])
        #     i += 1

    def PopulateDetails(self, fileExtension):

        # get a dictionary of config parameters
        d = utilities.parse_config_without_validation(fileExtension)

        root = self.DetailTree.AddRoot('Data')
        # get sorted sections
        sections = sorted(d.keys())

        for section in sections:
            # add this item as a group
            g = self.DetailTree.AppendItem(root, section)

            # all all sub elements

            if type(d[section]) == list:
                items = d[section]
                for item in items:
                    p = g
                    while len(item.keys()) > 0:
                    #for item in d[section]:
                        if 'variable_name_cv' in item:
                            var = item.pop('variable_name_cv')
                            p =  self.DetailTree.AppendItem(g,var)


                        # get the next item in the dictionary
                        i = item.popitem()


                        if i[0] != 'type':
                            k = self.DetailTree.AppendItem(p,i[0])
                            self.DetailTree.AppendItem(k, i[1])
            else:
                self.DetailTree.AppendItem(g,d[section])


    def OnSave(self, event):
        Publisher.subscribe(self.OnSave, 'textsavepath')
        # Grab the content to be saved
        itcontains = self.TextDisplay.GetValue().encode('utf-8').strip()

        # Open the file for write, write, close

        filehandle=open((self.current_file),'w')
        filehandle.write(itcontains)
        filehandle.close()


class MyTree(wx.TreeCtrl):

    def __init__(self,*args, **kwargs):

        wx.TreeCtrl.__init__(self, *args, **kwargs)
        # self.root = self.AddRoot('Model Information')
        # self.gen = self.AppendItem(self.root, 'General')
        # self.model = self.AppendItem(self.root, 'Model')
        # self.v = self.AppendItem(self.root, 'Variable')
        #
        # self.sn=self.AppendItem(self.gen, 'Name: ')
        # self.sc=self.AppendItem(self.gen, 'Start: ')
        # self.sc=self.AppendItem(self.gen, 'End: ')
        #
        # self.mn=self.AppendItem(self.model, 'Name: ')
        # self.md=self.AppendItem(self.model, 'Description: ')
        #
        # self.SetItemPyData(self.sc, 'value')
        #
        # self.vu=self.AppendItem(self.v, 'Name: ')
        # self.vc=self.AppendItem(self.v, 'Element Set: ')
        # self.vn=self.AppendItem(self.v, 'Unit: ')

        #self.PopulateDetails()

        self.Bind(wx.EVT_LEFT_UP,self.OnLeftUp)

    def PopulateDetails(self, fileExtension):

        return

        d = utilities.parse_config_without_validation(fileExtension)


        #d.pop(d.has_key())
        # d.pop(d.keys())

        groups = sorted(d.keys())

        for group in groups:
            # add this item as a group
            g = self.AppendItem(self.root, group)

            # all all sub elements

            if type(d[group]) == dict:

                for key, value in d[group].iteritems():
                    self.AppendItem(g, value)




        # print d.keys()
        #
        # for i in d:
        #     return i


            # self.DetailTree

    def OnLeftUp(self, event):

        item, location = self.HitTest(event.GetPositionTuple())

        data = self.GetPyData(item)
        if data is not None: print data
