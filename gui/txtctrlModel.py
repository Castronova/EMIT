__author__ = 'Mario'

import os
import wx


import wx
import wx.xrc

###########################################################################
## Class ModelTxtCtrl
###########################################################################

class ModelTxtCtrl ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        NBSizer = wx.BoxSizer( wx.VERTICAL )

        self.txtNotebook = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.txtctrlView = wx.Panel( self.txtNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        txtctrlSizer = wx.BoxSizer( wx.VERTICAL )

        self.TextDisplay = wx.TextCtrl( self.txtctrlView, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_WORDWRAP )
        txtctrlSizer.Add( self.TextDisplay, 0, wx.ALL|wx.EXPAND, 5 )


        self.txtctrlView.SetSizer( txtctrlSizer )
        self.txtctrlView.Layout()
        txtctrlSizer.Fit( self.txtctrlView )
        self.txtNotebook.AddPage( self.txtctrlView, u"TxtCtrl", True )
        self.treectrlView = wx.Panel( self.txtNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        treectrlSizer = wx.BoxSizer( wx.VERTICAL )

        self.IMPORTNEW = wx.TreeCtrl( self.treectrlView, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        treectrlSizer.Add( self.IMPORTNEW, 0, wx.ALL, 5 )


        self.treectrlView.SetSizer( treectrlSizer )
        self.treectrlView.Layout()
        treectrlSizer.Fit( self.treectrlView )
        self.txtNotebook.AddPage( self.treectrlView, u"ListCtrl", False )
        self.matplotView = wx.Panel( self.txtNotebook, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.txtNotebook.AddPage( self.matplotView, u"Spatial", False )

        NBSizer.Add( self.txtNotebook, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( NBSizer )
        self.Layout()

        self.Centre( wx.BOTH )






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
#             f = open(os.path.join(self.dirname, self.filename), 'r')
#             self.control.SetValue(f.read())
#             f.close()
#         dlg.Destroy()
#
# app = wx.App(False)
# frame = ModelTxtCtrl(None)
# app.MainLoop()