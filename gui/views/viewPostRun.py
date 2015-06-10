__author__ = 'Francisco'

import wx
import time

class viewPostRun(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, id=wx.ID_ANY, parent=None, title='Post Run', style=wx.STAY_ON_TOP)
        self.amount = 255  # Cannot be greater than 255 because its a 2 byte argument
        self.delta = 5
        self.panel = wx.Panel(self)
        self.runsummary = "Simulation Finished"

        sim_st = time.time()

        self.runsummary = '------------------------------------------\n' +\
                          '          Simulation Summary \n' +\
                          '------------------------------------------\n' +\
                          'Completed without error :)\n' +\
                          'Simulation duration: %3.2f seconds\n' % (time.time() - sim_st) +\
                          '------------------------------------------'

        self.boxsizer = wx.BoxSizer(wx.VERTICAL)

        self.statictext = wx.StaticText(self.panel, label=self.runsummary, style=wx.ALIGN_CENTRE)
        self.boxsizer.Add(self.statictext, flag=wx.ALL, border=5)
        self.panel.SetSizer(self.boxsizer)
        self.Center()
        self.boxsizer.Fit(self)

        self.SetTransparent(self.amount)

        ## ------- Fader Timer -------- ##
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.timer.Start(70)
        self.Bind(wx.EVT_TIMER, self.FadeOutAlphaCycle)

    def FadeInOutAlphaCycle(self, event):
        self.amount += self.delta
        if self.amount >= 255:
            self.delta = -self.delta
            self.amount = 255
        if self.amount <= 0:
            self.amount = 0
            self.Close()
        self.SetTransparent(self.amount)

    def FadeOutAlphaCycle(self, event):
        self.amount -= self.delta
        if self.amount <= 0:
            self.amount = 0
            self.Close()
        if self.amount <= 150:  # wait a second before fading
            self.SetTransparent(self.amount)
