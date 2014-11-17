__author__ = 'tonycastronova'


class Space():
    def __init__(self):
        pass

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

    def get_params(self):
        """
        :return: the names and default values of any parameters
        """
        raise Exception('Not Implemented')

    def set_param(self, name, value):
        """
        :param name: name of the parameter
        :param value: value to set
        :return: None
        """
        raise Exception('Not Implemented')