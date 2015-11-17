__author__ = 'tonycastronova'

import numpy
from osgeo import ogr
from coordinator.emitLogging import elog
import stdlib

def fromWKB(wkb):
    """
    Builds a stdlib.Geometry object from a WKB string
    :param wkb: wkb string
    :return: stdlib.Geometry
    """

    geom = None

    # parse the wkt string into ogr
    ogrgeom = ogr.CreateGeometryFromWkb(wkb)

    # get geometry type
    geomtype =  ogrgeom.GetGeometryName()

    if geomtype == stdlib.GeomType.POINT:
        geom = fromGdalPoint(ogrgeom)
    elif geomtype == stdlib.GeomType.LINESTRING:
        geom = fromGdalLinestring(ogrgeom)
    elif geomtype == stdlib.GeomType.POLYGON:
        geom = fromGdalPolygon(ogrgeom)
    else:
        elog.critical("Unsupported geometry type %s, in utilities.geometry.fromWKB" % geomtype)

    return geom[0]


def fromWKT(wkt):
    """
    Builds a stdlib.Geometry object from a WKT string
    :param wkt: wkt string
    :return: stdlib.Geometry
    """

    geom = None

    # parse the wkt string into ogr
    ogrgeom = ogr.CreateGeometryFromWkt(wkt)

    # get geometry type
    geomtype =  ogrgeom.GetGeometryName()

    if geomtype == stdlib.GeomType.POINT:
        geom = fromGdalPoint(ogrgeom)
    elif geomtype == stdlib.GeomType.LINESTRING:
        geom = fromGdalLinestring(ogrgeom)
    elif geomtype == stdlib.GeomType.POLYGON:
        geom = fromGdalPolygon(ogrgeom)
    else:
        elog.critical("Unsupported geometry type %s, in utilities.geometry.fromWKT" % geomtype)

    return geom[0]


def fromGdalPolygon(gdalpolygon):
    """
    Builds a stdlib.Geometry object from a GDAL polygon
    :param gdalpolygon: osgeo.gdal.Polygon
    :return: numpy.array(stdlib.Geometry)
    """

    # get the ring that defines the polygon
    ring = gdalpolygon.GetGeometryRef(0)

    # create the stdlib geometry
    g = stdlib.Geometry2(ogr.wkbPolygon)

    # add the ring
    g.AddGeometry(ring)

    # return the geometry
    return numpy.array([g])


def fromGdalPoint(gdalpoint):
    """
    Builds a stdlib.Geometry object from a GDAL point
    :param gdalpolygon: osgeo.gdal.Point
    :return: stdlib.Geometry
    """

    # get the geoms point
    pt = gdalpoint.GetPoint()

    # create the stdlib geometry
    g = stdlib.Geometry2(ogr.wkbPoint)

    # add the point
    g.AddPoint(*pt)

    # return the geometry
    return numpy.array([g])

def fromGdalLinestring(gdallinestring):
    """
    Builds a stdlib.Geometry object from a GDAL linstring
    :param gdalpolygon: osgeo.gdal.LineString
    :return: stdlib.Geometry
    """

    # get the points of the linestring
    pts = gdallinestring.GetPoints()

    # create the stdlib geometry
    g = stdlib.Geometry2(ogr.wkbLineString)

    # add points to the linestring
    for pt in pts:
        g.AddPoint(*pt)

    # return the geometry
    return numpy.array([g])


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


    geoms = numpy.empty((x.shape[0]), dtype=object)
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
    has_multiple = 1 if len(shape) > 2 else 0

    geoms = numpy.empty((poly_count), dtype=object)
    if has_multiple:
        for i in xrange(0, len(coords)):
            ring = ogr.Geometry(ogr.wkbLinearRing)
            for pt in coords[i]:
                ring.AddPoint(float(pt[0]), float(pt[1]))

            poly = stdlib.Geometry2(ogr.wkbPolygon)
            poly.AddGeometry(ring)
            geoms[i] = poly
    else:
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for pt in coords:
            ring.AddPoint(float(pt[0]), float(pt[1]))

        poly = stdlib.Geometry2(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        geoms[0] = poly


    return geoms

def build_polyline_geometries(coords):
    """
    Builds stdlib Geometry objects from coordinates
    :param coords: list or numpy array of polyline coordinates [[[1,2],[2,3], ], ]
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
    has_multiple = 1 if len(shape) > 2 else 0

    geoms = numpy.empty((poly_count), dtype=object)
    if has_multiple:
        for i in range(poly_count):
            line = stdlib.Geometry2(ogr.wkbLineString)
            for pt in coords[i]:
                line.AddPoint(float(pt[0]), float(pt[1]))
            geoms[i] = line
    else:
        line = stdlib.Geometry2(ogr.wkbLineString)
        for pt in coords:
            line.AddPoint(float(pt[0]), float(pt[1]))
        geoms[0] = line




    return geoms