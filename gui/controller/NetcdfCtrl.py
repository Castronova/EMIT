__author__ = 'francisco'

from gui.views.NetcdfViewer import NetcdfViewer

class NetcdfCtrl(NetcdfViewer):

    def __init__(self, parent):  # What parameters does this need?

        NetcdfViewer.__init__(self, parent=parent)

        root = self.tree_ctrl.AddRoot("Root 1")
        item1 = self.tree_ctrl.AppendItem(root, "Item 1")

        file1 = self.tree_ctrl.AppendItem(item1, "file1")
        item2 = self.tree_ctrl.AppendItem(root, "Item 2")

        self.tree_ctrl.ExpandAll()


