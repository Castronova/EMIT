__author__ = 'tonycastronova'



def get_input_geoms(cmd, model_id):

    # get the model by id
    model = cmd.get_model_by_id(model_id)

    # get the mdoel inputs
    inputs_exchange_items = model.get_input_exchange_items()

    # store input geometries by exchange item name
    input_geoms = {}
    for iei in inputs_exchange_items:
        input_geoms[iei.name()] = get_coords(iei.geometries())

    return input_geoms

def get_output_geoms(cmd, model_id):

    # get the model by id
    model = cmd.get_model_by_id(model_id)

    # get the model outputs
    output_exchange_items = model.get_output_exchange_items()

    # store output geometries by exchange item name
    output_geoms = {}
    for oei in output_exchange_items:
        output_geoms[oei.name()] = get_coords(oei.geometries())

    return output_geoms


def get_coords(geometries):

    geoms = []
    for geometry in geometries:
        shapely_geom = geometry.geom()
        if shapely_geom.type == 'Polygon':

            coord_list = []
            for coord in shapely_geom.boundary.coords:
                coord_list.append(coord)

            geoms.append(coord_list)

    return geoms