import os
import wx
import wx.xrc
from shapely import wkt
from utilities import gui, spatial
from gui.views.ModelView import ViewModel
# todo: refactor
# from ..DirectoryLstCtrl import DirectoryListCtrl
from gui.controller.DirectoryListControlCtrl import LogicDirectoryListControl
from gui.Resources import icons
from coordinator.emitLogging import elog

[PreviousID, UpID, HomeID, SaveID, RefreshID, TerminalID, HelpID] = [wx.NewId() for _init_ctrls in range(7)]

class ViewDirectory(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(350, 300),
                          style=wx.TAB_TRAVERSAL)

        self.textCtrl = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(350, -1),
                                       wx.TE_READONLY|wx.TE_CHARWRAP)
        self.textCtrl.SetValue(os.getcwd())

        # self.dirCtrl = ViewDirectoryListControl(self, wx.ID_ANY, wx.DefaultPosition, wx.Size(1000, 400), wx.LC_REPORT)
        self.dirCtrl = LogicDirectoryListControl(self, wx.Size(1000, 400), wx.LC_REPORT)

        self.toolbar = self.iconToolBar()

        self.directoryStack = []
        self.directoryStack.append(self.dirCtrl.gethomepath())


        self.initInterface()


    def initInterface(self):
        border = 3
        panelSizer = wx.BoxSizer(wx.VERTICAL)


        panelSizer.Add(self.toolbar, 0, wx.EXPAND, border)

        listCtrlSizer = wx.BoxSizer(wx.VERTICAL)
        listCtrlSizer.SetMinSize(wx.Size(350, 600))
        listCtrlSizer.Add(self.textCtrl, 0, wx.ALL | wx.EXPAND, border)
        listCtrlSizer.Add(self.dirCtrl, 1, wx.ALL, border)

        panelSizer.Add(listCtrlSizer, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, border)

        self.SetSizer(panelSizer)
        self.Layout()




    def iconToolBar(self):
        toolbar = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        toolbar.AddSeparator()

        tool = toolbar.AddLabelTool(PreviousID, label='Previous', bitmap=icons.go_previous.GetBitmap())
        tool = toolbar.AddLabelTool(UpID, label='Up one directory', bitmap=icons.go_up.GetBitmap())
        tool = toolbar.AddLabelTool(HomeID, label='Go Home', bitmap=icons.go_home.GetBitmap())
        tool = toolbar.AddLabelTool(RefreshID, label='Refresh', bitmap=icons.view_refresh.GetBitmap())
        # tool = toolbar.AddLabelTool(SaveID, label='Save', bitmap=icons.document_save.GetBitmap())
        # tool = toolbar.AddLabelTool(TerminalID, label='Terminal', bitmap=icons.draw_star.GetBitmap())
        # tool = toolbar.AddLabelTool(HelpID, label='Help', bitmap=icons.help_info.GetBitmap())

        toolbar.AddSeparator()
        toolbar.Realize()
        return toolbar



    def ShowDetails(self):

        # create the details view
        view = ViewModel(self, spatial=False)


        # load the file contents
        view.PopulateEdit(self.sb.GetValue())


        # load the geometry data
        # view.PopulateSpatial(self.read_geoms(self.sb.GetValue(),'input'),'input')
        # view.PopulateSpatial(self.read_geoms(self.sb.GetValue(),'output'),'output')

        # show the details view
        #listview = MyTree(self)
        view.PopulateEdit(self.sb.GetValue())
        view.PopulateDetails(self.sb.GetValue())

        #listview.PopulateDetails(self.sb.GetValue())
        view.Show()


    def read_geoms(self, filepath, type):

        coords = []

        # if this is a mdl file
        if filepath.split('.')[-1] == 'mdl':

            # parse the mdl file
            dic = gui.parse_config(self.sb.GetValue())

            geom = []
            if type in dic:
                for input in dic[type]:

                    # return empty coord array if no elementset is defined
                    if 'elementset' not in input:
                        return []

                    eset = input['elementset']

                    # check if the value is a path
                    if os.path.dirname(eset ) != '':
                        if not os.path.isfile(eset):
                            elog.warning('Could not find file: %s' % eset)
                            raise Exception('Could not find file: %s' % eset)

                        geom,srs = spatial.read_shapefile(eset)

                    # otherwise it must be a wkt
                    else:
                        value = ''
                        try:
                            value = eset.strip('\'').strip('"')
                            geoms = wkt.loads(value)

                            if 'Multi' in geoms.geometryType():
                                    geom  = [g for g in geoms]
                            else:
                                geom = [geoms]

                        except:
                            elog.warning('Could not load WKT string: %s.' % value)
                            raise Exception('Could not load WKT string: %s.' % value)



                # build coord list
                for g in geom:
                    if g.type == 'Polygon':
                        coords.append(list(g.boundary.coords))
                    elif g.type == 'Point':
                        coords.append(list(g.coords))
                    elif g.type == 'LineString':
                        coords.append(list(g.coords))

        return coords

        #ShowModel.Show()

