from utilities import spatial

__author__ = 'tonycastronova'


import wx
from txtctrlModel import ModelTxtCtrl

class LinkContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(LinkContextMenu, self).__init__()

        self.cmd = parent.cmd
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

        self.cmd = parent.cmd
        self.model_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)
        #self.Bind(wx.EVT_MENU, DirectoryContextMenu.OnViewDetails, mmi)
        self.Bind(wx.EVT_MENU, self.ShowModelDetails, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Remove')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.RemoveModel, mmi)

        #self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        # cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        # self.AppendItem(cmi)
        # self.Bind(wx.EVT_MENU, self.OnClose, cmi)

    def ShowModelDetails(self, e):

        # get model id
        id = self.model_obj.ID

        # create a frame to bind the details page to
        f = wx.Frame(self.GetParent())

        # create the details view (no edit)
        view = ModelTxtCtrl(f, edit=False)

        # get the input geometries
        ogeoms = spatial.get_output_geoms(self.cmd, id)

        # get the output geometries
        igeoms = spatial.get_input_geoms(self.cmd, id)

        # load geometry data
        view.PopulateSpatialGeoms(ogeoms, type='output')
        view.PopulateSpatialGeoms(igeoms, type='input')

        # # load the file contents
        # view.PopulateEdit(self.sb.GetValue())
        #
        #
        # # load the geometry data
        # view.PopulateSpatial(self.read_geoms(self.sb.GetValue(),'input'),'input')
        # view.PopulateSpatial(self.read_geoms(self.sb.GetValue(),'output'),'output')
        #
        # # show the details view
        # # listview = MyTree(self)
        # view.PopulateEdit(self.sb.GetValue())

        mdl_path= self.cmd.get_model_by_id(self.model_obj.ID)._Model__attrib['mdl']
        view.PopulateDetails(mdl_path)

        # listview.PopulateDetails(self.sb.GetValue())
        view.Show()



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

        self.cmd = parent.cmd
        self.parent = parent

        # mmi = wx.MenuItem(self, wx.NewId(), 'Add Model')
        # self.AppendItem(mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Add Link')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        # mmi = wx.MenuItem(self, wx.NewId(), 'Load Configuration')
        # self.AppendItem(mmi)
        #
        # mmi = wx.MenuItem(self, wx.NewId(), 'Save Configuration')
        # self.AppendItem(mmi)
        # self.Bind(wx.EVT_MENU, self.SaveConfiguration, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Run')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClickRun, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Clear Configuration')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnClickClear, mmi)

        #self.Bind(wx.EVT_MENU, self.OnAddLink, mmi)

        # cmi = wx.MenuItem(self, wx.NewId(), 'Close')
        # self.AppendItem(cmi)
        # self.Bind(wx.EVT_MENU, self.OnClose, cmi)

    def OnAddLink(self, e):

        self.parent.FloatCanvas.SetMode(self.parent.Canvas.GuiLink)

    def OnClickRun(self, e):

        self.parent.run()

    def OnClickClear(self, e):
        dlg = wx.MessageDialog(None, 'Are you sure you would like to clear configuration?', 'Question', wx.YES_NO | wx.YES_DEFAULT | wx.ICON_WARNING)

        if dlg.ShowModal() !=wx.ID_NO:
            self.parent.clear()

        # elif dlg.ShowModal() !=wx.ID_NO:
        #     self.parent.clear()

    def SaveConfiguration(self,e):

        save = wx.FileDialog(self.parent.Canvas.GetTopLevelParent(), "Save Configuration","","",
                             "Simulation Files (*.sim)|*.sim", wx.FD_SAVE  | wx.FD_OVERWRITE_PROMPT)

        if save.ShowModal() != wx.ID_OK:
            path = save.GetPath()
            self.parent.SaveSimulation(path)

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

    def Warn(parent, message, caption = 'Warning!'):
        dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
        dlg.ShowModal()
        dlg.Destroy()

class DirectoryContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(DirectoryContextMenu, self).__init__()

        self.cmd = parent.cmd
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

class TreeContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(TreeContextMenu, self).__init__()

        self.cmd = parent.cmd
        self.arrow_obj = e
        self.parent = parent

        # mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        # self.AppendItem(mmi)
        # self.Bind(wx.EVT_MENU, self.OnViewDetails, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Expand All')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnExpandAll, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Collapse All')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnCollapseAll, mmi)

    def OnViewDetails(self, e):
       # self.parent.ArrowClicked(self.arrow_obj)
        self.parent.ShowDetails()

    def OnExpandAll(self, e):
        self.parent.OnExpandAll()

    def OnCollapseAll(self, e):
        self.parent.OnCollapseAll()

    def OnMinimize(self, e):
        self.parent.Iconize()

    def OnClose(self, e):
        self.parent.Close()

class TreeItemContextMenu(wx.Menu):

    def __init__(self, parent, e):
        super(TreeItemContextMenu, self).__init__()

        self.cmd = parent.cmd
        self.arrow_obj = e
        self.parent = parent

        mmi = wx.MenuItem(self, wx.NewId(), 'View Details')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnViewDetails, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Expand All')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnExpandAll, mmi)

        mmi = wx.MenuItem(self, wx.NewId(), 'Collapse All')
        self.AppendItem(mmi)
        self.Bind(wx.EVT_MENU, self.OnCollapseAll, mmi)

    def OnViewDetails(self, e):

        self.parent.ShowDetails()

    def OnExpandAll(self, e):
        self.parent.OnExpandAll()

    def OnCollapseAll(self, e):
        self.parent.OnCollapseAll()

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