__author__ = 'tonycastronova'

import re
from shapely.geometry import *
from osgeo import ogr
from utilities import geometry as geom_utilites

def build_catchments(inp):
    geoms = {}
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

    for name,coords in nodes.iteritems():


        g = geom_utilites.build_polygon_geometries(coords)

        geoms[name] = {'geometry': g}

    return geoms


def build_nodes(inp):
    geoms = {}
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


    for name,coords in nodes.iteritems():
        ptx = [x for x,y in coords]
        pty = [y for x,y in coords]
        g = geom_utilites.build_point_geometries(ptx, pty)
        geoms[name] = {'geometry':g}

    return geoms



def build_links(inp):
    geoms = {}
    lines = None
    with open(inp,'r') as f:
        lines = f.readlines()



    # get all the coordinates
    nodes = {}
    cidx = find(lines, lambda x: 'COORDINATES' in x)
    for line in lines[cidx+3:]:
        if line.strip() == '':
            break
        vals = re.split(' +',line.strip())


        nodes[vals[0].strip()] = (float(vals[1].strip()), float(vals[2].strip()))

    #scoords = sorted_nicely(nodes)

    # read all the vertices
    vertices = {k:[v] for k,v in nodes.iteritems()}
    cidx = find(lines, lambda x: 'VERTICES' in x)
    for line in lines[cidx+3:]:
        if line.strip() == '':
            break
        vals = re.split(' +',line.strip())


        if vals[0] in vertices:
            vertices[vals[0].strip()].append((float(vals[1].strip()), float(vals[2].strip())))
        else:
            # get start node
            #start_node = nodes[vals[0]]

            vertices[vals[0].strip()] = [(float(vals[1].strip()), float(vals[2].strip()))]


    # add conduits
    cidx = find(lines, lambda x: 'CONDUITS' in x)
    for line in lines[cidx+4:]:
        if line.strip() == '':
            break
        vals = re.split(' +',line.strip())

        if vals[0].strip() != ';':    # skip commented lines
            node_id = vals[0].strip()
            inlet_id = vals[1].strip()
            outlet_id = vals[2].strip()

            inlet_node = nodes[inlet_id]
            outlet_node= nodes[outlet_id]

            # create the link geometry
            # g = LineString([inlet_node, outlet_node])

            g = geom_utilites.build_polyline_geometries([inlet_node, outlet_node])

            geoms[node_id] = {'geometry':g , 'inlet':inlet_id, 'outlet':outlet_id}

            # add inlet node coordinate to the outlet node list
            #vertices[inlet_id].append(outlet_node)



    # for i,coords in vertices.iteritems():
    #     if len(coords) > 1:
    #         geoms.append((i,LineString(coords)))

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