__author__ = 'Mario'

import os
import wx


import wx
import wx.xrc
from pnlSpatial import pnlSpatial
from pnlDetails import pnlDetails

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
        self.IMPORTNEW = pnlDetails( self.treectrlView )
        self.matplotView = pnlSpatial( self.txtNotebook )

        self.txtNotebook.AddPage( self.treectrlView, u"Detail View", False )
        self.txtNotebook.AddPage( self.txtctrlView, u"Edit", True )
        self.txtNotebook.AddPage( self.matplotView, u"Spatial View", False )

        self.SaveButton = wx.Button( self.txtctrlView, wx.ID_ANY, u"Save Changes", wx.DefaultPosition, wx.DefaultSize, 0 )


        #InitSubscibers
        Publisher.subscribe(self.OnOpen, 'texteditpath')



        #Sizers
        NBSizer = wx.BoxSizer( wx.VERTICAL )
        txtctrlSizer = wx.BoxSizer( wx.VERTICAL )
        treectrlSizer = wx.BoxSizer( wx.VERTICAL )

        self.txtctrlView.SetSizer( txtctrlSizer )
        self.treectrlView.SetSizer( treectrlSizer )

        txtctrlSizer.Add( self.TextDisplay, 0, wx.ALL|wx.EXPAND, 5 )
        txtctrlSizer.Add( self.SaveButton, 0, wx.ALL, 5 )
        treectrlSizer.Add( self.IMPORTNEW, 0, wx.ALL, 5 )
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

    def OnOpen(self, fileExtension):

        # Open the file, read the contents and set them into
        # the text edit window
        filehandle=open(fileExtension)
        self.TextDisplay.SetValue(filehandle.read())
        filehandle.close()

        # Report on name of latest file read
        self.SetTitle("Editor")
        # Later - could be enhanced to include a "changed" flag whenever
        # the text is actually changed, could also be altered on "save" ...

    def OnSave(self, fileExtension):
        Publisher.subscribe(self.OnSave, 'textsavepath')
        # Grab the content to be saved
        itcontains = self.TextDisplay.GetValue()

        # Open the file for write, write, close

        filehandle=open((fileExtension),'w')
        filehandle.write(itcontains)
        filehandle.close()

class MyTree(wx.TreeCtrl):

    def __init__(self, parent, id, pos, size, style):

        wx.TreeCtrl.__init__(self, parent, id, pos, size, style)

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

# class MainWindow(wx.Frame):
#     def __init__(self, parent, title):
#         wx.Frame.__init__(self, parent, title=title, size=(500,400))
#         self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)
#         self.CreateStatusBar() # A StatusBar in the bottom of the window
#
#         # Setting up the menu.
#         filemenu= wx.Menu()
#
#         # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
#         menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
#         menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
#         menuOpen = filemenu.Append(wx.ID_OPEN,"O&pen"," Open File")
#
#         # Creating the menubar.
#         menuBar = wx.MenuBar()
#         menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
#         self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
#
#         # Set events.
#         self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
#         self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
#         self.Bind(wx.EVT_MENU, self.OnOpen, menuOpen)
#
#         self.Show(True)
#
#     def OnAbout(self,e):
#         # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
#         dlg = wx.MessageDialog( self, "A small text editor", "About Sample Editor", wx.OK)
#         dlg.ShowModal() # Show it
#         dlg.Destroy() # finally destroy it when finished.
#
#     def OnExit(self,e):
#         self.Close(True)  # Close the frame.
#
#     def OnOpen(self,e):
#         """ Open a file"""
#         self.dirname = ''
#         dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
#         if dlg.ShowModal() == wx.ID_OK:
#             self.filename = dlg.GetFilename()
#             self.dirname = dlg.GetDirectory()
#             f = OnOpen(os.path.join(self.dirname, self.filename), 'r')
#             self.control.SetValue(f.read())
#             f.close()
#         dlg.Destroy()
#
# app = wx.App(False)
# frame = ModelTxtCtrl(None)
# app.MainLoop()