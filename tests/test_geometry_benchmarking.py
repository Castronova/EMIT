__author__ = 'tonycastronova'

import timeit

from osgeo import ogr
import numpy
import numpy.random
from shapely.geometry import Point



# inputs
benchmarks = []
num_runs = 2
num_points = 100000


def test_shapely_nditer(xcoords, ycoords):
    i = 0
    geoms = numpy.empty((xcoords.shape), dtype=object)
    for x, y in numpy.nditer([xcoords,ycoords]):
        geoms[i] = Point(x,y)
        i += 1
    return geoms

def test_shapely_nditer_comprehension(xcoords, ycoords):
    geoms = [ Point(x,y) for x,y in numpy.nditer([xcoords,ycoords])]
    return geoms

def test_shapely_looping(xcoords, ycoords):
    geoms = numpy.empty((xcoords.shape), dtype=object)
    for i in xrange(0, len(xcoords)):
        geoms[i] = Point(xcoords[i],ycoords[i])
    return geoms

def test_gdal_nditer_python_lists(xcoords, ycoords):
    geoms = []
    for x, y in numpy.nditer([xcoords,ycoords]):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(x),float(y))
        geoms.append(point)
    return geoms

def test_gdal_nditer_numpy_arrays(xcoords, ycoords):
    i = 0
    geoms = numpy.empty((xcoords.shape), dtype=object)
    for x, y in numpy.nditer([xcoords,ycoords]):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(x),float(y))
        geoms[i] = point
        i += 1
    return geoms

def test_gdal_looping_python_lists(xcoords, ycoords):
    geoms = []
    for i in xrange(0, len(xcoords)):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(xcoords[i]),float(ycoords[i]))
        geoms.append(point)
    return geoms

def test_gdal_looping_numpy_arrays(xcoords, ycoords):
    geoms = numpy.empty((xcoords.shape), dtype=object)
    for i in xrange(0, len(xcoords)):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(xcoords[i]),float(ycoords[i]))
        geoms[i] = point
    return geoms


# generate a random list of points
x = numpy.random.random_integers(0,100,num_points)
y = numpy.random.random_integers(0,100,num_points)
coords = numpy.vstack((x,y))

# make sure the functions are working properly
print 'Testing test_shapely_nditer ...',
geoms = test_shapely_nditer(x,y)
if len(geoms) != len(x):
    print 'test_shapely_nditer geoms not equal length!'
elif None in geoms:
    print 'test_shapely_nditer geoms has NoneTypes!'
else: print 'ok'

print 'Testing test_shapely_nditer_comprehension ...',
geoms = test_shapely_nditer_comprehension(x,y)
if len(geoms) != len(x):
    print 'test_shapely_nditer_comprehension geoms not equal length!'
if None in geoms:
    print 'test_shapely_nditer_comprehension geoms has NoneTypes!'
else: print 'ok'

print 'Testing test_shapely_looping ...',
geoms = test_shapely_looping(x,y)
if len(geoms) != len(x):
    print 'test_shapely_looping geoms not equal length!'
if None in geoms:
    print 'test_shapely_looping geoms has NoneTypes!'
else: print 'ok'

print 'Testing test_gdal_nditer_python_lists ...',
geoms = test_gdal_nditer_python_lists(x,y)
if len(geoms) != len(x):
    print 'test_gdal_nditer_python_lists geoms not equal length!'
if None in geoms:
    print 'test_gdal_nditer_python_lists geoms has NoneTypes!'
else: print 'ok'

print 'Testing test_gdal_nditer_numpy_arrays ...',
geoms = test_gdal_nditer_numpy_arrays(x,y)
if len(geoms) != len(x):
    print 'test_gdal_nditer_numpy_arrays geoms not equal length!'
if None in geoms:
    print 'test_gdal_nditer_numpy_arrays geoms has NoneTypes!'
else: print 'ok'

print 'Testing test_gdal_looping ...',
geoms = test_gdal_looping_python_lists(x,y)
if len(geoms) != len(x):
    print 'test_gdal_looping_python_lists geoms not equal length!'
if None in geoms:
    print 'test_gdal_looping_python_lists geoms has NoneTypes!'
else: print 'ok'

print 'Testing test_gdal_looping_numpy_arrays ...',
geoms = test_gdal_looping_numpy_arrays(x,y)
if len(geoms) != len(x):
    print 'test_gdal_looping_numpy_arrays geoms not equal length!'
if None in geoms:
    print 'test_gdal_looping_numpy_arrays geoms has NoneTypes!'
else: print 'ok'


print '\nBenchmarking  test_shapely_nditer ...',
t = timeit.Timer(lambda: test_shapely_nditer(x,y))
time = min(t.repeat(num_runs,1))
benchmarks.append([time, '%3.5f sec:\t\ttest_shapely_nditer' % time])
print 'done'

print 'Benchmarking  test_shapely_nditer_comprehension ...',
t = timeit.Timer(lambda: test_shapely_nditer_comprehension(x,y))
time = min(t.repeat(num_runs,1))
benchmarks.append( [time, '%3.5f sec:\t\ttest_shapely_nditer_comprehension' % time])
print 'done'

print 'Benchmarking  test_shapely_looping ...',
t = timeit.Timer(lambda: test_shapely_looping(x,y))
time = min(t.repeat(num_runs,1))
benchmarks.append( [time, '%3.5f sec:\t\ttest_shapely_looping' % time])
print 'done'

print 'Benchmarking  test_gdal_nditer_python_lists ...',
t = timeit.Timer(lambda: test_gdal_nditer_python_lists(x,y))
time = min(t.repeat(num_runs,1))
benchmarks.append( [time, '%3.5f sec:\t\ttest_gdal_nditer_python_lists' % time])
print 'done'

print 'Benchmarking  test_gdal_nditer_numpy_arrays ...',
t = timeit.Timer(lambda: test_gdal_nditer_numpy_arrays(x,y))
time = min(t.repeat(num_runs,1))
benchmarks.append([time,  '%3.5f sec:\t\ttest_gdal_nditer_numpy_arrays' % time])
print 'done'

print 'Benchmarking  test_gdal_looping_python_lists ...',
t = timeit.Timer(lambda: test_gdal_looping_python_lists(x,y))
time = min(t.repeat(num_runs,1))
benchmarks.append([time,  '%3.5f sec:\t\ttest_gdal_looping_python_lists' % time])
print 'done'

print 'Benchmarking  test_gdal_looping_numpy_arrays ...',
t = timeit.Timer(lambda: test_gdal_looping_numpy_arrays(x,y))
time = min(t.repeat(num_runs,1))
benchmarks.append([time, '%3.5f sec:\t\ttest_gdal_looping_numpy_arrays' % time ])
print 'done'


sorted_benchmarks = sorted(benchmarks,key=lambda x: x[0])
print '\n' + 36*'-'
print 'Fastest Geometry Building Algorithms'
print 36*'-'
print 'Number of Points: %d'%num_points
print 'Number of Benchmarking Runs: %d'%num_runs
for b in sorted_benchmarks:
    print b[1]