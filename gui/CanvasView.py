from images import icons

__author__ = 'Mario'

import wx
import sys
from NavToolbar import NavCanvas

# from wx.lib.floatcanvas import NavCanvas

sys.path.append("..")

class Canvas(NavCanvas):

    def __init__(self, *args, **kwargs):
        NavCanvas.__init__(self, *args,**kwargs)




#class DrawFrame(wx.Frame):
class MyFrame2(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY,
                        title = wx.EmptyString, pos = wx.DefaultPosition,
                        size = wx.Size( 900,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        draw = Canvas(self )
        '''
        canvas = NavCanvas.NavCanvas(id=wx.ID_ANY,parent=self,
                          ProjectionFun = None,
                          Debug = 0,
                          BackgroundColor = "White",
                          )
        '''
class ClearCanvas(NavCanvas):
    def __init__(self):
        def __init__(self, *args, **kwargs):
            NavCanvas.__init__(self, *args,**kwargs)

            self.onRightDown()

    def onRightDown(self, event):
        self.Canvas.ClearAll()
        self.Canvas.Draw()

class Link:
    def __init__(self):
        pass


def SimpleFrame(parent):
    return MyFrame2(parent)
'''
app = wx.App(False)
frame = SimpleFrame(None)
frame.Show(True)

app.MainLoop()
'''

