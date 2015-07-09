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
        elog.error("Could not build point geometries: invalid geometryType detected, %s"%geometryType)
        return 0

    elif gtype == 'shapely':
        return [ Point(x,y) for x,y in numpy.nditer([x,y])]

    else:
        return [ ogr.Geometry(ogr.wkbPoint).AddPoint(float(x),float(y)) for x,y in numpy.nditer([x,y])]