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
