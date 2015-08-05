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
        self.logfilename = "prerunlog.txt"

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

        # todo:  this should be opened after simulation has completed, not right here.
        # if self.viewprerun.page1.displayMessage.GetValue():
            # frm = viewPostRun()
            # frm.Show()

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
        connections_txt = os.path.abspath(os.path.join(currentdir, '../../log/' + self.logfilename))
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
        filepath = self.CreatePreRunLogFile()
        file = open(filepath, 'r')
        if simname in file.read():
            file.close()
            return True
        else:
            file.close()
            return False

    def CreatePreRunLogFile(self):
        currentdir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.abspath(os.path.join(currentdir, '../../log/' + self.logfilename))
        if os.path.exists(filepath):
            return filepath
        else:
            file = open(filepath, 'w')
            file.close()
            return filepath
