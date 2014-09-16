__author__ = 'tonycastronova'

import re
from shapely.geometry import *


def build_catchments(inp):
        lines = None
        with open(inp,'r') as f:
            lines = f.readlines()


        # first read all the node coordinates
        nodes = {}
        node_order = []
        cidx = find(lines, lambda x: 'Polygons' in x)
        for line in lines[cidx+3:]:
            if line.strip() == '':
                break
            vals = re.split(' +',line.strip())

            if vals[0] in nodes:
                nodes[vals[0]].append((float(vals[1]), float(vals[2])))
            else:
                nodes[vals[0]] = [(float(vals[1]), float(vals[2]))]
                node_order.append(vals[0])


        geoms = []
        for name,coords in nodes.iteritems():
            geoms.append((name,Polygon(coords)))

        return geoms


def build_coordinates(inp):
        lines = None
        with open(inp,'r') as f:
            lines = f.readlines()


        # first read all the node coordinates
        nodes = {}
        node_order = []
        cidx = find(lines, lambda x: 'COORDINATES' in x)
        for line in lines[cidx+3:]:
            if line.strip() == '':
                break
            vals = re.split(' +',line.strip())

            if vals[0] in nodes:
                nodes[vals[0]].append((float(vals[1]), float(vals[2])))
            else:
                nodes[vals[0]] = [(float(vals[1]), float(vals[2]))]
                node_order.append(vals[0])


        geoms = []
        for name,coords in nodes.iteritems():
            geoms.append((name,Point(coords)))

        return geoms


def build_links(inp):
        lines = None
        with open(inp,'r') as f:
            lines = f.readlines()



        # get all the coordinates
        coordinates = {}
        cidx = find(lines, lambda x: 'COORDINATES' in x)
        for line in lines[cidx+3:]:
            if line.strip() == '':
                break
            vals = re.split(' +',line.strip())

            if vals[0] in coordinates:
                coordinates[vals[0]].append((float(vals[1]), float(vals[2])))
            else:
                coordinates[vals[0]] = [(float(vals[1]), float(vals[2]))]

        scoords = sorted_nicely(coordinates)

        # first read all the node coordinates
        nodes = {}
        node_order = []
        cidx = find(lines, lambda x: 'VERTICES' in x)
        for line in lines[cidx+3:]:
            if line.strip() == '':
                break
            vals = re.split(' +',line.strip())

            if vals[0] in nodes:
                nodes[vals[0]].append((float(vals[1]), float(vals[2])))
            else:
                nodes[vals[0]] = [(float(vals[1]), float(vals[2]))]
                node_order.append(vals[0])

        snodes = sorted_nicely(nodes)




        for i in range(1, len(scoords)-1):

            # set first value as previous node

            coordinates[scoords[i]].insert(0,coordinates[scoords[i-1]][-1])

            if scoords[i] in nodes:
                coords = nodes[scoords[i]]

                # insert middle coords
                for c in reversed(coords):
                    coordinates[scoords[i]].insert(1,c)




        geoms = []
        for name,coords in coordinates.iteritems():
            if len(coords) > 1:
                geoms.append((name,LineString(coords)))

        return geoms



def connect_coordinates(inp):
        lines = None
        with open(inp,'r') as f:
            lines = f.readlines()



        # get all the coordinates
        coordinates = []
        cidx = find(lines, lambda x: 'COORDINATES' in x)
        for line in lines[cidx+3:]:
            if line.strip() == '':
                break
            vals = re.split(' +',line.strip())


            coordinates.append((float(vals[1]), float(vals[2])))


        geoms = []
        for i in range(0,len(coordinates)-1):

            # calculate the distance between the points to make sure they are next to each other
            dist = Point(coordinates[i]).distance(Point(coordinates[i+1]))

            if dist < 100:
                geoms.append(LineString([coordinates[i],coordinates[i+1]]))


        return geoms


def find(lst, predicate):
    return (i for i, j in enumerate(lst) if predicate(j)).next()

import re
def sorted_nicely( l ):
    """ Sorts the given iterable in the way that is expected.

    Required arguments:
    l -- The iterable to be sorted.

    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)