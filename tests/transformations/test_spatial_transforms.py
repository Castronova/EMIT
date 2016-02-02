__author__ = 'tonycastronova'

import unittest
#import odm2.api



import utilities
from shapely.wkt import loads

#from ODMconnection import dbconnection

from api_old import dbconnection

## from ODMconnection import SessionFactory

from api_old.ODM2.Core.model import *
from sqlalchemy import func

import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np

from numpy import random as random


from shapely.geometry import Point
from transform.space import SpatialInterpolation
# from stdlib import Geometry
from copy import copy
import time

from utilities import geometry

##################################################################
##############           !     NOTE     !           ##############
#                                                                #
# You must run insert_test_geometries before running these tests #
# /tests/data/sample gis/insert_test_geometies.py                #
##################################################################

class testSpatial(unittest.TestCase):


    def setUp(self):
        # build database connection string
        engine = 'postgresql'
        address = 'localhost'
        db = 'odm2CamelCase'
        user = 'tonycastronova'
        pwd = 'water'

        dbconn = dbconnection()
        self.session = dbconn.createConnection(engine,address,db,user,pwd)




    def test_get_intersecting(self):

        """
        1.) determine potential source ts based on variable/unit/location(bbox) (omitted)
        2.) Query all sampling features that belong to this set of series ids
        3.) for each target feature, determine the points that intersect it
        """

        # this will already be known on the client (querying from the db for testing purposes only)
        targets = [ 'POLYGON ((-111.961138093451495 41.896360920478401,-111.752777525493116 41.893660783528617,-111.756504446950089 41.606066677767103,-111.964865014908469 41.608766814716887,-111.961138093451495 41.896360920478401))',
                    'POLYGON ((-111.752777525493116 41.893660783528617,-111.499522658320416 41.892196863718198,-111.501743961064676 41.507916435626953,-111.754998828237376 41.509380355437372,-111.752777525493116 41.893660783528617))',
                    'POLYGON ((-111.340098770929785 41.625102365813746,-111.132370933565824 41.620863022194158,-111.135345259823112 41.475121035587051,-111.343073097187073 41.479360379206639,-111.340098770929785 41.625102365813746))'
                  ]

        res = None

        # isolate only the samplingfeature ids that I am interested in (i.e. a set of points)
        sourceids = ['points_nad83_0','points_nad83_1','points_nad83_2','points_nad83_3','points_nad83_4']

        sources = {}
        for target in targets:
            try:
                #ST_Equals(geometry, geometry)
                #return self._session.query(Samplingfeature).filter(func.ST_AsText(Samplingfeature.FeatureGeometry) == func.ST_AsText(wkt_geometry)).first()
                res = self._session.query(Samplingfeature).filter(Samplingfeature.SamplingFeatureCode.in_(sourceids)).filter(func.ST_Intersects(Samplingfeature.FeatureGeometry,target)).all()
                sources[target] = res
            except Exception, e:
                print e
                return None

        print 'done'

        pass

        """
        # SELECT points.* FROM points_table points
        INNER JOIN polygon_table polys ON ST_Within(points.geometry,polys.geometry)
        WHERE polys.id = 1 -
        """

    def test_build_theissen(self):

        print 'BUILD THEISSEN POLYGONS'


        # isolate only the samplingfeature ids that I am interested in (i.e. a set of points)
        sourceids = ['points_nad83_0','points_nad83_1','points_nad83_2','points_nad83_3','points_nad83_4']

        sources = {}
        try:
            res = self._session.query(Samplingfeature, Samplingfeature.FeatureGeometry.ST_AsText()).filter(Samplingfeature.SamplingFeatureCode.in_(sourceids)).all()
        except Exception, e:
            return None

        # build coordinates
        coords = []
        for r in res:
            point = loads(r[1])
            coords.append((point.x, point.y))

        points = np.array(coords)

            #np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
            #             [2, 0], [2, 1], [2, 2]])

        vor = Voronoi(points)
        regions, vertices = self.voronoi_finite_polygons_2d(vor)

        # colorize
        for region in regions:
            polygon = vertices[region]
            plt.fill(*zip(*polygon), alpha=0.4)

        plt.plot(points[:,0], points[:,1], 'ko')
        plt.xlim(vor.min_bound[0] - 0.1, vor.max_bound[0] + 0.1)
        plt.ylim(vor.min_bound[1] - 0.1, vor.max_bound[1] + 0.1)

#        plt.show()


    def test_voronoi(self):
        # make up data points
        np.random.seed(1234)
        points = np.random.rand(15, 2)

        # compute Voronoi tesselation
        vor = Voronoi(points)

        # plot
        regions, vertices = self.voronoi_finite_polygons_2d(vor)
        print "--"
        print regions
        print "--"
        print vertices

        # colorize
        for region in regions:
            polygon = vertices[region]
            plt.fill(*zip(*polygon), alpha=0.4)

        plt.plot(points[:,0], points[:,1], 'ko')
        plt.xlim(vor.min_bound[0] - 0.1, vor.max_bound[0] + 0.1)
        plt.ylim(vor.min_bound[1] - 0.1, vor.max_bound[1] + 0.1)

#        plt.show()


    def voronoi_finite_polygons_2d(self, vor, radius=None):
        if vor.points.shape[1] != 2:
            raise ValueError("Requires 2D input")

        new_regions = []
        new_vertices = vor.vertices.tolist()

        center = vor.points.mean(axis=0)
        if radius is None:
            radius = vor.points.ptp().max()

        # Construct a map containing all ridges for a given point
        all_ridges = {}
        for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
            all_ridges.setdefault(p1, []).append((p2, v1, v2))
            all_ridges.setdefault(p2, []).append((p1, v1, v2))

        # Reconstruct infinite regions
        for p1, region in enumerate(vor.point_region):
            vertices = vor.regions[region]

            if all(v >= 0 for v in vertices):
                # finite region
                new_regions.append(vertices)
                continue

            # reconstruct a non-finite region
            ridges = all_ridges[p1]
            new_region = [v for v in vertices if v >= 0]

            for p2, v1, v2 in ridges:
                if v2 < 0:
                    v1, v2 = v2, v1
                if v1 >= 0:
                    # finite ridge: already in the region
                    continue

                # Compute the missing endpoint of an infinite ridge

                t = vor.points[p2] - vor.points[p1] # tangent
                t /= np.linalg.norm(t)
                n = np.array([-t[1], t[0]])  # normal

                midpoint = vor.points[[p1, p2]].mean(axis=0)
                direction = np.sign(np.dot(midpoint - center, n)) * n
                far_point = vor.vertices[v2] + direction * radius

                new_region.append(len(new_vertices))
                new_vertices.append(far_point.tolist())

            # sort region counterclockwise
            vs = np.asarray([new_vertices[v] for v in new_region])
            c = vs.mean(axis=0)
            angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])
            new_region = np.array(new_region)[np.argsort(angles)]

            # finish
            new_regions.append(new_region.tolist())

        return new_regions, np.asarray(new_vertices)


    def test_nearest(self):

        # this will already be known on the client (querying from the db for testing purposes only)
        targets = [ 'POLYGON ((-111.961138093451495 41.896360920478401,-111.752777525493116 41.893660783528617,-111.756504446950089 41.606066677767103,-111.964865014908469 41.608766814716887,-111.961138093451495 41.896360920478401))',
                    'POLYGON ((-111.752777525493116 41.893660783528617,-111.499522658320416 41.892196863718198,-111.501743961064676 41.507916435626953,-111.754998828237376 41.509380355437372,-111.752777525493116 41.893660783528617))',
                    'POLYGON ((-111.340098770929785 41.625102365813746,-111.132370933565824 41.620863022194158,-111.135345259823112 41.475121035587051,-111.343073097187073 41.479360379206639,-111.340098770929785 41.625102365813746))'
                  ]
        # isolate only the samplingfeature ids that I am interested in (i.e. a set of points)
        sourceids = ['points_nad83_0','points_nad83_1','points_nad83_2','points_nad83_3','points_nad83_4']

        nearest = []
        for target in targets:
            try:
                res = self._session.query(Samplingfeature, Samplingfeature.FeatureGeometry.ST_AsText()).\
                                filter(Samplingfeature.SamplingFeatureCode.in_(sourceids)). \
                                order_by(Samplingfeature.FeatureGeometry.distance_centroid(target)).limit(1).all()
                nearest.append(res[0][1])
            except Exception, e:
                print e
                return None



        #for n in nearest: print n


        # plotting
        for i in range(0,len(targets)):
            # plot the polygon
            polygon = [(x,y) for x,y in loads(targets[i]).boundary.coords]
            p = plt.fill(*zip(*polygon), alpha=0.4)

            # set the point color
            face_color = p[0].get_facecolor()
            ptc = list(face_color)
            ptc[3] = 1.0
            pt_color = tuple(ptc)

            # plot the point
            n = loads(nearest[i])
            plt.plot(n.x,n.y,marker='o',color=pt_color)

        # plot ignored points
        res = self._session.query(Samplingfeature.FeatureGeometry.ST_AsText()).\
                        filter(Samplingfeature.SamplingFeatureCode.in_(sourceids)).all()

        for geom in res:
            if geom[0] not in nearest:
                # plot the point
                n = loads(geom[0])
                plt.plot(n.x,n.y,marker='o',color=(0.0,0.0,0.0,0.2))

#        plt.show()


    def func(self, x, y):
        return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2

    def test_spline(self):

        from scipy.interpolate import SmoothBivariateSpline

        # this will already be known on the client (querying from the db for testing purposes only)
        targets = [ 'POLYGON ((-111.961138093451495 41.896360920478401,-111.752777525493116 41.893660783528617,-111.756504446950089 41.606066677767103,-111.964865014908469 41.608766814716887,-111.961138093451495 41.896360920478401))',
                    'POLYGON ((-111.752777525493116 41.893660783528617,-111.499522658320416 41.892196863718198,-111.501743961064676 41.507916435626953,-111.754998828237376 41.509380355437372,-111.752777525493116 41.893660783528617))',
                    'POLYGON ((-111.340098770929785 41.625102365813746,-111.132370933565824 41.620863022194158,-111.135345259823112 41.475121035587051,-111.343073097187073 41.479360379206639,-111.340098770929785 41.625102365813746))'
                  ]
        # isolate only the samplingfeature ids that I am interested in (i.e. a set of points)
        sourceids = ['points_nad83_0','points_nad83_1','points_nad83_2','points_nad83_3','points_nad83_4']


        # plot all points
        res = self._session.query(Samplingfeature.FeatureGeometry.ST_AsText()).\
                filter(Samplingfeature.SamplingFeatureCode.in_(sourceids)).all()



        x = []
        y = []
        w = []
        i = 0
        for geom in res:
            # plot the point
            n = loads(geom[0])
            x.append(n.x)
            y.append(n.y)
            w.append(i)

            #plt.plot(n.x,n.y,marker='o',color=(0.0,0.0,0.0,0.2))

            i += 1

        # calculate spline
        #s = SmoothBivariateSpline(x,y,w)


        #plt.imshow(s)

        from scipy.interpolate import griddata


        grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]

        points = np.random.rand(10, 2)
        values = self.func(points[:,0], points[:,1])

        grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
        grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
        grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')


        plt.subplot(221)
        plt.imshow(self.func(grid_x, grid_y).T, extent=(0,1,0,1), origin='lower')
        plt.plot(points[:,0], points[:,1], 'ko', ms=1)
        plt.title('Original')
        plt.subplot(222)
        plt.imshow(grid_z0.T, extent=(0,1,0,1), origin='lower')
        plt.title('Nearest')
        plt.subplot(223)
        plt.imshow(grid_z1.T, extent=(0,1,0,1), origin='lower')
        plt.title('Linear')
        plt.subplot(224)
        plt.imshow(grid_z2.T, extent=(0,1,0,1), origin='lower')
        plt.title('Cubic')
        plt.gcf().set_size_inches(6, 6)
#        plt.show()


    def test_2d_iterp(self):

        import numpy as np
        from scipy.interpolate import Rbf
        import matplotlib.pyplot as plt
        from matplotlib import cm

        # 2-d tests - setup scattered data
        x = np.random.rand(3)*4.0-2.0
        y = np.random.rand(3)*4.0-2.0
        z = x*np.exp(-x**2-y**2)
        ti = np.linspace(-2.0, 2.0, 100)
        XI, YI = np.meshgrid(ti, ti)

        # use RBF
        rbf = Rbf(x, y, z, epsilon=2)
        ZI = rbf(XI, YI)

        # plot the result
        n = plt.Normalize(-2., 2.)
        plt.subplot(1, 1, 1)
        plt.pcolor(XI, YI, ZI, cmap=cm.jet)
        plt.scatter(x, y, 100, z, cmap=cm.jet)
        plt.title('RBF interpolation - multiquadrics')
        plt.xlim(-2, 2)
        plt.ylim(-2, 2)
        plt.colorbar()

#        plt.show()

    def test_2d_iterp_pts(self):

        import numpy as np
        from scipy.interpolate import Rbf
        import matplotlib.pyplot as plt
        from matplotlib import cm


        sourceids = ['points_nad83_0','points_nad83_1','points_nad83_2','points_nad83_3','points_nad83_4']
        # plot ignored points
        res = self._session.query(Samplingfeature.FeatureGeometry.ST_AsText()).\
                        filter(Samplingfeature.SamplingFeatureCode.in_(sourceids)).all()


        x = []
        y = []
        z = []
        i = 0
        for geom in res:
            # plot the point
            n = loads(geom[0])
            x.append(n.x)
            y.append(n.y)
            z.append(i)
            i += 1

        minx = min(x)-.1
        maxx = max(x)+.1
        miny = min(y)-.1
        maxy = max(y)+.1
        xspace = np.linspace(minx,maxx)
        yspace = np.linspace(miny,maxy)

        xi,yi = np.meshgrid(xspace,yspace)

        rbf = Rbf(x, y, z, epsilon=2)
        zi = rbf(xi, yi)


        n = plt.Normalize(minx,maxy)
        plt.subplot(1, 1, 1)
        plt.pcolor(xi, yi, zi, cmap=cm.jet)
        plt.scatter(x, y, 100, z, cmap=cm.jet)
        plt.title('RBF interpolation - multiquadrics')
        plt.xlim(minx,maxx)
        plt.ylim(miny,maxy)
        plt.colorbar()

        # 2-d tests - setup scattered data
        # x = np.random.rand(3)*4.0-2.0
        # y = np.random.rand(3)*4.0-2.0
        # z = x*np.exp(-x**2-y**2)
        # ti = np.linspace(-2.0, 2.0, 100)
        # XI, YI = np.meshgrid(ti, ti)
        #
        # # use RBF
        # rbf = Rbf(x, y, z, epsilon=2)
        # ZI = rbf(XI, YI)
        #
        # # plot the result
        # n = plt.Normalize(-2., 2.)
        # plt.subplot(1, 1, 1)
        # plt.pcolor(XI, YI, ZI, cmap=cm.jet)
        # plt.scatter(x, y, 100, z, cmap=cm.jet)
        # plt.title('RBF interpolation - multiquadrics')
        # plt.xlim(-2, 2)
        # plt.ylim(-2, 2)
        # plt.colorbar()

#        plt.show()


    def test_spatial_exact_match(self):



        # create a bunch of random points
        x = random.randint(1000,size=5000)
        y = random.randint(1000,size=5000)

        in_geoms = []
        for i in xrange(0, len(x)):
            pt = Point(x[i],y[i])
            geometry_object = Geometry(geom=pt)
            in_geoms.append(geometry_object)

        out_geoms = copy(in_geoms)
        random.shuffle(out_geoms)

        self.assertTrue(in_geoms[i] != out_geoms[i])
        self.assertTrue(in_geoms[i] in out_geoms)


        interpolation = SpatialInterpolation.ExactMatch
        self.assertTrue(interpolation.name() == 'Exact Match')
        st = time.time()
        mapped = interpolation.transform(in_geoms,out_geoms)
        print '%s seconds' %(time.time() - st)

        self.assertTrue('None' not in mapped)


    def test_spatial_nearest_neighbor_radial(self):


        # build some test points
        x_in = [0,4,2,0,4]
        y_in = [0,0,2,4,4]
        x_out = [0,2,4]
        y_out = [1,0,3]
        pts_in = geometry.build_point_geometries(x_in, y_in)
        pts_out = geometry.build_point_geometries(x_out, y_out)

        # instantiate the interpolation class
        interpolation = SpatialInterpolation.NearestNeighborRadial

        # test multiple matches (large search distance)
        interpolation.set_param("max_distance", 10)
        mapped = interpolation.transform(pts_in, pts_out)
        self.assertTrue('None' not in mapped)
        self.assertTrue(len(mapped) == 3)

        # test no matches (very small search distance)
        interpolation.set_param("max_distance", 0)
        mapped = interpolation.transform(pts_in, pts_out)
        self.assertTrue('None' not in mapped)
        self.assertTrue(len(mapped) == 0)

        # test partial matches (small search distance)
        interpolation.set_param("max_distance", 1)
        mapped = interpolation.transform(pts_in, pts_out)
        self.assertTrue('None' not in mapped)
        self.assertTrue(len(mapped) == 2)






# backup of database pts
#pts = [(u'POINT(-111.884043556863 41.8462732663056)',),
#        (u'POINT(-111.647763078984 41.8412763981934)',),
#        (u'POINT(-111.64633540238 41.6599614695491)',),
#        (u'POINT(-111.889754263277 41.6556784397386)',),
#        (u'POINT(-111.179485153036 41.7641818616045)',)]
