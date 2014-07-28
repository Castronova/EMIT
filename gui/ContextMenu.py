__author__ = 'tonycastronova'


import wx

class LinkContextMenu(wx.Menu):

    def __init__(self, parent):
        super(LinkContextMenu, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Edit')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveLink, mmi)


    def OnAddLink(self, e):
        self.parent.ArrowClicked(e)

    def RemoveLink(self, e):
        # todo:
        #self.parent.RemoveLink(e)
        pass

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class ModelContextMenu(wx.Menu):

    def __init__(self, parent):
        super(ModelContextMenu, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)

        #self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        # cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        # self.AppendItem(cmi)
        # self.Bind(wx.EVT_MENU, self.OnClose, cmi)

    def OnAddLink(self, e):
        self.parent.ArrowClicked(e)

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class GeneralContextMenu(wx.Menu):

    def __init__(self, parent):
        super(GeneralContextMenu, self).__init__()

        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'Add Model')
        self.AppendItem(mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Add Link')
        self.AppendItem(mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Load Configuration')
        self.AppendItem(mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Save Configuration')
        self.AppendItem(mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Clear Configuration')
        self.AppendItem(mmi)



        #self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        # cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        # self.AppendItem(cmi)
        # self.Bind(wx.EVT_MENU, self.OnClose, cmi)

    def OnAddLink(self, e):
        self.parent.ArrowClicked(e)

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