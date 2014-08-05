import wx
import wx.xrc
import LinkWizard

###########################################################################
## Class MyFrame1
###########################################################################

class LinkStart ( wx.Frame ):

    def __init__( self, parent, from_model, to_model, input, output, cmd):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 750,250 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.input = input
        self.output = output
        self.FloatCanvas = parent
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.cmd = cmd
        self.from_model = from_model
        self.to_model = to_model


        panel = wx.Panel(self, -1)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.listbox = wx.ListBox(panel, -1)
        hbox.Add(self.listbox, 1, wx.EXPAND | wx.ALL, 20)

        btnPanel = wx.Panel(panel, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        new = wx.Button(btnPanel, wx.ID_NEW, 'Add', size=(90, 30))
        ren = wx.Button(btnPanel, wx.ID_RESET, 'Rename', size=(90, 30))
        dlt = wx.Button(btnPanel, wx.ID_DELETE, 'Delete', size=(90, 30))
        close = wx.Button(btnPanel, wx.ID_CLEAR, 'Close', size=(90, 30))

        self.Bind(wx.EVT_BUTTON, self.AddClick, id=wx.ID_NEW)
        self.Bind(wx.EVT_BUTTON, self.OnRename, id=wx.ID_RESET)
        self.Bind(wx.EVT_BUTTON, self.OnDelete, id=wx.ID_DELETE)
        self.Bind(wx.EVT_BUTTON, self.OnClear, id=wx.ID_CLEAR)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename)

        vbox.Add((-1, 20))
        vbox.Add(new)
        vbox.Add(ren, 0, wx.TOP, 5)
        vbox.Add(dlt, 0, wx.TOP, 5)
        vbox.Add(close, 0, wx.TOP, 5)

        btnPanel.SetSizer(vbox)
        hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)

        # populate listctrl with links
        self.PopulateLinks()

        #
        # self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

    def AddClick(self, event):
        linkwiz = LinkWizard.wizLink(self.FloatCanvas, self.from_model.get_id(), self.to_model.get_id(), self.output, self.input, self.cmd)

        self.PopulateLinks()

    def CloseClick(self, event):
        self.Destroy()

    def PopulateLinks(self):

        links = self.cmd.get_links_btwn_models(self.from_model.get_id(), self.to_model.get_id())

        for link in links:
            text = "%s : %s --> %s : %s"%(link[0][0].get_name(),link[0][1].name(),link[1][0].get_name(),link[1][1].name())

            #text = 'This is overflowing'
            self.listbox.Append(text)


    def NewItem(self, event):
        text = wx.GetTextFromUser('Enter a new item', 'Insert dialog')
        if text != '':
            self.listbox.Append(text)

    def OnRename(self, event):
        sel = self.listbox.GetSelection()
        text = self.listbox.GetString(sel)
        renamed = wx.GetTextFromUser('Rename item', 'Rename dialog', text)
        if renamed != '':
            self.listbox.Delete(sel)
            self.listbox.Insert(renamed, sel)


    def OnDelete(self, event):
        sel = self.listbox.GetSelection()
        if sel != -1:
            self.listbox.Delete(sel)

    def OnClear(self, event):
        self.Destroy()


    def __del__( self ):
        pass
