__author__ = 'tonycastronova'



"""
Standard classes
"""

# On OSX you also need to install geos. e.g, sudo port install geos
from shapely.wkt import loads
import datetime
import uuid
import utilities

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
    def __init__(self,timeseries=None):

        # timeseries = [(date,val),(date,val),]
        self.__timeseries = timeseries

        # element = shapely geometry
        #self.__element = element

        self.__start = None
        self.__end = None

        # start and end are the defined by the date range of the dataset
        if timeseries is not None:
            self.update_start_end_times()

    def timeseries(self):
        return self.__timeseries

    def set_timeseries(self,value):
        self.__timeseries = value
        self.update_start_end_times()

    #def element(self):
    #    return self.__element

    def get_dates_values(self):
        if self.__timeseries:
            return zip(*self.__timeseries)
        else:
            return None

    def earliest_date(self):
        return self.__start

    def latest_date(self):
        return self.__end

    def update_start_end_times(self):
        dates,values = zip(*self.__timeseries)
        self.__start = min(dates)
        self.__end = max(dates)

    def start(self):
        if self.__start is None:
            self.update_start_end_times()
        return self.__start
    def end(self):
        if self.__end is None:
            self.update_start_end_times()
        return self.__end

class Geometry(object):

    def __init__(self,geom=None,srs=None,elev=None,datavalues=None,id=uuid.uuid4().hex[:5]):
        self.__geom = geom
        self.__srs = srs
        self.__elev = elev
        self.__datavalues = datavalues
        self.__id = id

        # TODO: use enum
        self.__type = None

        if self.__srs is None:
            # set default srs
            self.__srs = utilities.get_srs_from_epsg('4269')

    def id(self):
        return self.__id

    def geom(self,value=None):
        if value is None:
            return self.__geom
        else:
            self.__geom = value

    def set_geom_from_wkt(self,wkt):
        self.__geom = loads(wkt)

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

    def datavalues(self,value=None):
        if value is None:
            return self.__datavalues
        else:
            self.__datavalues = value

class ExchangeItem(object):
    def __init__ (self,id,name=None,desc=None, geometry=[],unit=None,variable=None,type=ExchangeItemType.Input):
        self.__name = name
        self.__description = desc

        # variable and unit come from Variable and Unit standard classes
        self.__unit = unit
        self.__variable = variable

        self.__type = type

        # A dataset is a list of [one or more values per element,]
        # [[element1,[ts,]],[element2,[ts,,]],   ]
        #self.__dataset =  ds

        #self.StartTime = datetime.datetime(2999,1,1,1,0,0)
        #self.EndTime = datetime.datetime(1900,1,1,1,0,0)

        self.__id = id

        self.__geoms = geometry

        # variables for saving/retrieving values from database
        self.__session = None
        self.__saved = False
        self.__seriesID = None

        # # determine start and end times
        # for geom in self.__geoms:
        #     self.__calculate_start_and_end_times(geom.datavalues())

    def getStartTime(self):
        return min(g.datavalues().start() for g in self.__geoms)

    def getEndTime(self):
        return max(g.datavalues().end() for g in self.__geoms)

    def get_id(self):
        return self.__id

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

    def geometries(self):
        return self.__geoms

    def add_geometry(self, geom):

        if isinstance(geom,list):
            self.__geoms.extend(geom)
            for g in geom:
                self.__calculate_start_and_end_times(g.datavalues())
        else:
            self.__geoms.append(geom)
            self.__calculate_start_and_end_times(geom.datavalues())

    def get_dataset(self,geometry):
        for geom in self.__geoms:
            if geom.geom() == geometry:
                return geometry.datavalues()
        raise Exception('Could not find geometry in exchange item instance: %s'%geometry)
        #return self.__dataset

    def get_all_datasets(self):
        """
        returns the input dataset as a dictionary of geometries
        """
        geom_dict = {}
        for geom in self.__geoms:
            geom_dict[geom] = geom.datavalues()
        return geom_dict

        # for datavalues in self.__dataset:
        #     dict[datavalues.element] = datavalues.values()
        # return dict

    def get_timeseries_by_geom(self,geom):
        # """
        # geom = the geom of the desired timeseries
        # """
        # dict = self.get_dataset_dict()
        # for element in dict.keys():
        #     if element.geom() == geom:
        #         return dict[element]
        # return None
        pass

    def get_timeseries_by_element(self,element):
        # """
        # element = the element of the desired timeseries
        # """
        # dict = self.get_dataset_dict()
        # return dict[element]
        pass

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
        # """
        # datavalues = list of datavalue objects
        # """
        # if isinstance(datavalues,list):
        #     self.get_dataset().extend(datavalues)
        #     self.__calculate_start_and_end_times(datavalues)
        #
        #     # save the geometries
        #
        # else:
        #     self.get_dataset().append(datavalues)
        #     self.__calculate_start_and_end_times([datavalues])
        pass

    def clear(self):
        #self.__dataset = []
        self.__geoms = []
        self.StartTime = datetime.datetime(2999,1,1,1,0,0)
        self.EndTime = datetime.datetime(1900,1,1,1,0,0)


    def set_dataset(self,value):
        # self.__dataset = value
        # self.__calculate_start_and_end_times(value)
        pass

    # def __calculate_start_and_end_times(self,dv):
    #     #for dv in datavalues:
    #     if dv.earliest_date() is not None and dv.latest_date() is not None:
    #         if dv.earliest_date() < self.StartTime:
    #             self.StartTime = dv.earliest_date()
    #         if dv.latest_date() > self.EndTime:
    #             self.EndTime = dv.latest_date()

    def session(self,value=None):
        """
        gets/sets the database session for this exchange item
        :param value: database session object
        :return: database session object
        """
        if value is not None:
            self.__session == value
        else:
            return self.__session

    def is_saved(self,value=None):
        """
        gets/sets the saved state of the exchange item
        :param value: Boolean type indicated if the exchange item has been saved to db
        :return: Boolean
        """
        if value is not None:
            self.__saved = value
        else:
            return self.__saved

    def resultid(self,value):
        """
        gets/sets the database series id for the simulation results
        :param value: ODM2 resultID
        :return: ODM2 resultID
        """
        if value is not None:
            return self.__seriesID
        else:
            self.__seriesID = value













