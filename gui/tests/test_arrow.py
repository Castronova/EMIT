__author__ = 'tonycastronova'

import wx
import sys
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

sys.path.append("..")

from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources, Utilities, GUIMode

from wx.lib.ogl import RectangleShape

from wx.lib.floatcanvas.Utilities import GUI
from math import *
import numpy as N

from numpy import meshgrid, linspace


class DrawFrame(wx.Frame):

    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        self.CreateStatusBar()
        # Add the Canvas
        NC = NavCanvas.NavCanvas(self,
                                 size= (500,500),
                                 ProjectionFun = None,
                                 Debug = 0,
                                 )

        self.Canvas = NC.Canvas


        self.Show(True)


        # --- draw link between centroids ---

        # build link
        link_pts = get_line_pts([-100,-170],[500,301],order=4, num=1000)

        # construct arrow in center of line
        arrow_coords = build_arrow(link_pts)

        # plot the link and arrowhead
        self.Canvas.AddObject(FloatCanvas.Polygon(arrow_coords,FillColor='Blue',InForeground=True))
        #self.Canvas.AddObject(FloatCanvas.Line(link_pts,LineWidth=2,InForeground=False))


        cmap = plt.cm.jet
        num_colors = len(link_pts)
        colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

        # import random
        # r = lambda: random.randint(0,255)
        for i in range(0,len(link_pts)-1):
            #color = '#%02X%02X%02X' % (r(),r(),r())
            color = mcolors.rgb2hex(colors[i])
            #color = colors[i][:-1]
            self.Canvas.AddObject(FloatCanvas.Line((link_pts[i],link_pts[i+1]),LineColor=color,LineWidth=2,InForeground=False))



        # --- draw rounded rectangle objects ---
        # draw some boxes
        draw_rounded_rectangle(self.Canvas,(-100,-170),width=200, height=100)
        draw_rounded_rectangle(self.Canvas,(500,301), width=250, height=150)






        # zoom to bounding box
        self.Canvas.ZoomToBB()

        return None


def build_arrow(pts,arrow_length=3):

    if arrow_length > len(pts)/2:
        print '> Arrow length is too large! Setting arrow length to default (i.e. 3)'
        arrow_length = 3



    # get the center coordinate of line
    x1,y1 = pts[len(pts)/2]

    # get the point at 'length' away from center
    x2,y2 = pts[(len(pts)/2) - int(arrow_length)]


    actual_length = sqrt((x2-x1)**2 + (y2-y1)**2)

    # determine the slope of this line segment
    m = (y2-y1) / (x2-x1)
    M = -1./m

    # determine y intercept
    b = y2 - M*x2


    # determine (x3,y3) and (x4,y4)
    x3 = x2 + actual_length/3
    y3 = M*x3 + b

    x4 = x2 - actual_length/3
    y4 = M*x4 + b


    return (x1,y1), (x3,y3),(x4,y4)



def draw_rounded_rectangle(canvas, center, width=50, height=50):

        bez = bezier()
        s = N.array(center)
        w = width
        h = height
        wh = N.array([width,height])

        # build rounded rectangle points
        start = s - wh/2
        end = s + wh/2

        tb = range(start[1],end[1],1)
        lr = range(start[0],end[0],1)

        # build the edges
        l = [(start[0],tb[i]) for i in range(0,len(tb))]
        r = [(end[0],tb[i]) for i in range(0,len(tb))]
        t = [(lr[i],end[1]) for i in range(0,len(lr))]
        b = [(lr[i],start[1]) for i in range(0,len(lr))]

        # order lists clockwise
        r.reverse()
        b.reverse()

        # remove radius coords
        l = N.array(l[10:-10])
        t = N.array(t[10:-10])
        r = N.array(r[10:-10])
        b = N.array(b[10:-10])


        # # plot the edges
        #for coords in [l,r,t,b]:
        #    canvas.AddObject(FloatCanvas.Line(coords,LineColor = 'red'))


        # build corners
        corners = []


        ltc = bez.GetBezier([l[-1],l[-1]+[0,5],t[0]-[5,0],t[0]])
        rtc = bez.GetBezier([t[-1],t[-1]+[5,0],r[0]+[0,5],r[0]])
        rbc = bez.GetBezier([r[-1],r[-1]-[0,5],b[0]+[5,0],b[0]])
        lbc = bez.GetBezier([b[-1],b[-1]-[5,0],l[0]-[0,5],l[0]])

        corners =[  [ltc, [l[-1],l[-1]+[0,5]],[t[0]-[5,0],t[0]]],
                    [rtc, [t[-1],t[-1]+[5,0]],[r[0]+[0,5],r[0]]],
                    [rbc, [r[-1],r[-1]-[0,5]],[b[0]+[5,0],b[0]]],
                    [lbc, [b[-1],b[-1]-[5,0]],[l[0]-[0,5],l[0]]]
                    ]

        # plot corners
        # for corner in corners:
        #     pts = corner[0]
        #     canvas.AddObject(FloatCanvas.Line(N.array([pts[0],pts[1]])))
        #     canvas.AddObject(FloatCanvas.Line(N.array([pts[2],pts[3]])))
        #     canvas.AddObject(FloatCanvas.Line(corner[1],LineColor='green'))


        # build polygon object
        coords = N.vstack((l,ltc,t,rtc,r,rbc,b,lbc))

        canvas.AddObject(FloatCanvas.Polygon(coords,FillColor='yellow',FillStyle='Solid'))


#        canvas.Canvas.AddObject(FloatCanvas.Line(lc,LineColor='yellow'))






class SmoothLine(FloatCanvas.Line):
    """

    The SmoothLine class is identical to the Line class except that it uses a
    GC rather than a DC.

    """
    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        Points = WorldToPixel(self.Points)
        GC = wx.GraphicsContext.Create(dc)
        GC.SetPen(self.Pen)
        GC.DrawLines(Points)


class AlphaLine(FloatCanvas.Line):
    """

    The AlphaLine class draws a line with a border and a fill colour with
    optional 'start alpha' and 'end alpha' to determine the fill gradient

    """
    def __init__(self,Points,
            LineColor = "Blue",
            LineStyle = "Solid",
            LineWidth    = 1,
            InForeground = True,
            StartAlpha = 0,
            EndAlpha = 255,
            BorderColour = "White"):

        FloatCanvas.DrawObject.__init__(self, InForeground)

        self.Points = N.array(Points,N.float)
        self.CalcBoundingBox()

        self.LineColor = LineColor
        self.LineStyle = LineStyle
        self.LineWidth = LineWidth
        self.StartAlpha = StartAlpha
        self.EndAlpha = EndAlpha
        self.BorderColour = BorderColour

    def Perpendicular(self, line, length):
        """Return a point that is perpendicular to 'line'

        Given a line defined as two points [(x1, y1), (x2, y2)] return a point
        that will create a new line that is perpendicular. 'length' gives the
        vertical distance from (x2, y2)

        """
        x1,y1 = line[0]
        x2,y2 = line[1]
        angle = pi

        theta = atan((x2 - x1) / (y2 - y1))
        alpha = 2 * pi - (angle + theta)
        l = length * cos(alpha)
        dx = l * sin(alpha)
        dy = l * cos(alpha)

        if dx != abs(dx):
            dx *= -1

        if dy != abs(dy):
            dy *= -1

        x3 = x2 - dx
        y3 = y2 - dy

        return x3,y3

    def _Draw(self, dc , WorldToPixel, ScaleWorldToPixel, HTdc=None):
        #Points = WorldToPixel(self.Points)
        bcolour = self.BorderColour

        Points = self.Points
        GC = wx.GraphicsContext.Create(dc)



        c = wx.Colour()
        c.SetFromName(self.LineColor)
        r,g,b = c.Get()

        c1 = wx.Colour(r, g, b, self.StartAlpha)
        c2 = wx.Colour(r, g, b, self.EndAlpha)

        Path = GC.CreatePath()

        bottomline = Points[1:].copy()

        lastline = Points[-2:]
        firstline = Points[:2]
        firstline = firstline[::-1]
        perplast = self.Perpendicular(lastline, self.LineWidth)
        perpfirst = self.Perpendicular(firstline, self.LineWidth)
        data = Points[:]
        data[:,1] -= self.LineWidth

        while perplast[0] >  data[-1,0]:
            data = data[:-1]

        data = N.resize(data, (len(data) + 1,2))
        data[-1] = perplast

        data = data[::-1]

        while  perpfirst[0] > data[-1,0]:
            data = data[:-1]

        data = N.resize(data, (len(data) + 1,2))
        data[-1] = perpfirst
        topline = data


        Path.MoveToPoint(WorldToPixel(perpfirst))

        if bottomline[-1, 0] >= perplast[0]:
            bottomline[-1] = perplast

        bottomline = WorldToPixel(bottomline)
        for point in bottomline:
            Path.AddLineToPoint(point)

        topline = WorldToPixel(topline)
        for point in topline:
            Path.AddLineToPoint(point)

        GC.SetPen(wx.Pen(bcolour))
        GC.DrawPath(Path)

        Points = WorldToPixel(Points)
        m = Points[:,0].size - 1

        Brush = \
            GC.CreateLinearGradientBrush(Points[0,0], \
            Points[0,1], Points[m,0], Points[m,1], c1, c2)

        GC.SetBrush(Brush)
        GC.FillPath(Path)



def get_line_pts(start, end, order=3, num=10):


        # get start and end x,y
        startX = start[0]
        startY = start[1]
        endX   = end[0]
        endY   = end[1]

        # get the arrow vertices
        _trianglePoints = GetTrianglePoints( startX, startY, endX, endY );

        lineArray = []

        # draw curved line
        lineArray.append((startX,startY))
        lineArray.append((startX - ((startX - endX) / 3), startY))
        lineArray.append((endX - ((endX - startX) / 3), endY))
        lineArray.append((endX, endY))

        control_pts = N.array(lineArray)

        from numpy import linspace

        n = order
        V = num

        b = bezier()
        bez = b.Bezier_Curve_n(control_pts,n)

        pts = []
        for val in linspace( 0, 1, V ):
            #print '%s: %s' % (val, bez( val ))
            pts.append(tuple(bez(val)))

        #for pt in pts:
        #    print pt

        return pts
        # g.SmoothingMode = SmoothingMode.AntiAlias;
        # g.DrawBeziers(arrowPen, lineArray);
        # _arrowPath.AddBeziers(lineArray);
        # _arrowPath.Flatten();
        #
        # //g.DrawLine(linePen, startX, startY, endX, endY);
        #
        # if (Math.Abs(startX - endX) + Math.Abs(startY - endY) > 10)
        # {
        #     return windowTrianglePoints;
        # }
        # else
        #     return new Point[0];


def GetTrianglePoints(startx,starty,endx,endy):

        trianglePoints = []

        # define the size of the triangles
        size = 50

        # determine x,y midpoints
        midx   = (endx + startx) / 2
        midy   = (endy + starty) / 2

        # calculate the arrow length
        length = sqrt((startx-midx)**2) + (starty-midy)**2


        # calculate the arrow vertices
        px = midx + size *(startx - midx)/length
        py = midy + size *(starty - midy)/length

        vx = midx - px
        vy = midy - py

        t1x = px - vy
        t1y = py + vx

        t2x = px + vy
        t2y = py - vx

        # save the arrow vertices
        trianglePoints.append((midx,midy))
        trianglePoints.append((t1x,t1y))
        trianglePoints.append((t2x,t2y))

        return trianglePoints




class bezier():
    def __init__(self):
        pass

    ## n := len( P ) - 1
    ## n is the degree.  If n == 3, the bezier is cubic.
    ## t is the parameter along the curve.  t is in [0,1].

    def fac(self, k ):
        '''
        Returns k!.
        '''

        if k == 0: return 1
        else: return reduce(lambda i,j : i*j, range(1,k+1))

    def binom(self, n, k ):
        '''
        Returns n choose k.
        '''

        if k < 0 or k > n: return 0

        return self.fac( n ) / ( self.fac( k ) * self.fac( n - k ) )

    def B(self, P, t ):
        '''
        Evaluates the bezier curve of degree len(P) - 1, using control points 'P',
        at parameter value 't' in [0,1].
        '''
        n = len( P ) - 1
        assert n > 0

        from numpy import zeros
        result = zeros( len( P[0] ) )
        for i in xrange( n + 1 ):
            result += self.binom( n, i ) * P[i] * (1 - t)**(n-i) * t**i

        return result

    def B_n(self, P, n, t ):
        '''
        Evaluates the bezier curve of degree 'n', using control points 'P',
        at parameter value 't' in [0,1].
        '''

        ## clamp t to the range [0,1]
        t = min( 1., max( 0., t ) )

        num_segments = 1 + (len( P ) - (n+1) + n-1) // n
        assert num_segments > 0
        from math import floor
        segment_offset = min( int( floor( t * num_segments ) ), num_segments-1 )

        P_offset = segment_offset * n

        return self.B( P[ P_offset : P_offset + n+1 ], ( t - segment_offset/float(num_segments) ) * num_segments )

    def Bezier_Curve(self, P ):
        '''
        Returns a function object that can be called with parameters between 0 and 1
        to evaluate the Bezier Curve with control points 'P' and degree len(P)-1.
        '''
        return lambda t: self.B( P, t )

    def Bezier_Curve_n(self, P, n ):
        '''
        Returns a function object that can be called with parameters between 0 and 1
        to evaluate the Bezier Curve strip with control points 'P' and degree n.
        '''
        return lambda t: self.B_n( P, n, t )

    def GetBezier(self,points):
        #print '====== test1() ======'


        #P = meshgrid([0,0],range(3+1))[1]

        #print 'P:'
        #print P

        P = points
        V = 50
        bez = self.Bezier_Curve( P )

        #return bez

        pts = []
        for val in linspace( 0, 1, V ):
            #print '%s: %s' % (val, bez( val ))
            pts.append(tuple(bez(val)))

        return pts
    def test2(self, v):
        #print '====== test2() ======'

        from numpy import meshgrid, linspace
        #P = meshgrid([0,0],range(3+1))[1]

        #print 'P:'
        #print P


        p = [(100, 100), (17, 100), (-66, 0), (-150, 0)]
        P = N.array(p)
        #print P

        n = 3
        #print 'n:', n

        V = v
        bez = self.Bezier_Curve_n( P, n )

        #return bez
        pts = []
        for val in linspace( 0, 1, V ):
            #print '%s: %s' % (val, bez( val ))
            pts.append(tuple(bez(val)))

        return pts


app = wx.PySimpleApp()
DrawFrame(None, -1, "FloatCanvas Rectangle Drawer", wx.DefaultPosition, (700,700) )
app.MainLoop()

