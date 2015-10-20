__author__ = 'tonycastronova'

import numpy
from osgeo import ogr
from shapely.geometry import Point, Polygon
from coordinator.emitLogging import elog
import stdlib

def build_point_geometries(x, y):
    """
    Builds stdlib Geometry objects from a list of  x and y coordinates
    :param x: single value, list, or numpy array of x coordinates
    :param y: single value, list, or numpy array of y coordinates
    :return: numpy array of stdlib geometries
    """

    # try to convert x,y coordinates into numpy arrays
    if type(x) != type(y):
        elog.critical('Could not convert the x,y coordinates into numpy array objects: X and Y types do not match')
        return None

    try:
        if not isinstance(x, numpy.ndarray) and not isinstance(y, numpy.ndarray):
            if isinstance(x, list) and isinstance(y, list):
                x = numpy.asarray(x)
                y = numpy.asarray(y)
            else:
                x = numpy.array([x])
                y = numpy.array([y])
    except:
        elog.critical('Could not convert the x,y coordinates into numpy array objects!')
        return None


    geoms = numpy.empty((x.shape), dtype=object)
    for i in range(len(x)):

        point = stdlib.Geometry2(ogr.wkbPoint)


        # point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(x[i]), float(y[i]))

        geoms[i] = point

    return geoms


def build_polygon_geometries(coords):
    """
    Builds stdlib Geometry objects from coordinates
    :param coords: list or numpy array of polygons coordinates [[[1,2],[2,3], ], ]
    :return: numpy array of stdlib geometries
    """


    # try to convert x,y coordinates into numpy arrays
    try:
        if not isinstance(coords, numpy.ndarray):
            if isinstance(coords, list):
                coords = numpy.asarray(coords)
            else:
                coords = numpy.array([coords])
    except:
        elog.critical('Could not convert the x,y coordinates into numpy array objects!')
        return None


    shape = coords.shape
    poly_count = shape[0] if len(shape) == 3 else 1

    geoms = numpy.empty((poly_count), dtype=object)
    for i in xrange(0, len(coords)):
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for pt in coords[i]:
            ring.AddPoint(float(pt[0]), float(pt[1]))

        poly = stdlib.Geometry2(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        geoms[i] = poly


    return geoms