__author__ = 'tonycastronova'

import numpy
from osgeo import ogr

import stdlib
from emitLogging import elog


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
    elif geomtype == stdlib.GeomType.MULTILINESTRING:
        geom = fromGdalMultiLinestring(ogrgeom)
    elif geomtype == stdlib.GeomType.MULTIPOINT:
        geom = fromGdalMultiPoint(ogrgeom)
    elif geomtype == stdlib.GeomType.MULTIPOLYGON:
        geom = fromGdalMultiPolygon(ogrgeom)
    else:
        elog.critical("Unsupported geometry type %s, in utilities.geometry.fromWKT" % geomtype)

    return geom


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

def fromGdalMultiLinestring(gdallinestring):
    """
    Builds a stdlib.Geometry object from a GDAL linstring
    :param gdalpolygon: osgeo.gdal.LineString
    :return: stdlib.Geometry
    """


    geom_count = gdallinestring.GetGeometryCount()
    geometry_array = []
    for i in range(0, geom_count):

        geom = gdallinestring.GetGeometryRef(i)

        # get the points of the linestring
        pts = geom.GetPoints()

        # create the stdlib geometry
        g = stdlib.Geometry2(ogr.wkbLineString)

        # add points to the linestring
        for pt in pts:
            g.AddPoint(*pt)

        geometry_array.append(g)

    # return the geometry
    return numpy.array(geometry_array)

def fromGdalMultiPoint(gdalmultipoint):
    """
    Builds a stdlib.Geometry object from a GDAL multipoint
    :param gdalmultipoint: osgeo.gdal.MultiPoint
    :return: numpy.array(stdlib.Geometry)
    """


    geom_count = gdalmultipoint.GetGeometryCount()
    geometry_array = []
    for i in range(0, geom_count):

        geom = gdalmultipoint.GetGeometryRef(i)

        # get the points of the linestring
        pt = geom.GetPoint()

        # create the stdlib geometry
        g = stdlib.Geometry2(ogr.wkbPoint)

        # add point to geometry
        g.AddPoint(*pt)

        geometry_array.append(g)

    # return the geometry
    return numpy.array(geometry_array)

def fromGdalMultiPolygon(gdalmultipolygon):
    """
    Builds a stdlib.Geometry object from a GDAL multipolygon
    :param gdalmultipolygon: osgeo.gdal.MultiPolygon
    :return: numpy.array(stdlib.Geometry)
    """


    geom_count = gdalmultipolygon.GetGeometryCount()
    geometry_array = []
    for i in range(0, geom_count):

        polygon = gdalmultipolygon.GetGeometryRef(i)

        # create the stdlib geometry
        g = stdlib.Geometry2(ogr.wkbPolygon)

        ring_count = polygon.GetGeometryCount()
        for j in range(0, ring_count):

            # get the ring for this geometry
            ring = polygon.GetGeometryRef(j)

            # add ring to geometry
            g.AddGeometry(ring)

        # save the polygon geometry in numpy array
        geometry_array.append(g)

    # return the geometry
    return numpy.array(geometry_array)


def build_point_geometry(x, y, z=0):
    """
    Builds stdlib point Geometry object
    :param x: single value (float)
    :param y: single value (float)
    :return: stdlib point geometru
    """

    # create an empty point
    point = stdlib.Geometry2(ogr.wkbPoint)
    try:
        # add the x, y, z coordinates
        point.AddPoint(float(x), float(y), float(z))
    except Exception, e:
        print e
    return point

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
            if (isinstance(x, list) or isinstance(x, tuple) ) and ( isinstance(y, list) or isinstance(y, tuple) ):
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