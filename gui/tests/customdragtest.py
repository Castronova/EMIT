__author__ = 'marioharper'
import wx

app = wx.App()
frame = wx.Frame(None, -1, 'simple.py')
frame.Show()

def getMouse(event):
    frame.Bind(wx.EVT_COMMAND_ENTER, getCoords)

def getCoords(event):
    evt=event
    # print('Hi')
    print(evt.Position)

def leftUp(event):
    print(event.Position)
    # mouse = frame.ScreenToClient(wx.MouseState.GetPosition())
    # print(mouse)


# frame.Bind(wx.EVT_ENTER_WINDOW, getMouse)
# frame.Bind(wx.EVT_MOTION, getCoords)
frame.Bind(wx.EVT_LEFT_UP, leftUp)
app.MainLoop()
