__author__ = 'tonycastronova'

import uuid
from stdlib import *
import os
from shapely import wkt
import cPickle as pickle
from osgeo import ogr, osr
from utilities.spatial import *


def create_variable(variable_name_cv):
    """
    creates a variable object using the lookup table
    """

    dir = os.path.dirname(__file__)
    var = pickle.load(open(os.path.join(dir,'../data/var_cv.dat'),'rb'))

    if variable_name_cv in var:
        V = Variable()
        V.VariableNameCV(value=variable_name_cv)
        V.VariableDefinition(value=var[variable_name_cv].strip())
        return V
    else:
        V = Variable()
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
        U = Unit()
        U.UnitName(value=unit_name)
        U.UnitTypeCV(value=var[unit_name][0].strip())
        U.UnitAbbreviation(value=var[unit_name][1].strip())
        return U
    else:
        U = Unit()
        U.UnitName(value=unit_name)
        U.UnitTypeCV(value='unknown')
        U.UnitAbbreviation(value='unknown')
        #print '> [WARNING] Unit not found in controlled vocabulary : '+unit_name
        return U

def build_exchange_items(params):

    exchange_items = []
    oei = []
    iei = []

    # get all inputs and outputs
    iitems = params['input'] if 'input' in params else []
    oitems = params['output'] if 'output' in params else []
    eitems = iitems + oitems

    itemid = 0

    # loop through each input/output and create an exchange item
    for io in eitems:
        variable = None
        unit = None
        elementset = []


        iotype = ExchangeItemType.Output if io['type'].lower() == 'output' else ExchangeItemType.Input

        #if 'output' in io.keys(): type = stlib.ExchangeItemType.Output
        #else: type = stlib.ExchangeItemType.Input

        for key,value in io.iteritems():

            if key == 'variable_name_cv': variable = create_variable(value)
            elif key == 'unit_type_cv': unit = create_unit(value)
            elif key == 'elementset' :
                # check if the value is a path
                if os.path.dirname(value ) != '':
                    if not os.path.isfile(value):
                        raise Exception('Could not find file: %s'%value)

                    geom,srs = read_shapefile(value)


                # otherwise it must be a wkt
                else:
                    try:
                        value = value.strip('\'').strip('"')
                        geoms = wkt.loads(value)
                        geom = []
                        if 'Multi' in geoms.geometryType():
                                geom  = [g for g in geoms]
                        else:
                            geom = [geoms]

                    except: raise Exception('Could not load WKT string: %s.'%value)
                    srs = get_srs_from_epsg(io['epsg_code'])


                for element in geom:
                    # define initial dataset for element
                    dv = stdlib.DataValues()

                    if srs is None:
                        # set default srs
                        srs = get_srs_from_epsg('4269')

                    # create element
                    elem = stdlib.Geometry()
                    elem.geom(element)
                    elem.type(element.geom_type)
                    elem.srs(srs)
                    elem.datavalues(dv)
                    elementset.append(elem)


        # increment item id
        itemid += 1
        #id = iotype.upper()+str(itemid)
        id = uuid.uuid4().hex[:5]

        # create exchange item
        ei = stdlib.ExchangeItem(id,
                                name=variable.VariableNameCV(),
                                desc=variable.VariableDefinition(),
                                geometry=elementset,
                                unit= unit,
                                variable=variable,
                                type=iotype)

        # add to exchange item
        #for ds in datasets:
        #    ei.add_geometry(ds)

        exchange_items.append(ei)

    return exchange_items