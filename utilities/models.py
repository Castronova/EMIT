import cPickle as pickle
import datetime
import imp
import sys
import utilities.io as io
from emitLogging import elog
from sprint import *
import json


class json_types():
    # todo: add the ability to extend these types via inputfile
    name = 'str'
    description = 'str'
    value = 'int'
    unit_type_cv = 'str'
    variable_name_cv = 'str'
    simulation_start = '%m/%d/%Y %H:%M:%S'
    simulation_end = '%m/%d/%Y %H:%M:%S'
    elementset = 'str'
    epsg_code = 'int'
    filepath = 'str'
    classname = 'str'
    ignorecv = 'str'
    code = 'str'
    generic_string = 'str'
    directory = 'str'


def join_model_path_base_directory(data, path):
    """
    Sometimes the models json files do not contain a full path
    so this method adds the full path to any missing values
    :param data: comes from parse_json()
    :return: updates the dictionary it received
    """
    for key, value in data.items():
        for item in value:
            for k, v in item.items():
                if v:
                    if str(v)[0] == ".":
                        new_value = {
                            k: path + v[1:]
                        }
                        item.update(new_value)


def parse_json(path):
    with open(path, "r") as f:
        try:
            data = json.load(f)

            for key, value in data.iteritems():
                for item in value:
                    item["type"] = key.upper()

            basedir = os.path.realpath(os.path.dirname(path))

            join_model_path_base_directory(data, basedir)

            # Set the base directory
            data["basedir"] = basedir

        except ValueError:
            print "Failed to parse json"
            data = {}

    return data


def validate_json_model(data):
    """
    Checks json model's values are valid
    :param data: dictionary where the values are a list of dictionary. Type(dict: [dict])
    :return:
    """
    try:
        # if no sections are found, than the file format must be incorrect
        if len(data) == 0:
            raise Exception('> [Exception] Invalid model configuration file')

        var_cv = os.path.join(io.getAppDataDir(), 'dat/var_cv.dat')
        unit_cv = os.path.join(io.getAppDataDir(), 'dat/units_cv.dat')
        var = pickle.load(open(var_cv, 'rb'))
        unit = pickle.load(open(unit_cv, 'rb'))

        ignorecv = int(data["options"][0]["ignorecv"])

        for key, value in data.iteritems():
            if isinstance(value, list):
                for item in value:
                    for k, v in item.iteritems():
                        if v == "simulation_start" or v == "simulation_end":
                            try:
                                datetime.datetime.strptime(v, getattr(json_types, k))
                            except ValueError:
                                raise ValueError("Incorrect data format, should be " + getattr(json_types, k))
                        else:
                            if not ignorecv:
                                if k == "variable_name_cv":
                                    if v not in var:
                                        raise Exception(v + ' is not a valid controlled vocabulary term')

                                if k == "unit_type_cv":
                                    if v not in unit:
                                        raise Exception(v + ' is not a valid controlled vocabulary term')

        software = data["software"][0]
        relpath = software["filepath"]  # Change name to filepath
        basedir = data["basedir"]
        abspath = os.path.abspath(os.path.join(basedir, relpath))

        sys.path.append(basedir)
        if not os.path.isfile(abspath):
            raise Exception(abspath + " is not a valid file")

        classname = software["classname"]
        filename = os.path.basename(abspath)
        module = imp.load_source(filename.split(".")[0], abspath)
        m = getattr(module, classname)

    except Exception, e:
        elog.error('Configuration Parsing Error: ' + str(e))
        sPrint('Configuration Parsing Error: ' + str(e), MessageType.ERROR)
        return 0

    return 1


def convert_datetime_json_serial(data):
    """
    A Recursive function that loops through the entire data and converts and datetime.datetime to strings
    Its recursive so it can handle any size of dictionary or any number of nested dictionary
    :param data: type(dict(dict))
    :return: data with any datetime.datetime in strings
    """

    # Base case
    if not isinstance(data, dict):
        return

    for key, value in data.items():
        if isinstance(value, datetime.datetime):
            data[key] = value.isoformat()
        elif isinstance(value, dict):
            data[key] = convert_datetime_json_serial(value)

    return data


def save_netcdf_json(model_data, canvas_object, links, path):
    data = convert_datetime_json_serial(model_data)
    return data

def write_simulation_json(models, canvas_shapes, links, path):

    json_models = []
    json_links = []
    for i in range(len(models)):

        model = models[i]

        if "type" not in model:
            sPrint("model does not have type as key. Model should have 'type' as key. Incorrect format", MessageType.DEBUG)
            return
        if model["type"] == "NETCDF":
            json_models.append(save_netcdf_json(model, canvas_shapes, links, path))
        else:


            # parse the original parameters to identify model inputs
            params = parse_json(model['params']['path'])

            # model input properties
            model_inputs = dict()
            if 'model_inputs' in params:
                for input in params['model_inputs']:
                    # get the variable name
                    var = input['variable']

                    # get the variable value from the model
                    model_inputs[var] = model['params'][var]

            # set the model type to mdl if mdl path is present
            if 'path' in model['params']:
                model_type = 'MDL'
            else:
                model_type = model['type']

            # canvas object properties
            bbox = canvas_shapes[i].BoundingBox
            model_properties = dict(xcoordinate=str((bbox[0][0] + bbox[1][0]) / 2),
                                   ycoordinate=str((bbox[0][1] + bbox[1][1]) / 2),
                                   name=model['name'],
                                   id=model['id'],
                                   model_inputs=model_inputs,
                                   path=model['params']['path'],
                                   model_type=model_type
                                   )
            json_models.append(model_properties)

    for link in links:
        link = dict(from_name=link['source_component_name'],
                    from_id=link['source_component_id'],
                    from_item=link['output_name'],
                    from_item_id=link['output_id'],
                    to_name=link['target_component_name'],
                    to_id=link['target_component_id'],
                    to_item=link['input_name'],
                    to_item_id=link['input_name'],
                    temporal_transformation=link['temporal_interpolation'],
                    spatial_transformation=link['spatial_interpolation']
        )
        json_links.append(link)

    # add models and links to obj that will be serialized
    sim = dict(models=json_models,
               links=json_links)

    with open(path, 'w') as f:
        sim_json = json.dumps(sim, sort_keys=True, indent=4, separators=(',', ': '))
        f.write(sim_json)

    elog.info('Configuration saved: ', path)
    sPrint('Configuration was saved successfully: ' + str(path))
