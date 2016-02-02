__author__ = 'tonycastronova'


class Space(object):
    def __init__(self):
        self.__params = {}

    def transform(self, ingeoms, outgeoms):
        """
        This funciton is used to map ingeoms to outgeoms
        :param ingeoms: the geometries that will be mapped
        :param outgeoms: the geometris to map ingeoms to
        :return: mapped geometry tuples [(ingeom0, outgeom1), ...]
        """
        raise Exception('Not Implemented')

    def name(self):
        """
        The name of the transformation
        :return: the name of the transformation
        """
        raise Exception('Not Implemented')

    def get_params(self, value=None):
        """
        :return: the names and default values of any parameters
        """
        if value is not None:
            if value in self.__params:
                return self.__params[value]
        return self.__params

    def set_param(self, name, value):
        """
        :param name: name of the parameter
        :param value: value to set
        :return: None
        """
        self.__params[name] = value


    def source_geometry(self, stdlib_geometry_type = None):
        """
        get/set the source geometry type for the interpolation method
        :param stdlib_geometry_type: a geometry type defined by stdlib.GeomType
        :return: source geometry type
        """
        if stdlib_geometry_type is not None:
            self.__source_geometry_type = stdlib_geometry_type
        return self.__source_geometry_type

    def target_geometry(self, stdlib_geometry_type = None):
        """
        get/set the target geometry type for the interpolation method
        :param stdlib_geometry_type: a geometry type defined by stdlib.GeomType
        :return: target geometry type
        """
        if stdlib_geometry_type is not None:
            self.__target_geometry_type = stdlib_geometry_type
        return self.__target_geometry_type