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

        # self.txtctrlView = wx.Panel( self.txtNotebook, wx.ID_ANY, wx.DefaultPosition,
        #                              wx.DefaultSize, wx.TAB_TRAVERSAL )
        # self.TextDisplay = wx.TextCtrl( self.txtctrlView, wx.ID_ANY, wx.EmptyString,
        #                                 wx.DefaultPosition, wx.Size(450, 350), wx.TE_MULTILINE|wx.TE_WORDWRAP )

        self.treectrlView = wx.Panel( self.txtNotebook, wx.ID_ANY, wx.DefaultPosition,
                                      wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.DetailTree = MyTree( self.treectrlView, id=wx.ID_ANY, pos=wx.Point(0, 0),
                                  size=wx.Size(423, 319), style=wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT )
        # self.DetailTree = wx.TreeCtrl( self.treectrlView )

        self.matplotView = pnlSpatial( self.txtNotebook )

        self.txtNotebook.AddPage( self.treectrlView, u"General", True )
        self.txtNotebook.AddPage( self.matplotView, u"Spatial", False )
        # self.txtNotebook.AddPage( self.txtctrlView, u"Edit", False )
        # self.SaveButton = wx.Button( self.txtctrlView, wx.ID_ANY, u"Save Changes",
        #                              wx.DefaultPosition, wx.DefaultSize, 0 )


        #Sizers
        NBSizer = wx.BoxSizer( wx.VERTICAL )
        txtctrlSizer = wx.BoxSizer( wx.VERTICAL )
        treectrlSizer = wx.BoxSizer( wx.VERTICAL )

        # self.txtctrlView.SetSizer( txtctrlSizer )
        self.treectrlView.SetSizer( treectrlSizer )

        # txtctrlSizer.Add( self.TextDisplay, 0, wx.ALL|wx.EXPAND, 5 )
        # txtctrlSizer.Add( self.SaveButton, 0, wx.ALL, 5 )
        treectrlSizer.Add( self.DetailTree, 0, wx.ALL, 5 )
        # treectrlSizer.Add( self.DetailTree, 0, wx.ALL, 5 )
        NBSizer.Add( self.txtNotebook, 1, wx.EXPAND |wx.ALL, 5 )


        #Bindings
        # self.SaveButton.Bind( wx.EVT_BUTTON, self.OnSave )
        #
        # self.txtctrlView.Layout()
        # txtctrlSizer.Fit( self.txtctrlView )

        self.treectrlView.Layout()
        treectrlSizer.Fit( self.treectrlView )

        self.SetSizer( NBSizer )
        self.Layout()

        self.Centre( wx.BOTH )
        # self.InitMenu()


    def InitMenu(self):

        menubar = wx.MenuBar()
        viewMenu = wx.Menu()

        self.shst = viewMenu.Append(wx.ID_ANY, 'Show Edit',
                                    'Show Edit', kind=wx.ITEM_CHECK)

        viewMenu.Check(self.shst.GetId(), False)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)

        menubar.Append(viewMenu, '&Edit')
        self.SetMenuBar(menubar)

        self.SetSize((500, 500))
        self.SetTitle('Check menu item')
        self.Centre()
        self.Show(True)


    def ToggleStatusBar(self, e):

        if self.shst.IsChecked():


            pass

        else:
            pass

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
        if type == 'input':
            self.matplotView.input_data(coordlist)
        elif type == 'output':
            self.matplotView.output_data(coordlist)

    def PopulateDetails(self, fileExtension):

        # get a dictionary of config parameters
        d = utilities.parse_config_without_validation(fileExtension)

        root = self.DetailTree.AddRoot('Data')
        self.DetailTree.ExpandAll()

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

        self.ExpandAll()

        self.Bind(wx.EVT_LEFT_UP,self.OnLeftUp)

    def OnLeftUp(self, event):

        item, location = self.HitTest(event.GetPositionTuple())

        data = self.GetPyData(item)
        if data is not None: print data
