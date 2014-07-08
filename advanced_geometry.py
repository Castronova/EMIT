__author__ = 'tonycastronova'

from shapely.wkt import loads
import numpy as np
from stdlib import *
from shapely.geometry import point

class GriddedGeometry(object):
    """
    This is an extension class to handle gridded geometry types.
    + Good for expressing geometries as cell arrays
    """

    def __init__(self, geom_list, xspacing, yspacing, numcols, numrows):
        self.__geoms = geom_list
        self.__xspacing = xspacing
        self.__yspacing = yspacing
        self.__numcols = numcols
        self.__numrows = numrows
        self.__dates = None

        # build geometry array


        # build value array
        self.__gridded_values = self.build_array(geom_list,numcols,numrows)

    def build_array(self,geom_list,numcols,numrows):
        """
        This function assumes that geometries points which are listed in order left->right, top->bottom
        :param geom_list: list of geoms left->right, top->bottom
        :param numcols: number of columns in grid
        :param numrows: number of rows in grid
        :return: array of lats and lons
        """
        i = 0
        lats = []
        lons = []
        values = []
        for x in range(0,numcols):
            lat_row = []
            lon_row = []
            val_row = []
            for y in range(0,numrows):
                lon_row.append(geom_list[i].geom().x)
                lat_row.append(geom_list[i].geom().y)

                d,v = geom_list[i].datavalues().get_dates_values()
                val_row.append(list(v))

                i += 1



            lats.append(lat_row)
            lons.append(lon_row)
            values.append(val_row)


        # arrange data by timeslices
        tmp = [map(list,zip(*values[i])) for i in range(0,len(values))]
        a = np.zeros((len(tmp[0]),len(tmp),len(tmp[0][0])))

        for i in range(0,len(a[0][0])):
            for j in range(0, len(a)):
                a[j][i] = tmp[i][j]

        self.__gridded_values = a


        return self.__gridded_values


    def get_time_slice(self,datetime):
        """
        This function returns the values for the entire grid for a slice in time
        :param datetime: desired datetime
        :return: numpy array of values
        """

        i = self.get_nearest_time(datetime)

        return self.__gridded_values[i]


    def add_point(self,x,y):

        pass

    def get_nearest_time(self,dt):
        # get datelist from first geometry datavalues
        dates,values = self.__geoms[0].datavalues().get_dates_values()

        # return the index of the nearest date value
        return dates.index(min(dates,key=lambda date : abs(dt-date)))
