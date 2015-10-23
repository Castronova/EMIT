__author__ = 'tonycastronova'

import uuid
import os
from shapely import wkt
import cPickle as pickle
from osgeo import ogr, osr
import utilities.spatial
from utilities import geometry
import stdlib
from coordinator.emitLogging import elog
import numpy

def create_variable(variable_name_cv):
    """
    creates a variable object using the lookup table
    """

    dir = os.path.dirname(__file__)
    var = pickle.load(open(os.path.join(dir,'../data/var_cv.dat'),'rb'))

    if variable_name_cv in var:
        V = stdlib.Variable()
        V.VariableNameCV(value=variable_name_cv)
        V.VariableDefinition(value=var[variable_name_cv].strip())
        return V
    else:
        V = stdlib.Variable()
        V.VariableNameCV(value=variable_name_cv)
        V.VariableDefinition(value='unknown')
        #print '> [WARNING] Variable not found in controlled vocabulary : '+variable_name_cv
        return V

def create_unit(unit_name):
    """
    creates a unit object using the lookup table
    """
    dir = os.path.dirname(__file__)
    var = pickle.load(open(os.path.join(dir,'../data/units_cv.dat'),'rb'))

    if unit_name in var:
        U = stdlib.Unit()
        U.UnitName(value=unit_name)
        U.UnitTypeCV(value=var[unit_name][0].strip())
        U.UnitAbbreviation(value=var[unit_name][1].strip())
        return U
    else:
        U = stdlib.Unit()
        U.UnitName(value=unit_name)
        U.UnitTypeCV(value='unknown')
        U.UnitAbbreviation(value='unknown')
        #print '> [WARNING] Unit not found in controlled vocabulary : '+unit_name
        return U

def build_exchange_items_from_config(params):

    exchange_items = []
    oei = []
    iei = []

    # get all inputs and outputs
    iitems = params['input'] if 'input' in params else []
    oitems = params['output'] if 'output' in params else []
    eitems = iitems + oitems

    items = {stdlib.ExchangeItemType.INPUT:[],stdlib.ExchangeItemType.OUTPUT:[]}


    # loop through each input/output and create an exchange item
    for io in eitems:
        variable = None
        unit = None

        # get all input and output exchange items as a list
        iotype = stdlib.ExchangeItemType.OUTPUT if io['type'].upper() == stdlib.ExchangeItemType.OUTPUT else stdlib.ExchangeItemType.INPUT

        for key,value in io.iteritems():

            if key == 'variable_name_cv':
                variable = create_variable(value)
                if 'variable_definition' in io.keys():
                    variable.VariableDefinition(io['variable_definition'])
            elif key == 'unit_type_cv': unit = create_unit(value)
            elif key == 'elementset' :
                # check if the value is a path
                if os.path.dirname(value ) != '':
                    gen_path = os.path.abspath(os.path.join(params['basedir'],value))
                    if not os.path.isfile(gen_path):
                        # get filepath relative to *.mdl
                        elog.critical('Could not find file at path %s, generated from relative path %s'%(gen_path, value))
                        raise Exception('Could not find file at path %s, generated from relative path %s'%(gen_path, value))

                    # parse the geometry from the shapefile
                    geom, srs = utilities.spatial.read_shapefile(gen_path)


                # otherwise it must be a wkt
                else:
                    try:
                        # get the wkt text string
                        value = value.strip('\'').strip('"')

                        # parse the wkt string into a stdlib.Geometry object
                        geom = utilities.geometry.fromWKT(value)

                    except:
                        elog.warning('Could not load component geometry from *.mdl file')
                        # this is OK.  Just set the geoms to [] and assume that they will be populated during initialize.
                        geom = []

                    srs = None
                    if 'espg_code' in io:
                        srs = utilities.spatial.get_srs_from_epsg(io['epsg_code'])

        # generate a unique uuid for this exchange item
        id = uuid.uuid4().hex

        # create exchange item
        ei = stdlib.ExchangeItem(id,
                                name=variable.VariableNameCV(),
                                desc=variable.VariableDefinition(),
                                unit= unit,
                                variable=variable,
                                type=iotype)


        # add geometry to exchange item (NEW)
        ei.addGeometries2(geom)

        # save exchange items based on type
        items[ei.get_type()].append(ei)

    return items
