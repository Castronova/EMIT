__author__ = 'tonycastronova'

import space_base
from shapely.geometry import LineString, MultiPoint, Point, Polygon



# TODO!  These should utilize database queries, see test_spatial.py.  Also, they should take actionID as input?

# adapted from https://github.com/ojdo/python-tools.git
class spatial_nearest_neighbor(space_base.Space):

    def __init__(self):
        super(spatial_nearest_neighbor,self).__init__()
        self.__params = {'max_distance':10}

    def name(self):
        return 'Nearest Neighbor'

    def transform(self, ingeoms, outgeoms):

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
        return 'Nearest Neighbor - Point to Polygon'

    def transform(self, ingeoms, outgeoms):
        """Find the nearest geometry among a list, measured from fixed point.

        Args:
            outgeoms: a list of shapely geometry objects
            ingeoms: list of shapely Points

        Returns:
            dictionary of mapped geometries: {ingeom:outgeom,...}
        """

        # isolate the shapely geometries
        points = [geom.geom() for geom in ingeoms]
        polygons = [geom.geom() for geom in outgeoms]

        mapped = []

        i = 0
        for polygon in polygons:
            min_dist, min_index = min((polygon.distance(geom), k) for (k, geom) in enumerate(points))

            mapped.append([ingeoms[min_index], outgeoms[i]])

            i += 1
        return mapped
