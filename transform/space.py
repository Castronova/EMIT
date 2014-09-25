__author__ = 'tonycastronova'

import space_base
from shapely.geometry import LineString, MultiPoint, Point, Polygon



# TODO!  These should utilize database queries, see test_spatial.py.  Also, they should take actionID as input?

# adapted from https://github.com/ojdo/python-tools.git
class nearest_neighbor(space_base):

    def __init__(self):
        super(nearest_neighbor,self).init()
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

def nearest_neighbor_a(others, point, max_distance):
    """Find nearest point among others up to a maximum distance.

    Args:
        others: a list of Points or a MultiPoint
        point: a Point
        max_distance: maximum distance to search for the nearest neighbor

    Returns:
        A shapely Point if one is within max_distance, None otherwise
    """
