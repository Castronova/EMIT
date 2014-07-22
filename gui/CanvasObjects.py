__author__ = 'Mario'

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


        # --- draw link between centroids ---

        # # build link
        # link_pts = get_line_pts([-100,-170],[500,301],order=4, num=100)
        #
        # # construct arrow in center of line
        # arrow_coords = build_arrow(link_pts, arrow_length=3)

        # plot the link and arrowhead
        #self.Canvas.AddObject(FloatCanvas.Polygon(arrow_coords,FillColor='Blue',InForeground=True))


        # cmap = plt.cm.Blues
        # num_colors = len(link_pts)
        # colors = [cmap(1.*i/num_colors) for i in range(num_colors)]
        #
        # for i in range(0,len(link_pts)-1):
        #     color = mcolors.rgb2hex(colors[i])
        #     #self.Canvas.AddObject(FloatCanvas.Line((link_pts[i],link_pts[i+1]),LineColor=color,LineWidth=2,InForeground=False))



        # --- draw rounded rectangle objects ---
        # draw some boxes
        # draw_rounded_rectangle(self.Canvas,(-100,-170),width=200, height=100)
        # draw_rounded_rectangle(self.Canvas,(500,301), width=250, height=150)




        #
        #
        # # zoom to bounding box
        # self.Canvas.ZoomToBB()
        #
        # return None


def get_hex_from_gradient(gradient, num):
    cmap = gradient
    num_colors = num
    colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

    hexcolors = []
    for i in range(0,num_colors):
        hexcolors.append(mcolors.rgb2hex(colors[i]))

    return hexcolors

def build_arrow(pts,arrow_length=3):

    if arrow_length > len(pts)/2:
        print '> Arrow length is too large! Setting arrow length to default (i.e. 3)'
        arrow_length = 3




    # get the center coordinate of line
    x1,y1 = pts[len(pts)/2]

    # get the point at 'length' away from center
    x2,y2 = pts[(len(pts)/2) - int(arrow_length)]

    #return (x1,y1), ()

    actual_length = sqrt((x2-x1)**2 + (y2-y1)**2)

    # determine the slope of this line segment
    m = (y2-y1) / (x2-x1)
    M = -1./m

    # determine y intercept
    b = y2 - M*x2

    import numpy as np
    import math

    # find start and end range based on distance from x2,y2
    idx = np.where(pts==x2)[0][0]

    distance = 0
    xstart = None
    ystart = None
    for x,y in pts[idx+1:]:
        xstart = x
        ystart = y
        distance = math.sqrt((x2-x)**2 + (y2-y)**2)
        if distance > 10: break

    distance = 0
    xend  = None
    yend = None
    for x,y in list(reversed(pts))[idx+1:]:
        xend= x
        yend = y
        distance = math.sqrt((x2-x)**2 + (y2-y)**2)
        if distance > 10: break


    # from numpy import linspace
    # x3 = linspace(pts[len(pts)/2 -10][0],pts[len(pts)/2 +10][0],100)

    x3 = np.arange(xstart,xend,.1)

    y3 = [M*x + b for x in x3]
    inverse = zip(x3, y3)

    diff = [abs(x2-x)for x in x3]
    idx = diff.index(min(diff))

    v1 = inverse[idx+5]
    v2 = inverse[idx-5]
    v3 = (x1,y1)
    return v1,v2,v3




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



        ltc = bez.GetBezier([l[-1],l[-1]+[0,5],t[0]-[5,0],t[0]])
        rtc = bez.GetBezier([t[-1],t[-1]+[5,0],r[0]+[0,5],r[0]])
        rbc = bez.GetBezier([r[-1],r[-1]-[0,5],b[0]+[5,0],b[0]])
        lbc = bez.GetBezier([b[-1],b[-1]-[5,0],l[0]-[0,5],l[0]])

        corners =[  [ltc, [l[-1],l[-1]+[0,5]],[t[0]-[5,0],t[0]]],
                    [rtc, [t[-1],t[-1]+[5,0]],[r[0]+[0,5],r[0]]],
                    [rbc, [r[-1],r[-1]-[0,5]],[b[0]+[5,0],b[0]]],
                    [lbc, [b[-1],b[-1]-[5,0]],[l[0]-[0,5],l[0]]]
                    ]

        # build polygon object
        coords = N.vstack((l,ltc,t,rtc,r,rbc,b,lbc))


        return coords


def get_line_pts(start, end, order=3, num=100):


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
        import numpy
        n = order
        V = num

        b = bezier()
        bez = b.Bezier_Curve_n(control_pts,n)

        pts = []
        for val in linspace( 0, 1, V ):
            #pts.append(tuple(bez(val)))
            pts.append(numpy.array(bez(val)))


        return pts


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
        # px = midx + size *(startx - midx)/length
        # py = midy + size *(starty - midy)/length
        px = py = 10

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

