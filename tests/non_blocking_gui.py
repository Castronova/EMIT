import wx
import functools
import threading
import subprocess
import time
import random
from threading import Thread
from functools import wraps

def runAsync(func):
    '''Decorates a method to run in a separate thread'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl
    return wrapper


def wxCallafter(target):
    '''Decorates a method to be called as a wxCallafter'''
    @wraps(target)
    def wrapper(*args, **kwargs):
        wx.CallAfter(target, *args, **kwargs)
    return wrapper

class Frame(wx.Frame):
    def __init__(self):
        super(Frame, self).__init__(None, -1, 'Threading Example')
        # add some buttons and a text control
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # for i in range(3):
        #     name = 'Button %d' % (i+1)
        #     button = wx.Button(panel, -1, name)
        #     func = functools.partial(self.on_button, button=name)
        #     button.Bind(wx.EVT_BUTTON, func)
        #     sizer.Add(button, 0, wx.ALL, 5)
        text = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.text = text
        sizer.Add(text, 1, wx.EXPAND|wx.ALL, 5)
        panel.SetSizer(sizer)

    # def on_button(self, event, button):
    #     # create a new thread when a button is pressed
    #     thread = threading.Thread(target=self.run, args=(button,))
    #     thread.setDaemon(True)
    #     thread.start()

    def on_text(self, text):
        self.text.AppendText(text)


    def run(self):

        while 1:
            time.sleep(.5)
            r = str(random.random())
            wx.CallAfter(self.on_text, r+'\n')

class Frame2(wx.Frame):
    def __init__(self):
        super(Frame2, self).__init__(None, -1, 'Threading Example2')
        # add some buttons and a text control
        panel = wx.Panel(self, -1)
        sizer = wx.BoxSizer(wx.VERTICAL)

        name = 'Button %d' % (1)
        button = wx.Button(panel, -1, name)
        func = functools.partial(self.on_button, button=name)
        button.Bind(wx.EVT_BUTTON, func)
        sizer.Add(button, 0, wx.ALL, 5)

        name = 'Button %d' % (2)
        button = wx.Button(panel, -1, name)
        func = functools.partial(self.on_button2, button=name)
        button.Bind(wx.EVT_BUTTON, func)
        sizer.Add(button, 0, wx.ALL, 5)


        text = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.text = text
        sizer.Add(text, 1, wx.EXPAND|wx.ALL, 5)
        panel.SetSizer(sizer)

    @runAsync
    def on_button2(self, event, button):
        val = 0
        time.sleep(5)
        for i in range(0,100):
            val += random.random()
        wx.CallAfter(self.on_text, str(val)+'\n')

        print 'here'

    @runAsync
    def on_button(self, event, button):
        # create a new thread when a button is pressed
        # thread = threading.Thread(target=self.run, args=(button,))
        # thread.setDaemon(True)
        # thread.start()
        #
        # j = thread.join()
        # print 'here'

        self.run(button)

    def on_text(self, text):
        self.text.AppendText(text)
    def run(self, button):

        for i in range(0,10):
            time.sleep(.5)
            r = str(random.random())
            wx.CallAfter(self.on_text, r+'\n')

        return [1,2,3,4]

if __name__ == '__main__':

    app = wx.PySimpleApp()
    # frame = Frame()
    # thread = threading.Thread(target=frame.run, args=())
    # thread.setDaemon(True)
    # thread.start()
    # frame.Show()


    frame2 = Frame2()
    frame2.Show()
    app.MainLoop()
