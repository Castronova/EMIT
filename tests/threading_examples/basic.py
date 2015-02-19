__author__ = 'tonycastronova'

import wx
import time
import threading


ID_COUNT = wx.NewId()

myEVT_COUNT = wx.NewEventType()
EVT_COUNT = wx.PyEventBinder(myEVT_COUNT, 1)
class CountEvent(wx.PyCommandEvent):
    """Event to signal that a count value is ready"""
    def __init__(self, etype, eid, value=None):
        """Creates the event object"""
        wx.PyCommandEvent.__init__(self, etype, eid)
        self._value = value

    def GetValue(self):
        """Returns the value from the event.
        @return: the value of this event

        """
        return self._value



class CountingThread(threading.Thread):
    def __init__(self, parent, value):
        """
        @param parent: The gui object that should recieve the value
        @param value: value to 'calculate' to
        """
        threading.Thread.__init__(self)
        self._parent = parent
        self._value = value

    def run(self):
        """Overrides Thread.run. Don't call this directly its called internally
        when you call Thread.start().
        """
        time.sleep(10) # our simulated calculation time
        evt = CountEvent(myEVT_COUNT, -1, self._value)
        wx.PostEvent(self._parent, evt)

#-----------------------------------------------------------------------------#

class CountingFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, title="Lets Count", size=(300, 300))

        # Attributes

        # Layout
        self.__DoLayout()
        self.CreateStatusBar()

        # Event Handlers

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(CountingPanel(self), 1, wx.ALIGN_CENTER)
        self.SetSizer(sizer)
        self.SetMinSize((300, 300))

#-----------------------------------------------------------------------------#

class CountingPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        # Attributes
        self._counter = wx.StaticText(self, label="0")
        self._counter.SetFont(wx.Font(16, wx.MODERN, wx.NORMAL, wx.NORMAL))

        self.button = wx.Button(self, ID_COUNT, "Increment Counter")
        self.msg_btn = wx.Button(self, ID_COUNT, "Popup Message")

        # Layout
        self.__DoLayout()

        # Event Handlers
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)
        self.msg_btn.Bind(wx.EVT_BUTTON, self.popup_message)
        self.Bind(EVT_COUNT, self.OnCount)

    def __DoLayout(self):
        sizer = wx.BoxSizer(wx.VERTICAL)


        # sizer.Add(button, proportion=0, border=5, flag=wx.ALIGN_CENTER)
        # sizer.AddSpacer(10)
        # sizer.Add(msg_btn, proportion=0,border=5, flag=wx.ALIGN_CENTER)
        sizer.AddMany([(self.button, 0, wx.ALIGN_CENTER),((15, 15), 0),
                       (self._counter, 0, wx.ALIGN_CENTER),
                       (self.msg_btn, 0, wx.ALIGN_CENTER),((15, 15), 0)])
        self.SetSizer(sizer)


    def OnButton(self, evt):
        worker = CountingThread(self, 1)
        worker.start()

    def OnCount(self, evt):
        val = int(self._counter.GetLabel()) + evt.GetValue()
        self._counter.SetLabel(unicode(val))

    # def OnButton(self, evt):
    #     # This thread is fairly lazy by itself so it takes it
    #     # 10 seconds to figure out what the next value is.
    #     time.sleep(10)
    #     val = int(self._counter.GetLabel()) + 1
    #     self._counter.SetLabel(unicode(val))

    def popup_message(self, event):
        dlg = wx.MessageDialog(None, 'HELLO', 'some caption', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

        # wx.MessageBox(None, 'HELLO!', style=wx.OK)
#-----------------------------------------------------------------------------#

if __name__ == '__main__':
    APP = wx.App(False)
    FRAME = CountingFrame(None)
    FRAME.Show()
    APP.MainLoop()