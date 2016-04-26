import numpy
import timeit
import numpy.random
from shapely.geometry import Point
from osgeo import gdal, ogr

def test_shapely_nditer(xcoords, ycoords):
    shapely_points = []
    for x, y in numpy.nditer([xcoords,ycoords]):
        shapely_points.append(Point(x,y))
    return shapely_points

def test_shapely_nditer_comprehension(xcoords, ycoords):
    return [ Point(x,y) for x,y in numpy.nditer([xcoords,ycoords])]

def test_shapely_looping(xcoords, ycoords):
    shapely_points = []
    for i in xrange(0, len(xcoords)):
        shapely_points.append(Point(xcoords[i],ycoords[i]))
    return shapely_points

def test_gdal_nditer(xcoords, ycoords):
    shapely_points = []
    for x, y in numpy.nditer([xcoords,ycoords]):
        shapely_points.append(ogr.Geometry(ogr.wkbPoint).AddPoint(float(x),float(y)))
    return shapely_points

def test_gdal_nditer_comprehension(xcoords, ycoords):
    return [ ogr.Geometry(ogr.wkbPoint).AddPoint(float(x),float(y)) for x,y in numpy.nditer([xcoords,ycoords])]

def test_gdal_looping(xcoords, ycoords):
    shapely_points = []
    for i in xrange(0, len(xcoords)):
        shapely_points.append(ogr.Geometry(ogr.wkbPoint).AddPoint(float(xcoords[i]),float(ycoords[i])))
    return shapely_points



# generate a random list of points
x = numpy.random.random_integers(0,100000,10000)
y = numpy.random.random_integers(0,100000,10000)
coords = numpy.vstack((x,y))

t = timeit.Timer(lambda: test_shapely_nditer(x,y))
print '%3.5f sec:\t\ttest_shapely_nditer' % t.timeit(number=2)

t = timeit.Timer(lambda: test_shapely_nditer_comprehension(x,y))
print '%3.5f sec:\t\ttest_shapely_nditer_comprehension' % t.timeit(number=2)

# don't run with more than 1000 pts
t = timeit.Timer(lambda: test_shapely_looping(x,y))
print '%3.5f sec:\t\ttest_shapely_looping' % t.timeit(number=2)

t = timeit.Timer(lambda: test_gdal_nditer(x,y))
print '%3.5f sec:\t\ttest_gdal_nditer' % t.timeit(number=2)

t = timeit.Timer(lambda: test_gdal_nditer_comprehension(x,y))
print '%3.5f sec:\t\ttest_gdal_nditer_comprehension' % t.timeit(number=2)

# don't run with more than 1000 pts
t = timeit.Timer(lambda: test_gdal_looping(x,y))
print '%3.5f sec:\t\ttest_gdal_looping' % t.timeit(number=2)