__author__ = 'Francisco'

import wx
from gui.views.viewPreRun import viewPreRun
from gui import events
import os


class logicPreRun(viewPreRun):
    def __init__(self, parent):

        self.parent = ""
        self.logic = ""
        self.page1 = ""

        self.logic = viewPreRun.__init__(self)
        self.parent = parent

        self.dlg = self.page1.onAddUser()
        self.initBinding()

    def initBinding(self):
        self.page1.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.page1.runButton.Bind(wx.EVT_BUTTON, self.OnRun)
        self.page1.addAccountButton.Bind(wx.EVT_BUTTON, self.OnAddNew)
        self.dlg.okbutton.Bind(wx.EVT_BUTTON, self.OnOkButton)

    def OnCancel(self, event):
        frame = self.GetTopLevelParent()
        frame.Close(True)

    def OnRun(self, event):
        e = dict()
        events.onClickRun.fire(**e)  # Calls onClickRun from viewContext.py
        self.OnCancel(event)  # Close after Run is clicked

    def OnAddNew(self, event):
        self.dlg.CenterOnScreen()
        self.dlg.ShowModal()

    def OnOkButton(self, event):

        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/preferences'))
        file = open(connections_txt, 'a')
        self.accountinfo = self.dlg.GetTextBoxValues()
        accounttxt = "[person]\n" \
                "firstname = " + self.accountinfo[0] + "\n"\
                 + "lastname = " + self.accountinfo[1] + "\n"\
                 + "organizationcode = " + self.accountinfo[2] + "\n"\
                 + "phone = " + self.accountinfo[3] + "\n"\
                 + "email = " + self.accountinfo[4] + "\n"\
                 + "address = " + self.accountinfo[5] + "\n"\
                 + "start_date = " + self.accountinfo[6] + "\n"\
                     + "\n"
        self.RefreshCombo()

        file.write(accounttxt)
        file.close()
        self.dlg.Close(True)

    def RefreshCombo(self):
        # Simply appends the item to the combobox
        self.page1.accountCombo.AppendItems([self.accountinfo[1]])

