__author__ = 'marioharper'

__author__ = 'Mario'


import sys
import numpy as np
import wx
from math import *
from numpy import linspace
import matplotlib.colors as mcolors
from wx.lib.floatcanvas import FloatCanvas as FC

sys.path.append("..")


class ShapeType():
    ArrowHead = 'ArrowHead'
    Model = 'Model'
    Link = 'Link'
    Label= 'Label'


def get_hex_from_gradient(gradient, num):
    cmap = gradient
    num_colors = num
    colors = [cmap(1.*i/num_colors) for i in range(num_colors)]

    hexcolors = []
    for i in range(0,num_colors):
        hexcolors.append(mcolors.rgb2hex(colors[i]))

    return hexcolors

def build_arrow(pts, arrow_length=3):

    # get the center coordinate of line
    x1,y1 = pts[len(pts)/2]

    # build triangle
    v1 = (10,0)
    v2 = (0,22)
    v3 = (20,22)
    v4 = (10,22) # point bisecting base of triangle

    # todo: snap center of mass of triangle to line rather than v1
    # move to center of line
    dx = v1[0] - x1
    dy = v1[1] - y1

    v1 = (v1[0]-dx,v1[1]-dy)
    v2 = (v2[0]-dx,v2[1]-dy)
    v3 = (v3[0]-dx,v3[1]-dy)
    v4 = (v4[0]-dx,v4[1]-dy)

    # determine angle of rotation
    p1 = v1
    p2 = v4
    p3 = pts[len(pts)/2 + 5]
    p12 = sqrt((p1[0] - p2[0])**2 + (p1[1]-p2[1])**2)
    p13 = sqrt((p1[0] - p3[0])**2 + (p1[1]-p3[1])**2)
    p23 = sqrt((p2[0] - p3[0])**2 + (p2[1]-p3[1])**2)
    c = acos((p12**2 + p13**2 - p23**2) / (2 * p12 * p13))


    # determine quadrant, using source model as origin
    dX = p3[0] - p1[0]
    dY = p3[1] - p1[1]
    if dX > 0 and dY > 0: c = pi - c
    elif dX > 0 and dY < 0: c = pi - c
    elif dX < 0 and dY < 0: c += pi
    elif dX < 0 and dY < 0: c += pi
    else : c += pi

    # set the origin for rotation as v1
    ox,oy = v1
    coords = [v1]
    for x,y in [v2,v3]:
        new_x = (x - ox) * cos(c) - (y-oy)*sin(c) + ox
        new_y = (y - oy) * cos(c) + (x-ox)*sin(c) + oy
        coord = (new_x,new_y)
        coords.append(coord)

    return coords

def build_rounded_rectangle(center, width=50, height=50):

        bez = bezier()
        s = np.array(center,dtype=int)
        wh = np.array([width,height])

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
        l = np.array(l[10:-10])
        t = np.array(t[10:-10])
        r = np.array(r[10:-10])
        b = np.array(b[10:-10])

        ltc = bez.GetBezier([l[-1],l[-1]+[0,5],t[0]-[5,0],t[0]])
        rtc = bez.GetBezier([t[-1],t[-1]+[5,0],r[0]+[0,5],r[0]])
        rbc = bez.GetBezier([r[-1],r[-1]-[0,5],b[0]+[5,0],b[0]])
        lbc = bez.GetBezier([b[-1],b[-1]-[5,0],l[0]-[0,5],l[0]])

        # build polygon object
        coords = np.vstack((l,ltc,t,rtc,r,rbc,b,lbc))


        return coords


def get_line_pts(start, end, order=3, num=100):


        # get start and end x,y
        startX = start[0]
        startY = start[1]
        endX   = end[0]
        endY   = end[1]

        lineArray = []

        # draw curved line
        lineArray.append((startX,startY))
        lineArray.append((startX - ((startX - endX) / 3), startY))
        lineArray.append((endX - ((endX - startX) / 3), endY))
        lineArray.append((endX, endY))

        control_pts = np.array(lineArray)

        n = order
        V = num

        b = bezier()
        bez = b.Bezier_Curve_n(control_pts,n)

        pts = []
        for val in linspace( 0, 1, V ):
            pts.append(np.array(bez(val)))


        return pts


class bezier():
    def __init__(self):
        pass

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

        # clamp t to the range [0,1]
        t = min( 1., max( 0., t ) )

        num_segments = 1 + (len( P ) - (n+1) + n-1) // n
        assert num_segments > 0
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

        P = points
        V = 50
        bez = self.Bezier_Curve( P )

        pts = []
        for val in linspace( 0, 1, V ):
            pts.append(tuple(bez(val)))

        return pts
