__author__ = 'tonycastronova'

import stdlib

def get_input_geoms(cmd, model_id):

    # # get the model by id
    # model = cmd.get_model_by_id(model_id)
    #
    # # get the mdoel inputs
    # inputs = model.get_instance().inputs()
    # # inputs_exchange_items = model.get_input_exchange_items()
    #
    # # store input geometries by exchange item name
    # input_geoms = {}
    # for iei in inputs:
    #     input_geoms[iei.name()] = get_coords(iei.geometries())
    #
    # return input_geoms

    pass

def get_output_geoms(cmd, model_id):

    # get the model by id
    model = cmd.get_model_by_id(model_id)

    # get the model outputs
    outputs = model.get_instance().outputs()
    # output_exchange_items = model.get_output_exchange_items()

    # store output geometries by exchange item name
    output_geoms = {}
    for oei in outputs:
        output_geoms[oei.name()] = get_coords(oei.geometries())

    return output_geoms


def set_output_geoms(model, variable, geoms):


    # find the item by variable name
    oei = model.get_output_by_name(variable)

    for g in geoms:
        # create a stdlib geometry
        geom = stdlib.Geometry(geom=g)

        # add this geometry to the exchange item
        oei.add_geometry(geom)


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
    return geoms