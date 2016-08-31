__author__ = 'tonycastronova'

import numpy
from shapely.geometry import MultiPoint, Point, Polygon

import space_base
import stdlib
from emitLogging import elog
from sprint import *


class spatial_nearest_neighbor_radial(space_base.Space):

    def __init__(self, distance=10):
        super(spatial_nearest_neighbor_radial, self).__init__()

        # set initial parameters
        self.set_param('max_distance', 10)

        # set source and target geometries
        self.source_geometry(stdlib.GeomType.POINT)
        self.target_geometry(stdlib.GeomType.POINT)

    def name(self):
        return 'Nearest Neighbor - Radial'

    def transform(self, ingeoms, outgeoms):

        mapped_geoms = []
        distance = self.get_params('max_distance')

        # put points into numpy array
        in_geoms = numpy.array(ingeoms)
        # out_geoms = numpy.array(outgeoms)

        # build arrays for out geoms
        x = numpy.zeros(shape=in_geoms.shape)
        y = numpy.zeros(shape=in_geoms.shape)
        z = numpy.zeros(shape=in_geoms.shape)
        r = numpy.zeros(shape=in_geoms.shape)

        for i in range(len(in_geoms)):
            xcoord, ycoord, zcoord = in_geoms[i].GetPoint()
            x[i] = xcoord
            y[i] = ycoord
            z[i] = zcoord


        # find the nearest ingeom for each outgeom
        for o in outgeoms:
            o_x, o_y, o_z = o.GetPoint()
            # calculate radii for ingeoms
            xdists = x - o_x
            ydists = y - o_y
            zdists = z - o_z
            r = (xdists**2 + ydists**2)

            # find all elements that are within the specified distance
            # r_idx = r[r <= self.__distance**2]
            r_idx = numpy.where(r <= distance**2)[0]

            # if more than one, choose closest
            matches = len(r_idx)
            if matches > 1:
                # get the nearest point
                idx = numpy.argmin(r[r_idx])
            elif matches == 1:
                # get the only match
                idx = r_idx[0]
            else:
                # no match found
                idx = None

            # only save the geometry if a match is found!
            if idx is not None:
                mapped_geoms.append((ingeoms[idx], o))


        return mapped_geoms



    # 1. Calculate difference between point and all points (radial) using numpy indexing
    # 2. loop through all results that are less than radius provided
    # 3. select the smallest difference
    # 4. steps 2 and 3 can be combined by sorting radii less than specified radius


# adapted from https://github.com/ojdo/python-tools.git
class spatial_nearest_neighbor(space_base.Space):

    def __init__(self):
        super(spatial_nearest_neighbor,self).__init__()
        self.__params = {'max_distance':10}

    def name(self):
        return 'Nearest Neighbor'

    def transform(self, ingeoms, outgeoms):

        # if isinstance(ingeoms[0], stdlib.Geometry2):
        #     ingeoms = [i.geom() for i in ingeoms]  # convert Geometry objects into a list of shapely geometries
        # if isinstance(outgeoms[0], stdlib.Geometry2):
        #     outgeoms = [i.geom() for i in outgeoms]  # convert Geometry objects into a list of shapely geometries

        # get parameters
        max_distance = self.__params['max_distance']

        # todo: this should map everything to point sets
        # create multipoint feature from ingeoms
        in_pts = MultiPoint(ingeoms)


        # create container for mapped geometries
        mapped_geoms = []

        # map each outgeom to its respective ingeom
        for point in outgeoms:

            # get the search region for this point
            search_region = point.buffer(max_distance)
            interesting_points = search_region.intersection(in_pts)

            if not interesting_points:
                closest_point = None
            elif isinstance(interesting_points, Point):
                closest_point = interesting_points
            else:
                distances = [point.distance(ip) for ip in interesting_points
                             if point.distance(ip) > 0]
                closest_point = interesting_points[distances.index(min(distances))]

            mapped_geoms.append((point,closest_point))

        return mapped_geoms

    def get_params(self):
        return self.__params

    def set_param(self, name, value):
        if name in self.__params.keys():
            self.__params[name] = value

class spatial_closest_object(space_base.Space):

    def __init__(self):
            super(spatial_closest_object,self).__init__()

    def name(self):
        return 'Nearest Object - Point to Polygon'

    def transform(self, ingeoms, outgeoms):
        """Find the nearest geometry among a list, measured from fixed point.

        Args:
            outgeoms: a list of shapely geometry objects
            ingeoms: list of shapely Points

        Returns:
            dictionary of mapped geometries: {ingeom:outgeom,...}
        """

        # isolate the shapely geometries
        points = [Point(geom.GetPoint()) for geom in ingeoms]
        polygons = [Polygon(geom.GetGeometryRef(0).GetPoints()) for geom in outgeoms]

        mapped = []

        i = 0
        for polygon in polygons:
            min_dist, min_index = min((polygon.distance(geom), k) for (k, geom) in enumerate(points))

            mapped.append([ingeoms[min_index], outgeoms[i]])

            i += 1
        return mapped



class spatial_intersect_polygon_point(space_base.Space):

    def __init__(self):
            super(spatial_intersect_polygon_point,self).__init__()

    def name(self):
        return 'Intersection - Polygon to Point'

    def transform(self, ingeoms, outgeoms):

        # isolate the shapely geometries
        polygons = [geom.geom() for geom in ingeoms]
        points = [geom.geom() for geom in outgeoms]

        if len(polygons) ==  0 or len(points) == 0:
            raise Exception('Number of geometries must be greater than 0.')

        # todo: what about MultiPoint, MultiPolygon?
        # assert that the correct shapes have been provided
        if polygons[0].geom_type != 'Polygon':
            raise Exception('Incorrect geometry type provided')
        if points[0].geom_type != 'Point':
            raise Exception('Incorrect geometry type provided')

        mapped = []

        i = 0

        for point in points:

            min_dist, min_index = min((point.distance(geom), k) for (k, geom) in enumerate(polygons))
            mapped.append([ingeoms[min_index], outgeoms[i]])

            i += 1
        return mapped

class spatial_exact_match(space_base.Space):
    def __init__(self):
        super(spatial_exact_match,self).__init__()

    def name(self):
        return 'Exact Match'

    def transform(self, ingeoms, outgeoms):

        mapped_geoms = []

        # todo: this should use Geometry2 hash instead of WKT
        igeoms = [ingeoms[i].ExportToWkt() for i in range(0, len(ingeoms))]
        ogeoms = [outgeoms[i].ExportToWkt() for i in range(0, len(outgeoms))]

        for i in range(0, len(igeoms)):
            igeom = igeoms[i]
            if igeom in ogeoms:
                o = ogeoms.index(igeom)
                mapped_geoms.append((ingeoms[i], outgeoms[o]))
        return mapped_geoms

class spatial_index(space_base.Space):

    def __init__(self):
            super(spatial_index,self).__init__()

    def name(self):
        return 'Index-based'

    def transform(self, ingeoms, outgeoms):

        if len(ingeoms) != len(outgeoms):
            sPrint('input and output geometries have different lengths. This may lead to inconsistencies during %s spatial mapping.' % self.name(), MessageType.WARNING)
            elog.warning('input and output geometries have different lengths. This may lead to inconsistencies during %s spatial mapping.' % self.name())

        # determine the minimum length array
        max_idx = min(len(ingeoms), len(outgeoms))

        # loop from 0 to min length and map geometry indices
        mapped = []
        for i in range(0, max_idx):
            mapped.append([ingeoms[i],outgeoms[i]])
        return mapped

class SpatialInterpolation():
    Index = spatial_index()
    NearestNeighbor = spatial_nearest_neighbor()
    NearestObject = spatial_closest_object()
    ExactMatch = spatial_exact_match()
    IntersectPolygonPoint = spatial_intersect_polygon_point()
    NearestNeighborRadial = spatial_nearest_neighbor_radial()

    def methods(self):
        return [self.Index,
                self.NearestNeighbor,
                self.NearestObject,
                self.ExactMatch,
                self.IntersectPolygonPoint,
                self.NearestNeighborRadial,
                ]

