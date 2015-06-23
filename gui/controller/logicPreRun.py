__author__ = 'Francisco'

import wx
from gui.views.viewPreRun import viewPreRun
from gui import events
import os
from gui.views.viewPostRun import viewPostRun
import time


class logicPreRun:
    def __init__(self):
        self.viewprerun = viewPreRun()
        self.dlg = self.viewprerun.page1.onAddUser()

        self.initBinding()

    def initBinding(self):
        self.viewprerun.page1.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
        self.viewprerun.page1.runButton.Bind(wx.EVT_BUTTON, self.OnRun)
        self.viewprerun.page1.addAccountButton.Bind(wx.EVT_BUTTON, self.OnAddNew)
        self.dlg.okbutton.Bind(wx.EVT_BUTTON, self.OnOkButton)

    def OnCancel(self, e):
        self.viewprerun.Close(True)


    def OnRun(self, e):
        if self.viewprerun.page1.logMessage.GetValue():  # If log Message Checkbox is checked
            exist = self.CheckSimulationName(self.viewprerun.page1.simulationNameTextBox.GetValue())  # Check if sim name exist

            if exist:
                message = wx.MessageDialog(None, "Simulation name already exist\nWould you like to save and continue?",
                                           "Question", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
                if message.ShowModal() == wx.ID_YES:
                    self.LogSimulation()
                    self.RunSim()
                else:
                    self.viewprerun.page1.simulationName.SetForegroundColour((200, 60, 0))
            else:
                self.LogSimulation()
                self.RunSim()

        else:
            self.RunSim()

    def RunSim(self):
        e = dict()
        events.onClickRun.fire(**e)  # Calls onClickRun from viewContext.py
        self.OnCancel(e)
        if self.viewprerun.page1.displayMessage.GetValue():
            frm = viewPostRun()
            frm.Show()

    def OnAddNew(self, e):
        self.dlg.CenterOnScreen()
        self.dlg.ShowModal()

    def OnOkButton(self, event):

        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/preferences'))
        file = open(connections_txt, 'a')
        self.accountinfo = self.dlg.GetTextBoxValues()
        accounttxt = "[person]\n" \
                     "firstname = " + self.accountinfo[0] + "\n" \
                     + "lastname = " + self.accountinfo[1] + "\n" \
                     + "organizationcode = " + self.accountinfo[2] + "\n" \
                     + "phone = " + self.accountinfo[3] + "\n" \
                     + "email = " + self.accountinfo[4] + "\n" \
                     + "address = " + self.accountinfo[5] + "\n" \
                     + "start_date = " + self.accountinfo[6] + "\n" \
                     + "\n"
        self.RefreshCombo()

        file.write(accounttxt)
        file.close()
        self.dlg.Close(True)

    def RefreshCombo(self):
        # Simply appends the item to the combobox
        self.viewprerun.page1.accountCombo.AppendItems([self.accountinfo[1]])

    def LogSimulation(self):
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../log/log'))
        file = open(connections_txt, 'a')
        loginfo = self.viewprerun.page1.GetLogValues()
        logtxt = "[Simulation]\n" + \
                 "Simulation Name = " + loginfo[0] + "\n" + \
                 "Database = " + loginfo[1] + "\n" + \
                 "User = " + loginfo[2] + "\n" +\
                 "Date = " + time.strftime("%m/%d/%Y") + "\n" + \
                 "Message = " + viewPostRun().runsummary + \
                 "\n\n"
        file.write(logtxt)
        file.close()

    def CheckSimulationName(self, simname):
        currentdir = os.path.dirname(os.path.abspath(__file__))
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../log/log'))
        file = open(connections_txt, 'r')
        if simname in file.read():
            return True
        else:
            return False



'''
# class logicPreRun(viewPreRun):
#     def __init__(self, parent):
#
#         self.parent = ""
#         self.logic = ""
#         self.page1 = ""
#
#         self.logic = viewPreRun.__init__(self)
#         self.parent = parent
#
#         self.dlg = self.page1.onAddUser()
#         self.initBinding()
#
#     def initBinding(self):
#         self.page1.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
#         self.page1.runButton.Bind(wx.EVT_BUTTON, self.OnRun)
#         self.page1.addAccountButton.Bind(wx.EVT_BUTTON, self.OnAddNew)
#         self.dlg.okbutton.Bind(wx.EVT_BUTTON, self.OnOkButton)
#
#     def OnCancel(self, event):
#         frame = self.GetTopLevelParent()
#         frame.Close(True)
#
#     def OnRun(self, event):
#         e = dict()
#         events.onClickRun.fire(**e)  # Calls onClickRun from viewContext.py
#         self.OnCancel(event)
#         if self.page1.displayMessage.GetValue():  # If Checkbox Display Message is checked
#             frm = viewPostRun()
#             frm.Show()
#
#
#     def OnAddNew(self, event):
#         self.class logicPreRun(viewPreRun):
#     def __init__(self, parent):
#
#         self.parent = ""
#         self.logic = ""
#         self.page1 = ""
#
#         self.logic = viewPreRun.__init__(self)
#         self.parent = parent
#
#         self.dlg = self.page1.onAddUser()
#         self.initBinding()
#
#     def initBinding(self):
#         self.page1.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
#         self.page1.runButton.Bind(wx.EVT_BUTTON, self.OnRun)
#         self.page1.addAccountButton.Bind(wx.EVT_BUTTON, self.OnAddNew)
#         self.dlg.okbutton.Bind(wx.EVT_BUTTON, self.OnOkButton)
#
#     def OnCancel(self, event):
#         frame = selclass logicPreRun(viewPreRun):
#     def __init__(self, parent):
#
#         self.parent = ""
#         self.logic = ""
#         self.page1 = ""
#
#         self.logic = viewPreRun.__init__(self)
#         self.parent = parent
#
#         self.dlg = self.page1.onAddUser()
#         self.initBinding()
#
#     def initBinding(self):
#         self.page1.cancelButton.Bind(wx.EVT_BUTTON, self.OnCancel)
#         self.page1.runButton.Bind(wx.EVT_BUTTON, self.OnRun)
#         self.page1.addAccountButton.Bind(wx.EVT_BUTTON, self.OnAddNew)
#         self.dlg.okbutton.Bind(wx.EVT_BUTTON, self.OnOkButton)
#
#     def OnCancel(self, event):
#         frame = self.GetTopLevelParent()
#         frame.Close(True)
#
#     def OnRun(self, event):
#         e = dict()
#         events.onClickRun.fire(**e)  # Calls onClickRun from viewContext.py
#         self.OnCancel(event)
#         if self.page1.displayMessage.GetValue():  # If Checkbox Display Message is checked
#             frm = viewPostRun()
#             frm.Show()
#
#
#     def OnAddNew(self, event):
#         self.dlg.CenterOnScreen()
#         self.dlg.ShowModal()
#
#     def OnOkButton(self, event):
#
#         currentdir = os.path.dirname(os.path.abspath(__file__))
#         connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/preferences'))
#         file = open(connections_txt, 'a')
#         self.accountinfo = self.dlg.GetTextBoxValues()
#         accounttxt = "[person]\n" \
#                      "firstname = " + self.accountinfo[0] + "\n" \
#                      + "lastname = " + self.accountinfo[1] + "\n" \
#                      + "organizationcode = " + self.accountinfo[2] + "\n" \
#                      + "phone = " + self.accountinfo[3] + "\n" \
#                      + "email = " + self.accountinfo[4] + "\n" \
#                      + "address = " + self.accountinfo[5] + "\n" \
#                      + "start_date = " + self.accountinfo[6] + "\n" \
#                      + "\n"
#         self.RefreshCombo()
#
#         file.write(accounttxt)
#         file.close()
#         self.dlg.Close(True)
#
#     def RefreshCombo(self):
#         # Simply appends the item to the combobox
#         self.page1.accountCombo.AppendItems([self.accountinfo[1]])
f.GetTopLevelParent()
#         frame.Close(True)
#
#     def OnRun(self, event):
#         e = dict()
#         events.onClickRun.fire(**e)  # Calls onClickRun from viewContext.py
#         self.OnCancel(event)
#         if self.page1.displayMessage.GetValue():  # If Checkbox Display Message is checked
#             frm = viewPostRun()
#             frm.Show()
#
#
#     def OnAddNew(self, event):
#         self.dlg.CenterOnScreen()
#         self.dlg.ShowModal()
#
#     def OnOkButton(self, event):
#
#         currentdir = os.path.dirname(os.path.abspath(__file__))
#         connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/preferences'))
#         file = open(connections_txt, 'a')
#         self.accountinfo = self.dlg.GetTextBoxValues()
#         accounttxt = "[person]\n" \
#                      "firstname = " + self.accountinfo[0] + "\n" \
#                      + "lastname = " + self.accountinfo[1] + "\n" \
#                      + "organizationcode = " + self.accountinfo[2] + "\n" \
#                      + "phone = " + self.accountinfo[3] + "\n" \
#                      + "email = " + self.accountinfo[4] + "\n" \
#                      + "address = " + self.accountinfo[5] + "\n" \
#                      + "start_date = " + self.accountinfo[6] + "\n" \
#                      + "\n"
#         self.RefreshCombo()
#
#         file.write(accounttxt)
#         file.close()
#         self.dlg.Close(True)
#
#     def RefreshCombo(self):
#         # Simply appends the item to the combobox
#         self.page1.accountCombo.AppendItems([self.accountinfo[1]])
dlg.CenterOnScreen()
#         self.dlg.ShowModal()
#
#     def OnOkButton(self, event):
#
#         currentdir = os.path.dirname(os.path.abspath(__file__))
#         connections_txt = os.path.abspath(os.path.join(currentdir, '../../data/preferences'))
#         file = open(connections_txt, 'a')
#         self.accountinfo = self.dlg.GetTextBoxValues()
#         accounttxt = "[person]\n" \
#                      "firstname = " + self.accountinfo[0] + "\n" \
#                      + "lastname = " + self.accountinfo[1] + "\n" \
#                      + "organizationcode = " + self.accountinfo[2] + "\n" \
#                      + "phone = " + self.accountinfo[3] + "\n" \
#                      + "email = " + self.accountinfo[4] + "\n" \
#                      + "address = " + self.accountinfo[5] + "\n" \
#                      + "start_date = " + self.accountinfo[6] + "\n" \
#                      + "\n"
#         self.RefreshCombo()
#
#         file.write(accounttxt)
#         file.close()
#         self.dlg.Close(True)
#
#     def RefreshCombo(self):
#         # Simply appends the item to the combobox
#         self.page1.accountCombo.AppendItems([self.accountinfo[1]])
'''