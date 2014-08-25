__author__ = 'tonycastronova'


import wx

class LinkContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(LinkContextMenu, self).__init__()

        self.arrow_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Edit')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)


        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveLink, mmi)


    def OnAddLink(self, e):
        self.parent.ArrowClicked(self.arrow_obj)

    def RemoveLink(self, e):
        self.parent.RemoveLink(self.arrow_obj)


    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class ModelContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(ModelContextMenu, self).__init__()

        self.model_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, DirectoryContextMenu.OnViewDetails, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveModel, mmi)

        #self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        # cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        # self.AppendItem(cmi)
        # self.Bind(wx.EVT_MENU, self.OnClose, cmi)

    def PopupDisplay(self, e):
        self.parent.DetailView(e)

    def OnAddLink(self, e):
        self.parent.ArrowClicked(e)

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

    def RemoveModel(self, e):
        self.parent.RemoveModel(self.model_obj)

class GeneralContextMenu(wx.Menu):

    def __init__(self, parent):
        super(GeneralContextMenu, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Add Model')
        self.AppendItem(mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Add Link')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Load Configuration')
        self.AppendItem(mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Save Configuration')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.SaveConfiguration, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Clear Configuration')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClickClear, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Run')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClickRun, mmi)

        #self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        # cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        # self.AppendItem(cmi)
        # self.Bind(wx.EVT_MENU, self.OnClose, cmi)

    def OnAddLink(self, e):

        self.parent.FloatCanvas.SetMode(self.parent.Canvas.GuiLink)

    def OnClickRun(self, e):

        self.parent.run()

    def OnClickClear(self, e):

        self.parent.clear()

    def SaveConfiguration(self,e):

        save = wx.FileDialog(self.parent.Canvas.GetTopLevelParent(), "Save Configuration","","",
                             "Simulation Files (*.sim)|*.sim", wx.FD_SAVE  | wx.FD_OVERWRITE_PROMPT)

        if save.ShowModal() != wx.ID_CANCEL:
            path = save.GetPath()
            self.parent.SaveSimulation(path)

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()


class DirectoryContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(DirectoryContextMenu, self).__init__()

        self.arrow_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnViewDetails, mmi)

    def OnViewDetails(self, e):
       # self.parent.ArrowClicked(self.arrow_obj)
        self.parent.ShowDetails()

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()



class Example(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Example, self).__init__(*args, **kwargs)

        self.InitUI()

    def InitUI(self):

        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)

        self.SetSize((250, 200))
        self.SetTitle('Context menu')
        self.Centre()
        self.Show(True)

    def OnRightDown(self, e):
        self.PopupMenu(LinkContextMenu(self), e.GetPosition())

def main():

    ex = wx.App()
    Example(None)
    ex.MainLoop()


if __name__ == '__main__':
    main()