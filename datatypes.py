__author__ = 'tonycastronova'


class ini_types():
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
    description = 'str'
    generic_string = 'str'
    directory = 'str'

class ModelTypes():
    FeedForward = 'FEEDFORWARD'
    Data = 'DATA'
    Undefined = 'UNDEFINED'