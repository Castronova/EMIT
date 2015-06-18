__author__ = 'tonycastronova'

import os
import stdlib
from shapely import wkt
from osgeo import ogr, osr
import cPickle as pickle
import shapefile
from shapely.geometry import shape
# import coordinator.engineAccessors as engine


# def get_input_geoms(model_id):
#
#     # get the model by id
#     # model = cmd.get_model_by_id(model_id)
#     # model = engine.getModelById(model_id)
#
#     # get the mdoel inputs
#     # inputs = model.get_instance().inputs()
#     inputs = engine.getInputExchangeItems(model_id)
#
#     # store input geometries by exchange item name
#     input_geoms = {}
#
#     if inputs is not None:
#         for iei in inputs.values():
#             input_geoms[iei.name()] = {}
#             input_geoms[iei.name()]['data'] = get_coords(iei.geometries())
#             # hack: assumes all geoms will be the same type
#             input_geoms[iei.name()]['type'] =iei.geometries()[0].type()
#
#
#     return input_geoms

# def get_output_geoms(model_id):
#
#     # get the model by id
#     # model = cmd.get_model_by_id(model_id)
#     # model = engine.getModelById(model_id)
#
#     # get the model outputs
#     # outputs = model.get_instance().outputs()
#     outputs = engine.getOutputExchangeItems(model_id)
#     # output_exchange_items = model.get_output_exchange_items()
#
#     # store output geometries by exchange item name
#     output_geoms = {}
#
#     if outputs is not None:
#         for oei in outputs.values():
#             output_geoms[oei.name()] = {}
#             output_geoms[oei.name()]['data'] = get_coords(oei.geometries())
#             # hack: assumes all geoms will be the same type
#             output_geoms[oei.name()]['type'] =oei.geometries()[0].type()
#
#     return output_geoms

# def set_output_geoms(model, variable, geoms):
#
#
#     # find the item by variable name
#     oei = model.get_output_by_name(variable)
#
#     for g in geoms:
#         # create a stdlib geometry
#         geom = stdlib.Geometry(geom=g)
#
#         # add this geometry to the exchange item
#         oei.add_geometry(geom)
#
def get_coords(geometries):

    geoms = []
    for geometry in geometries:
        shapely_geom = geometry.geom()
        if shapely_geom.type == 'Polygon':

            coord_list = []
            for coord in shapely_geom.boundary.coords:
                coord_list.append(coord)

            geoms.append(coord_list)

        elif shapely_geom.type == 'LineString':
            coord_list = []
            for coord in shapely_geom.coords:
                coord_list.append(coord)

            geoms.append(coord_list)

        elif shapely_geom.type == 'Point':
            coord_list = []
            for coord in shapely_geom.coords:
                coord_list.append(coord)

            geoms.append(coord_list)

    return geoms

def shapefile_to_shapely(filepath):
    """
    reads esri shapefiles into shapely geometry objects
    :param filepath:
    :return:
    """
    # read the shapefile
    reader = shapefile.Reader(filepath)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        geom = sr.shape.__geo_interface__
        buffer.append(dict(type="Feature", geometry=geom, properties=atr))

    return shape(buffer[0]['geometry'])

def get_srs_from_epsg(code=None):
    """
    returns a spatial projection. code is an integer EPSG code, e.g. 2000
    """

    if code is None:
        # set default srs
        code = '4269'

    # validate the EPSG code
    dir = os.path.dirname(__file__)
    #os.path.join(dir, '/relative/path/to/file/you/want')
    codes = pickle.load(open(os.path.join(dir,'../data/epsg_codes.dat'),'rb'))
    if not str(code) in codes:
        raise Exception('Invalid EPSG code: %d'%code)

    # load spatial reference
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(int(code))
    return srs

def read_shapefile(shp):
    """
    returns (shapely geometry, spatial reference system)
    """

    # OnOpen the shapefile
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataset = driver.Open(shp)

    layer = dataset.GetLayer()
    spatialRef = layer.GetSpatialRef()

    # from Geometry
    geoms = []
    for i in xrange(0,layer.GetFeatureCount()):
        feature = layer.GetNextFeature()
        geom = feature.GetGeometryRef()

        # convert into shapely geometry
        geom_wkt = geom.ExportToWkt()
        shapely_geom = wkt.loads(geom_wkt)

        geoms.append(shapely_geom)

    return geoms, spatialRef
