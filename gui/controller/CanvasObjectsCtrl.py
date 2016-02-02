import os
import math
from math import *
from os import path

import wx
from wx.lib.floatcanvas import FloatCanvas as FC

import datatypes

#sys.path.append("..")


class ShapeType():
    ArrowHead = 'ArrowHead'
    Model = 'Model'
    Link = 'Link'
    Label= 'Label'

class SmoothLine(FC.Line):
    """
    The SmoothLine class is identical to the Line class except that it uses a
    GC rather than a DC.
    """
    def __init__(self, Points, LineColor = "Black", LineStyle = "Solid", LineWidth = 1, InForeground = False):
        FC.Line.__init__(self, Points, LineColor, LineStyle, LineWidth, InForeground)
        midX = (Points[0][0]+Points[1][0])/2
        midY = (Points[0][1]+Points[1][1])/2
        self.MidPoint = (midX,midY)

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Points = WorldToPixel(self.Points)
        midX = (self.Points[0][0]+self.Points[1][0])/2
        midY = (self.Points[0][1]+self.Points[1][1])/2
        self.MidPoint = (midX,midY)
        GC = wx.GraphicsContext.Create(dc)
        GC.SetPen(self.Pen)
        GC.DrawLines(Points)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.DrawLines(Points)

    def GetAngleRadians(self):
        # Calculate the angle of the line and set the arrow to that angle
        xdiff = self.Points[1][0]-self.Points[0][0]
        ydiff = self.Points[1][1]-self.Points[0][1]
        return math.atan2(ydiff, xdiff)


class ScaledBitmapWithRotation(FC.ScaledBitmap):

    def __init__(self, Bitmap, XY, Angle=0.0, Position = 'cc', InForeground = True):
        FC.ScaledBitmap.__init__(self, Bitmap, XY, Height=Bitmap.Height, Position = 'cc', InForeground = True)
        self.ImageMidPoint = (self.Image.Width/2, self.Image.Height/2)
        self.RotationAngle = Angle
        if Angle != 0.0:
            Img = self.Image.Rotate(self.RotationAngle, (0,0))
            self.ScaledBitmap = wx.BitmapFromImage(Img)
        self.LastRotationAngle = 0.0

    def _Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Img = self.Image.Rotate(self.RotationAngle, (0,0), interpolating=True)
        self.Height = Img.Height
        self.ImageMidPoint = (Img.Width/2, Img.Height/2)

        XY = WorldToPixel(self.XY)
        H = ScaleWorldToPixel(self.Height)[0]
        W = H * (self.bmpWidth / self.bmpHeight)

        if (self.ScaledBitmap is None) or (H != self.ScaledHeight):
            self.ScaledHeight = H
            self.ScaledBitmap = wx.BitmapFromImage(Img)

        XY = self.ShiftFun(XY[0], XY[1], W, H)
        dc.DrawBitmapPoint(self.ScaledBitmap, XY, True)
        if HTdc and self.HitAble:
            HTdc.SetPen(self.HitPen)
            HTdc.SetBrush(self.HitBrush)
            HTdc.DrawRectanglePointSize(XY, (W, H))

        self.LastRotationAngle = self.RotationAngle

    def Rotate(self, angle):

        self.RotationAngle = angle

class SmoothLineWithArrow(SmoothLine):
    '''
    Based on FloatCanvas Line and ScaledBitmap. This simply integrates
    the two and adds the rotation feature that we need. This might be able
    to be better implemented as FloatCanvas Group
    '''
    def __init__(self, Points, LineColor="#3F51B5", LineStyle="Solid", LineWidth = 4):
        super(SmoothLineWithArrow, self).__init__(Points, LineColor, LineStyle, LineWidth)
        imgs_base_path = os.environ['APP_IMAGES_PATH']
        arrow_image = path.join(imgs_base_path, 'rightArrowBlue60.png')
        arrow_bitmap = wx.Image(arrow_image, wx.BITMAP_TYPE_PNG)
        self.Arrow = ScaledBitmapWithRotation(Angle=self.GetAngleRadians(), Bitmap=arrow_bitmap, XY=self.MidPoint)
        self.Arrow.line = self  # This allows us to remove the entire object given a reference to just the arrow

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        super(SmoothLineWithArrow,self)._Draw(dc , WorldToPixel, ScaleWorldToPixel, HTdc=None)
        # Uncomment the line below if we figure out how to bind to the entire SmoothLineWithArrow object
        # self.Arrow._Draw(dc, WorldToPixel, ScaleWorldToPixel, HTdc=None)

    # FloatCanvas' RemoveObject function does not remove the arrow,
    # so we use this helper function instead which takes a FloatCanvas obj
    def Remove(self, FC):
        FC.RemoveObject(self)
        FC.RemoveObject(self.Arrow)

class ModelBox(FC.Group):
    def __init__(self, type, XY, text, id):
        self.Links = []
        self.XY = XY
        self.ID = id

        # Set box color based on model type
        imgs_base_path = os.environ['APP_IMAGES_PATH']
        bmp = None
        if type == datatypes.ModelTypes.TimeStep:
            bmp = wx.Image(path.join(imgs_base_path,'E.png'), wx.BITMAP_TYPE_PNG)
        elif type == datatypes.ModelTypes.FeedForward:
            bmp = wx.Image(path.join(imgs_base_path,'B.png'), wx.BITMAP_TYPE_PNG)
        elif type == datatypes.ModelTypes.Data:
            bmp = wx.Image(path.join(imgs_base_path, 'N.png'), wx.BITMAP_TYPE_PNG)
        else: # default type
            bmp = wx.Image(path.join(imgs_base_path, 'M.png'), wx.BITMAP_TYPE_PNG)

        self.box = FC.Bitmap(bmp, XY, Position="cc", InForeground=True)
        self.Width = bmp.Width
        self.Height = bmp.Height

        font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        font_size = 15
        self.label = FC.ScaledTextBox(text, XY, Color="Black", Size=font_size,
                                      Width=bmp.Width-30, Position="cc",
                                      Alignment="center", Weight=wx.BOLD,
                                      InForeground=True, Font=font, LineWidth=0,
                                      LineColor=None)

        FC.Group.__init__(self, [self.box, self.label], InForeground=True)

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel = None, HTdc = None):
        FC.Group._Draw(self, dc, WorldToPixel, ScaleWorldToPixel, HTdc)
        # The box's XY is updated in FloatCanvas's Bitmap Draw function, so we will copy that
        self.XY = self.box.XY


