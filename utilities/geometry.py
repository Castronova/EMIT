__author__ = 'tonycastronova'

import numpy
from osgeo import ogr
from shapely.geometry import Point

from coordinator.emitLogging import elog


def build_point_geometries(x, y, geometryType='gdal'):
    """
    Converts x and y coordinate lists into point geometries
    :param x: numpy array of x coordinates
    :param y: numpy array of y coordinates
    :param geometryType: 'gdal' for gdal geometries, 'shapely' for shapely geometries
    :return: numpy array of Point objects
    """

    gtype = geometryType.lower()
    if gtype != 'gdal' and gtype != 'shapely':
        elog.error("Could not build point geometries: invalid geometryType detected, %s" % geometryType)
        return 0

    elif gtype == 'shapely':
        geoms = numpy.empty((x.shape), dtype=object)
        for i in xrange(0, len(x)):
            geoms[i] = Point(x[i], y[i])

    else:
        geoms = numpy.empty((x.shape), dtype=object)
        for i in xrange(0, len(x)):
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(float(x[i]), float(y[i]))
            geoms[i] = point

    return geoms
