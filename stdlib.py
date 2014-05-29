__author__ = 'tonycastronova'



"""
Standard classes
"""

# On OSX you also need to install geos. e.g, sudo port install geos
from shapely.wkt import loads
import datetime

class ElementType():
    Point = 'Point'
    Polygon = 'Polygon'
    PolyLine = 'PolyLine'
    Id = 'Id'

class ExchangeItemType():
    Input = 'input'
    Output = 'output'


class Variable(object):
    """
    Defines the variable object
    """
    def __init__(self):

        # ODM2 terms
        #__variableid = None
        #__variableCode = None
        self.__variableNameCV = None
        self.__variableDefinition = None
        #__speciationCV = None
        #__noDataValue = None


    def VariableNameCV(self,value=None):
        if value is None:
            return self.__variableNameCV
        else:
            self.__variableNameCV = value

    def VariableDefinition(self,value=None):
        if value is None:
            return self.__variableNameDefinition
        else:
            self.__variableNameDefinition = value

class Unit(object):
    """
    Defines the unit object
    """
    def __init__(self):

        # ODM2 terms
        #__unitID= None
        self.__unitTypeCV = None
        self.__unitAbbreviation = None
        self.__unitName = None


    def UnitTypeCV(self,value=None):
        if value is None:
            return self.__unitTypeCV
        else:
            self.__unitTypeCV = value

    def UnitAbbreviation(self,value=None):
        if value is None:
            return self.__unitAbbreviation
        else:
            self.__unitAbbreviation = value

    def UnitName(self,value=None):
        if value is None:
            return self.__unitName
        else:
            self.__unitName = value

class Element(object):
    """
    Spatial definition of a calculation or timeseries
    """

    # TODO: SRS should be an ogr object NOT defined by name,def,and code!

    def __init__(self):
        self.__geom = None
        #self.__srs_def = None
        #self.__srs_name = None
        #self.__srs_code = None
        self.__srs = None
        self.__elev = None

        # TODO: use enum
        self.__type = None


    def geom(self,value=None):
        if value is None:
            return self.__geom
        else:
            self.__geom = value

    def set_geom_from_wkt(self,wkt):
        self.__geom = loads(wkt)


    # def srs(self,srsname=None,srscode=None):
    #     if srsname is None and srscode is None:
    #         return (self.__srs_name,self.__srs_code)
    #     else:
    #         self.__srs_name = srsname
    #         self.__srs_code = srscode

    def srs(self,value=None):
        if value is None:
            return self.__srs
        else:
            self.__srs = value

    def elev(self,value=None):
        if value is None:
            return self.__elev
        else:
            self.__elev = value

    def type(self,value=None):
        if value is None:
            return self.__type
        else:
            self.__type = value

class DataValues(object):
    """
    A dataset associated with a geometry
    """
    def __init__(self,element,timeseries=None):

        # timeseries = [(date,val),(date,val),]
        self.__timeseries = timeseries

        # element = shapely geometry
        self.__element = element

        # start and end are the defined by the date range of the dataset
        if timeseries is not None:
            dates,values = zip(*self.__timeseries)
            self.__start = min(dates)
            self.__end = max(dates)
        else:
            self.__start = None
            self.__end = None



    def timeseries(self):
        return self.__timeseries

    def element(self):
        return self.__element

    def get_dates_values(self):
        return zip(*self.__timeseries)

    def earliest_date(self):
        return self.__start

    def latest_date(self):
        return self.__end

class ExchangeItem(object):
    def __init__(self,name=None,desc=None,unit=None,variable=None,type=ExchangeItemType.Input,dataset=[]):
        self.__name = name
        self.__description = desc

        # variable and unit come from Variable and Unit standard classes
        self.__unit = unit
        self.__variable = variable

        self.__type = type

        # A dataset is a list of [one or more values per element,]
        # [[element1,[ts,]],[element2,[ts,,]],   ]
        self.__dataset =  dataset

        self.StartTime = datetime.datetime(2999,1,1,1,0,0)
        self.EndTime = datetime.datetime(1900,1,1,1,0,0)

    def get_type(self):
        return self.__type

    def name(self,value=None):
        if value is None:
            return self.__name
        else:
            self.__name = value

    def description(self,value=None):
        if value is None:
            return self.__description
        else:
            self.__description = value

    def get_geoms(self):
        """
        returns the input geometries
        """
        geoms = []
        dict = self.get_dataset_dict()
        for element in dict.keys():
            geoms.append(element.geom())
        return geoms

    def get_dataset(self):
        return self.__dataset

    def get_dataset_dict(self):
        """
        returns the input dataset as a dictionary of geometries
        """
        dict = {}
        for datavalues in self.__dataset:
            dict[datavalues.element] = datavalues.values()
        return dict

    def get_timeseries_by_geom(self,geom):
        """
        geom = the geom of the desired timeseries
        """
        dict = self.get_dataset_dict()
        for element in dict.keys():
            if element.geom() == geom:
                return dict[element]
        return None

    def get_timeseries_by_element(self,element):
        """
        element = the element of the desired timeseries
        """
        dict = self.get_dataset_dict()
        return dict[element]

    def unit(self,value=None):
        if value is None:
            return self.__unit
        else:
            self.__unit = value

    def variable(self,value=None):
        if value is None:
            return self.__variable
        else:
            self.__variable = value

    def add_dataset(self,datavalues):
        """
        datavalues = list of datavalue objects
        """
        if isinstance(datavalues,list):
            self.get_dataset().extend(datavalues)
            self.__calculate_start_and_end_times(datavalues)

        else:
            self.get_dataset().append(datavalues)
            self.__calculate_start_and_end_times([datavalues])

    def clear_dataset(self):
        self.__dataset = []

    def set_dataset(self,value):
        self.__dataset = value
        self.__calculate_start_and_end_times(value)

    def __calculate_start_and_end_times(self,datavalues):
        for dv in datavalues:
            if dv.earliest_date() is not None and dv.latest_date() is not None:
                if dv.earliest_date() < self.StartTime:
                    self.StartTime = dv.earliest_date()
                if dv.latest_date() > self.EndTime:
                    self.EndTime = dv.latest_date()

